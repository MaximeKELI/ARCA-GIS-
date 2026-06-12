"""Estimation séquestration carbone par parcelle."""

SEQUESTRATION = {"maize": 2.0, "rice": 1.5, "cassava": 1.8, "cocoa": 5.0, "forest": 8.0}


def estimate_carbon(area_ha: float, crop_type: str) -> dict:
    rate = SEQUESTRATION.get(crop_type, 2.0)
    co2 = round(area_ha * rate, 2)
    return {
        "area_hectares": area_ha,
        "crop_type": crop_type,
        "co2_tons_year": co2,
        "credit_value_usd": round(co2 * 15, 2),
        "methodology": "ARCA-GIS-VM001",
    }
