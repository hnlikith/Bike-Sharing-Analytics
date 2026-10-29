import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

FEATURES = ["season", "yr", "mnth", "holiday", "weekday", "workingday",
            "weathersit", "temp", "atemp", "hum", "windspeed"]

def train_daily_model(df):
    """Train a demo regression model for daily rental count; returns metrics and pipeline."""
    X = df[FEATURES].copy()
    y = df["cnt"].astype(float)
    numeric = FEATURES
    prep = ColumnTransformer(
        [("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), numeric)],
        remainder="drop"
    )
    model = Pipeline([
        ("prep", prep),
        ("rf", RandomForestRegressor(n_estimators=250, random_state=42,
                                     min_samples_leaf=2, n_jobs=-1))
    ])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    metrics = {
        "MAE": mean_absolute_error(y_test, pred),
        "RMSE": mean_squared_error(y_test, pred) ** 0.5,
        "R²": r2_score(y_test, pred),
    }
    return model, metrics, X_test, y_test, pred

def feature_importance(model):
    imp = model.named_steps["rf"].feature_importances_
    return pd.DataFrame({"Feature": FEATURES, "Importance": imp}).sort_values(
        "Importance", ascending=False
    )
