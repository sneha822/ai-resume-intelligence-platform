"""LLM scoring drift gate.

Evaluates golden candidate/job pairs and asserts the rubric evaluator returns the
expected fit level and a score in the expected band. Skipped unless RUN_LLM_EVALS=1
and an LLM is configured (real API cost). This is the drift guard for scoring.
"""

from __future__ import annotations

import os

import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_LLM_EVALS") != "1",
    reason="Set RUN_LLM_EVALS=1 (and configure an LLM) to run scoring-drift evals.",
)

_JOB = {
    "title": "Senior NLP Engineer",
    "description": "Build RAG systems; require Python, transformers, LLM fine-tuning.",
}

_STRONG = {
    "name": "Strong Fit",
    "profile": {"skills": ["Python", "transformers", "RAG", "LLM fine-tuning", "NLP"]},
}
_WEAK = {
    "name": "Weak Fit",
    "profile": {"skills": ["Excel", "bookkeeping", "customer support"]},
}


async def test_scoring_separates_strong_from_weak() -> None:
    from backend.adapters.llm.factory import get_llm_provider
    from backend.services.evaluation_service import EvaluationService

    service = EvaluationService(get_llm_provider())

    strong = await service.evaluate(candidate=_STRONG, job=_JOB)
    weak = await service.evaluate(candidate=_WEAK, job=_JOB)

    assert strong.overall_score > weak.overall_score
    assert strong.overall_score >= 60
    assert weak.overall_score <= 50
