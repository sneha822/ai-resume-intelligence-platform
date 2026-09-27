"""Evaluations + copilot endpoint wiring tests (no LLM, no Postgres)."""

from __future__ import annotations

from fastapi import FastAPI
from httpx import AsyncClient

from backend.api.deps import get_copilot_service
from backend.core.schemas import CopilotResponse


async def test_evaluation_requires_llm_configured(client: AsyncClient) -> None:
    # No ANTHROPIC_API_KEY in the test env -> guard returns 503 before any DB work.
    resp = await client.post(
        "/api/v1/evaluations",
        json={
            "candidate_id": "00000000-0000-0000-0000-000000000001",
            "job_id": "00000000-0000-0000-0000-000000000002",
        },
    )
    assert resp.status_code == 503
    assert resp.headers["content-type"].startswith("application/problem+json")


class _FakeCopilot:
    async def answer(self, question: str, candidates: list[dict[str, object]]) -> str:
        return f"Considered {len(candidates)} candidate(s). Answer to: {question}"


async def test_copilot_answers_with_no_candidates(app: FastAPI, client: AsyncClient) -> None:
    app.dependency_overrides[get_copilot_service] = lambda: _FakeCopilot()

    resp = await client.post(
        "/api/v1/copilot", json={"question": "Who is strongest in NLP?", "candidate_ids": []}
    )
    assert resp.status_code == 200
    body = CopilotResponse(**resp.json())
    assert "Answer to:" in body.answer


async def test_copilot_validation_error(app: FastAPI, client: AsyncClient) -> None:
    app.dependency_overrides[get_copilot_service] = lambda: _FakeCopilot()
    resp = await client.post("/api/v1/copilot", json={"question": ""})
    assert resp.status_code == 422
