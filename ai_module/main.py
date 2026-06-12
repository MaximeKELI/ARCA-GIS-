"""Module IA ARCA-GIS — API FastAPI pour analyse climatique et recommandations agricoles."""

from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field

from climate_analyzer import WeatherData, analyze_climate, generate_weather_for_location
from crop_advisor import assess_crop_health, generate_recommendations
from digital_twin import simulate_scenarios
from forecast_engine import generate_forecast
from ndvi_analyzer import compute_ndvi
from parcel_detector import detect_parcels
from sentinel_ndvi import compute_enhanced_ndvi
from carbon_estimator import estimate_carbon
from disease_detector import detect_from_image, detect_from_pest_count
from drone_pest import analyze_drone_image
from input_optimizer import optimize_inputs
from irrigation_advisor import advise_irrigation
from ml_model import predict_health, retrain
from price_forecaster import forecast_price
from rag_agent import rag_query
from yield_fusion import fuse_yield
from voice_assistant import get_voice_response
from yield_predictor import predict_yield

app = FastAPI(
    title="ARCA-GIS AI Module",
    description="Analyse climatique, NDVI et recommandations agricoles pour l'Afrique",
    version="5.0.0",
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


class ForecastRequest(BaseModel):
    lat: float
    lng: float
    crop_type: str = "maize"
    days: int = Field(default=14, ge=1, le=30)


class NDVIRequest(BaseModel):
    lat: float
    lng: float
    crop_type: str = "maize"


@app.get("/health")
def health():
    return {"status": "ok", "service": "arca-gis-ai", "version": "5.0.0"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    if request.temperature is not None:
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
    ndvi = compute_ndvi(request.lat, request.lng, request.crop_type)

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
            {"type": r.risk_type, "severity": r.severity,
             "probability": r.probability, "description": r.description}
            for r in risks
        ],
        "crop_health": crop_health,
        "health_score": health_score,
        "ndvi": ndvi,
        "recommendations": recommendations,
        "confidence": confidence,
        "source": "ai_module",
        "analyzed_at": datetime.utcnow().isoformat(),
    }


@app.post("/analyze/batch")
def analyze_batch(request: BatchAnalyzeRequest):
    return {"results": [analyze(loc) for loc in request.locations]}


@app.post("/forecast")
def forecast(request: ForecastRequest):
    return generate_forecast(request.lat, request.lng, request.crop_type, request.days)


@app.post("/ndvi")
def ndvi_analysis(request: NDVIRequest):
    return compute_ndvi(request.lat, request.lng, request.crop_type)


class YieldRequest(BaseModel):
    crop_type: str = "maize"
    area_hectares: float = 1.0
    ndvi_score: float = 0.5
    soil_moisture: float = 50.0
    temperature: float = 28.0


class DetectRequest(BaseModel):
    lat: float
    lng: float
    radius_km: float = 2.0


class TwinRequest(BaseModel):
    lat: float
    lng: float
    crop_type: str = "maize"
    area_hectares: float = 1.0


class VoiceRequest(BaseModel):
    query: str
    language: str = "fr"
    context: dict | None = None


@app.post("/yield")
def yield_prediction(request: YieldRequest):
    return predict_yield(
        request.crop_type, request.area_hectares,
        request.ndvi_score, request.soil_moisture, request.temperature,
    )


@app.post("/detect-parcels")
def auto_detect_parcels(request: DetectRequest):
    return {"parcels": detect_parcels(request.lat, request.lng, request.radius_km)}


@app.post("/sentinel-ndvi")
def sentinel_ndvi(request: NDVIRequest):
    return compute_enhanced_ndvi(request.lat, request.lng, request.crop_type)


@app.post("/digital-twin")
def digital_twin(request: TwinRequest):
    return simulate_scenarios(request.lat, request.lng, request.crop_type, request.area_hectares)


@app.post("/voice")
def voice_assistant(request: VoiceRequest):
    return get_voice_response(request.query, request.language, request.context)


@app.get("/crops")
def list_crops():
    from crop_advisor import CROP_PROFILES
    return {
        crop: {"name": p["name"], "optimal_temp": p["optimal_temp"]}
        for crop, p in CROP_PROFILES.items()
    }


class DiseaseRequest(BaseModel):
    image_b64: str | None = None
    crop_type: str = "maize"


class PestDetectRequest(BaseModel):
    pest_count: int = 0
    crop_type: str = "maize"


class IrrigationRequest(BaseModel):
    lat: float
    lng: float
    crop_type: str = "maize"
    soil_moisture: float = 50.0


class HealthPredictRequest(BaseModel):
    temperature: float = 28.0
    rainfall_mm: float = 5.0
    humidity: float = 60.0
    soil_moisture: float = 50.0
    ndvi: float = 0.5


@app.post("/disease-detect")
def disease_detect(request: DiseaseRequest):
    return detect_from_image(request.image_b64, request.crop_type)


@app.post("/disease-detect/pest")
def pest_detect(request: PestDetectRequest):
    return detect_from_pest_count(request.pest_count, request.crop_type)


@app.post("/irrigation")
def irrigation_advice(request: IrrigationRequest):
    return advise_irrigation(request.lat, request.lng, request.crop_type, request.soil_moisture)


@app.post("/predict-health")
def health_predict(request: HealthPredictRequest):
    return predict_health(
        request.temperature, request.rainfall_mm, request.humidity,
        request.soil_moisture, request.ndvi,
    )


@app.post("/retrain")
def model_retrain(samples: list[dict]):
    return retrain(samples)
