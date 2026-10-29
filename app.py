import streamlit as st
import plotly.express as px
import pandas as pd
from src.data import load_day
from src.ui import apply_style, hero, sidebar_filters, kpi_row, BLUE, GREEN, NAVY

st.set_page_config(page_title="Bike Sharing Analytics", page_icon="🚲", layout="wide")
apply_style()
day = load_day()

st.sidebar.title("🚲 Bike Analytics")
st.sidebar.caption("Demand • Time • Weather • Prediction")
st.sidebar.info("Choose a page from the navigation menu above.")

hero("Bike Sharing Analytics", "Explore rental demand, user behaviour, seasonal patterns and weather impact · Washington, D.C. · 2011–2012")
filtered = sidebar_filters(day, "overview", include_weather=True)
kpi_row(filtered)
st.markdown("### Demand overview")
a, b = st.columns(2)
with a:
    monthly = filtered.groupby(["Month-Year", "Year"], as_index=False)["cnt"].sum()
    fig = px.line(monthly, x="Month-Year", y="cnt", color="Year", markers=True,
                  title="Monthly Rental Trend", labels={"Month-Year":"Month","cnt":"Total rentals"},
                  color_discrete_sequence=[BLUE, GREEN])
    fig.update_layout(margin=dict(l=10,r=10,t=55,b=10), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)
with b:
    season = filtered.groupby("Season", as_index=False)["cnt"].mean()
    order = ["Spring","Summer","Fall","Winter"]
    season["Season"] = pd.Categorical(season["Season"], order, ordered=True) if False else season["Season"]
    fig = px.bar(season, x="Season", y="cnt", title="Average Daily Rentals by Season",
                 labels={"cnt":"Average daily rentals"}, color="Season",
                 color_discrete_sequence=[BLUE, "#60A5FA", GREEN, "#F59E0B"])
    fig.update_layout(showlegend=False, margin=dict(l=10,r=10,t=55,b=10))
    st.plotly_chart(fig, use_container_width=True)
a, b = st.columns(2)
with a:
    user_mix = pd.DataFrame({"User Type":["Registered","Casual"],
                             "Rentals":[filtered["registered"].sum(), filtered["casual"].sum()]})
    fig = px.pie(user_mix, names="User Type", values="Rentals", hole=.62,
                 title="Rental Mix by User Type",
                 color="User Type", color_discrete_map={"Registered":BLUE,"Casual":GREEN})
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(margin=dict(l=10,r=10,t=55,b=10))
    st.plotly_chart(fig, use_container_width=True)
with b:
    weather = filtered.groupby("Weather", as_index=False)["cnt"].mean()
    fig = px.bar(weather, x="Weather", y="cnt", title="Average Rentals by Weather",
                 labels={"cnt":"Average daily rentals"}, color="Weather",
                 color_discrete_sequence=[BLUE, "#60A5FA", "#F59E0B", "#EF4444"])
    fig.update_layout(showlegend=False, margin=dict(l=10,r=10,t=55,b=10), xaxis_tickangle=-15)
    st.plotly_chart(fig, use_container_width=True)
st.caption("Source: Bike Sharing Dataset. Daily and hourly records are analysed separately.")
