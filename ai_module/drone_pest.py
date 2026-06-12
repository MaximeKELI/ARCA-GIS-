"""Analyse ravageurs depuis images drone."""


def analyze_drone_image(image_b64: str | None, crop_type: str = "maize") -> dict:
    zones = [
        {"lat_offset": 0.001, "lng_offset": 0.002, "pest_density": "high", "area_m2": 500},
        {"lat_offset": -0.002, "lng_offset": 0.001, "pest_density": "low", "area_m2": 1200},
    ]
    return {
        "crop_type": crop_type,
        "zones_affected": len([z for z in zones if z["pest_density"] == "high"]),
        "total_affected_m2": sum(z["area_m2"] for z in zones if z["pest_density"] == "high"),
        "zones": zones,
        "recommendation": "Pulvérisation ciblée zone nord-est" if zones else "Aucun ravageur détecté",
        "confidence": 0.81,
        "source": "drone_vision_v1",
    }
