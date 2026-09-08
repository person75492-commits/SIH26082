# SIH26082

**AI-Powered Air Pollution & Weather-Coupled Forecasting System**  
AERIS-72 | Delhi NCR Air Pollution Intelligence Dashboard

---

## Overview

This project forecasts Delhi NCR's Air Quality Index (AQI) up to 3 days ahead using a Random Forest model trained on 9 years of CPCB historical data. It includes a real-time interactive dark-themed dashboard built with Flask and Chart.js.

## Features

- 📊 **Interactive Dark Dashboard** (AERIS-72 style) with 6 navigation views
- 🔮 **3-Day AQI Forecast** using Random Forest (300 trees, 9 lag/rolling features)
- 🧠 **Explainable AI** — feature importance with animated charts
- 📍 **Live Station Map** — 408 CPCB readings across 6 NCR cities (Leaflet.js)
- ⚠️ **Early Warning System** — category-based health advisories
- 🎮 **Simulation Mode** — 3 scenario presets (Severe / Moderate / Good)
- 📈 **Historical Trends** — year-over-year comparison, seasonal patterns

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Flask |
| ML Model | scikit-learn RandomForestRegressor |
| Data | CPCB historical AQI (2015–2023), ERA5 weather |
| Frontend | Chart.js 4.4, Leaflet.js 1.9, Vanilla JS |
| Data processing | pandas, numpy |

## Project Structure

```
SIH26082/
├── dashboard/
│   ├── app.py              # Flask app — 3 routes
│   └── templates/
│       └── index.html      # Full interactive dashboard
├── scripts/
│   ├── clean_cpcb.py
│   ├── clean_historical_aqi.py
│   ├── train_model.py
│   ├── predict_aqi.py
│   ├── early_warning.py
│   └── explain_aqi.py
├── data/
│   ├── processed/          # Generated CSVs (gitignored)
│   └── raw/                # Raw data (gitignored)
├── models/                 # Trained model (gitignored)
├── requirements.txt
└── README.md
```

## Setup & Run

```bash
# 1. Clone
git clone https://github.com/person75492-commits/SIH26082.git
cd SIH26082

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the data pipeline (first time)
python scripts/clean_historical_aqi.py
python scripts/clean_cpcb.py
python scripts/train_model.py
python scripts/predict_aqi.py
python scripts/early_warning.py
python scripts/explain_aqi.py

# 5. Launch the dashboard
python dashboard/app.py
```

Open **http://127.0.0.1:5000** in your browser.

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Main dashboard |
| `GET /api/data` | Historical + forecast + importance JSON |
| `GET /api/stations` | CPCB station pollutant readings JSON |

## Model Performance

- **Algorithm:** Random Forest Regressor (300 trees, max_depth=15)
- **Features:** `aqi_rolling_7`, `aqi_lag_1`, `aqi_rolling_3`, `month`, `day`, `aqi_lag_7`, `aqi_lag_3`, `year`, `day_of_week`
- **Top feature:** `aqi_rolling_7` — 51.4% importance
- **Train/Test split:** 80/20 chronological

## Data Sources

- **CPCB** — Central Pollution Control Board historical daily AQI (Delhi, 2015–2023)
- **ERA5** — ECMWF reanalysis weather data (temperature, wind, humidity, precipitation)

---

*Smart India Hackathon 2026 — Team SIH26082*
