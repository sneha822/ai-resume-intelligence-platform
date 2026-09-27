"""EvaluationService tests using a fake LLM provider (no network)."""

from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

from backend.core.schemas.evaluation import (
    EvaluationResult,
    FitLevel,
    GapAnalysis,
    RubricScore,
)
from backend.services.evaluation_service import RUBRIC_CRITERIA, EvaluationService

T = TypeVar("T", bound=BaseModel)

_CANNED = EvaluationResult(
    candidate_id="c1",
    job_id="j1",
    overall_score=82.0,
    fit_level=FitLevel.STRONG,
    rubric=[
        RubricScore(criterion=c, score=8.0, reasoning="ok", evidence=["x"]) for c in RUBRIC_CRITERIA
    ],
    strengths=["Python"],
    gaps=GapAnalysis(missing_skills=[], experience_gaps=[], recommendation="hire"),
    summary="Strong fit.",
)


class FakeLLMProvider:
    def __init__(self) -> None:
        self.last_response_model: type[BaseModel] | None = None
        self.last_system: str | None = None

    async def generate(self, prompt: str, system: str | None = None) -> str:
        return "unused"

    async def structured(
        self, prompt: str, response_model: type[T], system: str | None = None
    ) -> T:
        self.last_response_model = response_model
        self.last_system = system
        return _CANNED  # type: ignore[return-value]


async def test_evaluate_returns_structured_result() -> None:
    fake = FakeLLMProvider()
    service = EvaluationService(fake)

    result = await service.evaluate(
        candidate={"name": "Jane", "skills": ["Python"]},
        job={"title": "ML Engineer"},
    )

    assert isinstance(result, EvaluationResult)
    assert result.fit_level is FitLevel.STRONG
    assert len(result.rubric) == len(RUBRIC_CRITERIA)
    # The service must request the EvaluationResult contract, with a system prompt.
    assert fake.last_response_model is EvaluationResult
    assert fake.last_system is not None
