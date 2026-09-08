import pandas as pd
import numpy as np
import os
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

INPUT = "data/processed/delhi_historical_aqi_clean.csv"
MODEL_DIR = "models"

os.makedirs(MODEL_DIR, exist_ok=True)

print("Loading data...")

df = pd.read_csv(INPUT)
df["date"] = pd.to_datetime(df["date"])

# Create features using ONLY previous AQI values
df["aqi_lag_1"] = df["Index Value"].shift(1)
df["aqi_lag_3"] = df["Index Value"].shift(3)
df["aqi_lag_7"] = df["Index Value"].shift(7)

df["aqi_rolling_3"] = df["Index Value"].shift(1).rolling(3).mean()
df["aqi_rolling_7"] = df["Index Value"].shift(1).rolling(7).mean()

# Predict NEXT DAY AQI
df["target"] = df["Index Value"].shift(-1)

df = df.dropna(subset=[
    "aqi_lag_1",
    "aqi_lag_3",
    "aqi_lag_7",
    "aqi_rolling_3",
    "aqi_rolling_7",
    "target"
])

features = [
    "year",
    "month",
    "day",
    "day_of_week",
    "aqi_lag_1",
    "aqi_lag_3",
    "aqi_lag_7",
    "aqi_rolling_3",
    "aqi_rolling_7"
]

X = df[features]
y = df["target"]

# Chronological split
split = int(len(df) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

print("\nTraining model...")

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")
print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R2   : {r2:.3f}")

joblib.dump(model, f"{MODEL_DIR}/aqi_random_forest.pkl")
joblib.dump(features, f"{MODEL_DIR}/features.pkl")

print("\nModel saved successfully!")