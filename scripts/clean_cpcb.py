import pandas as pd
import os

input_file = "data/raw/cpcb/cpcb_air_quality.csv"
output_file = "data/processed/cpcb_clean.csv"

os.makedirs("data/processed", exist_ok=True)

print("Reading CPCB data...")

df = pd.read_csv(input_file)

# Convert timestamp
df["last_update"] = pd.to_datetime(df["last_update"], errors="coerce")

# Convert pollutant values to numeric
df["pollutant_avg"] = pd.to_numeric(df["pollutant_avg"], errors="coerce")

# Remove rows without timestamp or pollutant value
df = df.dropna(subset=["last_update", "pollutant_avg"])

# Keep Delhi NCR cities
ncr_cities = [
    "Delhi",
    "New Delhi",
    "Noida",
    "Greater Noida",
    "Ghaziabad",
    "Gurugram",
    "Gurgaon",
    "Faridabad"
]

df = df[df["city"].isin(ncr_cities)]

# Sort data
df = df.sort_values(["city", "station", "last_update"])

# Save cleaned dataset
df.to_csv(output_file, index=False)

print("\nCleaning completed!")
print("Rows remaining:", len(df))
print("Cities:", df["city"].unique().tolist())
print("Pollutants:", df["pollutant_id"].unique().tolist())
print("Saved to:", output_file)