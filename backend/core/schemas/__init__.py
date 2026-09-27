"""Pydantic v2 schemas: API I/O contracts and LLM structured-output models."""

from backend.core.schemas.candidate import (
    CandidateCreate,
    CandidateDetail,
    CandidateRead,
    CandidateSummary,
    EvaluationRead,
    ResumeRead,
)
from backend.core.schemas.copilot import CopilotRequest, CopilotResponse
from backend.core.schemas.evaluation import (
    EvaluationRequest,
    EvaluationResult,
    FitLevel,
    GapAnalysis,
    RubricScore,
)
from backend.core.schemas.extraction import ResumeExtraction
from backend.core.schemas.job import JobCreate, JobRead, JobUpdate
from backend.core.schemas.search import SearchQuery, SearchResult

__all__ = [
    "CandidateCreate",
    "CandidateDetail",
    "CandidateRead",
    "CandidateSummary",
    "CopilotRequest",
    "CopilotResponse",
    "EvaluationRead",
    "EvaluationRequest",
    "EvaluationResult",
    "FitLevel",
    "GapAnalysis",
    "JobCreate",
    "JobRead",
    "JobUpdate",
    "ResumeExtraction",
    "ResumeRead",
    "RubricScore",
    "SearchQuery",
    "SearchResult",
]
