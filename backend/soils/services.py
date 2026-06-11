from django.contrib.gis.geos import Point

from .models import SoilZone

CROP_SUITABILITY = {
    "ferralsol": {"maize": "good", "cassava": "excellent", "cocoa": "good", "rice": "moderate"},
    "leptosol": {"maize": "moderate", "cassava": "good", "groundnut": "good"},
    "vertisol": {"rice": "excellent", "cotton": "excellent", "maize": "good"},
    "cambisol": {"maize": "excellent", "rice": "good", "coffee": "good"},
    "fluvisol": {"rice": "excellent", "maize": "good", "vegetables": "excellent"},
    "arenosol": {"groundnut": "good", "cassava": "moderate", "maize": "poor"},
}


def get_soil_at_location(lat: float, lng: float) -> dict | None:
    point = Point(lng, lat, srid=4326)
    zone = SoilZone.objects.filter(geometry__contains=point).first()
    if not zone:
        return None
    suitability = CROP_SUITABILITY.get(zone.soil_type, {})
    return {
        "zone": zone.name,
        "soil_type": zone.soil_type,
        "soil_type_display": zone.get_soil_type_display(),
        "ph": zone.ph,
        "organic_matter": zone.organic_matter,
        "texture": zone.texture,
        "crop_suitability": suitability,
        "source": zone.source,
    }
