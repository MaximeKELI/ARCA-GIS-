"""Optimisation intrants (engrais, semences) par parcelle."""

CROP_INPUTS = {
    "maize": {"seed_kg_ha": 25, "npk_kg_ha": 200, "urea_kg_ha": 50},
    "rice": {"seed_kg_ha": 40, "npk_kg_ha": 150, "urea_kg_ha": 80},
    "cassava": {"cuttings_ha": 10000, "npk_kg_ha": 100, "urea_kg_ha": 0},
}


def optimize_inputs(crop_type: str, area_ha: float, soil_quality: str = "medium") -> dict:
    base = CROP_INPUTS.get(crop_type, CROP_INPUTS["maize"])
    factor = {"poor": 1.2, "medium": 1.0, "good": 0.85}.get(soil_quality, 1.0)

    inputs = {k: round(v * area_ha * factor, 1) for k, v in base.items()}
    cost_xof = inputs.get("npk_kg_ha", 0) * 350 + inputs.get("urea_kg_ha", 0) * 300 + inputs.get("seed_kg_ha", 0) * 500

    return {
        "crop_type": crop_type,
        "area_hectares": area_ha,
        "soil_quality": soil_quality,
        "inputs": inputs,
        "estimated_cost_xof": round(cost_xof),
        "tips": ["Appliquer NPK 3 semaines après semis", "Composter les résidus de récolte"],
    }
