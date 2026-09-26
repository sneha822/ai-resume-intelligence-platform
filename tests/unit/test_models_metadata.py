"""Schema-level tests that do not require a live database."""

from __future__ import annotations

from backend.core.config import settings
from backend.db import models  # noqa: F401  (registers tables on Base.metadata)
from backend.db.base import Base

EXPECTED_TABLES = {
    "users",
    "jobs",
    "candidates",
    "resumes",
    "evaluations",
    "audit_log",
}


def test_all_tables_registered() -> None:
    assert set(Base.metadata.tables) >= EXPECTED_TABLES


def test_resume_embedding_dimension_matches_settings() -> None:
    embedding = Base.metadata.tables["resumes"].c.embedding
    assert embedding.type.dim == settings.embedding_dim  # type: ignore[attr-defined]


def test_evaluation_has_unique_candidate_job() -> None:
    constraints = {c.name for c in Base.metadata.tables["evaluations"].constraints}
    assert "candidate_job" in constraints
