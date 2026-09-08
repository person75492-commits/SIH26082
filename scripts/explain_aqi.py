import pandas as pd
import joblib
import os

MODEL_PATH = "models/aqi_random_forest.pkl"
FEATURES_PATH = "models/features.pkl"
DATA_PATH = "data/processed/delhi_historical_aqi_clean.csv"

model = joblib.load(MODEL_PATH)
features = joblib.load(FEATURES_PATH)

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Use the latest available historical data
latest = df.iloc[-1]

input_data = pd.DataFrame([{
    "year": latest["date"].year,
    "month": latest["date"].month,
    "day": latest["date"].day,
    "day_of_week": latest["date"].dayofweek,
    "aqi_lag_1": latest["aqi_lag_1"],
    "aqi_lag_3": latest["aqi_lag_3"],
    "aqi_lag_7": latest["aqi_lag_7"],
    "aqi_rolling_3": latest["aqi_rolling_3"],
    "aqi_rolling_7": latest["aqi_rolling_7"]
}])

prediction = model.predict(input_data[features])[0]

# Random Forest feature importance
importance = model.feature_importances_

explanation = pd.DataFrame({
    "feature": features,
    "importance": importance
})

explanation = explanation.sort_values(
    "importance",
    ascending=False
)

print("\n==============================")
print("EXPLAINABLE AI")
print("==============================")

print(f"Latest historical date: {latest['date'].date()}")
print(f"Latest AQI: {latest['Index Value']:.0f}")
print(f"Predicted AQI: {prediction:.2f}")

print("\nTop factors influencing the model:")

for _, row in explanation.head(5).iterrows():
    print(
        f"• {row['feature']} : "
        f"{row['importance']:.3f}"
    )

# Save explanation
os.makedirs("data/processed", exist_ok=True)

explanation.to_csv(
    "data/processed/aqi_feature_importance.csv",
    index=False
)

print("\nExplanation saved to:")
print("data/processed/aqi_feature_importance.csv")