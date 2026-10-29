import streamlit as st
import pandas as pd
import plotly.express as px
from src.data import load_day, load_hour
from src.ui import apply_style, hero, BLUE
apply_style()
day, hour = load_day(), load_hour()
hero("Data Quality", "Inspect missing values, duplicates, data types, ranges and dataset consistency")
which = st.radio("Dataset", ["Daily (day.csv)", "Hourly (hour.csv)"], horizontal=True)
df = day if which.startswith("Daily") else hour
c1,c2,c3,c4 = st.columns(4)
c1.metric("Rows", f"{len(df):,}")
c2.metric("Columns", f"{df.shape[1]:,}")
c3.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")
c4.metric("Duplicate rows", f"{int(df.duplicated().sum()):,}")
missing = df.isna().sum().rename("Missing values").reset_index().rename(columns={"index":"Column"})
fig = px.bar(missing, x="Column", y="Missing values", title="Missing Values by Column",
             color_discrete_sequence=[BLUE])
st.plotly_chart(fig, use_container_width=True)
with st.expander("Column data types"):
    types = pd.DataFrame({"Column":df.columns, "Data type":[str(t) for t in df.dtypes]})
    st.dataframe(types, use_container_width=True, hide_index=True)
with st.expander("Numeric summary"):
    st.dataframe(df.select_dtypes("number").describe().T, use_container_width=True)
with st.expander("Preview records"):
    st.dataframe(df.head(100), use_container_width=True, hide_index=True)
