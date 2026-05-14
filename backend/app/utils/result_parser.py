from datetime import datetime

from app.models.response import AnalysisResult, CongestionLevel, FrameTimeline, VehicleBreakdown


def build_fallback_result(frame_count: int) -> AnalysisResult:
    breakdown = VehicleBreakdown(car=frame_count * 4, motorcycle=frame_count * 2, truck=frame_count, bus=0, pedestrian=frame_count // 2)
    congestion_score = min(1.0, frame_count / 30.0)
    level = _level_from_score(congestion_score)
    return AnalysisResult(
        congestion_level=level,
        congestion_score=congestion_score,
        total_vehicles_detected=sum(breakdown.model_dump().values()),
        vehicle_breakdown=breakdown,
        average_speed_kmh=max(5.0, 30.0 - congestion_score * 18.0),
        frames_analyzed=frame_count,
        timeline=[FrameTimeline(frame_index=index, timestamp_seconds=float(index), vehicle_count=min(25, 5 + index), congestion_score=min(1.0, 0.2 + index * 0.03)) for index in range(frame_count)],
        summary="Synthetic congestion result generated because no Roboflow payload was provided.",
        processed_at=datetime.utcnow(),
        processing_duration_ms=0,
    )


def _level_from_score(score: float) -> CongestionLevel:
    if score < 0.25:
        return CongestionLevel.LOW
    if score < 0.5:
        return CongestionLevel.MEDIUM
    if score < 0.75:
        return CongestionLevel.HIGH
    return CongestionLevel.CRITICAL
