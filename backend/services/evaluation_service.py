"""Multi-criteria candidate evaluation with chain-of-thought reasoning."""

from __future__ import annotations

from typing import Any

from backend.core.ports.llm import LLMProvider
from backend.core.schemas.evaluation import EvaluationResult

RUBRIC_CRITERIA = [
    "Technical Proficiency",
    "Domain Alignment",
    "Experience Depth",
    "Leadership Signal",
]

SYSTEM_PROMPT = (
    "You are an expert technical recruiter. Evaluate the candidate against each "
    "rubric criterion. Think step by step before assigning each score and cite "
    "specific evidence from the resume. Do not invent facts. Assign an overall "
    "score from 0-100 and a fit level of strong, moderate, or weak."
)


class EvaluationService:
    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm

    async def evaluate(self, candidate: dict[str, Any], job: dict[str, Any]) -> EvaluationResult:
        prompt = self._build_prompt(candidate, job)
        return await self._llm.structured(
            prompt=prompt,
            response_model=EvaluationResult,
            system=SYSTEM_PROMPT,
        )

    @staticmethod
    def _build_prompt(candidate: dict[str, Any], job: dict[str, Any]) -> str:
        criteria = ", ".join(RUBRIC_CRITERIA)
        return (
            f"JOB POSTING:\n{job}\n\n"
            f"CANDIDATE PROFILE:\n{candidate}\n\n"
            f"Evaluate the candidate against these criteria: {criteria}.\n"
            "Return one rubric entry per criterion, the strengths, a gap analysis, "
            "and a concise summary."
        )
