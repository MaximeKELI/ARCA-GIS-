"""Prédiction de rendement agricole (tonnes/ha)."""

import hashlib

YIELD_BASELINES = {
    "maize": {"min": 1.5, "avg": 3.5, "max": 8.0},
    "rice": {"min": 2.0, "avg": 4.5, "max": 9.0},
    "cassava": {"min": 8.0, "avg": 15.0, "max": 25.0},
    "cocoa": {"min": 0.3, "avg": 0.8, "max": 1.5},
    "coffee": {"min": 0.4, "avg": 1.0, "max": 2.0},
    "groundnut": {"min": 0.8, "avg": 1.5, "max": 3.0},
    "cotton": {"min": 1.0, "avg": 2.0, "max": 4.0},
}


def predict_yield(
    crop_type: str,
    area_hectares: float,
    ndvi_score: float = 0.5,
    soil_moisture: float = 50.0,
    temperature: float = 28.0,
) -> dict:
    baseline = YIELD_BASELINES.get(crop_type, YIELD_BASELINES["maize"])

    ndvi_factor = 0.5 + ndvi_score * 0.8
    moisture_factor = 1.0 if 40 <= soil_moisture <= 70 else 0.7
    temp_factor = 1.0 if 20 <= temperature <= 35 else 0.75

    predicted_per_ha = baseline["avg"] * ndvi_factor * moisture_factor * temp_factor
    predicted_per_ha = max(baseline["min"], min(baseline["max"], predicted_per_ha))

    total = round(predicted_per_ha * area_hectares, 2)
    confidence = round(min(0.9, 0.5 + ndvi_score * 0.3 + (moisture_factor - 0.5) * 0.2), 2)

    return {
        "crop_type": crop_type,
        "area_hectares": area_hectares,
        "yield_per_hectare": round(predicted_per_ha, 2),
        "total_yield": total,
        "unit": "tonnes" if crop_type not in ("cassava",) else "tonnes",
        "confidence": confidence,
        "factors": {
            "ndvi": round(ndvi_factor, 2),
            "moisture": round(moisture_factor, 2),
            "temperature": round(temp_factor, 2),
        },
    }
