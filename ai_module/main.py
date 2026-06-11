"""Module IA ARCA-GIS — API FastAPI pour analyse climatique et recommandations agricoles."""

from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field

from climate_analyzer import analyze_climate, generate_weather_for_location
from crop_advisor import assess_crop_health, generate_recommendations

app = FastAPI(
    title="ARCA-GIS AI Module",
    description="Analyse climatique et recommandations agricoles pour l'Afrique",
    version="1.0.0",
)


class AnalyzeRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    crop_type: str = "maize"
    temperature: float | None = None
    rainfall_mm: float | None = None
    humidity: float | None = None
    soil_moisture: float | None = None


class BatchAnalyzeRequest(BaseModel):
    locations: list[AnalyzeRequest]


@app.get("/health")
def health():
    return {"status": "ok", "service": "arca-gis-ai", "version": "1.0.0"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    if request.temperature is not None:
        from climate_analyzer import WeatherData
        weather = WeatherData(
            temperature=request.temperature,
            rainfall_mm=request.rainfall_mm or 0,
            humidity=request.humidity or 50,
            soil_moisture=request.soil_moisture,
        )
    else:
        weather = generate_weather_for_location(request.lat, request.lng)

    risks = analyze_climate(weather, request.lat, request.lng)
    crop_health, health_score = assess_crop_health(request.crop_type, weather, risks)
    recommendations = generate_recommendations(request.crop_type, weather, risks)

    confidence = 0.85 if request.temperature else 0.75

    return {
        "location": {"lat": request.lat, "lng": request.lng},
        "crop_type": request.crop_type,
        "weather": {
            "temperature": weather.temperature,
            "rainfall_mm": weather.rainfall_mm,
            "humidity": weather.humidity,
            "wind_speed": weather.wind_speed,
            "soil_moisture": weather.soil_moisture,
        },
        "risks": [
            {
                "type": r.risk_type,
                "severity": r.severity,
                "probability": r.probability,
                "description": r.description,
            }
            for r in risks
        ],
        "crop_health": crop_health,
        "health_score": health_score,
        "recommendations": recommendations,
        "confidence": confidence,
        "source": "ai_module",
        "analyzed_at": datetime.utcnow().isoformat(),
    }


@app.post("/analyze/batch")
def analyze_batch(request: BatchAnalyzeRequest):
    return {"results": [analyze(loc) for loc in request.locations]}


@app.get("/crops")
def list_crops():
    from crop_advisor import CROP_PROFILES
    return {
        crop: {"name": p["name"], "optimal_temp": p["optimal_temp"]}
        for crop, p in CROP_PROFILES.items()
    }
