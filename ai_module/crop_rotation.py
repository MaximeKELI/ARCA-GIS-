def plan_rotation(parcel_id: int, current_crop: str, soil_quality: str = "medium") -> dict:
    rotations = {
        "maize": [
            {"year": 1, "crop": "maize", "reason": "Culture principale"},
            {"year": 2, "crop": "cowpea", "reason": "Fixation azote"},
            {"year": 3, "crop": "cassava", "reason": "Repos du sol"},
        ],
        "rice": [
            {"year": 1, "crop": "rice", "reason": "Riz pluvial"},
            {"year": 2, "crop": "maize", "reason": "Drainage sol"},
            {"year": 3, "crop": "rice", "reason": "Retour riziculture"},
        ],
    }
    plan = rotations.get(current_crop, rotations["maize"])
    return {"parcel_id": parcel_id, "current_crop": current_crop, "soil_quality": soil_quality, "plan_years": plan}
