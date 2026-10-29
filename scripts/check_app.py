import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import numpy as np
import pandas as pd
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

import app_helpers

data = pd.read_pickle(ROOT / "data" / "app_predictions.pkl")
app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60).run()


def no_errors():
    assert not app.exception, [error.message for error in app.exception]


def select_row(row):
    app.switch_page("pages/predictions.py").run()
    app.selectbox[0].select(int(row["Season"])).run()
    app.selectbox[1].select(row["EventName"]).run()
    app.selectbox[2].select(row["Driver"]).run()
    app.selectbox[3].select(int(row["PredictedLap"])).run()
    no_errors()


no_errors()
assert [metric.value for metric in app.metric] == ["108.380 s", "108.279 s", "108.282 s", "108.279 s"]
assert any("Closest on this lap: Smoothing" in info.value for info in app.info)

for method in ["ARIMA", "Baseline: short history", "Baseline: unreliable fit"]:
    row = data.loc[data["ARIMAMethod"].eq(method)].iloc[0]
    select_row(row)
    assert len(app.metric) == 4
    assert app.metric[3].value == f"{row['ARIMA']:.3f} s"
    if method == "ARIMA":
        assert any("own forecast" in item.value for item in app.caption)
    else:
        assert row["ARIMA"] == row["Baseline"]
        assert any("ARIMA used the baseline" in item.value for item in app.info)
    print("Prediction branch passed:", method)

select_row(data.loc[data["Actual"].isna()].iloc[0])
assert app.metric[0].value == "Unavailable"
assert len(app.metric) == 1
assert any("Prediction unavailable" in item.value for item in app.info)

for season in [2022, 2023, 2024, 2025]:
    select_row(data.loc[data["Season"].eq(season) & data["PredictionAvailable"]].iloc[-1])

app.switch_page("pages/model_evaluation.py").run()
no_errors()
assert [m.value for m in app.metric] == ["0.3855 s", "0.3807 s", "0.3900 s"]
assert "4.82 milliseconds (1.25%)" in app.info[0].value
assert len(app.dataframe[2].value) == 24
app.selectbox[0].select("Validation").run()
no_errors()
assert [m.value for m in app.metric] == ["0.4645 s", "0.4601 s", "0.4690 s"]

app.switch_page("pages/data_sample.py").run()
no_errors()
assert [m.value for m in app.metric] == ["101,290", "92", "78,236"]
app.selectbox[3].select(10).run()
assert len(app.dataframe[0].value) == 10

for page in ["pages/methodology.py", "pages/privacy.py"]:
    app.switch_page(page).run()
    no_errors()

with TemporaryDirectory() as folder:
    with patch.object(app_helpers, "ROOT", Path(folder)):
        missing = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60).run()
        assert not missing.exception
        assert missing.error[0].value == "The saved forecast file is missing."

available = data.loc[data["PredictionAvailable"]]
assert np.isfinite(available[["Actual", "Baseline", "Smoothing", "ARIMA"]]).all().all()
assert len(available) == 78236
assert not data.duplicated(["Season", "RoundNumber", "DriverNumber", "PredictedLap"]).any()
print("All app checks passed: selections, missing data, fallbacks, metrics, sample and navigation.")
