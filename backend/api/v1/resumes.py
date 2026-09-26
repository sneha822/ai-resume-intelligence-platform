"""Async resume ingestion endpoints.

Upload returns immediately with a task id; the actual parse/embed/index work
runs on a Celery worker so large batches never block the API.
"""

from __future__ import annotations

import base64

from fastapi import APIRouter, UploadFile, status
from pydantic import BaseModel

from backend.workers.celery_app import celery_app
from backend.workers.tasks import ingest_resume

router = APIRouter(prefix="/resumes", tags=["resumes"])


class TaskAccepted(BaseModel):
    task_id: str
    status: str = "queued"


class TaskStatus(BaseModel):
    task_id: str
    state: str
    result: object | None = None


@router.post("", response_model=TaskAccepted, status_code=status.HTTP_202_ACCEPTED)
async def upload_resume(file: UploadFile) -> TaskAccepted:
    raw = await file.read()
    content_b64 = base64.b64encode(raw).decode("ascii")
    task = ingest_resume.delay(file.filename or "resume.pdf", content_b64)
    return TaskAccepted(task_id=task.id)


@router.get("/tasks/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str) -> TaskStatus:
    async_result = celery_app.AsyncResult(task_id)
    result = async_result.result if async_result.successful() else None
    return TaskStatus(task_id=task_id, state=async_result.state, result=result)
