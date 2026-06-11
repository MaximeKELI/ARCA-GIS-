"""Analyse NDVI simulée à partir de coordonnées (proxy satellite)."""

import hashlib


def compute_ndvi(lat: float, lng: float, crop_type: str = "maize") -> dict:
    """Calcule un score NDVI simulé basé sur la géolocalisation et la culture."""
    seed = int(hashlib.md5(f"ndvi:{lat:.3f},{lng:.3f},{crop_type}".encode()).hexdigest()[:8], 16)

    base_ndvi = 0.3 + (seed % 60) / 100

    crop_factors = {
        "maize": 0.05, "rice": 0.08, "cassava": 0.03,
        "cocoa": 0.06, "coffee": 0.04, "cotton": 0.02,
        "groundnut": 0.03,
    }
    ndvi = min(0.95, base_ndvi + crop_factors.get(crop_type, 0.03))

    if ndvi >= 0.7:
        health = "excellent"
        description = "Végétation dense et saine"
    elif ndvi >= 0.5:
        health = "good"
        description = "Couverture végétale satisfaisante"
    elif ndvi >= 0.3:
        health = "moderate"
        description = "Stress végétatif modéré détecté"
    elif ndvi >= 0.15:
        health = "poor"
        description = "Végétation clairsemée — intervention recommandée"
    else:
        health = "critical"
        description = "Sol nu ou culture très dégradée"

    return {
        "ndvi_score": round(ndvi, 3),
        "health_from_ndvi": health,
        "description": description,
        "crop_type": crop_type,
        "location": {"lat": lat, "lng": lng},
    }
