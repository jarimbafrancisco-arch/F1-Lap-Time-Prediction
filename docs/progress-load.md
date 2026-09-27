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
