# F1 Lap Time Prediction

Predicting a Formula 1 driver's next lap time with historical race data,
baseline comparisons and an interactive Streamlit app.

## Video demo

**[Open or download the app demo (MP4, approximately 66 MB)](media/demo.mp4?raw=true)**

Watch the recorded Streamlit demo without installing or running the project.
If your browser downloads the video, open it with your preferred video player.

## About the project

This is my Practice Challenge for the AI, Machine Learning and Data semester.
I predict a Formula 1 driver's next lap time using information available when
the current lap finishes. The FastF1 dataset covers 92 races from 2022 to 2025,
with 78,236 eligible lap pairs after filtering.

I compared linear regression, exponential smoothing and ARIMA against a
baseline that repeats the latest lap time. I used 2022-2023 for development
and training, 2024 for validation and 2025 for testing.

## Results

The final comparison covers all 20,969 eligible test pairs:

| Model | MAE (seconds) |
| --- | ---: |
| Simple exponential smoothing | 0.3807 |
| Same-lap baseline | 0.3855 |
| ARIMA (0,1,1), including baseline fallbacks | 0.3900 |

Smoothing improved on the baseline by about 1.25%, below my initial 10% target.
I expected the baseline to be easier to beat. This was one of the main things
I learned: a more complex model does not necessarily predict better.
These results apply to the filtered lap pairs, not every race situation.

## Explore the app

The Streamlit app has pages for lap predictions, evaluation, a data sample,
methodology and privacy. It reads saved historical forecasts; it does not refit
models when a user chooses a lap. Missing forecasts and ARIMA fallbacks are labelled.

## Project structure

| Path | Contents |
| --- | --- |
| `app.py`, `app_helpers.py` | Streamlit entry point and shared data helpers |
| `pages/` | Predictions, evaluation, data sample, methodology and privacy |
| `notebooks/` | Data collection, analysis, model experiments and app data preparation |
| `data/` | Tracked CSV samples and locally generated datasets |
| `docs/` | Academic reports, supporting figures and progress log |
| `exports/` | Saved HTML and PDF versions of the EDA notebook |
| `media/` | Recorded app demo |
| `scripts/` | App checks and notebook export utility |
| `.streamlit/` | Local server and theme configuration |

### Notebook guide

| Notebook | Purpose |
| --- | --- |
| [01 — Data download](notebooks/01_f1_data_download.ipynb) | Collect race schedules and lap data through FastF1 |
| [02 — EDA](notebooks/02_EDA.ipynb) | Explore lap times and data quality |
| [03 — Dataset creation](notebooks/03_dataset_creation.ipynb) | Prepare next-lap targets and eligible pairs |
| [04 — Linear regression](notebooks/04_linearegression_model.ipynb) | Compare regression models with the baseline |
| [05 — Time series forecasting](notebooks/05_timeseriesforecasting.ipynb) | Evaluate exponential smoothing |
| [06 — ARIMA](notebooks/06_arima_model.ipynb) | Tune and evaluate ARIMA with fallback predictions |
| [07 — App data](notebooks/07_app_data.ipynb) | Generate the saved forecasts used by the app |
| [08 — Prepared-data EDA](notebooks/08.eda_2nd_version.ipynb) | Explore the prepared dataset |

For a quick look at the analysis, open the [EDA PDF](exports/02_EDA.pdf).
The [HTML export](exports/02_EDA.html) can be downloaded and opened in a browser.
The [progress log](docs/progress-load.md) records the project's development.

## Run locally

The project was checked on Windows with Python 3.14.5. The commands below use
PowerShell; a notebook editor such as VS Code with Jupyter support is also needed.

### 1. Set up the environment

Clone the repository and install the dependencies:

```powershell
git clone https://github.com/jarimbafrancisco-arch/F1-Lap-Time-Prediction.git
cd F1-Lap-Time-Prediction
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If you already have the project, run only the last two commands from its folder.

### 2. Prepare the data

**A fresh clone does not include `data/app_predictions.pkl`.** Watching the
video needs no setup; running the app requires generating this file first.

Then select the `.venv` Python environment as the notebook kernel in VS Code
and run notebooks 01–07 in numbered order, with `notebooks/` as the working directory.
The race downloads need an internet connection. The notebooks create the raw
and prepared `.pkl` files in `data/`; those files and local caches are excluded
from Git. `EligiblePair` and the future-lap helper columns are for preparing
and evaluating the data, not model inputs.

Notebook 07 fits ARIMA thousands of times and can take a long time. If
`data/app_predictions.pkl` already exists, you can go straight to the next step.
Notebook 08 provides additional analysis and is optional for running the app.

### 3. Start the app

Run this from the project folder:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The default address is http://localhost:8501. Configuration limits access to
this computer and disables Streamlit usage statistics.

### 4. Verify the app

To check the app's selections, pages, fallback messages and saved metrics:

```powershell
.\.venv\Scripts\python.exe scripts/check_app.py
```

These checks use the generated local data. They cover page navigation, lap
selections, unavailable forecasts, ARIMA fallbacks and saved evaluation metrics.

## Scope and limitations

2025 is the designated test period, but its results were inspected during
development; it is not an entirely untouched independent test. The app is a
local educational demo. Public hosting needs institution-specific privacy and
data-use details. Circuit/ghost animation remains outside the current scope.

This is an independent educational project using data accessed through FastF1.
My learning goals include becoming less dependent on AI guidance and being able
to explain the code, decisions and results myself.
