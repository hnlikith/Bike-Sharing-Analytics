from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DAY_PATH = ROOT / "day.csv"
HOUR_PATH = ROOT / "hour.csv"

SEASON_MAP = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
WEATHER_MAP = {
    1: "Clear",
    2: "Mist / Cloudy",
    3: "Light Rain / Snow",
    4: "Heavy Rain / Snow",
}
WEEKDAY_MAP = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
               4: "Thursday", 5: "Friday", 6: "Saturday"}

def _load(path, hourly=False):
    if not path.exists():
        st.error(f"Dataset not found: {path.name}. Place it beside app.py.")
        st.stop()
    df = pd.read_csv(path)
    required = {"dteday", "cnt", "casual", "registered", "season", "yr",
                "mnth", "weekday", "workingday", "weathersit", "temp", "atemp",
                "hum", "windspeed"}
    if hourly:
        required.add("hr")
    missing = required.difference(df.columns)
    if missing:
        st.error(f"{path.name} is missing required columns: {', '.join(sorted(missing))}")
        st.stop()
    df["dteday"] = pd.to_datetime(df["dteday"], errors="coerce", dayfirst=False)
    df = df.dropna(subset=["dteday"]).copy()
    df["Year"] = df["yr"].map({0: "2011", 1: "2012"}).fillna(df["yr"].astype(str))
    df["Season"] = df["season"].map(SEASON_MAP).fillna("Unknown")
    df["Weather"] = df["weathersit"].map(WEATHER_MAP).fillna("Unknown")
    df["Weekday"] = df["weekday"].map(WEEKDAY_MAP).fillna("Unknown")
    df["Working Day"] = df["workingday"].map({0: "Non-working day", 1: "Working day"}).fillna("Unknown")
    df["Month"] = df["dteday"].dt.month
    df["Month Name"] = df["dteday"].dt.strftime("%b")
    df["Month-Year"] = df["dteday"].dt.to_period("M").astype(str)
    df["Temp (°C)"] = df["temp"] * 41
    df["Feels Like (°C)"] = df["atemp"] * 50
    df["Humidity (%)"] = df["hum"] * 100
    df["Wind Speed (km/h)"] = df["windspeed"] * 67
    if hourly:
        df["Hour Label"] = df["hr"].astype(int).map(lambda x: f"{x:02d}:00")
    return df

@st.cache_data(show_spinner=False)
def load_day():
    return _load(DAY_PATH, hourly=False)

@st.cache_data(show_spinner=False)
def load_hour():
    return _load(HOUR_PATH, hourly=True)
