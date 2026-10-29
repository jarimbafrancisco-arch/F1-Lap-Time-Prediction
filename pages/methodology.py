import pandas as pd
import streamlit as st

from app_helpers import page_header

page_header(
    "Understand / methodology", "From lap history to a forecast.",
    "Three simple models answer one question: how long will the driver's next lap take?"
)
st.subheader("What the app does")
st.write(
    "The app reads saved one-step forecasts for races from 2022–2025. Selecting lap 21 "
    "shows forecasts made after lap 20, together with lap 21's recorded time. "
    "Race, driver and lap selectors retrieve the relevant history; they are not extra model features."
)
st.markdown(
    "1. Load race timing data through FastF1.\n"
    "2. Order laps within each season, race and driver, then align each lap with its next lap.\n"
    "3. Build consecutive usable histories, restarting after gaps.\n"
    "4. Forecast one lap ahead using only the history available at that point.\n"
    "5. Compare saved forecasts with the actual next-lap time."
)

st.subheader("How the models make a prediction")
with st.expander("Baseline: repeat the previous lap", expanded=True):
    st.write("If the last lap took 108.279 seconds, predict 108.279 seconds for the next one.")
    st.latex(r"\hat{y}_{t+1} = y_t")
    st.caption("A strong reference when consecutive laps have similar times.")

with st.expander("Smoothing: give recent laps more weight"):
    st.write(
        "Update the smoothed level with 90% of the latest lap time and 10% of the previous "
        "smoothed level. Use the new level as the next forecast. The first level is the first usable lap."
    )
    st.latex(r"L_t = 0.9y_t + 0.1L_{t-1}, \qquad \hat{y}_{t+1}=L_t")
    st.write("For a lap of 108 seconds and a previous level of 109 seconds, the forecast is 108.1 seconds.")
    st.caption("The Holt model selected beta = 0 with an initial trend of zero, so it reduces to this smoothing rule.")

with st.expander("ARIMA: correct using an estimated recent error"):
    st.write(
        "ARIMA(0,1,1) models changes between lap times. It adjusts the latest time using "
        "the latest estimated innovation (an error inside the fitted model)."
    )
    st.latex(r"\hat{y}_{t+1}=y_t+\theta\hat{\epsilon}_t")
    st.write(
        "The coefficient theta is estimated from the available history during fitting. "
        "The 1 in q = 1 counts the error term; it is not the coefficient. "
        "An estimated innovation is not necessarily identical to a previously saved forecast error."
    )
    st.write(
        "The project requires at least 10 usable consecutive laps. Short histories, failed fits "
        "or unreliable results use the baseline instead. A successful fit does not guarantee a good prediction."
    )

st.subheader("How the settings were selected")
st.dataframe(pd.DataFrame({
    "Period": ["2022–2023", "2024", "2025"],
    "Role": ["Training and development", "Validation and model selection", "Designated final test"]
}), hide_index=True)
st.write(
    "Smoothing was selected from 24 alpha/beta combinations. ARIMA was compared across "
    "16 configurations on 2,400 sampled eligible pairs from the 24 validation races. "
    "ARIMA(0,1,0), without a trend, ranked first and is equivalent to the baseline. "
    "The second-ranked (0,1,1) was retained to investigate error corrections; it was not the search winner."
)
st.write(
    "Each forecast uses an expanding history inside its own consecutive segment. "
    "The project uses chronological splits, not a separate time-series cross-validation study. "
    "The 2025 results had already been inspected during development, so they should not be described "
    "as an entirely untouched independent test."
)

st.subheader("Where these results apply")
st.write(
    "Eligible pairs require consecutive laps, recorded times, no pit-in or pit-out on either lap, "
    "track status exactly '1', and FastF1's IsAccurate flag on both laps. These conditions restrict "
    "the evaluation; they do not guarantee perfectly normal racing conditions."
)
st.info(
    "The next lap's quality and track-status flags are checked retrospectively to select evaluation pairs. "
    "They are not model inputs and would not be known before a future lap. This app is a historical explorer."
)
st.write(
    "The models use lap times alone. Weather, traffic, tyre compound, fuel, pit strategy and driver "
    "identity are not explanatory inputs. Large changes can remain after filtering. "
    "Restart-specific changes, additional models and uncertainty intervals are outside the completed scope."
)

st.subheader("Transparency and explainability")
st.write(
    "The data preparation, model settings and comparisons are documented in notebooks 01–07. "
    "The equations above describe how the forecasts work; the baseline and displayed errors help "
    "interpret their practical value. Notebook 05 also checks smoothing calculations manually."
)
st.markdown(
    "Using [NIST's four explainability principles](https://nvlpubs.nist.gov/nistpubs/ir/2021/NIST.IR.8312.pdf) "
    "as a review framework:\n\n"
    "- **Explanation:** show the forecasting rules and fallback decisions.\n"
    "- **Meaningful:** use seconds, examples and a simple reference model; user comprehension still needs feedback.\n"
    "- **Explanation accuracy:** use the actual implemented equations and verify examples. "
    "The app does not expose each ARIMA fit's coefficient because those coefficients were not saved.\n"
    "- **Knowledge limits:** show missing forecasts, limited scope and the modest observed improvement."
)

with st.expander("Reporting design"):
    st.write(
        "The interface uses consistent seconds, decimal precision and model order, clear comparisons, "
        "and solid actual lines versus dashed forecast lines. These choices support the clarity goals "
        "of IBCS; they are not a claim of full IBCS or ISO certification."
    )
    st.markdown("[IBCS standards and communication principles](https://www.ibcs.com/ibcs-version-2-0/)")
