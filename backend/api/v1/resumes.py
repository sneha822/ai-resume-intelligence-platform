"""Resume ingestion endpoints.

Two modes (``INGEST_MODE``):
- ``async`` (default): enqueue a Celery task, return 202 + task id (needs worker+Redis)
- ``sync``: run the parse/embed/persist pipeline inline, return 201 (no worker/Redis —
  ideal for free hosting)
"""

from __future__ import annotations

import base64

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import SessionDep
from backend.core.config import settings

router = APIRouter(prefix="/resumes", tags=["resumes"])


async def _sync_ingest(session: AsyncSession, filename: str, content: bytes) -> str:
    """Run the full ingestion pipeline inline; returns the new resume id."""
    from backend.adapters.embeddings.factory import get_embedder
    from backend.adapters.parsing.pymupdf_parser import PyMuPDFParser
    from backend.services.extraction_service import build_default_extractor
    from backend.services.ingestion_service import IngestionService

    service = IngestionService(
        session, PyMuPDFParser(), get_embedder(), extractor=build_default_extractor()
    )
    return await service.ingest(filename, content)


@router.post("")
async def upload_resume(file: UploadFile, session: SessionDep) -> JSONResponse:
    raw = await file.read()
    filename = file.filename or "resume.pdf"

    if settings.ingest_mode == "sync":
        resume_id = await _sync_ingest(session, filename, raw)
        return JSONResponse(
            status_code=201,
            content={"mode": "sync", "status": "ingested", "resume_id": resume_id},
        )

    from backend.workers.tasks import ingest_resume

    content_b64 = base64.b64encode(raw).decode("ascii")
    task = ingest_resume.delay(filename, content_b64)
    return JSONResponse(
        status_code=202,
        content={"mode": "async", "status": "queued", "task_id": task.id},
    )


@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str) -> JSONResponse:
    from backend.workers.celery_app import celery_app

    async_result = celery_app.AsyncResult(task_id)
    result = async_result.result if async_result.successful() else None
    return JSONResponse(content={"task_id": task_id, "state": async_result.state, "result": result})
