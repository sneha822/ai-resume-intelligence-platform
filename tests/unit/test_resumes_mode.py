"""Resume upload mode branching: sync (inline) vs async (Celery)."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

import backend.api.v1.resumes as resumes_module
from backend.core.config import settings


class _FakeAsyncResult:
    id = "task-xyz"


async def test_async_mode_enqueues_and_returns_202(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "ingest_mode", "async")

    def fake_delay(filename: str, content_b64: str) -> _FakeAsyncResult:
        return _FakeAsyncResult()

    # Patch the lazily-imported task's delay.
    from backend.workers import tasks

    monkeypatch.setattr(tasks.ingest_resume, "delay", fake_delay)

    resp = await client.post(
        "/api/v1/resumes", files={"file": ("r.pdf", b"%PDF-1.4", "application/pdf")}
    )
    assert resp.status_code == 202
    body = resp.json()
    assert body["mode"] == "async"
    assert body["task_id"] == "task-xyz"


async def test_sync_mode_runs_inline_and_returns_201(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "ingest_mode", "sync")

    async def fake_sync_ingest(session: object, filename: str, content: bytes) -> str:
        return "resume-123"

    monkeypatch.setattr(resumes_module, "_sync_ingest", fake_sync_ingest)

    resp = await client.post(
        "/api/v1/resumes", files={"file": ("r.pdf", b"%PDF-1.4", "application/pdf")}
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["mode"] == "sync"
    assert body["resume_id"] == "resume-123"
