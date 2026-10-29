import streamlit as st
import plotly.express as px
from src.data import load_day
from src.ui import apply_style, hero, sidebar_filters
apply_style()
day = load_day()
hero("Rental Explorer", "Search, filter, inspect and export daily rental records")
f = sidebar_filters(day, "explorer")
q = st.text_input("Search table (date, year, season or weather)")
if q:
    mask = f.astype(str).apply(lambda col: col.str.contains(q, case=False, na=False)).any(axis=1)
    f = f[mask]
st.write(f"Showing **{len(f):,}** of {len(day):,} daily records")
st.dataframe(f, use_container_width=True, hide_index=True)
st.download_button("Download filtered records (CSV)", f.to_csv(index=False).encode("utf-8"),
                   "filtered_bike_rentals.csv", "text/csv")
