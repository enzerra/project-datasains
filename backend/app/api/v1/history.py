from datetime import datetime

from fastapi import APIRouter, Query

from app.models.response import CongestionLevel, HistoryItem, HistoryListResponse

router = APIRouter()


@router.get("/history", response_model=HistoryListResponse)
async def list_history(limit: int = Query(default=20, ge=1, le=100), offset: int = Query(default=0, ge=0)) -> HistoryListResponse:
    items = [
        HistoryItem(
            analysis_id="demo-analysis",
            label="Jl. Sudirman - Karet",
            congestion_level=CongestionLevel.HIGH,
            total_vehicles=142,
            analyzed_at=datetime.utcnow(),
        )
    ]
    return HistoryListResponse(items=items, total=len(items), limit=limit, offset=offset)
