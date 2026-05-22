from datetime import datetime
from uuid import uuid4
import logging
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import FileResponse

from app.models.request import AnalyzeRequest
from app.models.response import AnalysisStatusResponse
from app.services.annotation_service import generate_annotated_image
from app.services.roboflow_service import RoboflowService
from app.services.upload_registry import get_upload

logger = logging.getLogger(__name__)

router = APIRouter()
_analysis_store: dict[str, dict] = {}
roboflow_service = RoboflowService()


@router.post("/analyze", response_model=AnalysisStatusResponse, status_code=status.HTTP_202_ACCEPTED)
async def analyze_video(payload: AnalyzeRequest, background_tasks: BackgroundTasks) -> AnalysisStatusResponse:
    logger.info("Analyze requested for upload_id=%s", payload.upload_id)
    analysis_id = str(uuid4())
    response = AnalysisStatusResponse(
        analysis_id=analysis_id,
        upload_id=payload.upload_id,
        status="processing",
        estimated_seconds=15,
        progress={"current_step": "queued", "steps_completed": 0, "steps_total": 3, "message": "Queued for photo analysis..."},
    )
    _analysis_store[analysis_id] = {"response": response, "created_at": datetime.utcnow()}
    background_tasks.add_task(_process_analysis, analysis_id)
    return response


@router.get("/status/{analysis_id}", response_model=AnalysisStatusResponse)
async def get_status(analysis_id: str) -> AnalysisStatusResponse:
    if analysis_id not in _analysis_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    return _analysis_store[analysis_id]["response"]


async def _process_analysis(analysis_id: str) -> None:
    logger.info(f"Starting analysis: {analysis_id}")
    
    record = _analysis_store.get(analysis_id)
    if not record:
        logger.error(f"Analysis {analysis_id} not found in store")
        return

    response: AnalysisStatusResponse = record["response"]

    try:
        logger.info(f"Fetching upload: {response.upload_id}")
        upload = get_upload(response.upload_id)
        if not upload:
            raise ValueError(f"Upload {response.upload_id} not found")
        
        logger.info(f"Photo found: {upload.stored_path}")
        response.progress = {"current_step": "running_model", "steps_completed": 1, "steps_total": 3, "message": "Sending photo to Roboflow..."}

        logger.info("Starting Roboflow photo analysis...")
        result = await roboflow_service.analyze_frames(
            [upload.stored_path],
            progress_callback=_make_progress_callback(response),
        )
        logger.info(f"Analysis complete: {result.total_vehicles_detected} vehicles detected")

        response.progress = {"current_step": "compiling_results", "steps_completed": 2, "steps_total": 3, "message": "Compiling final results..."}
        response.result = result

        try:
            annotated_dir = Path("tmp") / "annotated_images"
            annotated_path = annotated_dir / f"{analysis_id}.jpg"

            raw_frame_results = getattr(roboflow_service, "_last_frame_results", None) or []
            first_result = raw_frame_results[0] if raw_frame_results else None
            detections = first_result.detections if first_result and hasattr(first_result, "detections") else []

            generate_annotated_image(upload.stored_path, detections, annotated_path)
            response.annotated_image_url = f"/api/v1/result/{analysis_id}/annotated-image"
            logger.info(f"Annotated image generated successfully: {annotated_path}")
        except Exception as image_error:
            logger.exception(f"Annotated image generation failed: {image_error}")

        response.progress = {"current_step": "completed", "steps_completed": 3, "steps_total": 3, "message": "Photo analysis complete"}
        response.status = "completed"
        response.estimated_seconds = None
    except Exception as exc:
        logger.error(f"Analysis failed: {exc}", exc_info=True)
        response.status = "failed"
        response.progress = {"current_step": "failed", "steps_completed": 0, "steps_total": 3, "message": str(exc)}
    finally:
        try:
            if getattr(upload, "stored_path", None) and upload.stored_path.exists():
                logger.info("Cleaning up uploaded photo...")
                upload.stored_path.unlink(missing_ok=True)
        except Exception as e:
            logger.error(f"Cleanup failed: {e}", exc_info=True)


@router.get("/result/{analysis_id}/annotated-image")
async def get_annotated_image(analysis_id: str):
    record = _analysis_store.get(analysis_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    response = record.get("response")
    if not response or not getattr(response, "annotated_image_url", None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Annotated image not ready")

    annotated_path = Path("tmp") / "annotated_images" / f"{analysis_id}.jpg"
    if not annotated_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Annotated image file missing")

    return FileResponse(path=str(annotated_path), media_type="image/jpeg", filename=f"annotated_{analysis_id}.jpg")


def _make_progress_callback(response: AnalysisStatusResponse):
    async def progress_callback(index: int, total: int, frame_path):
        response.progress = {
            "current_step": "running_model",
            "steps_completed": 1,
            "steps_total": 3,
            "message": f"Analyzing photo: {frame_path.name}",
        }

    return progress_callback
