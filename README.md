# F1 Lap Time Prediction

This is my Practice Challenge for the AI, Machine Learning and Data semester.
I want to predict a Formula 1 driver's next lap time in seconds, using only
information available when the current lap finishes. I am using FastF1 race
data from 2022 to 2025 and starting with predictions during uninterrupted racing.

I want to understand how previous lap times, tyre age, compound and race
conditions can help predict the next lap. I plan to compare a regression model
with ARIMA and with a simple baseline that predicts the next lap taking the
same time as the current one. MAE in seconds will be my main measure of error.

Through this project, I want to get better at understanding the data before
choosing a model, explaining my filtering decisions, avoiding data leakage and
evaluating predictions on later races. I also want to become less dependent on
AI tools. I am using guidance to work through questions, but I want to understand
the code I write and be able to explain why each step is there. Overall, I hope to improve my knowledge and become more and more independent in this area and having a broader knowledge on ML pipelines and possible solutions for different problems.

The notebooks are numbered in the order I worked on them and show how the
project developed over the weeks. Each notebook covers a stage of the work,
including the code, observations and decisions I made along the way. My
supporting documents and [progress log](docs/progress-load.md) are in `docs/`.

To set up the environment on Windows, run these commands from the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Then select the `.venv` Python environment as the notebook kernel in VS Code.
The race downloads need an internet connection. The notebooks create the raw
and prepared `.pkl` files in `data/`; those files and local caches are excluded
from Git. `EligiblePair` and the future-lap helper columns are for preparing
and evaluating the data, not model inputs.
