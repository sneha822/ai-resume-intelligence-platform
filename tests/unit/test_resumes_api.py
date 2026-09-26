"""Async resume upload endpoint tests (Celery mocked, no broker)."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

import backend.api.v1.resumes as resumes_module


class _FakeAsyncResult:
    id = "task-123"


async def test_upload_returns_202_with_task_id(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict[str, str] = {}

    def fake_delay(filename: str, content_b64: str) -> _FakeAsyncResult:
        captured["filename"] = filename
        captured["content_b64"] = content_b64
        return _FakeAsyncResult()

    monkeypatch.setattr(resumes_module.ingest_resume, "delay", fake_delay)

    resp = await client.post(
        "/api/v1/resumes",
        files={"file": ("jane.pdf", b"%PDF-1.4 fake", "application/pdf")},
    )

    assert resp.status_code == 202
    body = resp.json()
    assert body["task_id"] == "task-123"
    assert body["status"] == "queued"
    assert captured["filename"] == "jane.pdf"
    # bytes must be base64-encoded for the JSON serializer
    assert captured["content_b64"]
