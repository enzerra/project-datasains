from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import threading
import uuid


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


@dataclass
class UploadRecord:
    upload_id: str
    filename: str
    size_bytes: int
    content_type: str
    filepath: str
    created_at: str


@dataclass
class AnalysisRecord:
    analysis_id: str
    upload_id: str
    status: str
    progress: dict[str, Any] = field(default_factory=dict)
    result: dict[str, Any] | None = None
    annotated_image_url: str | None = None
    error: str | None = None
    started_at: datetime = field(default_factory=_utc_now)
    completed_at: datetime | None = None


class AnalysisStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._uploads: dict[str, UploadRecord] = {}
        self._analyses: dict[str, AnalysisRecord] = {}

    def create_upload(
        self,
        *,
        filename: str,
        size_bytes: int,
        content_type: str,
        filepath: str,
    ) -> UploadRecord:
        upload_id = str(uuid.uuid4())
        record = UploadRecord(
            upload_id=upload_id,
            filename=filename,
            size_bytes=size_bytes,
            content_type=content_type,
            filepath=filepath,
            created_at=_iso(_utc_now()),
        )
        with self._lock:
            self._uploads[upload_id] = record
        return record

    def get_upload(self, upload_id: str) -> UploadRecord | None:
        with self._lock:
            return self._uploads.get(upload_id)

    def create_analysis(self, upload_id: str) -> AnalysisRecord:
        analysis_id = str(uuid.uuid4())
        record = AnalysisRecord(
            analysis_id=analysis_id,
            upload_id=upload_id,
            status="processing",
            progress={
                "current_step": "queued",
                "steps_completed": 0,
                "steps_total": 3,
                "message": "Menyiapkan antrean analisis...",
            },
        )
        with self._lock:
            self._analyses[analysis_id] = record
        return record

    def get_analysis(self, analysis_id: str) -> AnalysisRecord | None:
        with self._lock:
            return self._analyses.get(analysis_id)

    def update_analysis(self, analysis_id: str, **changes: Any) -> AnalysisRecord | None:
        with self._lock:
            record = self._analyses.get(analysis_id)
            if not record:
                return None
            for key, value in changes.items():
                setattr(record, key, value)
            return record

    def list_history(self, limit: int = 20) -> list[AnalysisRecord]:
        with self._lock:
            records = list(self._analyses.values())
        records.sort(key=lambda item: item.started_at, reverse=True)
        return records[:limit]


store = AnalysisStore()
