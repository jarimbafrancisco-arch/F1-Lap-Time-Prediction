import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from app_helpers import MODELS, choose_driver_race, default_index, load_data, page_header

page_header(
    "Explore / predictions", "One lap. Three predictions.",
    "Choose a recorded lap to compare its actual time with forecasts made from earlier laps."
)
data = load_data()
driver_data, season, race, driver = choose_driver_race(data, "predict")
laps = sorted(driver_data["PredictedLap"].dropna().astype(int).unique())
lap = st.selectbox("Lap to predict", laps, index=default_index(laps, 21))
row = driver_data.loc[driver_data["PredictedLap"].eq(lap)].iloc[0]

st.subheader(f"{driver} · {race} {season} · Lap {lap}")
st.caption(f"{row['DatasetSplit']} period · All times in seconds")
actual = row["Actual"]
st.metric("Actual lap time", f"{actual:.3f} s" if pd.notna(actual) else "Unavailable")

if row["PredictionAvailable"]:
    st.caption(
        f"Forecast made after lap {lap - 1}, using "
        f"{int(row['HistoryLaps'])} consecutive usable laps."
    )
    for column, model in zip(st.columns(3), MODELS):
        prediction = row[model]
        difference = prediction - actual
        with column:
            st.metric(model, f"{prediction:.3f} s")
            st.write(f"**Error: {abs(difference):.3f} s**")
            if abs(difference) < 0.0005:
                st.caption("Matches the actual time to 0.001 s.")
            else:
                direction = "faster" if difference < 0 else "slower"
                st.caption(f"Predicted {abs(difference):.3f} s {direction} than the actual lap.")

    errors = row[MODELS].astype(float).sub(actual).abs()
    closest = errors.index[np.isclose(errors, errors.min(), atol=1e-9, rtol=0)].tolist()
    if len(closest) == 1:
        st.info(f"Closest on this lap: {closest[0]}. One lap does not determine the best model overall.")
    else:
        st.info(f"Closest on this lap: {' and '.join(closest)} (tied).")

    if row["ARIMAMethod"] == "ARIMA":
        st.caption("ARIMA produced its own forecast for this lap.")
    elif "short history" in row["ARIMAMethod"]:
        st.info(
            f"ARIMA used the baseline: only {int(row['HistoryLaps'])} usable consecutive laps "
            "were available. The model requires at least 10 in this project."
        )
    else:
        st.info("ARIMA used the baseline because its fit failed or was unreliable.")
else:
    st.info(
        "Prediction unavailable. This lap does not have an eligible forecast under the "
        "project's history, pit-lap, track-status and timing-quality rules. "
        "The actual time is still shown when recorded."
    )

st.subheader("Recent laps in context")
st.caption(
    "Up to 20 laps ending at the selected lap. Actual times are solid; forecasts are dashed. "
    "The vertical scale is zoomed to the lap times. Gaps indicate missing times or forecasts."
)
recent = driver_data.loc[driver_data["PredictedLap"].between(max(1, lap - 19), lap)]
chart_data = recent[["PredictedLap", "Actual"] + MODELS].melt(
    id_vars="PredictedLap", var_name="Series", value_name="Time (s)"
)
chart = alt.Chart(chart_data).mark_line(
    point=True, invalid="break-paths-show-domains"
).encode(
    x=alt.X("PredictedLap:Q", title="Lap", axis=alt.Axis(tickMinStep=1)),
    y=alt.Y("Time (s):Q", scale=alt.Scale(zero=False)),
    color=alt.Color(
        "Series:N", sort=["Actual"] + MODELS,
        scale=alt.Scale(domain=["Actual"] + MODELS, range=["#18232d", "#7b858e", "#007d85", "#8055a5"])
    ),
    strokeDash=alt.StrokeDash(
        "Series:N", sort=["Actual"] + MODELS,
        scale=alt.Scale(domain=["Actual"] + MODELS, range=[[1, 0], [3, 3], [7, 3], [2, 3]])
    ),
    tooltip=[alt.Tooltip("PredictedLap:Q", title="Lap", format=".0f"), "Series:N",
             alt.Tooltip("Time (s):Q", format=".3f")]
).properties(height=300).configure_legend(orient="bottom", columns=2, symbolType="stroke", labelLimit=150)
st.altair_chart(chart, width="stretch")
st.caption("Forecasts use only earlier laps. Actual times are revealed here for historical comparison.")
