# Progress log

23 September 2026 - first three and a half weeks.

I set up Python, FastF1, the notebook environment and GitHub. I started with
Monza 2024 to understand the data, then downloaded the 2022-2025 race data.
I now have 92 races and 101,290 lap records, with no duplicate lap identifiers.

I worked on the domain research and analysis documents. I looked into factors
that affect lap times, such as tyres, fuel load, traffic and weather. Some of
these are not directly available in my data, especially fuel load.

In the EDA, I compared Leclerc, Verstappen and Alonso at Monza. I plotted lap
times, tyre age, compounds and temperatures. Removing pit laps made the race
pace easier to see. I corrected my assumption that the track became hotter:
it actually cooled. I also realised that average compound times across
different circuits do not show which tyre is faster.

My teacher suggested looking at time-series forecasting and ARIMA. I will
compare ARIMA with regression and a baseline that predicts the next lap will
take the same time as the current one.

I created current-lap/next-lap pairs for each driver and race. I required
consecutive laps, both lap times, no pit laps, clear track status and passed
FastF1 timing checks. This left 78,236 eligible pairs for evaluating
uninterrupted racing. I saved the full history with an `EligiblePair` flag,
so the other laps are still available.

I checked the remaining missing tyre information and left it unchanged until
I choose the model inputs. I also learned why the target must use the same
driver's next lap and why future information cannot be used as an input.

Next I will build the baseline and models. I still need to decide how ARIMA
will handle interruptions in the lap sequence. The plan is to use 2022-2023
for training, 2024 for validation and 2025 for testing, with MAE in seconds
as the main metric. No models have been trained yet.

28 September 2026 - this week.

I wrote the model selection document and chose linear regression, gradient
boosting and ARIMA to compare. In notebook 04, I used 2022-2023 for training
and 2024 for validation. I kept 2025 for the final test.

I compared two linear regression models with a baseline that predicts the same
time as the current lap. On 2024 data, the baseline had the lowest MAE at
0.465 seconds. Regression using only current lap time scored 0.505 seconds;
adding tyre age and lap number scored 0.513 seconds. For missing tyre ages, I
used the training median and kept the validation pairs the same.

I also checked errors by race. Some of the largest lap-time differences came
from standing restarts that passed my filtering checks. The first regression
also predicted Belgian laps too fast on average. Next I will check how much
restart laps affect the results before trying the other selected models.


7 October 2026 - this week.

I built the smoothing model in notebook 05, using separate lap sequences for
each driver and race and restarting after interruptions. I compared 24
combinations of alpha and beta on training and validation data. Training
favoured the same-lap baseline, while validation selected alpha=0.9 and beta=0.

On 2024 data, smoothing achieved an MAE of 0.460 seconds, compared with
0.465 seconds for the baseline. It improved MAE in 19 of the 24 races. I also
compared RMSE and R2 and learned that a high R2 does not mean the predictions
are accurate enough for every real-life decision.

I checked ten predictions by writing out the calculation in Python. They
matched the model output, helping me understand how the level updates and
providing evidence for explainability. With beta=0, the trend stays at zero.

I tested the selected settings on 2025. The MAE was 0.3807 seconds, compared
with 0.3855 seconds for the baseline, an improvement of about 1.25%. This is
a small improvement, rather than proof that the model is ready for live use.
Next I will document the LO5 evidence and improvement proposals, then work
on ARIMA as another model to compare.
