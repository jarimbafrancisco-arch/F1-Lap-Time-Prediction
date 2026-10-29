import pandas as pd
import streamlit as st

from app_helpers import choose_driver_race, load_data, page_header

page_header(
    "Explore / data", "The data behind the lap.",
    "Inspect a small sample and see which recorded laps have forecasts."
)
data = load_data()
total_races = data[["Season", "RoundNumber"]].drop_duplicates().shape[0]
for column, label, value in zip(
    st.columns(3), ["Recorded laps", "Races", "Laps with forecasts"],
    [len(data), total_races, data["PredictionAvailable"].sum()]
):
    column.metric(label, f"{value:,}")

selected, season, race, driver = choose_driver_race(data, "sample")
row_count = st.selectbox("Rows to show", [10, 25, 50, 100], index=1)
columns = ["PredictedLap", "Actual", "Baseline", "Smoothing", "ARIMA", "HistoryLaps", "ARIMAMethod"]
sample = selected[columns].head(row_count).copy()
sample["PredictedLap"] = sample["PredictedLap"].astype("Int64")
sample["HistoryLaps"] = sample["HistoryLaps"].astype("Int64")
sample = sample.rename(columns={
    "PredictedLap": "Lap", "Actual": "Actual (s)", "Baseline": "Baseline (s)",
    "Smoothing": "Smoothing (s)", "ARIMA": "ARIMA (s)",
    "HistoryLaps": "History laps", "ARIMAMethod": "ARIMA status"
})
st.caption(f"{driver} · {race} {season} · First {len(sample)} of {len(selected)} recorded laps")
st.dataframe(sample.round(3), hide_index=True)
st.caption("Blank values mean unavailable, not zero. Forecasts in a row predict that row's lap.")

with st.expander("What do the columns mean?", expanded=True):
    st.dataframe(pd.DataFrame({
        "Column": ["Lap", "Actual (s)", "Baseline (s)", "Smoothing (s)", "ARIMA (s)",
                   "History laps", "ARIMA status"],
        "Meaning": [
            "The lap being predicted, not the last input lap.",
            "Recorded lap duration, revealed for historical evaluation.",
            "The previous lap time used as the next-lap forecast.",
            "Forecast from exponential smoothing with alpha = 0.9.",
            "ARIMA(0,1,1) forecast, or the baseline when a fallback was needed.",
            "Usable consecutive laps available before the predicted lap.",
            "Whether ARIMA fitted, fell back, or had no eligible prediction."
        ]
    }), hide_index=True)

st.subheader("Coverage by season")
coverage = data.groupby("Season").agg(
    RecordedLaps=("PredictedLap", "size"), Forecasts=("PredictionAvailable", "sum")
).reset_index()
coverage["Forecast availability (%)"] = 100 * coverage["Forecasts"] / coverage["RecordedLaps"]
st.dataframe(coverage.rename(columns={"RecordedLaps": "Recorded laps"}).round(1), hide_index=True)
st.caption(
    "Availability uses all recorded laps as its denominator. The evaluation page's ARIMA-use "
    "percentage uses only laps with forecasts, so the two percentages answer different questions."
)
st.write(
    "Source: race timing data accessed through [FastF1](https://docs.fastf1.dev/). "
    "The prepared dataset retains the full history and flags eligible pairs instead of deleting other laps."
)
