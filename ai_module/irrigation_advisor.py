"""Conseils d'irrigation basés sur humidité sol et culture."""

CROP_WATER = {
    "maize": {"optimal_moisture": 55, "daily_mm": 5, "critical_low": 35},
    "rice": {"optimal_moisture": 80, "daily_mm": 8, "critical_low": 60},
    "cassava": {"optimal_moisture": 45, "daily_mm": 3, "critical_low": 25},
    "cocoa": {"optimal_moisture": 65, "daily_mm": 4, "critical_low": 40},
}


def advise_irrigation(lat: float, lng: float, crop_type: str, soil_moisture: float) -> dict:
    profile = CROP_WATER.get(crop_type, CROP_WATER["maize"])
    deficit = profile["optimal_moisture"] - soil_moisture
    should_irrigate = soil_moisture < profile["critical_low"]

    if should_irrigate:
        amount = max(deficit * 0.5, profile["daily_mm"] * 2)
        frequency = "quotidien"
        urgency = "high"
    elif deficit > 10:
        amount = profile["daily_mm"]
        frequency = "tous les 2 jours"
        urgency = "medium"
    else:
        amount = 0
        frequency = "non nécessaire"
        urgency = "low"

    return {
        "location": {"lat": lat, "lng": lng},
        "crop_type": crop_type,
        "soil_moisture": soil_moisture,
        "optimal_moisture": profile["optimal_moisture"],
        "should_irrigate": should_irrigate or amount > 0,
        "amount_mm": round(amount, 1),
        "best_time": "05:00-07:00",
        "frequency": frequency,
        "urgency": urgency,
        "tips": [
            "Irriguer tôt le matin pour limiter l'évaporation",
            "Vérifier le drainage après fortes pluies",
            "Utiliser goutte-à-goutte si disponible",
        ],
    }
