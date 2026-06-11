import logging
from datetime import datetime

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def fetch_real_weather(lat: float, lng: float) -> dict | None:
    """Récupère la météo via OpenWeatherMap ou NASA POWER (fallback)."""
    api_key = getattr(settings, "OPENWEATHER_API_KEY", None)
    if api_key:
        try:
            resp = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"lat": lat, "lon": lng, "appid": api_key, "units": "metric"},
                timeout=8,
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "temperature": data["main"]["temp"],
                "rainfall_mm": data.get("rain", {}).get("1h", 0),
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"] * 3.6,
                "description": data["weather"][0]["description"],
                "source": "openweathermap",
            }
        except requests.RequestException as e:
            logger.warning("OpenWeatherMap error: %s", e)

    try:
        resp = requests.get(
            "https://power.larc.nasa.gov/api/temporal/daily/point",
            params={
                "parameters": "T2M,PRECTOTCORR,RH2M",
                "community": "AG",
                "longitude": lng,
                "latitude": lat,
                "start": datetime.now().strftime("%Y%m%d"),
                "end": datetime.now().strftime("%Y%m%d"),
                "format": "JSON",
            },
            timeout=10,
        )
        resp.raise_for_status()
        params = resp.json()["properties"]["parameter"]
        return {
            "temperature": round(list(params["T2M"].values())[-1], 1),
            "rainfall_mm": round(list(params["PRECTOTCORR"].values())[-1], 1),
            "humidity": round(list(params["RH2M"].values())[-1], 1),
            "source": "nasa_power",
        }
    except (requests.RequestException, KeyError, IndexError) as e:
        logger.warning("NASA POWER error: %s", e)
        return None


def fetch_forecast(lat: float, lng: float, days: int = 7) -> list[dict]:
    """Prévisions météo sur N jours."""
    api_key = getattr(settings, "OPENWEATHER_API_KEY", None)
    if not api_key:
        return _simulated_forecast(lat, lng, days)

    try:
        resp = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={"lat": lat, "lon": lng, "appid": api_key, "units": "metric", "cnt": days * 8},
            timeout=8,
        )
        resp.raise_for_status()
        forecasts = []
        for item in resp.json().get("list", [])[:days]:
            forecasts.append({
                "datetime": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "rainfall_mm": item.get("rain", {}).get("3h", 0),
                "humidity": item["main"]["humidity"],
            })
        return forecasts
    except requests.RequestException:
        return _simulated_forecast(lat, lng, days)


def _simulated_forecast(lat: float, lng: float, days: int) -> list[dict]:
    import hashlib
    from datetime import timedelta

    seed = int(hashlib.md5(f"{lat},{lng}".encode()).hexdigest()[:8], 16)
    forecasts = []
    for i in range(days):
        forecasts.append({
            "datetime": (datetime.now() + timedelta(days=i)).isoformat(),
            "temperature": round(28 + (seed % 10) - 5 + i * 0.3, 1),
            "rainfall_mm": round(max(0, (seed % 50) - 20 + i * 2), 1),
            "humidity": round(50 + (seed % 40), 1),
        })
    return forecasts


def request_ai_analysis(lat: float, lng: float, crop_type: str) -> dict:
    weather = fetch_real_weather(lat, lng)
    payload = {"lat": lat, "lng": lng, "crop_type": crop_type}
    if weather:
        payload.update(weather)

    try:
        response = requests.post(
            f"{settings.AI_MODULE_URL}/analyze",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        result = response.json()
        if weather:
            result["weather"] = {**result.get("weather", {}), **weather}
        return result
    except requests.RequestException as e:
        logger.warning("AI module unavailable: %s", e)
        return _fallback_analysis(lat, lng, crop_type, weather)


def _fallback_analysis(lat: float, lng: float, crop_type: str, weather: dict | None = None) -> dict:
    import random

    if not weather:
        temp = round(random.uniform(22, 38), 1)
        rainfall = round(random.uniform(0, 80), 1)
        humidity = round(random.uniform(30, 95), 1)
        weather = {"temperature": temp, "rainfall_mm": rainfall, "humidity": humidity}

    risks = []
    recommendations = []
    temp = weather["temperature"]
    rainfall = weather.get("rainfall_mm", 0)
    humidity = weather.get("humidity", 50)

    if rainfall < 10:
        risks.append({"type": "drought", "severity": "high", "probability": 0.75})
        recommendations.append("Irrigation recommandée.")
    elif rainfall > 60:
        risks.append({"type": "flood", "severity": "medium", "probability": 0.6})
        recommendations.append("Améliorer le drainage.")

    if temp > 35:
        risks.append({"type": "heatwave", "severity": "high", "probability": 0.7})
        recommendations.append("Arrosage matinal recommandé.")

    crop_health = "good" if len(risks) <= 1 else "poor" if len(risks) >= 2 else "moderate"

    return {
        "location": {"lat": lat, "lng": lng},
        "crop_type": crop_type,
        "weather": weather,
        "risks": risks,
        "crop_health": crop_health,
        "recommendations": recommendations or ["Conditions favorables."],
        "confidence": 0.75 if weather.get("source") else 0.65,
        "source": weather.get("source", "fallback"),
        "analyzed_at": datetime.utcnow().isoformat(),
    }
