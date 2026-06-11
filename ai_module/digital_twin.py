"""Jumeau numérique de parcelle — simulation de scénarios."""

from datetime import datetime, timedelta

from climate_analyzer import WeatherData, analyze_climate, generate_weather_for_location
from crop_advisor import assess_crop_health, generate_recommendations
from yield_predictor import predict_yield


def simulate_scenarios(
    lat: float, lng: float,
    crop_type: str = "maize",
    area_hectares: float = 1.0,
    scenarios: list[str] | None = None,
) -> dict:
    if scenarios is None:
        scenarios = ["current", "drought", "flood", "optimal"]

    base_weather = generate_weather_for_location(lat, lng)
    results = {}

    scenario_weather = {
        "current": base_weather,
        "drought": WeatherData(temperature=38, rainfall_mm=2, humidity=25, soil_moisture=15),
        "flood": WeatherData(temperature=26, rainfall_mm=150, humidity=95, soil_moisture=90),
        "optimal": WeatherData(temperature=27, rainfall_mm=40, humidity=65, soil_moisture=55),
    }

    for scenario in scenarios:
        weather = scenario_weather.get(scenario, base_weather)
        risks = analyze_climate(weather, lat, lng)
        health, score = assess_crop_health(crop_type, weather, risks)
        recommendations = generate_recommendations(crop_type, weather, risks)
        yield_pred = predict_yield(crop_type, area_hectares, score, weather.soil_moisture or 50, weather.temperature)

        results[scenario] = {
            "weather": {
                "temperature": weather.temperature,
                "rainfall_mm": weather.rainfall_mm,
                "humidity": weather.humidity,
            },
            "crop_health": health,
            "health_score": score,
            "risks": [{"type": r.risk_type, "severity": r.severity} for r in risks],
            "yield_prediction": yield_pred,
            "recommendations": recommendations,
        }

    return {
        "location": {"lat": lat, "lng": lng},
        "crop_type": crop_type,
        "area_hectares": area_hectares,
        "scenarios": results,
        "best_scenario": max(results, key=lambda s: results[s]["health_score"]),
        "simulated_at": datetime.utcnow().isoformat(),
    }
