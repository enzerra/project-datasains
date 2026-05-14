from __future__ import annotations

import logging
from dataclasses import dataclass
from math import ceil
from pathlib import Path

import cv2

from app.config import settings

logger = logging.getLogger(__name__)


@dataclass
class VideoMetadata:
    duration_seconds: float
    fps: float
    frame_count: int
    width: int
    height: int


class VideoService:
    async def extract_frames(self, video_path: Path, fps: int = 1, max_frames: int = 30) -> list[Path]:
        logger.info(f"Extracting frames from: {video_path} (fps={fps}, max_frames={max_frames})")
        
        if max_frames <= 0:
            logger.warning("max_frames is 0 or negative")
            return []

        capture = cv2.VideoCapture(str(video_path))
        if not capture.isOpened():
            logger.error(f"Unable to open video file: {video_path.name}")
            raise ValueError(f"Unable to open video file: {video_path.name}")

        output_dir = video_path.parent / f"{video_path.stem}_frames"
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Frame output directory: {output_dir}")

        source_fps = capture.get(cv2.CAP_PROP_FPS) or 0.0
        sample_rate = max(1, fps)
        frame_step = 1 if source_fps <= 0 else max(1, int(round(source_fps / sample_rate)))
        total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        
        logger.info(f"Video info: fps={source_fps}, total_frames={total_frames}, frame_step={frame_step}")

        frame_paths: list[Path] = []
        frame_index = 0
        saved_index = 0

        try:
            while saved_index < max_frames:
                capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                success, frame = capture.read()
                if not success:
                    logger.debug(f"Failed to read frame at index {frame_index}")
                    break

                frame_path = output_dir / f"frame_{saved_index:04d}.jpg"
                resized_frame = _resize_frame(frame)
                cv2.imwrite(str(frame_path), resized_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
                frame_paths.append(frame_path)
                saved_index += 1
                logger.debug(f"Saved frame {saved_index}: {frame_path}")

                if total_frames and frame_index >= total_frames - 1:
                    break
                frame_index += frame_step
        finally:
            capture.release()

        logger.info(f"Extracted {len(frame_paths)} frames total")
        return frame_paths

    def get_video_metadata(self, video_path: Path) -> VideoMetadata:
        _ = video_path
        return VideoMetadata(duration_seconds=0.0, fps=0.0, frame_count=0, width=0, height=0)

    async def cleanup_frames(self, frame_paths: list[Path]) -> None:
        for frame_path in frame_paths:
            if frame_path.exists():
                frame_path.unlink()

        if frame_paths:
            frame_dir = frame_paths[0].parent
            try:
                frame_dir.rmdir()
            except OSError:
                pass


def _resize_frame(frame, max_width: int = 1280):
    height, width = frame.shape[:2]
    if width <= max_width:
        return frame

    scale = max_width / float(width)
    new_height = ceil(height * scale)
    return cv2.resize(frame, (max_width, new_height), interpolation=cv2.INTER_AREA)
