import streamlit as st
import plotly.express as px
from src.data import load_day, load_hour
from src.ui import apply_style, hero, BLUE, GREEN
apply_style()
day, hour = load_day(), load_hour()
hero("Time Analysis", "Understand hourly peaks, weekdays, working days and month-by-month demand")
years = st.multiselect("Year", sorted(hour["Year"].unique()), default=sorted(hour["Year"].unique()), key="time_year")
h = hour[hour["Year"].isin(years)]
c1,c2 = st.columns(2)
with c1:
    byhour = h.groupby(["hr","Working Day"], as_index=False)["cnt"].mean()
    byhour["Hour Label"] = byhour["hr"].map(lambda x: f"{int(x):02d}:00")
    fig = px.line(byhour, x="Hour Label", y="cnt", color="Working Day", markers=True,
                  title="Average Rentals by Hour", labels={"cnt":"Average rentals per hour"},
                  color_discrete_sequence=[BLUE,GREEN])
    st.plotly_chart(fig, use_container_width=True)
with c2:
    wd = h.groupby("Weekday", as_index=False)["cnt"].mean()
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    wd["sort"] = wd["Weekday"].map({x:i for i,x in enumerate(order)})
    wd = wd.sort_values("sort")
    fig = px.bar(wd, x="Weekday", y="cnt", title="Average Rentals by Weekday",
                 labels={"cnt":"Average rentals per hour"}, color_discrete_sequence=[BLUE])
    st.plotly_chart(fig, use_container_width=True)
c1,c2 = st.columns(2)
with c1:
    work = h.groupby("Working Day", as_index=False)["cnt"].mean()
    fig = px.bar(work, x="Working Day", y="cnt", title="Working vs Non-working Day",
                 labels={"cnt":"Average rentals per hour"}, color="Working Day",
                 color_discrete_sequence=[BLUE,GREEN])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    monthly = h.groupby(["Month-Year","Year"], as_index=False)["cnt"].sum()
    fig = px.line(monthly, x="Month-Year", y="cnt", color="Year", markers=True,
                  title="Hourly Dataset: Monthly Total Rentals", labels={"cnt":"Total rentals"},
                  color_discrete_sequence=[BLUE,GREEN])
    st.plotly_chart(fig, use_container_width=True)
st.caption("Hourly and daily records overlap by design. Do not sum their totals together.")
