import cdsapi
import os
import calendar

OUTPUT_DIR = "data/raw/era5"

os.makedirs(OUTPUT_DIR, exist_ok=True)

client = cdsapi.Client()

dataset = "reanalysis-era5-single-levels"

for year in ["2021", "2022", "2023"]:

    for month in range(1, 13):

        month_str = f"{month:02d}"
        days = [
            f"{day:02d}"
            for day in range(1, calendar.monthrange(int(year), month)[1] + 1)
        ]

        output = os.path.join(
            OUTPUT_DIR,
            f"era5_delhi_ncr_{year}_{month_str}.zip"
        )

        # Skip if already downloaded
        if os.path.exists(output):
            print(f"Already exists: {output}")
            continue

        request = {
            "product_type": ["reanalysis"],

            "variable": [
                "10m_u_component_of_wind",
                "10m_v_component_of_wind",
                "2m_dewpoint_temperature",
                "2m_temperature",
                "surface_pressure",
                "total_precipitation"
            ],

            "year": [year],
            "month": [month_str],
            "day": days,

            "time": [
                f"{hour:02d}:00"
                for hour in range(24)
            ],

            # North, West, South, East
            "area": [29.0, 76.5, 27.75, 78.0],

            "data_format": "netcdf",
            "download_format": "zip"
        }

        print(f"\nDownloading ERA5: {year}-{month_str}")

        client.retrieve(
            dataset,
            request,
            output
        )

        print(f"Saved: {output}")

print("\nAll ERA5 downloads completed!")