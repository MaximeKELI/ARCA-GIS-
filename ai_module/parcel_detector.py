"""Détection automatique de parcelles par analyse satellite."""

import hashlib


def detect_parcels(lat: float, lng: float, radius_km: float = 2.0) -> list[dict]:
    """Détecte des parcelles probables autour d'un point (simulation ML)."""
    seed = int(hashlib.md5(f"detect:{lat:.3f},{lng:.3f}".encode()).hexdigest()[:8], 16)
    parcels = []
    count = 2 + (seed % 4)

    for i in range(count):
        offset_lat = lat + ((seed + i * 7) % 100 - 50) / 5000
        offset_lng = lng + ((seed + i * 13) % 100 - 50) / 5000
        size = 0.002 + (seed % 5) * 0.001

        coords = [
            [offset_lng, offset_lat],
            [offset_lng + size, offset_lat],
            [offset_lng + size, offset_lat + size * 0.7],
            [offset_lng, offset_lat + size * 0.7],
            [offset_lng, offset_lat],
        ]

        crops = ["maize", "rice", "cassava", "cocoa"]
        crop = crops[(seed + i) % len(crops)]

        parcels.append({
            "id": f"auto-{i}",
            "crop_type": crop,
            "confidence": round(0.6 + (seed % 30) / 100, 2),
            "area_hectares": round(size * size * 111320 * 111320 / 10000 * 0.7, 2),
            "geometry": {"type": "Polygon", "coordinates": [coords]},
            "centroid": {"lat": offset_lat + size * 0.35, "lng": offset_lng + size * 0.5},
        })

    return parcels
