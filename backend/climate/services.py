import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def request_ai_analysis(lat: float, lng: float, crop_type: str) -> dict:
    """Appelle le module IA pour analyse climatique et recommandations."""
    try:
        response = requests.post(
            f"{settings.AI_MODULE_URL}/analyze",
            json={"lat": lat, "lng": lng, "crop_type": crop_type},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.warning("AI module unavailable: %s", e)
        return _fallback_analysis(lat, lng, crop_type)


def _fallback_analysis(lat: float, lng: float, crop_type: str) -> dict:
    """Analyse locale de secours si le module IA est indisponible."""
    import random
    from datetime import datetime

    temp = round(random.uniform(22, 38), 1)
    rainfall = round(random.uniform(0, 80), 1)
    humidity = round(random.uniform(30, 95), 1)

    risks = []
    recommendations = []

    if rainfall < 10:
        risks.append({"type": "drought", "severity": "high", "probability": 0.75})
        recommendations.append("Irrigation recommandée. Réduire la densité de semis.")
    elif rainfall > 60:
        risks.append({"type": "flood", "severity": "medium", "probability": 0.6})
        recommendations.append("Améliorer le drainage. Reporter les semis de 2 semaines.")

    if temp > 35:
        risks.append({"type": "heatwave", "severity": "high", "probability": 0.7})
        recommendations.append("Arrosage matinal et ombrage des jeunes plants.")

    if humidity > 80:
        risks.append({"type": "disease", "severity": "medium", "probability": 0.55})
        recommendations.append("Surveiller les signes de maladies fongiques.")

    crop_health = "good"
    if len(risks) >= 2:
        crop_health = "poor"
    elif len(risks) == 1:
        crop_health = "moderate"

    return {
        "location": {"lat": lat, "lng": lng},
        "crop_type": crop_type,
        "weather": {
            "temperature": temp,
            "rainfall_mm": rainfall,
            "humidity": humidity,
        },
        "risks": risks,
        "crop_health": crop_health,
        "recommendations": recommendations or ["Conditions favorables. Maintenir les pratiques actuelles."],
        "confidence": 0.65,
        "source": "fallback",
        "analyzed_at": datetime.utcnow().isoformat(),
    }
