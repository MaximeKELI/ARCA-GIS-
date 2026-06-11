"""Moteur de prévisions agricoles sur 7-14 jours."""

from datetime import datetime, timedelta

from climate_analyzer import WeatherData, analyze_climate, generate_weather_for_location
from crop_advisor import assess_crop_health, generate_recommendations


def generate_forecast(lat: float, lng: float, crop_type: str, days: int = 14) -> dict:
    forecasts = []
    cumulative_rain = 0
    max_temp = 0
    risk_counts: dict[str, int] = {}

    for day in range(days):
        offset_lat = lat + (day * 0.001)
        weather = generate_weather_for_location(offset_lat, lng)
        risks = analyze_climate(weather, offset_lat, lng)
        health, score = assess_crop_health(crop_type, weather, risks)

        cumulative_rain += weather.rainfall_mm
        max_temp = max(max_temp, weather.temperature)

        for r in risks:
            risk_counts[r.risk_type] = risk_counts.get(r.risk_type, 0) + 1

        forecasts.append({
            "day": day + 1,
            "date": (datetime.utcnow() + timedelta(days=day)).strftime("%Y-%m-%d"),
            "temperature": weather.temperature,
            "rainfall_mm": weather.rainfall_mm,
            "humidity": weather.humidity,
            "crop_health": health,
            "health_score": score,
            "risks": [{"type": r.risk_type, "severity": r.severity} for r in risks],
        })

    dominant_risk = max(risk_counts, key=risk_counts.get) if risk_counts else None
    summary = {
        "period_days": days,
        "cumulative_rainfall_mm": round(cumulative_rain, 1),
        "max_temperature": round(max_temp, 1),
        "dominant_risk": dominant_risk,
        "risk_frequency": risk_counts,
    }

    final_weather = WeatherData(
        temperature=forecasts[-1]["temperature"],
        rainfall_mm=cumulative_rain / days,
        humidity=forecasts[-1]["humidity"],
    )
    final_risks = analyze_climate(final_weather, lat, lng)
    recommendations = generate_recommendations(crop_type, final_weather, final_risks)

    return {
        "location": {"lat": lat, "lng": lng},
        "crop_type": crop_type,
        "summary": summary,
        "daily": forecasts,
        "recommendations": recommendations,
        "generated_at": datetime.utcnow().isoformat(),
    }
