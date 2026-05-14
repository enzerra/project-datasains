from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class UploadRecord:
    upload_id: str
    original_filename: str
    stored_filename: str
    stored_path: Path
    size_bytes: int
    created_at: datetime
    label: str | None = None
    recorded_at: datetime | None = None


UPLOAD_REGISTRY: dict[str, UploadRecord] = {}


def register_upload(record: UploadRecord) -> None:
    UPLOAD_REGISTRY[record.upload_id] = record


def get_upload(upload_id: str) -> UploadRecord:
    try:
        return UPLOAD_REGISTRY[upload_id]
    except KeyError as exc:
        raise KeyError(f"Upload not found: {upload_id}") from exc
