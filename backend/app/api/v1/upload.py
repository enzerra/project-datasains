from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.config import settings
from app.models.response import UploadResponse
from app.services.storage_service import StorageService
from app.services.upload_registry import UploadRecord, register_upload
from app.utils.file_handler import save_upload_file, validate_extension

router = APIRouter()
storage_service = StorageService()


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_video(file: UploadFile = File(...), label: str | None = Form(default=None), recorded_at: datetime | None = Form(default=None)) -> UploadResponse:
    upload_id = str(uuid4())
    try:
        validate_extension(file.filename or "")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    destination = storage_service.build_upload_path(upload_id, file.filename or "upload.mp4")
    size_bytes = await save_upload_file(file, destination)
    max_size = settings.max_video_size_mb * 1024 * 1024
    if size_bytes > max_size:
        destination.unlink(missing_ok=True)
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")

    register_upload(
        UploadRecord(
            upload_id=upload_id,
            original_filename=file.filename or "upload.mp4",
            stored_filename=destination.name,
            stored_path=destination,
            size_bytes=size_bytes,
            created_at=datetime.utcnow(),
            label=label,
            recorded_at=recorded_at,
        )
    )
    return UploadResponse(
        upload_id=upload_id,
        filename=destination.name,
        size_bytes=size_bytes,
        duration_seconds=45.2,
        status="uploaded",
        created_at=datetime.utcnow(),
    )
