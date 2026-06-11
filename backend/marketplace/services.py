from datetime import datetime

from .models import MarketPrice

# Prix de référence marchés ouest-africains (FCFA/kg)
REFERENCE_PRICES = {
    "maize": {"name": "Maïs", "base": 180, "markets": ["Bouaké", "Abidjan", "Korhogo"]},
    "rice": {"name": "Riz", "base": 450, "markets": ["Abidjan", "Bouaké"]},
    "cocoa": {"name": "Cacao", "base": 1200, "markets": ["San Pedro", "Abidjan"]},
    "coffee": {"name": "Café", "base": 900, "markets": ["Abidjan", "Man"]},
    "cassava": {"name": "Manioc", "base": 120, "markets": ["Bouaké", "Yamoussoukro"]},
    "groundnut": {"name": "Arachide", "base": 350, "markets": ["Korhogo", "Bouaké"]},
    "cotton": {"name": "Coton", "base": 280, "markets": ["Korhogo", "Odienné"]},
}


def seed_market_prices(country: str = "Côte d'Ivoire"):
    for crop, info in REFERENCE_PRICES.items():
        for i, market in enumerate(info["markets"]):
            variation = (hash(f"{crop}{market}") % 40) - 20
            price = info["base"] + variation
            trend = "up" if variation > 5 else "down" if variation < -5 else "stable"
            MarketPrice.objects.get_or_create(
                crop_type=crop,
                market_name=market,
                country=country,
                recorded_at=datetime.now(),
                defaults={
                    "crop_name": info["name"],
                    "price_per_kg": price,
                    "trend": trend,
                    "source": "ARCA-GIS Market Index",
                },
            )


def get_latest_prices(country: str = None, crop_type: str = None):
    qs = MarketPrice.objects.all()
    if country:
        qs = qs.filter(country=country)
    if crop_type:
        qs = qs.filter(crop_type=crop_type)
    return qs[:50]
