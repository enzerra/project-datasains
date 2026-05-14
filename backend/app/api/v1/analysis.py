from datetime import datetime
from uuid import uuid4
import logging
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import FileResponse

from app.models.request import AnalyzeRequest
from app.models.response import AnalysisStatusResponse
from app.services.roboflow_service import RoboflowService
from app.services.upload_registry import get_upload
from app.services.video_service import VideoService
from app.services.annotation_service import generate_annotated_video

logger = logging.getLogger(__name__)

router = APIRouter()
_analysis_store: dict[str, dict] = {}
video_service = VideoService()
roboflow_service = RoboflowService()


@router.post("/analyze", response_model=AnalysisStatusResponse, status_code=status.HTTP_202_ACCEPTED)
async def analyze_video(payload: AnalyzeRequest, background_tasks: BackgroundTasks) -> AnalysisStatusResponse:
    logger.info("Analyze requested for upload_id=%s", payload.upload_id)
    analysis_id = str(uuid4())
    response = AnalysisStatusResponse(
        analysis_id=analysis_id,
        upload_id=payload.upload_id,
        status="processing",
        estimated_seconds=25,
        progress={"current_step": "queued", "steps_completed": 0, "steps_total": 4, "message": "Queued for frame extraction..."},
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
        
        logger.info(f"Upload found: {upload.stored_path}")
        response.progress = {"current_step": "extracting_frames", "steps_completed": 1, "steps_total": 4, "message": "Extracting video frames..."}

        logger.info("Starting frame extraction...")
        frame_paths = await video_service.extract_frames(upload.stored_path, fps=1, max_frames=30)
        logger.info(f"Extracted {len(frame_paths)} frames")
        
        response.progress = {"current_step": "running_model", "steps_completed": 2, "steps_total": 4, "message": "Sending frames to Roboflow..."}

        logger.info("Starting Roboflow analysis...")
        result = await roboflow_service.analyze_frames(
            frame_paths,
            progress_callback=_make_progress_callback(response),
        )
        logger.info(f"Analysis complete: {result.total_vehicles_detected} vehicles detected")
        
        response.progress = {"current_step": "compiling_results", "steps_completed": 3, "steps_total": 4, "message": "Compiling final results..."}
        response.result = result

        # generate annotated video as a background step (synchronous here inside background task)
        try:
            response.progress = {"current_step": "rendering_video", "steps_completed": 3, "steps_total": 4, "message": "Rendering annotated video..."}
            annotated_dir = Path("tmp") / "annotated_videos"
            annotated_dir.mkdir(parents=True, exist_ok=True)
            annotated_path = annotated_dir / f"{analysis_id}.mp4"

            # Get raw frame results from roboflow service
            raw_frame_results = getattr(roboflow_service, "_last_frame_results", None)
            
            if raw_frame_results is None:
                # best-effort: create empty detections so output video still renders frames
                raw_frame_results = [{"detections": []} for _ in frame_paths]
            else:
                # Convert FrameDetectionResult objects to dicts with "detections" key
                frame_results_dicts = []
                for fr in raw_frame_results:
                    frame_results_dicts.append({
                        "detections": fr.detections if hasattr(fr, "detections") else []
                    })
                raw_frame_results = frame_results_dicts

            logger.info(f"Starting video annotation with {len(frame_paths)} frames and {len(raw_frame_results)} detection results")
            annotated = generate_annotated_video(frame_paths, raw_frame_results, annotated_path, fps=1)
            response.annotated_video_url = f"/api/v1/result/{analysis_id}/annotated"
            logger.info(f"Annotated video generated successfully: {annotated_path}")
        except Exception as ve:
            logger.exception(f"Annotated video generation failed: {ve}")

        response.progress = {"current_step": "completed", "steps_completed": 4, "steps_total": 4, "message": "Analysis complete"}
        response.status = "completed"
        response.estimated_seconds = None
    except Exception as exc:
        logger.error(f"Analysis failed: {exc}", exc_info=True)
        response.status = "failed"
        response.progress = {"current_step": "failed", "steps_completed": 0, "steps_total": 4, "message": str(exc)}
    finally:
        try:
            if "frame_paths" in locals():
                logger.info("Cleaning up frame files...")
                await video_service.cleanup_frames(frame_paths)
        except Exception as e:
            logger.error(f"Cleanup failed: {e}", exc_info=True)


@router.get("/result/{analysis_id}/annotated")
async def get_annotated_video(analysis_id: str):
    record = _analysis_store.get(analysis_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    response = record.get("response")
    if not response or not getattr(response, "annotated_video_url", None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Annotated video not ready")

    annotated_path = Path("tmp") / "annotated_videos" / f"{analysis_id}.mp4"
    if not annotated_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Annotated video file missing")

    return FileResponse(path=str(annotated_path), media_type="video/mp4", filename=f"annotated_{analysis_id}.mp4")


def _make_progress_callback(response: AnalysisStatusResponse):
    async def progress_callback(index: int, total: int, frame_path):
        response.progress = {
            "current_step": "running_model",
            "steps_completed": 2,
            "steps_total": 4,
            "message": f"Analyzing frame {index + 1} of {total}: {frame_path.name}",
        }

    return progress_callback
