import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.data import load_day, load_hour

st.set_page_config(page_title="Bike Sharing Analytics", page_icon="🚲", layout="wide")

NAVY = "#0B1F44"
BLUE = "#2563EB"
GREEN = "#10B981"
AMBER = "#F59E0B"
RED = "#EF4444"

def apply_style():
    st.markdown("""
    <style>
    .stApp { background: #F5F7FB; }
    [data-testid="stSidebar"] { background: #0B1F44; }
    [data-testid="stSidebar"] * { color: #F8FAFC; }
    .hero { background: linear-gradient(105deg,#0B1F44,#155A91); padding: 1.35rem 1.5rem;
            border-radius: 16px; color: white; margin-bottom: 1rem; }
    .hero h1 { color: white; margin: 0; font-size: 2rem; }
    .hero p { color: #DCEAFE; margin: .4rem 0 0; }
    div[data-testid="stMetric"] { background: white; border: 1px solid #E2E8F0;
        padding: 1rem; border-radius: 12px; box-shadow: 0 2px 8px #0B1F4410; }
    </style>
    """, unsafe_allow_html=True)

def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def fmt_num(x):
    return f"{x:,.0f}"

def sidebar_filters(df, key_prefix="f", include_weather=True):
    st.sidebar.subheader("Filters")
    years = sorted(df["Year"].dropna().unique().tolist())
    seasons = ["Spring", "Summer", "Fall", "Winter"]
    year = st.sidebar.multiselect("Year", years, default=years, key=f"{key_prefix}_year")
    season = st.sidebar.multiselect("Season", seasons, default=seasons, key=f"{key_prefix}_season")
    working = st.sidebar.multiselect("Day type", sorted(df["Working Day"].dropna().unique()),
                                     default=sorted(df["Working Day"].dropna().unique()),
                                     key=f"{key_prefix}_work")
    result = df[df["Year"].isin(year) & df["Season"].isin(season) & df["Working Day"].isin(working)]
    if include_weather:
        weather = st.sidebar.multiselect("Weather", sorted(df["Weather"].dropna().unique()),
                                         default=sorted(df["Weather"].dropna().unique()),
                                         key=f"{key_prefix}_weather")
        result = result[result["Weather"].isin(weather)]
    return result

def kpi_row(df):
    total = int(df["cnt"].sum()) if len(df) else 0
    avg = float(df["cnt"].mean()) if len(df) else 0
    reg = int(df["registered"].sum()) if len(df) else 0
    casual = int(df["casual"].sum()) if len(df) else 0
    c = st.columns(4)
    c[0].metric("Total Rentals", fmt_num(total))
    c[1].metric("Average Daily Rentals", f"{avg:,.1f}")
    c[2].metric("Registered Rentals", fmt_num(reg), f"{reg/total:.1%} of rentals" if total else None)
    c[3].metric("Casual Rentals", fmt_num(cas), f"{cas/total:.1%} of rentals" if total else None)
