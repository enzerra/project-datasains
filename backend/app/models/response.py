from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class CongestionLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class VehicleBreakdown(BaseModel):
    car: int = 0
    motorcycle: int = 0
    truck: int = 0
    bus: int = 0
    pedestrian: int = 0


class FrameTimeline(BaseModel):
    frame_index: int
    timestamp_seconds: float
    vehicle_count: int
    congestion_score: float = Field(ge=0.0, le=1.0)


class AnalysisResult(BaseModel):
    congestion_level: CongestionLevel
    congestion_score: float = Field(ge=0.0, le=1.0)
    total_vehicles_detected: int
    vehicle_breakdown: VehicleBreakdown
    average_speed_kmh: float | None = None
    frames_analyzed: int
    timeline: list[FrameTimeline]
    summary: str
    processed_at: datetime
    processing_duration_ms: int


class UploadResponse(BaseModel):
    upload_id: str
    filename: str
    size_bytes: int
    duration_seconds: float
    status: str
    created_at: datetime


class AnalysisStatusResponse(BaseModel):
    analysis_id: str
    upload_id: str
    status: str
    estimated_seconds: int | None = None
    progress: dict | None = None
    result: AnalysisResult | None = None
    annotated_video_url: str | None = None
    annotated_image_url: str | None = None


class HistoryItem(BaseModel):
    analysis_id: str
    label: str | None = None
    congestion_level: CongestionLevel
    total_vehicles: int
    analyzed_at: datetime


class HistoryListResponse(BaseModel):
    items: list[HistoryItem]
    total: int
    limit: int
    offset: int
