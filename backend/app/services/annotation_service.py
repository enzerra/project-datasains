from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

import cv2

logger = logging.getLogger(__name__)


def _parse_bbox(det: dict, img_w: int, img_h: int):
    # Try multiple Roboflow/bounding-box formats and return (x1,y1,x2,y2) ints
    try:
        # center format: x, y, width, height
        if all(k in det for k in ("x", "y", "width", "height")):
            cx = float(det.get("x", 0))
            cy = float(det.get("y", 0))
            w = float(det.get("width", 0))
            h = float(det.get("height", 0))
            x1 = int(max(0, cx - w / 2))
            y1 = int(max(0, cy - h / 2))
            x2 = int(min(img_w - 1, cx + w / 2))
            y2 = int(min(img_h - 1, cy + h / 2))
            return x1, y1, x2, y2

        # xmin/xmax ymin/ymax variants
        for a, b, c, d in (("xmin", "ymin", "xmax", "ymax"), ("x_min", "y_min", "x_max", "y_max")):
            if all(k in det for k in (a, b, c, d)):
                x1 = int(max(0, float(det.get(a))))
                y1 = int(max(0, float(det.get(b))))
                x2 = int(min(img_w - 1, float(det.get(c))))
                y2 = int(min(img_h - 1, float(det.get(d))))
                return x1, y1, x2, y2

        # bbox dict with keys
        if "bbox" in det and isinstance(det["bbox"], dict):
            b = det["bbox"]
            if all(k in b for k in ("x", "y", "w", "h")):
                cx = float(b.get("x"))
                cy = float(b.get("y"))
                w = float(b.get("w"))
                h = float(b.get("h"))
                x1 = int(max(0, cx - w / 2))
                y1 = int(max(0, cy - h / 2))
                x2 = int(min(img_w - 1, cx + w / 2))
                y2 = int(min(img_h - 1, cy + h / 2))
                return x1, y1, x2, y2
    except Exception:
        logger.debug("Failed to parse bbox from detection: %s", det)

    return None


def _label_for(det: dict) -> str:
    cls = det.get("class") or det.get("label") or det.get("name") or "obj"
    conf = det.get("confidence") or det.get("score") or det.get("confidence_score")
    if conf is not None:
        try:
            conf_val = float(conf)
            return f"{cls}:{conf_val:.2f}"
        except Exception:
            pass
    return str(cls)


def generate_annotated_video(frame_paths: Iterable[Path], frame_results: list[dict], output_path: Path, fps: int = 1) -> Path:
    """Render bounding boxes onto frames and write an MP4 video.

    frame_results is expected to be a sequence where each entry corresponds to a frame
    and contains a 'detections' key with list[dict]. This function is resilient to
    common bbox formats returned by Roboflow.
    """
    frame_paths = list(frame_paths)
    if not frame_paths:
        raise ValueError("No frames to annotate")

    first = cv2.imread(str(frame_paths[0]))
    if first is None:
        raise ValueError("Unable to read first frame for sizing")

    h, w = first.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(output_path), fourcc, float(fps), (w, h))

    colors = {}

    try:
        for idx, frame_path in enumerate(frame_paths):
            img = cv2.imread(str(frame_path))
            if img is None:
                logger.warning("Skipping unreadable frame %s", frame_path)
                continue

            detections = []
            if idx < len(frame_results) and isinstance(frame_results[idx], dict):
                detections = frame_results[idx].get("detections") or []

            for det in detections:
                bbox = _parse_bbox(det, w, h)
                if not bbox:
                    continue
                x1, y1, x2, y2 = bbox
                cls = str(det.get("class") or det.get("label") or "obj").lower()
                if cls not in colors:
                    # simple deterministic color
                    colors[cls] = tuple(int(x) for x in (hash(cls) & 0xFF, (hash(cls) >> 8) & 0xFF, (hash(cls) >> 16) & 0xFF))
                color = colors[cls]
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                label = _label_for(det)
                cv2.putText(img, label, (x1 + 2, max(y1 + 12, y1 + 14)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)

            writer.write(img)

    finally:
        writer.release()

    logger.info("Annotated video written: %s", output_path)
    return output_path
