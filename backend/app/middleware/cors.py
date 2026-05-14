from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


def configure_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in settings.allowed_origins.split(",") if origin.strip()],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
