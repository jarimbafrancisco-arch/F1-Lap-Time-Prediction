import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from app_helpers import load_data, page_header


data = load_data()

page_header(
    "Explore / evaluation", "Small errors. An honest comparison.",
    "See how close the models came across many laps, and how much they improved on a simple guess."
)

split = st.selectbox(
    "Choose the results",
    ["Test", "Validation"],
    format_func=lambda value: {
        "Test": "2025 - Final test results",
        "Validation": "2024 - Model selection results"
    }[value]
)

if split == "Test":
    st.caption("2025 is the designated test period. Its results were also inspected during development.")
else:
    st.caption("These races helped choose the model settings, so these are development results.")

evaluation = data.loc[
    data["DatasetSplit"].eq(split)
    & data["PredictionAvailable"]
].copy()

coverage = evaluation["ARIMAMethod"].eq("ARIMA").mean() * 100

if evaluation.empty:
    st.info("No evaluated laps are available for this dataset.")
    st.stop()

st.write(
    f"All three models are compared on the same **{len(evaluation):,} laps**. "
    "Only lap pairs meeting the project's filtering rules are included."
)

scores = []
actual = evaluation["Actual"]

for model in ["Baseline", "Smoothing", "ARIMA"]:
    predicted = evaluation[model]

    scores.append({
        "Model": model,
        "MAE (s)": mean_absolute_error(actual, predicted),
        "RMSE (s)": np.sqrt(mean_squared_error(actual, predicted)),
        "R²": r2_score(actual, predicted)
    })

comparison = pd.DataFrame(scores).sort_values("MAE (s)")

st.subheader("Average prediction error")
st.write(
    "Lower is better. An error of 0.400 seconds means predictions were "
    "0.400 seconds away from the real lap time on average. "
    "Individual errors can be larger or smaller."
)

descriptions = {
    "Baseline": "Repeats the previous lap time.",
    "Smoothing": "Averages past lap times, giving more weight to recent laps.",
    "ARIMA": "Adjusts the latest lap time using an estimated prediction error; includes fallbacks."
}
by_model = comparison.set_index("Model")

for column, model in zip(st.columns(3), ["Baseline", "Smoothing", "ARIMA"]):
    with column:
        st.metric(model, f"{by_model.at[model, 'MAE (s)']:.4f} s")
        st.caption(descriptions[model])

best = comparison.iloc[0]
baseline_error = by_model.at["Baseline", "MAE (s)"]
improvement = baseline_error - best["MAE (s)"]

if improvement > 0:
    reduction = 100 * improvement / baseline_error
    st.info(
        f"{best['Model']} has the lowest average error on these laps. "
        f"It reduces average error by {improvement * 1000:.2f} milliseconds "
        f"({reduction:.2f}%) compared with repeating the previous lap time. "
        "This is an average across the evaluated laps, not a win on every lap."
    )
else:
    st.info("Neither model improves on the baseline's average error on these laps.")

st.subheader("When ARIMA used the baseline")
fallback_count = evaluation["ARIMAMethod"].ne("ARIMA").sum()
st.write(
    f"ARIMA produced its own forecast for **{coverage:.1f}%** of the evaluated laps. "
    f"For the other **{fallback_count:,} laps**, it repeated the previous lap time "
    "because there were fewer than 10 usable consecutive laps or the fit was unreliable. "
    "Both types of prediction are included in its score."
)
st.caption("This percentage describes ARIMA use, not prediction accuracy.")

with st.expander("Technical details"):
    st.dataframe(comparison.round(4), hide_index=True)
    st.markdown(
        "- **MAE (seconds):** average absolute error, shown above. Lower is better.\n"
        "- **RMSE (seconds):** gives large errors more weight. Lower is better.\n"
        "- **R²:** compares squared errors with predicting the mean actual lap time. "
        "Higher is better; it is not a percentage accuracy.\n"
        "- **Smoothing:** alpha = 0.9.\n"
        "- **ARIMA:** (0, 1, 1), no trend, with a minimum history of 10 laps."
    )
    st.write(
        "Each eligible lap pair has equal weight in the headline metrics. "
        "The same laps are used for all models. This is a chronological split "
        "with expanding-history one-step forecasts, not time-series cross-validation."
    )
    st.write(
        "The original target was a 10% reduction in MAE against the baseline. "
        "The final test improvement is about 1.25%, so that target was not met. "
        "Results are descriptive: no confidence interval or significance test was calculated."
    )
    st.dataframe(
        evaluation["ARIMAMethod"].value_counts().rename_axis("Method").reset_index(name="Laps"),
        hide_index=True
    )

with st.expander("Results by race"):
    race_scores = []
    for (round_number, event), race_data in evaluation.groupby(["RoundNumber", "EventName"]):
        race_scores.append({
            "Round": round_number, "Race": event, "Laps": len(race_data),
            **{f"{model} MAE (s)": mean_absolute_error(race_data["Actual"], race_data[model])
               for model in ["Baseline", "Smoothing", "ARIMA"]}
        })
    st.caption("Average error within each race. Lower is better; all models use the same laps.")
    st.dataframe(pd.DataFrame(race_scores).round(4), hide_index=True)

st.caption(
    "These results describe historical, filtered lap pairs. "
    "They do not establish performance for every race situation or future races."
)
