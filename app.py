import streamlit as st

st.set_page_config(page_title="F1 Lap Lab", page_icon="🏁", layout="wide")

st.markdown("""
<style>
.stMainBlockContainer {max-width: 1200px; padding-top: 2rem; padding-bottom: 3rem;}
h1 {letter-spacing: -0.04em;}
[data-testid="stMetric"] {background: #f0f3f5; border: 1px solid #d8dfe5;
    border-radius: 10px; padding: 1rem;}
[data-testid="stMetricValue"] {font-variant-numeric: tabular-nums;}
@media (max-width: 640px) {
    .stMainBlockContainer {padding: 1rem;}
    h1 {font-size: 2rem;}
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## F1 Lap Lab")
    st.caption("A next-lap forecasting study")

page = st.navigation({
    "Explore": [
        st.Page("pages/predictions.py", title="Lap predictions", default=True),
        st.Page("pages/model_evaluation.py", title="Model evaluation"),
        st.Page("pages/data_sample.py", title="Data sample")
    ],
    "Understand": [
        st.Page("pages/methodology.py", title="How it works"),
        st.Page("pages/privacy.py", title="Privacy & scope")
    ]
})

with st.sidebar:
    st.divider()
    st.caption("2022–2025 · Historical race data")
    st.caption("Saved forecasts · No live race feed")

page.run()

st.divider()
st.caption("Practice Challenge · Data accessed through FastF1 · Independent student project")
