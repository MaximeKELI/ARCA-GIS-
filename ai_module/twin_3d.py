def generate_3d_twin(lat: float, lng: float, crop_type: str, area_ha: float) -> dict:
    return {
        "location": {"lat": lat, "lng": lng},
        "crop_type": crop_type,
        "area_hectares": area_ha,
        "model": {
            "format": "glTF",
            "vertices": int(area_ha * 1000),
            "elevation_range_m": [195, 220],
            "layers": ["terrain", "crop", "water", "buildings"],
        },
        "scenarios": [
            {"name": "sécheresse", "yield_impact_pct": -35},
            {"name": "optimal", "yield_impact_pct": +15},
        ],
        "viewer_url": f"/3d-twin?lat={lat}&lng={lng}",
    }
