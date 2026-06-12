from datetime import datetime, timedelta


def plan_autonomous(lat: float, lng: float, crop_type: str, soil_moisture: float) -> dict:
    actions = []
    if soil_moisture < 40:
        actions.append({"action": "irrigate", "when": "demain 06:00", "amount_mm": 25, "priority": "high"})
    actions.append({"action": "inspect_pests", "when": (datetime.utcnow() + timedelta(days=3)).strftime("%Y-%m-%d"), "priority": "medium"})
    actions.append({"action": "check_market_price", "when": (datetime.utcnow() + timedelta(days=14)).strftime("%Y-%m-%d"), "priority": "low"})
    return {
        "location": {"lat": lat, "lng": lng}, "crop_type": crop_type,
        "planned_actions": actions, "agent": "arca-autonomous-v1",
    }
