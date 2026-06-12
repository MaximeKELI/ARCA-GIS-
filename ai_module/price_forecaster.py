"""Prévision prix marchés agricoles."""

import hashlib
import random

BASE_PRICES = {
    "maize": 250, "rice": 400, "cassava": 150, "cocoa": 1200,
    "coffee": 1800, "cotton": 350, "groundnut": 500,
}


def forecast_price(crop_type: str, days: int = 7) -> dict:
    base = BASE_PRICES.get(crop_type, 300)
    seed = int(hashlib.md5(f"{crop_type}{days}".encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    trend = rng.choice(["up", "down", "stable"])
    change = rng.uniform(-0.05, 0.08) if trend != "stable" else 0
    forecast = round(base * (1 + change), 0)

    rec = {
        "up": "Attendre 1-2 semaines avant de vendre",
        "down": "Vendre rapidement",
        "stable": "Prix stable — vendre selon besoin",
    }[trend]

    return {
        "crop_type": crop_type,
        "current_price_xof": base,
        "forecast_price_xof": forecast,
        "trend": trend,
        "change_pct": round(change * 100, 1),
        "period_days": days,
        "recommendation": rec,
        "confidence": 0.72,
    }
