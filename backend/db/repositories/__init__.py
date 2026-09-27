"""Data-access repositories."""

from backend.db.repositories.candidate import CandidateRepository
from backend.db.repositories.evaluation import EvaluationRepository
from backend.db.repositories.job import JobRepository

__all__ = ["CandidateRepository", "EvaluationRepository", "JobRepository"]
