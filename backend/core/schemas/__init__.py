"""Pydantic v2 schemas: API I/O contracts and LLM structured-output models."""

from backend.core.schemas.candidate import CandidateCreate, CandidateRead
from backend.core.schemas.evaluation import (
    EvaluationResult,
    FitLevel,
    GapAnalysis,
    RubricScore,
)
from backend.core.schemas.job import JobCreate, JobRead, JobUpdate
from backend.core.schemas.search import SearchQuery, SearchResult

__all__ = [
    "CandidateCreate",
    "CandidateRead",
    "EvaluationResult",
    "FitLevel",
    "GapAnalysis",
    "JobCreate",
    "JobRead",
    "JobUpdate",
    "RubricScore",
    "SearchQuery",
    "SearchResult",
]
