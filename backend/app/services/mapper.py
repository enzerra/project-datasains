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


def _generate_recommendation(level: str) -> str:
    if level == "LOW":
        return "Lalu lintas terpantau lancar. Anda dapat melanjutkan perjalanan dengan kecepatan normal."
    elif level == "MEDIUM":
        return "Lalu lintas cukup padat. Tetap waspada dan jaga jarak aman dengan kendaraan di depan."
    elif level == "HIGH":
        return "Terjadi kemacetan. Pertimbangkan untuk mencari rute alternatif jika memungkinkan."
    elif level == "CRITICAL":
        return "Kemacetan parah! Sangat disarankan untuk mencari rute alternatif atau menunda perjalanan Anda."
    return "Lalu lintas sedang. Jaga kecepatan dan jarak aman."


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

    breakdown = {}
    for pred in predictions_list:
        if isinstance(pred, dict):
            vehicle_class = str(pred.get("class", "Vehicle")).capitalize()
            breakdown[vehicle_class] = breakdown.get(vehicle_class, 0) + 1

    if not breakdown and total_vehicles > 0:
        breakdown["Vehicle"] = total_vehicles

    return {
        "congestion_level": level,
        "congestion_score": score,
        "total_vehicles_detected": total_vehicles,
        "vehicle_breakdown": breakdown,
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
        "recommendation": _generate_recommendation(level),
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "processing_duration_ms": processing_duration_ms,
    }