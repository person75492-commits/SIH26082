from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HISTORICAL_FILE = os.path.join(
    BASE, "data", "processed", "delhi_historical_aqi_clean.csv"
)

FORECAST_FILE = os.path.join(
    BASE, "data", "processed", "aqi_forecast.csv"
)

WARNING_FILE = os.path.join(
    BASE, "data", "processed", "aqi_early_warning.csv"
)

IMPORTANCE_FILE = os.path.join(
    BASE, "data", "processed", "aqi_feature_importance.csv"
)


def get_aqi_category(aqi):

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


@app.route("/")
def dashboard():

    historical = pd.read_csv(HISTORICAL_FILE)
    forecast = pd.read_csv(FORECAST_FILE)
    warnings = pd.read_csv(WARNING_FILE)
    importance = pd.read_csv(IMPORTANCE_FILE)

    historical["date"] = pd.to_datetime(historical["date"])

    # Historical data for chart
    historical_chart = historical[
        ["date", "Index Value"]
    ].dropna().tail(365)

    historical_chart["date"] = (
        historical_chart["date"]
        .dt.strftime("%Y-%m-%d")
    )

    # Latest AQI
    latest_aqi = float(
        historical["Index Value"].dropna().iloc[-1]
    )

    latest_date = historical["date"].iloc[-1]

    # Forecast
    forecast_records = forecast.to_dict("records")

    # Warnings
    warning_records = warnings.to_dict("records")

    # Explainability
    factor_records = importance.head(5).to_dict("records")

    return render_template(
        "index.html",

        latest_aqi=round(latest_aqi),

        latest_category=get_aqi_category(
            latest_aqi
        ),

        latest_date=latest_date.strftime(
            "%Y-%m-%d"
        ),

        forecast=forecast_records,

        warnings=warning_records,

        factors=factor_records,

        historical_dates=historical_chart[
            "date"
        ].tolist(),

        historical_values=historical_chart[
            "Index Value"
        ].tolist()
    )


@app.route("/api/data")
def api_data():

    historical = pd.read_csv(HISTORICAL_FILE)
    forecast = pd.read_csv(FORECAST_FILE)
    warnings = pd.read_csv(WARNING_FILE)
    importance = pd.read_csv(IMPORTANCE_FILE)

    historical["date"] = pd.to_datetime(
        historical["date"]
    )

    historical_chart = historical[
        ["date", "Index Value"]
    ].dropna().tail(365)

    return jsonify({

        "historical": {
            "dates": historical_chart[
                "date"
            ].dt.strftime("%Y-%m-%d").tolist(),

            "values": historical_chart[
                "Index Value"
            ].tolist()
        },

        "forecast": forecast.to_dict(
            "records"
        ),

        "warnings": warnings.to_dict(
            "records"
        ),

        "importance": importance.to_dict(
            "records"
        )
    })


CPCB_FILE = os.path.join(
    BASE, "data", "processed", "cpcb_clean.csv"
)


@app.route("/api/stations")
def api_stations():
    """Return CPCB station pollutant data as JSON for the dashboard map
    and pollutant table.  Only numeric columns are cast; the rest are
    kept as-is so the frontend can display them directly."""

    cpcb = pd.read_csv(CPCB_FILE)

    # Ensure numeric fields are proper numbers (not strings)
    for col in ("pollutant_min", "pollutant_max", "pollutant_avg",
                "latitude", "longitude"):
        if col in cpcb.columns:
            cpcb[col] = pd.to_numeric(cpcb[col], errors="coerce")

    # Replace NaN with None so jsonify serialises them as null
    records = cpcb.where(cpcb.notna(), other=None).to_dict("records")

    return jsonify(records)


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )