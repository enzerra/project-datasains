import logging
import time

from fastapi import FastAPI, Request

from app.api.v1.router import api_router
from app.config import settings
from app.middleware.cors import configure_cors
from app.middleware.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title=settings.app_name, version="1.0.0")
    configure_cors(app)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger = logging.getLogger("app.request")
        start_time = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "%s %s -> %s (%.2fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response

    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
