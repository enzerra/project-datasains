from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path

from app.services.mapper import roboflow_to_analysis_result
from app.services.roboflow import run_roboflow_workflow
from app.services.store import store


async def run_analysis_job(analysis_id: str, upload_filepath: str) -> None:
    started = time.perf_counter()

    store.update_analysis(
        analysis_id,
        progress={
            "current_step": "preparing",
            "steps_completed": 1,
            "steps_total": 3,
            "message": "Membaca foto...",
        },
    )

    try:
        image_bytes = Path(upload_filepath).read_bytes()

        store.update_analysis(
            analysis_id,
            progress={
                "current_step": "inference",
                "steps_completed": 2,
                "steps_total": 3,
                "message": "Menjalankan model Roboflow...",
            },
        )

        workflow_result = await run_roboflow_workflow(image_bytes)
        duration_ms = int((time.perf_counter() - started) * 1000)
        result = roboflow_to_analysis_result(workflow_result, processing_duration_ms=duration_ms)

        store.update_analysis(
            analysis_id,
            status="completed",
            result=result,
            annotated_image_url=workflow_result.get("annotated_image_url"),
            progress={
                "current_step": "completed",
                "steps_completed": 3,
                "steps_total": 3,
                "message": "Analisis selesai.",
            },
            completed_at=datetime.now(timezone.utc),
        )
    except Exception as exc:
        store.update_analysis(
            analysis_id,
            status="failed",
            error=str(exc),
            progress={
                "current_step": "failed",
                "steps_completed": 3,
                "steps_total": 3,
                "message": str(exc),
            },
        )
