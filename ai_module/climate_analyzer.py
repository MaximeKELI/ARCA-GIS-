"""Analyse climatique pour ARCA-GIS — détection sécheresse, inondations, canicules."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class WeatherData:
    temperature: float
    rainfall_mm: float
    humidity: float
    wind_speed: float = 0.0
    soil_moisture: float | None = None


@dataclass
class ClimateRisk:
    risk_type: str
    severity: str
    probability: float
    description: str


# Seuils calibrés pour l'Afrique de l'Ouest / Centrale
DROUGHT_THRESHOLDS = {"rainfall_max": 15, "humidity_max": 45, "temp_min": 30}
FLOOD_THRESHOLDS = {"rainfall_min": 80, "humidity_min": 85}
HEATWAVE_THRESHOLDS = {"temp_min": 38, "humidity_max": 40}
DISEASE_THRESHOLDS = {"humidity_min": 75, "temp_range": (22, 32)}


def analyze_climate(weather: WeatherData, lat: float, lng: float) -> list[ClimateRisk]:
    """Analyse les conditions météo et retourne les risques détectés."""
    risks: list[ClimateRisk] = []

    if weather.rainfall_mm < DROUGHT_THRESHOLDS["rainfall_max"] and weather.humidity < DROUGHT_THRESHOLDS["humidity_max"]:
        prob = min(0.95, 0.5 + (DROUGHT_THRESHOLDS["rainfall_max"] - weather.rainfall_mm) / 30)
        risks.append(ClimateRisk(
            risk_type="drought",
            severity="high" if prob > 0.7 else "medium",
            probability=round(prob, 2),
            description=f"Sécheresse probable: pluie {weather.rainfall_mm}mm, humidité {weather.humidity}%",
        ))

    if weather.rainfall_mm > FLOOD_THRESHOLDS["rainfall_min"]:
        prob = min(0.9, 0.4 + (weather.rainfall_mm - FLOOD_THRESHOLDS["rainfall_min"]) / 100)
        risks.append(ClimateRisk(
            risk_type="flood",
            severity="high" if weather.rainfall_mm > 150 else "medium",
            probability=round(prob, 2),
            description=f"Risque d'inondation: précipitations {weather.rainfall_mm}mm",
        ))

    if weather.temperature > HEATWAVE_THRESHOLDS["temp_min"]:
        prob = min(0.9, 0.5 + (weather.temperature - HEATWAVE_THRESHOLDS["temp_min"]) / 10)
        risks.append(ClimateRisk(
            risk_type="heatwave",
            severity="high" if weather.temperature > 42 else "medium",
            probability=round(prob, 2),
            description=f"Canicule: température {weather.temperature}°C",
        ))

    t_min, t_max = DISEASE_THRESHOLDS["temp_range"]
    if weather.humidity > DISEASE_THRESHOLDS["humidity_min"] and t_min <= weather.temperature <= t_max:
        risks.append(ClimateRisk(
            risk_type="disease",
            severity="medium",
            probability=0.55,
            description="Conditions favorables aux maladies fongiques des cultures",
        ))

    if weather.soil_moisture is not None and weather.soil_moisture < 30:
        risks.append(ClimateRisk(
            risk_type="drought",
            severity="high",
            probability=0.8,
            description=f"Sol très sec: humidité du sol {weather.soil_moisture}%",
        ))

    return risks


def generate_weather_for_location(lat: float, lng: float) -> WeatherData:
    """Génère des données météo simulées basées sur la géolocalisation."""
    import hashlib

    seed = int(hashlib.md5(f"{lat:.2f},{lng:.2f}".encode()).hexdigest()[:8], 16)
    rng = seed % 1000

    base_temp = 28 + (abs(lat) % 10) * 0.5
    temp = base_temp + (rng % 100) / 20 - 2.5

    rainfall = max(0, (rng % 150) - 30 + (5 if abs(lng) < 10 else 0))
    humidity = 40 + (rng % 50)
    wind = 5 + (rng % 30)
    soil = 30 + (rng % 50)

    return WeatherData(
        temperature=round(temp, 1),
        rainfall_mm=round(rainfall, 1),
        humidity=round(humidity, 1),
        wind_speed=round(wind, 1),
        soil_moisture=round(soil, 1),
    )
