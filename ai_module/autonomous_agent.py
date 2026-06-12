from datetime import datetime, timedelta


def plan_autonomous(lat: float, lng: float, crop_type: str, soil_moisture: float) -> dict:
    actions = []
    if soil_moisture < 40:
        actions.append({"action": "irrigate", "when": "demain 06:00", "amount_mm": 25, "priority": "high", "label": "Irriguer (humidité basse)"})
    elif soil_moisture < 55:
        actions.append({"action": "monitor_moisture", "when": "aujourd'hui", "priority": "medium", "label": "Surveiller humidité sol"})
    actions.append({"action": "inspect_pests", "when": (datetime.utcnow() + timedelta(days=3)).strftime("%Y-%m-%d"), "priority": "medium", "label": "Inspection ravageurs"})
    actions.append({"action": "field_journal", "when": datetime.utcnow().strftime("%Y-%m-%d"), "priority": "low", "label": "Noter observations journal"})
    actions.append({"action": "check_market_price", "when": (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d"), "priority": "low", "label": "Vérifier prix marché"})
    return {
        "location": {"lat": lat, "lng": lng}, "crop_type": crop_type,
        "planned_actions": actions, "agent": "arca-autonomous-v1",
    }
