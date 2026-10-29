import streamlit as st
import pandas as pd
from src.data import load_day
from src.model import train_daily_model
from src.ui import apply_style, hero
apply_style()
day = load_day()
hero("Daily Rental Prediction", "Enter weather and calendar conditions to estimate daily bike rental demand")
with st.spinner("Preparing prediction model..."):
    model, metrics, _, _, _ = train_daily_model(day)
c1,c2,c3 = st.columns(3)
with c1:
    season = st.selectbox("Season", [1,2,3,4], format_func=lambda x:{1:"Spring",2:"Summer",3:"Fall",4:"Winter"}[x])
    year = st.selectbox("Year", [0,1], format_func=lambda x:{0:"2011",1:"2012"}[x])
    month = st.slider("Month", 1, 12, 6)
    weekday = st.selectbox("Weekday", list(range(7)), format_func=lambda x:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"][x])
with c2:
    holiday = st.selectbox("Holiday", [0,1], format_func=lambda x:"Yes" if x else "No")
    workingday = st.selectbox("Working day", [0,1], format_func=lambda x:"Yes" if x else "No")
    weather = st.selectbox("Weather", [1,2,3,4], format_func=lambda x:{1:"Clear",2:"Mist / Cloudy",3:"Light Rain / Snow",4:"Heavy Rain / Snow"}[x])
    temp_c = st.slider("Temperature (°C)", 0.0, 41.0, 20.0, .5)
with c3:
    feels_c = st.slider("Feels-like temperature (°C)", 0.0, 50.0, 22.0, .5)
    humidity = st.slider("Humidity (%)", 0.0, 100.0, 60.0, 1.0)
    wind = st.slider("Wind speed (km/h)", 0.0, 67.0, 12.0, 1.0)
if st.button("Predict daily rentals", type="primary"):
    row = pd.DataFrame([{
        "season":season, "yr":year, "mnth":month, "holiday":holiday, "weekday":weekday,
        "workingday":workingday, "weathersit":weather, "temp":temp_c/41,
        "atemp":feels_c/50, "hum":humidity/100, "windspeed":wind/67
    }])
    result = max(0, float(model.predict(row)[0]))
    st.success(f"Estimated daily rentals: {result:,.0f}")
    st.caption("This is a model estimate for educational use, not a guaranteed count.")
