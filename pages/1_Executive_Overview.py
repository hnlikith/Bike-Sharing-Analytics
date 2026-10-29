import streamlit as st
import plotly.express as px
from src.data import load_day
from src.ui import apply_style, hero, sidebar_filters, kpi_row, BLUE, GREEN
apply_style()
day = load_day()
hero("Executive Overview", "Headline rental KPIs and the most important demand patterns")
filtered = sidebar_filters(day, "exec")
kpi_row(filtered)
c1,c2 = st.columns(2)
with c1:
    fig = px.histogram(filtered, x="cnt", nbins=30, title="Distribution of Daily Rentals",
                       labels={"cnt":"Daily rentals"}, color_discrete_sequence=[BLUE])
    st.plotly_chart(fig, use_container_width=True)
with c2:
    byyear = filtered.groupby("Year", as_index=False)["cnt"].sum()
    fig = px.bar(byyear, x="Year", y="cnt", title="Total Rentals by Year",
                 labels={"cnt":"Total rentals"}, color="Year", color_discrete_sequence=[BLUE,GREEN])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
st.info("Use the sidebar filters to compare years, seasons, day types and weather conditions.")
