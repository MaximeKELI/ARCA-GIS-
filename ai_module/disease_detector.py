"""Diagnostic maladies des cultures par analyse d'image (simulation ML)."""

import hashlib
import random

DISEASES = {
    "maize": [
        {"id": "maize_rust", "name": "Rouille du maïs", "severity": "high"},
        {"id": "maize_blight", "name": "Brûlure des feuilles", "severity": "medium"},
        {"id": "healthy", "name": "Plante saine", "severity": "none"},
    ],
    "rice": [
        {"id": "rice_blast", "name": "Pyriculariose", "severity": "high"},
        {"id": "rice_brown_spot", "name": "Helminthosporiose", "severity": "medium"},
        {"id": "healthy", "name": "Plante saine", "severity": "none"},
    ],
    "cassava": [
        {"id": "cassava_mosaic", "name": "Mosaïque du manioc", "severity": "critical"},
        {"id": "cassava_brown_streak", "name": "Stries brunes", "severity": "high"},
        {"id": "healthy", "name": "Plante saine", "severity": "none"},
    ],
}

TREATMENTS = {
    "maize_rust": "Appliquer fongicide à base de triazole. Éviter l'irrigation par aspersion.",
    "maize_blight": "Rotation culturale et semences certifiées.",
    "rice_blast": "Traitement au tricyclazole. Réduire l'azote.",
    "rice_brown_spot": "Fongicide cuivrique préventif.",
    "cassava_mosaic": "Utiliser boutures saines certifiées. Éliminer plants infectés.",
    "cassava_brown_streak": "Arracher et brûler les plants infectés.",
    "healthy": "Continuer la surveillance. Pas de traitement nécessaire.",
}


def detect_from_image(image_b64: str | None, crop_type: str = "maize") -> dict:
    seed = int(hashlib.md5((image_b64 or "default").encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    diseases = DISEASES.get(crop_type, DISEASES["maize"])
    weights = [0.3, 0.25, 0.45] if len(diseases) == 3 else [1.0]
    diagnosis = rng.choices(diseases, weights=weights[: len(diseases)])[0]
    confidence = round(rng.uniform(0.72, 0.96), 2)

    return {
        "crop_type": crop_type,
        "diagnosis": diagnosis,
        "confidence": confidence,
        "treatment": TREATMENTS.get(diagnosis["id"], "Consulter un agronome"),
        "prevention": "Inspection hebdomadaire, rotation des cultures, semences certifiées.",
        "source": "arca_gis_disease_model_v1",
    }


def detect_from_pest_count(pest_count: int, crop_type: str = "maize") -> dict:
    if pest_count < 20:
        risk, rec = "low", "Surveillance normale"
    elif pest_count < 50:
        risk, rec = "medium", "Pièges supplémentaires, traitement bio recommandé"
    else:
        risk, rec = "high", "Traitement insecticide ciblé sous 48h"
    return {"pest_count": pest_count, "risk": risk, "recommendation": rec, "crop_type": crop_type}
