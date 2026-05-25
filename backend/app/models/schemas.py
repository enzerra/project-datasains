from pydantic import BaseModel, Field
from typing import Any, Optional


class AnalyzeRequest(BaseModel):
    upload_id: str


class UploadResponse(BaseModel):
    upload_id: str
    filename: str
    size_bytes: int
    duration_seconds: float = 0
    status: str
    created_at: str


class AnalyzeResponse(BaseModel):
    analysis_id: str
    upload_id: str
    status: str
    estimated_seconds: Optional[int] = 15


class AnalysisProgress(BaseModel):
    current_step: Optional[str] = None
    steps_completed: Optional[int] = None
    steps_total: Optional[int] = None
    message: Optional[str] = None


class AnalysisStatusResponse(BaseModel):
    analysis_id: str
    upload_id: str
    status: str
    estimated_seconds: Optional[int] = None
    progress: Optional[AnalysisProgress] = None
    result: Optional[dict[str, Any]] = None
    annotated_video_url: Optional[str] = None
    annotated_image_url: Optional[str] = None


class HistoryItem(BaseModel):
    analysis_id: str
    upload_id: str
    status: str
    congestion_level: Optional[str] = None
    total_vehicles_detected: Optional[int] = None
    analyzed_at: Optional[str] = None


class HistoryResponse(BaseModel):
    items: list[HistoryItem] = Field(default_factory=list)
