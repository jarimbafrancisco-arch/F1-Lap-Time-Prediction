# Progress Log

## Initial setup and data inspection

### Work completed

I set up a Python virtual environment, connected it to the VS Code notebook
kernel and installed FastF1 and ipykernel. I chose Monza 2024 as the first
race to explore the data.

In [01_f1_data_download.ipynb](../notebooks/01_f1_data_download.ipynb), I:

- Loaded the race session and inspected the columns, data types and summary statistics.
- Checked missing values. The missing first-sector times were on lap 1, and the missing finish-line speed readings coincided with pit entries.
- Inspected the available weather data.
- Saved the 2022–2025 event calendars, covering 92 scheduled events.

### What I learned

The calendar and lap data are separate downloads. I also learned that missing
values need context: an empty pit-entry time is expected when a driver did
not enter the pits on that lap.

## This week's research and EDA — updated 16 September 2026

### Research and documents

I worked on [Domain Understanding](<Domain Understanding.docx>) and
[Research – F1 Lap Time Prediction](Research_F1_Prediction.docx). These cover
the project scope, research questions, literature, possible features and
limitations of the available data.

The target is a driver's next lap time in seconds, using information available
when the current lap finishes. The research includes possible regression
models, a previous-lap baseline, chronological evaluation and error metrics.
These are plans; I have not trained or compared models yet. I also documented
questions about data permissions and privacy that still need clarification.

### Data analysis

In [02_EDA.ipynb](../notebooks/02_EDA.ipynb), I:

- Compared event coverage across seasons and added a check for missing race downloads.
- Added the multi-season lap-loading code. The saved check still lists 90 missing events, so the full dataset is not yet confirmed as loaded.
- Explored Monza 2024 using LEC, VER and ALO for the driver comparisons.
- Plotted lap times throughout the race, then repeated the plots without pit entry and exit laps.
- Compared lap times against tyre age within each stint and used boxplots to compare compounds.
- Plotted air and track temperatures during the race and added observations below the graphs.
- Prepared the code for a Pearson correlation matrix using lap time, lap number and tyre age. This section still needs to be saved and its results interpreted.

I also set up the GitHub repository and worked through linking the local project
and resolving the initial push rejection.

### What I found

For these three drivers, lap times generally dropped early in the race and
became more stable later. Removing pit laps made the smaller changes easier
to see. The pattern is not well described by one straight line across the
whole race, although individual stints can look flatter or roughly linear.

Track temperature fell from about 51°C to 44°C, while air temperature fell
from about 34°C to 32°C. This corrected my earlier assumption that the track
became hotter. I cannot check the fuel-load explanation with the current data.

The compound and tyre-age plots show differences, but they do not separate
tyre effects from race progress, traffic and other conditions. These findings
are limited to the selected race and drivers.

### Decisions and next steps

- Keep lap times: they are central to the prediction task. Excluding pit laps from a pace comparison does not mean removing lap-time data altogether.
- Treat safety-car and virtual-safety-car filtering as a rule still to implement and check.
- Keep temperature as a possible feature. The current graph does not establish how useful it will be for prediction.
- Save and interpret the correlation section, then tidy the notebook observations and conclusions.
- Write the EDA and analysis document using the notebook graphs, findings and reasons for the filtering decisions.
- Check the remaining race downloads before extending the analysis beyond Monza.
