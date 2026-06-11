"""Recommandations agricoles intelligentes pour ARCA-GIS."""

from climate_analyzer import ClimateRisk, WeatherData

CROP_PROFILES = {
    "maize": {
        "name": "Maïs",
        "optimal_temp": (20, 35),
        "water_need_mm": 500,
        "drought_tolerance": "medium",
        "flood_tolerance": "low",
    },
    "rice": {
        "name": "Riz",
        "optimal_temp": (20, 35),
        "water_need_mm": 1200,
        "drought_tolerance": "low",
        "flood_tolerance": "high",
    },
    "cassava": {
        "name": "Manioc",
        "optimal_temp": (25, 35),
        "water_need_mm": 400,
        "drought_tolerance": "high",
        "flood_tolerance": "medium",
    },
    "cocoa": {
        "name": "Cacao",
        "optimal_temp": (21, 32),
        "water_need_mm": 800,
        "drought_tolerance": "low",
        "flood_tolerance": "low",
    },
    "coffee": {
        "name": "Café",
        "optimal_temp": (18, 28),
        "water_need_mm": 600,
        "drought_tolerance": "medium",
        "flood_tolerance": "low",
    },
    "cotton": {
        "name": "Coton",
        "optimal_temp": (22, 35),
        "water_need_mm": 700,
        "drought_tolerance": "medium",
        "flood_tolerance": "low",
    },
    "groundnut": {
        "name": "Arachide",
        "optimal_temp": (22, 33),
        "water_need_mm": 500,
        "drought_tolerance": "high",
        "flood_tolerance": "low",
    },
}


def assess_crop_health(
    crop_type: str,
    weather: WeatherData,
    risks: list[ClimateRisk],
) -> tuple[str, float]:
    """Évalue la santé de la culture et retourne (status, score 0-1)."""
    profile = CROP_PROFILES.get(crop_type, CROP_PROFILES["maize"])
    score = 1.0

    t_min, t_max = profile["optimal_temp"]
    if weather.temperature < t_min or weather.temperature > t_max:
        score -= 0.2

    if weather.soil_moisture is not None:
        if weather.soil_moisture < 35:
            score -= 0.25 if profile["drought_tolerance"] == "low" else 0.1
        if weather.soil_moisture > 85:
            score -= 0.2 if profile["flood_tolerance"] == "low" else 0.05

    for risk in risks:
        if risk.severity == "high":
            score -= 0.2
        elif risk.severity == "medium":
            score -= 0.1

    score = max(0.0, min(1.0, score))

    if score >= 0.8:
        status = "excellent"
    elif score >= 0.6:
        status = "good"
    elif score >= 0.4:
        status = "moderate"
    elif score >= 0.2:
        status = "poor"
    else:
        status = "critical"

    return status, round(score, 2)


def generate_recommendations(
    crop_type: str,
    weather: WeatherData,
    risks: list[ClimateRisk],
) -> list[str]:
    """Génère des recommandations agricoles contextualisées."""
    profile = CROP_PROFILES.get(crop_type, CROP_PROFILES["maize"])
    crop_name = profile["name"]
    recommendations: list[str] = []

    risk_types = {r.risk_type for r in risks}

    if "drought" in risk_types:
        if profile["drought_tolerance"] == "low":
            recommendations.append(
                f"Irrigation urgente pour {crop_name}. Arroser tôt le matin (5h-7h)."
            )
        else:
            recommendations.append(
                f"Réduire l'espacement des plants de {crop_name}. Pailler le sol."
            )

    if "flood" in risk_types:
        recommendations.append(
            f"Améliorer le drainage des parcelles de {crop_name}. Créer des rigoles."
        )
        if profile["flood_tolerance"] == "low":
            recommendations.append(
                f"Récolter rapidement le {crop_name} mature. Déplacer les stocks."
            )

    if "heatwave" in risk_types:
        recommendations.append(
            "Installer de l'ombrage temporaire. Augmenter la fréquence d'arrosage."
        )

    if "disease" in risk_types:
        recommendations.append(
            f"Appliquer un traitement fongicide préventif sur {crop_name}. "
            "Surveiller les taches foliaires."
        )

    t_min, t_max = profile["optimal_temp"]
    if weather.temperature < t_min:
        recommendations.append(
            f"Température basse pour {crop_name}. Reporter les semis de 1-2 semaines."
        )
    elif weather.temperature > t_max:
        recommendations.append(
            f"Température élevée pour {crop_name}. Privilégier les variétés résistantes à la chaleur."
        )

    if not recommendations:
        recommendations.append(
            f"Conditions favorables pour {crop_name}. Maintenir les pratiques culturales actuelles."
        )

    return recommendations
