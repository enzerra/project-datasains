from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import router as v1_router
from app.config import settings

app = FastAPI(title="Traffic Congestion API")

static_dir = Path("static")
annotated_dir = static_dir / "annotated_images"
annotated_dir.mkdir(parents=True, exist_ok=True)
upload_dir = Path(settings.UPLOAD_DIR or "./tmp/uploads")
upload_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
if settings.ALLOWED_ORIGINS:
    allowed_origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Traffic Congestion API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}
