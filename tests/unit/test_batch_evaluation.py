"""Batch evaluation: concurrent orchestration + endpoint guard (no LLM/DB)."""

from __future__ import annotations

import uuid
from typing import Any, cast

import pytest
from httpx import AsyncClient

from backend.core.schemas.evaluation import (
    EvaluationResult,
    FitLevel,
    GapAnalysis,
)
from backend.db.models import Candidate
from backend.services.batch_evaluation_service import BatchEvaluationService


class FakeEvaluationService:
    def __init__(self) -> None:
        self.calls = 0

    async def evaluate(self, candidate: dict[str, Any], job: dict[str, Any]) -> EvaluationResult:
        self.calls += 1
        return EvaluationResult(
            candidate_id=str(candidate.get("email")),
            job_id="job",
            overall_score=75.0,
            fit_level=FitLevel.MODERATE,
            rubric=[],
            strengths=[],
            gaps=GapAnalysis(recommendation="proceed"),
            summary="ok",
        )


def _candidate(name: str) -> Candidate:
    return Candidate(id=uuid.uuid4(), name=name, email=f"{name}@ex.com", profile={"skills": []})


async def test_evaluate_all_covers_every_candidate() -> None:
    fake = FakeEvaluationService()
    service = BatchEvaluationService(cast("Any", None), cast("Any", fake), concurrency=2)
    candidates = [_candidate("a"), _candidate("b"), _candidate("c")]

    pairs = await service._evaluate_all(candidates, {"title": "Role", "description": "d"})

    assert fake.calls == 3
    assert [c.name for c, _ in pairs] == ["a", "b", "c"]
    assert all(r.overall_score == 75.0 for _, r in pairs)


class FlakyEvaluationService:
    """Fails for one candidate to exercise partial-result tolerance."""

    async def evaluate(self, candidate: dict[str, Any], job: dict[str, Any]) -> EvaluationResult:
        if candidate.get("name") == "b":
            raise RuntimeError("provider 503")
        return EvaluationResult(
            candidate_id=str(candidate.get("email")),
            job_id="job",
            overall_score=80.0,
            fit_level=FitLevel.STRONG,
            rubric=[],
            strengths=[],
            gaps=GapAnalysis(recommendation="hire"),
            summary="ok",
        )


async def test_evaluate_all_tolerates_partial_failures() -> None:
    service = BatchEvaluationService(
        cast("Any", None), cast("Any", FlakyEvaluationService()), concurrency=2
    )
    candidates = [_candidate("a"), _candidate("b"), _candidate("c")]

    pairs = await service._evaluate_all(candidates, {"title": "R", "description": "d"})

    # "b" failed and is dropped; the other two survive.
    assert [c.name for c, _ in pairs] == ["a", "c"]


async def test_batch_endpoint_requires_llm(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    from backend.core.config import settings

    # Force "no LLM configured" regardless of the ambient .env.
    monkeypatch.setattr(settings, "llm_provider", "anthropic")
    monkeypatch.setattr(settings, "anthropic_api_key", "")
    monkeypatch.setattr(settings, "gemini_api_key", "")

    resp = await client.post(
        "/api/v1/evaluations/batch",
        json={"job_id": "00000000-0000-0000-0000-000000000009", "candidate_ids": []},
    )
    assert resp.status_code == 503
    assert resp.headers["content-type"].startswith("application/problem+json")
