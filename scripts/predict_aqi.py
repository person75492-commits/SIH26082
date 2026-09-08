import pandas as pd
import numpy as np
import joblib
import os

MODEL_PATH = "models/aqi_random_forest.pkl"
FEATURES_PATH = "models/features.pkl"
DATA_PATH = "data/processed/delhi_historical_aqi_clean.csv"

OUTPUT_PATH = "data/processed/aqi_forecast.csv"

print("Loading model and data...")

model = joblib.load(MODEL_PATH)
features = joblib.load(FEATURES_PATH)

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date")

# Last known AQI
history = list(df["Index Value"].dropna().tail(7))

last_date = df["date"].iloc[-1]

forecasts = []

# Predict next 3 days
for day in range(1, 4):

    forecast_date = last_date + pd.Timedelta(days=day)

    aqi_lag_1 = history[-1]
    aqi_lag_3 = history[-3]
    aqi_lag_7 = history[-7]

    aqi_rolling_3 = np.mean(history[-3:])
    aqi_rolling_7 = np.mean(history[-7:])

    input_data = pd.DataFrame([{
        "year": forecast_date.year,
        "month": forecast_date.month,
        "day": forecast_date.day,
        "day_of_week": forecast_date.dayofweek,
        "aqi_lag_1": aqi_lag_1,
        "aqi_lag_3": aqi_lag_3,
        "aqi_lag_7": aqi_lag_7,
        "aqi_rolling_3": aqi_rolling_3,
        "aqi_rolling_7": aqi_rolling_7
    }])

    prediction = model.predict(input_data[features])[0]

    # AQI cannot exceed official scale
    prediction = max(0, min(500, prediction))

    forecasts.append({
        "date": forecast_date.strftime("%Y-%m-%d"),
        "predicted_aqi": round(prediction, 2)
    })

    # Add prediction to history for recursive forecasting
    history.append(prediction)

forecast_df = pd.DataFrame(forecasts)

os.makedirs("data/processed", exist_ok=True)

forecast_df.to_csv(OUTPUT_PATH, index=False)

print("\n==============================")
print("3-DAY AQI FORECAST")
print("==============================")

print(forecast_df.to_string(index=False))

print("\nForecast saved to:")
print(OUTPUT_PATH)