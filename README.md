# Bike Sharing Analytics Dashboard

A seven-page Streamlit dashboard inspired by the structure of the referenced Internship Selection dashboard. Uses the uploaded Bike Sharing daily and hourly datasets.

## Pages
1. Executive Overview — KPI cards, year comparison and rental distribution.
2. Rental Explorer — search, filter, inspect and export daily records.
3. Time Analysis — hourly peaks, weekday and working-day patterns.
4. Season & Weather Patterns — seasonal demand, weather effects and temperature relationships.
5. Model Evaluation — Random Forest regression metrics, actual-vs-predicted plot and feature importance.
6. Daily Rental Prediction — interactive estimate from calendar and weather inputs.
7. Data Quality — missing values, duplicates, types and descriptive statistics.

## Data
- `day.csv`: 731 rows, 16 columns.
- `hour.csv`: 17,379 rows, 17 columns.
- Rental totals in daily and hourly data overlap; do not add them together.
- Temperature, feels-like temperature, humidity and wind speed are converted from normalized dataset values for display.

## Run on Windows
Open PowerShell in this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit prints a local URL (usually `http://localhost:8501`). Open it in your browser.

## Notes
- Model evaluation uses a random train/test split and is intended as an educational demonstration. It is not a validated production forecast.
- Prediction scores are estimates, not guaranteed outcomes.
- The project reads CSVs placed next to `app.py`. Keep `day.csv` and `hour.csv` there.
