from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
MODELS = ["Baseline", "Smoothing", "ARIMA"]


@st.cache_data(show_spinner="Loading saved forecasts...")
def read_forecasts(path, modified):
    data = pd.read_pickle(path)
    required = [
        "Season", "RoundNumber", "EventName", "Driver", "DriverNumber",
        "PredictedLap", "Actual", "HistoryLaps", "Baseline", "Smoothing",
        "ARIMA", "ARIMAMethod", "PredictionAvailable", "DatasetSplit"
    ]
    if not set(required).issubset(data.columns):
        raise ValueError("The forecast file has missing columns.")
    keys = ["Season", "RoundNumber", "DriverNumber", "PredictedLap"]
    if data.duplicated(keys).any():
        raise ValueError("The forecast file contains duplicate lap selections.")
    available = data.loc[data["PredictionAvailable"], ["Actual"] + MODELS]
    if not np.isfinite(available.to_numpy(dtype=float)).all():
        raise ValueError("Some available forecasts have missing or invalid times.")
    if data.empty:
        raise ValueError("The forecast file is empty.")
    return data.sort_values(keys).reset_index(drop=True)


def load_data():
    path = ROOT / "data" / "app_predictions.pkl"
    if not path.exists():
        st.error("The saved forecast file is missing.")
        st.write(
            "Place app_predictions.pkl in the data folder. It is created by "
            "notebooks/07_app_data.ipynb; preparing it can take a long time."
        )
        st.stop()
    try:
        return read_forecasts(path, path.stat().st_mtime_ns)
    except (ValueError, OSError, EOFError, ImportError) as error:
        st.error("The saved forecast file could not be loaded.")
        st.caption(str(error))
        st.stop()


def page_header(label, title, description):
    st.caption(label.upper())
    st.title(title)
    st.write(description)


def default_index(options, preferred):
    return list(options).index(preferred) if preferred in options else 0


def choose_driver_race(data, prefix):
    columns = st.columns([1, 2, 1])
    seasons = sorted(data["Season"].unique())
    season = columns[0].selectbox(
        "Season", seasons, index=default_index(seasons, 2024), key=f"{prefix}_season"
    )
    selected = data.loc[data["Season"].eq(season)]
    races = selected.sort_values("RoundNumber")["EventName"].drop_duplicates().tolist()
    race = columns[1].selectbox(
        "Race", races, index=default_index(races, "Belgian Grand Prix"), key=f"{prefix}_race"
    )
    selected = selected.loc[selected["EventName"].eq(race)]
    drivers = sorted(selected["Driver"].dropna().unique())
    driver = columns[2].selectbox(
        "Driver", drivers, index=default_index(drivers, "LEC"), key=f"{prefix}_driver"
    )
    return selected.loc[selected["Driver"].eq(driver)].copy(), season, race, driver
