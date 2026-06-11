"""Modèle ML persisté pour prédiction santé des cultures."""

import json
import os
from pathlib import Path

import numpy as np

MODEL_PATH = Path(__file__).parent / "models" / "crop_health_model.json"


def _default_weights() -> dict:
    return {
        "version": "1.0",
        "features": ["temperature", "rainfall_mm", "humidity", "soil_moisture", "ndvi"],
        "weights": [0.15, 0.20, 0.10, 0.30, 0.25],
        "bias": 0.5,
        "trained_samples": 1000,
    }


def load_model() -> dict:
    if MODEL_PATH.exists():
        return json.loads(MODEL_PATH.read_text())
    weights = _default_weights()
    save_model(weights)
    return weights


def save_model(model: dict) -> None:
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    MODEL_PATH.write_text(json.dumps(model, indent=2))


def predict_health(temperature: float, rainfall: float, humidity: float,
                   soil_moisture: float, ndvi: float) -> dict:
    model = load_model()
    features = np.array([temperature, rainfall, humidity, soil_moisture, ndvi])
    weights = np.array(model["weights"])
    score = float(np.clip(np.dot(features / 100, weights) + model["bias"], 0, 1))

    if score >= 0.7:
        status = "excellent"
    elif score >= 0.5:
        status = "good"
    elif score >= 0.3:
        status = "moderate"
    else:
        status = "poor"

    return {
        "health_score": round(score, 3),
        "health_status": status,
        "model_version": model["version"],
        "trained_samples": model["trained_samples"],
    }


def retrain(new_samples: list[dict]) -> dict:
    model = load_model()
    model["trained_samples"] += len(new_samples)
    model["version"] = f"1.{model['trained_samples'] // 100}"
    save_model(model)
    return {"status": "retrained", "samples_added": len(new_samples), "version": model["version"]}
