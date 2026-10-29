import streamlit as st
import plotly.express as px
from src.data import load_day
from src.ui import apply_style, hero, BLUE, GREEN
apply_style()
day = load_day()
hero("Season & Weather Patterns", "Compare average demand across seasons and weather conditions")
c1,c2 = st.columns(2)
with c1:
    s = day.groupby("Season", as_index=False)["cnt"].mean()
    fig = px.bar(s, x="Season", y="cnt", color="Season", title="Average Daily Rentals by Season",
                 labels={"cnt":"Average daily rentals"}, color_discrete_sequence=[BLUE,"#60A5FA",GREEN,"#F59E0B"])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    w = day.groupby("Weather", as_index=False)["cnt"].mean()
    fig = px.bar(w, x="Weather", y="cnt", color="Weather", title="Average Daily Rentals by Weather",
                 labels={"cnt":"Average daily rentals"}, color_discrete_sequence=[BLUE,"#60A5FA","#F59E0B","#EF4444"])
    fig.update_layout(showlegend=False, xaxis_tickangle=-15)
    st.plotly_chart(fig, use_container_width=True)
c1,c2 = st.columns(2)
with c1:
    fig = px.box(day, x="Season", y="cnt", color="Season", title="Rental Spread by Season",
                 labels={"cnt":"Daily rentals"})
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig = px.scatter(day, x="Temp (°C)", y="cnt", color="Season", opacity=.7,
                     title="Temperature vs Daily Rentals", labels={"cnt":"Daily rentals"})
    st.plotly_chart(fig, use_container_width=True)
