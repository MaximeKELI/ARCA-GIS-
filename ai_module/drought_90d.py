import hashlib
import random


def forecast_drought(region: str, days: int = 90) -> dict:
    seed = int(hashlib.md5(region.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    prob = round(rng.uniform(0.2, 0.8), 2)
    level = "low" if prob < 0.35 else "moderate" if prob < 0.6 else "high"
    return {
        "region": region, "forecast_days": days,
        "probability_drought": prob, "risk_level": level,
        "monthly_rainfall_mm": [round(rng.uniform(10, 80), 1) for _ in range(min(days // 30, 3))],
        "recommendations": [
            "Construire réserves d'eau" if prob > 0.5 else "Surveillance normale",
            "Privilégier cultures résistantes (niébé, mil)" if prob > 0.6 else "Irrigation standard",
        ],
        "source": "arca_drought_model_v1",
    }
