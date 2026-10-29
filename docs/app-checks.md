# Local app checks — 29 October 2026

The app reads the saved forecasts. These checks did not fit models or change
the prepared data.

- `scripts/check_app.py` passed: all five pages, selections across four seasons,
  successful ARIMA, both saved fallback types, unavailable actual times and a
  missing forecast file.
- The 2025 MAEs match the notebooks: baseline 0.3855 s, smoothing 0.3807 s,
  ARIMA 0.3900 s. The 2024 values also match: 0.4645 s, 0.4601 s, 0.4690 s.
- The saved table contains 101,290 unique lap selections and 78,236 available
  forecasts, all with finite actual and predicted times.
- Chromium checks passed for navigation through all five pages, desktop layout
  at 1440 px and phone layout at 390 px. No browser page errors or page-width
  overflow were observed. The chart legend uses two columns on narrow screens.
- `pip check` found no broken requirements.

The reporting review covers consistent units, precision, model ordering,
actual/forecast distinction, labelled scope and plain-language conclusions.
It is not a full IBCS conformity assessment. User comprehension still needs
feedback from real users or the teacher.

The local privacy settings disable Streamlit usage statistics and bind to
127.0.0.1. Public-hosting responsibilities are documented as unresolved rather
than claiming GDPR compliance. No public deployment was performed.
