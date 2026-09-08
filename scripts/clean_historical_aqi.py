import pandas as pd
import os

INPUT = "data/raw/cpcb/delhi_historical_aqi.csv"
OUTPUT = "data/processed/delhi_historical_aqi_clean.csv"

os.makedirs("data/processed", exist_ok=True)

print("Reading historical Delhi AQI...")

df = pd.read_csv(INPUT)

# Clean column names
df.columns = df.columns.str.strip()

# Convert date
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Convert AQI to numeric
df["Index Value"] = pd.to_numeric(df["Index Value"], errors="coerce")

# Remove invalid records
df = df.dropna(subset=["date", "Index Value"])

# Keep Delhi only
df = df[df["City"].str.strip().str.lower() == "delhi"]

# Sort chronologically
df = df.sort_values("date")

# Remove duplicate dates
df = df.drop_duplicates(subset=["date"], keep="last")

# Create useful time features
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["day_of_week"] = df["date"].dt.dayofweek

# AQI lag features
df["aqi_lag_1"] = df["Index Value"].shift(1)
df["aqi_lag_3"] = df["Index Value"].shift(3)
df["aqi_lag_7"] = df["Index Value"].shift(7)

# Rolling averages
df["aqi_rolling_3"] = df["Index Value"].rolling(3).mean()
df["aqi_rolling_7"] = df["Index Value"].rolling(7).mean()

# Save
df.to_csv(OUTPUT, index=False)

print("\nCleaning completed!")
print("Rows:", len(df))
print("Date range:", df["date"].min().date(), "to", df["date"].max().date())
print("\nAQI statistics:")
print(df["Index Value"].describe())

print("\nSaved to:")
print(OUTPUT)