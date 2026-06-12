def detect_land_use_change(lat: float, lng: float, ndvi_history: list[float] | None = None) -> dict:
    history = ndvi_history or [0.6, 0.55, 0.4, 0.25]
    decline = history[0] - history[-1] if len(history) >= 2 else 0
    alert = decline > 0.2
    return {
        "lat": lat, "lng": lng, "ndvi_history": history,
        "change_detected": alert,
        "change_type": "deforestation" if alert else "stable",
        "severity": "high" if decline > 0.3 else "low" if not alert else "medium",
        "recommendation": "Inspection terrain urgente" if alert else "Surveillance continue",
    }
