"""FastAPI application factory.

Phase 0 exposes only health/readiness so CI and docker-compose have a real
target. Domain routers (jobs, resumes, search, evaluations, copilot) are added
in later phases under ``backend/api/v1``.
"""

from __future__ import annotations

from fastapi import FastAPI

from backend.api.errors import register_exception_handlers
from backend.api.v1.router import api_router
from backend.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    register_exception_handlers(app)
    app.include_router(api_router)

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "healthy", "app": settings.app_name}

    @app.get("/ready", tags=["system"])
    async def ready() -> dict[str, str]:
        # A later phase will check DB/Redis connectivity here.
        return {"status": "ready"}

    return app


app = create_app()
