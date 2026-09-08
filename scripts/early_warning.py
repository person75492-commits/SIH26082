import pandas as pd
import os

INPUT = "data/processed/aqi_forecast.csv"
OUTPUT = "data/processed/aqi_early_warning.csv"

df = pd.read_csv(INPUT)

def get_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    else:
        return "Severe"

def get_alert(category):
    if category == "Good":
        return "Normal conditions"
    elif category == "Satisfactory":
        return "Low risk"
    elif category == "Moderate":
        return "Sensitive groups should take care"
    elif category == "Poor":
        return "Health advisory"
    elif category == "Very Poor":
        return "Early warning: reduce outdoor exposure"
    else:
        return "Severe warning: avoid outdoor exposure"

df["category"] = df["predicted_aqi"].apply(get_category)
df["alert"] = df["category"].apply(get_alert)

df.to_csv(OUTPUT, index=False)

print("\n==============================")
print("EARLY WARNING SYSTEM")
print("==============================")

for _, row in df.iterrows():
    print(
        f"{row['date']} | "
        f"AQI: {row['predicted_aqi']:.2f} | "
        f"{row['category']} | "
        f"{row['alert']}"
    )

print("\nSaved to:")
print(OUTPUT)