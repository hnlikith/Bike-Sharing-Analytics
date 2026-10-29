import streamlit as st
import plotly.express as px
import pandas as pd
from src.data import load_day
from src.model import train_daily_model, feature_importance
from src.ui import apply_style, hero, BLUE
apply_style()
day = load_day()
hero("Model Evaluation", "A demonstration regression model that estimates daily bike rental demand")
st.warning("This is an educational model. Random train/test splitting is used here; results are not proof of real-world forecasting performance.")
with st.spinner("Training Random Forest regression model..."):
    model, metrics, X_test, y_test, pred = train_daily_model(day)
c = st.columns(3)
c[0].metric("MAE", f"{metrics['MAE']:,.1f}")
c[1].metric("RMSE", f"{metrics['RMSE']:,.1f}")
c[2].metric("R²", f"{metrics['R²']:.3f}")
eval_df = pd.DataFrame({"Actual rentals":y_test.values, "Predicted rentals":pred})
fig = px.scatter(eval_df, x="Actual rentals", y="Predicted rentals",
                 title="Actual vs Predicted Rentals", opacity=.7,
                 color_discrete_sequence=[BLUE])
maxval = max(eval_df.max().max(), 1)
fig.add_shape(type="line", x0=0, y0=0, x1=maxval, y1=maxval, line=dict(dash="dash", color="#EF4444"))
st.plotly_chart(fig, use_container_width=True)
imp = feature_importance(model)
fig = px.bar(imp.sort_values("Importance"), x="Importance", y="Feature", orientation="h",
             title="Feature Importance", color_discrete_sequence=[BLUE])
st.plotly_chart(fig, use_container_width=True)
st.download_button("Download holdout predictions CSV", eval_df.to_csv(index=False).encode("utf-8"),
                   "bike_model_holdout_predictions.csv", "text/csv")
