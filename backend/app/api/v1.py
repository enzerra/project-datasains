from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.config import settings
from app.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    AnalysisStatusResponse,
    HistoryItem,
    HistoryResponse,
    UploadResponse,
)
from app.services.pipeline import run_analysis_job
from app.services.store import store

router = APIRouter(prefix="/api/v1", tags=["analysis"])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
MAX_UPLOAD_BYTES = int(float(settings.MAX_VIDEO_SIZE_MB or "100")) * 1024 * 1024
UPLOAD_DIR = Path(settings.UPLOAD_DIR or "./tmp/uploads")


def _ensure_upload_dir() -> Path:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return UPLOAD_DIR


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    content_type = (file.content_type or "").lower()
    if not content_type.startswith("image/") and content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="File harus berupa gambar (JPEG/PNG/WEBP)")

    content = await file.read()
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail="Ukuran file melebihi batas maksimum")

    upload_dir = _ensure_upload_dir()
    extension = Path(file.filename or "upload.jpg").suffix or ".jpg"
    stored_name = f"{uuid.uuid4().hex}{extension}"
    filepath = upload_dir / stored_name
    filepath.write_bytes(content)

    record = store.create_upload(
        filename=file.filename or stored_name,
        size_bytes=len(content),
        content_type=file.content_type or "image/jpeg",
        filepath=str(filepath),
    )

    return UploadResponse(
        upload_id=record.upload_id,
        filename=record.filename,
        size_bytes=record.size_bytes,
        duration_seconds=0,
        status="uploaded",
        created_at=record.created_at,
    )


@router.post("/analyze", response_model=AnalyzeResponse)
async def start_analysis(body: AnalyzeRequest, background_tasks: BackgroundTasks) -> AnalyzeResponse:
    upload = store.get_upload(body.upload_id)
    if not upload:
        raise HTTPException(status_code=404, detail="Upload tidak ditemukan")

    if not Path(upload.filepath).exists():
        raise HTTPException(status_code=404, detail="File upload tidak ditemukan di server")

    analysis = store.create_analysis(upload.upload_id)
    background_tasks.add_task(run_analysis_job, analysis.analysis_id, upload.filepath)

    return AnalyzeResponse(
        analysis_id=analysis.analysis_id,
        upload_id=upload.upload_id,
        status="processing",
        estimated_seconds=15,
    )


@router.get("/status/{analysis_id}", response_model=AnalysisStatusResponse)
async def get_status(analysis_id: str) -> AnalysisStatusResponse:
    analysis = store.get_analysis(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analisis tidak ditemukan")

    return AnalysisStatusResponse(
        analysis_id=analysis.analysis_id,
        upload_id=analysis.upload_id,
        status=analysis.status,
        estimated_seconds=15 if analysis.status == "processing" else None,
        progress=analysis.progress,
        result=analysis.result,
        annotated_image_url=analysis.annotated_image_url,
    )


@router.get("/result/{analysis_id}/annotated-image")
async def get_annotated_image(analysis_id: str):
    analysis = store.get_analysis(analysis_id)
    if not analysis or not analysis.annotated_image_url:
        raise HTTPException(status_code=404, detail="Gambar beranotasi tidak tersedia")

    relative = analysis.annotated_image_url.lstrip("/")
    filepath = Path(relative)
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File gambar tidak ditemukan")

    return FileResponse(filepath, media_type="image/jpeg")


@router.get("/history", response_model=HistoryResponse)
async def get_history() -> HistoryResponse:
    items: list[HistoryItem] = []
    for record in store.list_history():
        result = record.result or {}
        items.append(
            HistoryItem(
                analysis_id=record.analysis_id,
                upload_id=record.upload_id,
                status=record.status,
                congestion_level=result.get("congestion_level"),
                total_vehicles_detected=result.get("total_vehicles_detected"),
                analyzed_at=result.get("processed_at"),
            )
        )
    return HistoryResponse(items=items)
