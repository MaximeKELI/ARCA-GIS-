"""Fusion NDVI + météo + sol pour prédiction rendement."""


def fuse_yield(crop_type: str, area_ha: float, ndvi: float,
               soil_moisture: float, temperature: float, rainfall_mm: float) -> dict:
    base_yield = {"maize": 3.5, "rice": 4.0, "cassava": 12.0, "cocoa": 0.8}.get(crop_type, 2.5)
    ndvi_factor = 0.5 + ndvi
    water_factor = min(soil_moisture / 60, 1.2)
    temp_factor = 1.0 if 22 <= temperature <= 32 else 0.7
    rain_factor = min(rainfall_mm / 30, 1.1)

    yield_per_ha = base_yield * ndvi_factor * water_factor * temp_factor * rain_factor
    total = round(yield_per_ha * area_ha, 2)

    return {
        "crop_type": crop_type,
        "area_hectares": area_ha,
        "yield_per_ha_tons": round(yield_per_ha, 2),
        "total_yield_tons": total,
        "factors": {"ndvi": ndvi_factor, "water": water_factor, "temp": temp_factor, "rain": rain_factor},
        "confidence": 0.78,
        "source": "fusion_model_v1",
    }
