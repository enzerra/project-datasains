from __future__ import annotations
from datetime import datetime, timezone
from typing import Any


def _normalize_level(raw: str | None) -> str:
    if not raw:
        return "LOW"
    normalized = raw.strip().upper()
    aliases = {
        "RENDAH": "LOW",
        "SEDANG": "MEDIUM",
        "MENENGAH": "MEDIUM",
        "TINGGI": "HIGH",
        "KRITIS": "CRITICAL",
    }
    return aliases.get(normalized, normalized if normalized in {"LOW", "MEDIUM", "HIGH", "CRITICAL"} else "MEDIUM")


def _normalize_score(raw: Any) -> float:
    if raw is None:
        return 0.0
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return 0.0
    if value > 10.0: 
        return min(value / 100.0, 1.0)
    return max(0.0, min(value / 10.0, 1.0))


def _level_summary(level: str, total_vehicles: int, score_percent: int) -> str:
    labels = {
        "LOW": "rendah",
        "MEDIUM": "sedang",
        "HIGH": "tinggi",
        "CRITICAL": "kritis",
    }
    label = labels.get(level, "sedang")
    return (
        f"Terdeteksi {total_vehicles} kendaraan dengan tingkat kemacetan {label}. "
        f"Skor kepadatan {score_percent}%."
    )


def roboflow_to_analysis_result(
    workflow_result: dict[str, Any],
    *,
    processing_duration_ms: int,
) -> dict[str, Any]:
    total_vehicles = int(workflow_result.get("count_objects") or 0)
    proximate_pairs = int(workflow_result.get("proximate_pairs") or 0)
    level = _normalize_level(workflow_result.get("congestion_level"))
    score = _normalize_score(workflow_result.get("density_score"))
    score_percent = round(score * 100)


    motorcycle_count = 0
    truck_count = 0
    car_count = 0


    def find_predictions(data: Any) -> list[Any]:
        if isinstance(data, list):
            if len(data) > 0 and isinstance(data[0], dict) and "class" in data[0]:
                return data
        elif isinstance(data, dict):
            if "predictions" in data and isinstance(data["predictions"], list):
                return data["predictions"]
            for val in data.values():
                res = find_predictions(val)
                if res: return res
        return []

    predictions_list = find_predictions(workflow_result)

    for pred in predictions_list:
        if isinstance(pred, dict):
            vehicle_class = str(pred.get("class", "")).lower()
            
            if "motorcycle" in vehicle_class or "motor" in vehicle_class:
                motorcycle_count += 1
            elif "truck" in vehicle_class or "truk" in vehicle_class:
                truck_count += 1
            elif "car" in vehicle_class or "mobil" in vehicle_class:
                car_count += 1

    return {
        "congestion_level": level,
        "congestion_score": score,
        "total_vehicles_detected": total_vehicles,

        "vehicle_breakdown": {
            "car": car_count,
            "motorcycle": motorcycle_count,
            "truck": truck_count,
            "proximate_pairs": proximate_pairs,
        },
        "average_speed_kmh": None,
        "frames_analyzed": 1,
        "timeline": [
            {
                "frame_index": 0,
                "timestamp_seconds": 0,
                "vehicle_count": total_vehicles,
                "congestion_score": score,
            }
        ],
        "summary": _level_summary(level, total_vehicles, score_percent),
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "processing_duration_ms": processing_duration_ms,
    }