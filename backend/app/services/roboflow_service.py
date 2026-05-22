from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from collections import Counter
from typing import Any

import httpx

from app.config import settings
from app.models.response import AnalysisResult, CongestionLevel, FrameTimeline, VehicleBreakdown

logger = logging.getLogger(__name__)


@dataclass
class FrameDetectionResult:
    frame_index: int
    vehicle_count: int
    detections: list[dict]


class RoboflowService:
    def __init__(self) -> None:
        self.api_url = settings.roboflow_api_url
        self.api_key = settings.roboflow_api_key
        self.model_id = f"{settings.roboflow_project_id}/{settings.roboflow_model_version}"
        self._endpoint = f"{self.api_url.rstrip('/')}/{self.model_id}"

    async def analyze_frames(self, frame_paths: list[Path], progress_callback=None) -> AnalysisResult:
        if not frame_paths:
            return self._aggregate_results([])

        semaphore = asyncio.Semaphore(5)

        async def run_frame(index: int, frame_path: Path) -> FrameDetectionResult:
            async with semaphore:
                if progress_callback:
                    await progress_callback(index, len(frame_paths), frame_path)
                return await self._send_single_frame(frame_path, index)

        frame_results = await asyncio.gather(*(run_frame(index, frame_path) for index, frame_path in enumerate(frame_paths)))
        # keep raw per-frame detections for downstream annotation
        self._last_frame_results = list(frame_results)
        return self._aggregate_results(list(frame_results))

    async def _send_single_frame(self, frame_path: Path, frame_index: int) -> FrameDetectionResult:
        try:
            result = await self._post_frame(frame_path)
            detections = _extract_detections(result)
            logger.info(f"Frame {frame_index}: {len(detections)} detections found")
            return FrameDetectionResult(frame_index=frame_index, vehicle_count=len(detections), detections=detections)
        except Exception as e:
            logger.error(f"Frame {frame_index} processing failed: {e}", exc_info=True)
            return FrameDetectionResult(frame_index=frame_index, vehicle_count=0, detections=[])

    async def _post_frame(self, frame_path: Path) -> dict[str, Any]:
        """Send image to Roboflow as multipart form data (required format)."""
        logger.debug(f"Sending frame to Roboflow: {frame_path}")
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                with open(frame_path, "rb") as f:
                    files = {"file": (frame_path.name, f, "image/jpeg")}
                    logger.debug(f"POST {self._endpoint}?api_key=***")
                    response = await client.post(
                        self._endpoint,
                        params={"api_key": self.api_key},
                        files=files,
                    )
                
                logger.debug(f"Roboflow response status: {response.status_code}")
                
                if response.status_code != 200:
                    error_msg = response.text
                    logger.error(f"Roboflow API error {response.status_code}: {error_msg}")
                    raise ValueError(
                        f"Roboflow API error {response.status_code}: {error_msg}"
                    )
                
                payload = response.json()
                logger.debug(f"Roboflow response: {payload}")

            if isinstance(payload, dict):
                return payload

            raise ValueError("Unexpected Roboflow response format")
        except Exception as e:
            logger.error(f"_post_frame failed: {e}", exc_info=True)
            raise

    def _aggregate_results(self, frame_results: list[FrameDetectionResult]) -> AnalysisResult:
        if not frame_results:
            breakdown = VehicleBreakdown()
            return AnalysisResult(
                congestion_level=CongestionLevel.LOW,
                congestion_score=0.0,
                total_vehicles_detected=0,
                vehicle_breakdown=breakdown,
                average_speed_kmh=30.0,
                frames_analyzed=0,
                timeline=[],
                summary="No frames were analyzed.",
                processed_at=datetime.utcnow(),
                processing_duration_ms=0,
            )

        total_vehicles = sum(frame.vehicle_count for frame in frame_results)
        average_vehicles = total_vehicles / len(frame_results)
        congestion_score = min(1.0, average_vehicles / 30.0)
        congestion_level = self._calculate_congestion_level(average_vehicles, max(frame.vehicle_count for frame in frame_results))
        breakdown = _build_breakdown(frame_results)
        timeline = [
            FrameTimeline(
                frame_index=frame.frame_index,
                timestamp_seconds=float(frame.frame_index),
                vehicle_count=frame.vehicle_count,
                congestion_score=min(1.0, frame.vehicle_count / 30.0),
            )
            for frame in frame_results
        ]
        return AnalysisResult(
            congestion_level=congestion_level,
            congestion_score=congestion_score,
            total_vehicles_detected=total_vehicles,
            vehicle_breakdown=breakdown,
            average_speed_kmh=max(5.0, 35.0 - average_vehicles),
            frames_analyzed=len(frame_results),
            timeline=timeline,
            summary=f"{congestion_level.value} congestion detected from {len(frame_results)} photo(s).",
            processed_at=datetime.utcnow(),
            processing_duration_ms=0,
        )

    def _calculate_congestion_level(self, avg_vehicles: float, peak_vehicles: int) -> CongestionLevel:
        score = max(avg_vehicles, float(peak_vehicles))
        if score <= 5:
            return CongestionLevel.LOW
        if score <= 15:
            return CongestionLevel.MEDIUM
        if score <= 30:
            return CongestionLevel.HIGH
        return CongestionLevel.CRITICAL


def _extract_detections(result: Any) -> list[dict]:
    if isinstance(result, dict):
        if isinstance(result.get("predictions"), list):
            return [prediction for prediction in result["predictions"] if isinstance(prediction, dict)]
        if isinstance(result.get("outputs"), list):
            outputs = result["outputs"]
            detections: list[dict] = []
            for output in outputs:
                if isinstance(output, dict) and isinstance(output.get("predictions"), list):
                    detections.extend(prediction for prediction in output["predictions"] if isinstance(prediction, dict))
            if detections:
                return detections
    return []


def _build_breakdown(frame_results: list[FrameDetectionResult]) -> VehicleBreakdown:
    counts: Counter[str] = Counter()
    for frame in frame_results:
        for detection in frame.detections:
            class_name = str(detection.get("class", "")).lower()
            counts[class_name] += 1

    return VehicleBreakdown(
        car=counts.get("car", 0),
        motorcycle=counts.get("motorcycle", 0),
        truck=counts.get("truck", 0),
        bus=counts.get("bus", 0),
        pedestrian=counts.get("pedestrian", 0),
    )
