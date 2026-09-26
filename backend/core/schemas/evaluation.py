"""Evaluation schemas.

``EvaluationResult`` is the deterministic contract the LLM must return (enforced
via Instructor in the Anthropic adapter), replacing the old dataclass +
``json.loads`` approach.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class FitLevel(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"


class RubricScore(BaseModel):
    criterion: str = Field(description="e.g. Technical Proficiency")
    score: float = Field(ge=0, le=10)
    reasoning: str = Field(description="Chain-of-thought justification grounded in resume evidence")
    evidence: list[str] = Field(default_factory=list)


class GapAnalysis(BaseModel):
    missing_skills: list[str] = Field(default_factory=list)
    experience_gaps: list[str] = Field(default_factory=list)
    recommendation: str


class EvaluationResult(BaseModel):
    candidate_id: str
    job_id: str
    overall_score: float = Field(ge=0, le=100)
    fit_level: FitLevel
    rubric: list[RubricScore]
    strengths: list[str] = Field(default_factory=list)
    gaps: GapAnalysis
    summary: str
