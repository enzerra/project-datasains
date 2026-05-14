from fastapi import APIRouter

from app.api.v1.analysis import router as analysis_router
from app.api.v1.history import router as history_router
from app.api.v1.upload import router as upload_router

api_router = APIRouter()
api_router.include_router(upload_router, tags=["upload"])
api_router.include_router(analysis_router, tags=["analysis"])
api_router.include_router(history_router, tags=["history"])
