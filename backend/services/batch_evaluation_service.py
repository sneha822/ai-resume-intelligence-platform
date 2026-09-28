"""Bulk candidate evaluation.

Evaluates many candidates against a job concurrently (bounded), then upserts the
results (unique per candidate+job). Shared by the sync API endpoint and the
Celery ``batch_evaluate`` task.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.schemas.evaluation import EvaluationResult
from backend.db.models import Candidate, Evaluation, Job
from backend.db.repositories import CandidateRepository, EvaluationRepository
from backend.services.evaluation_service import EvaluationService

logger = logging.getLogger(__name__)


class BatchEvaluationService:
    def __init__(
        self,
        session: AsyncSession,
        evaluation_service: EvaluationService,
        concurrency: int = 3,
    ) -> None:
        self._session = session
        self._eval = evaluation_service
        self._concurrency = max(1, concurrency)

    async def evaluate_job(
        self, job: Job, candidate_ids: list[uuid.UUID] | None = None
    ) -> list[tuple[Candidate, EvaluationResult]]:
        candidates = await self._load_candidates(candidate_ids)
        job_payload = {"title": job.title, "description": job.description}
        pairs = await self._evaluate_all(candidates, job_payload)
        await self._persist(job, pairs)
        return pairs

    async def _load_candidates(self, candidate_ids: list[uuid.UUID] | None) -> list[Candidate]:
        repo = CandidateRepository(self._session)
        if candidate_ids:
            loaded = [await repo.get(cid) for cid in candidate_ids]
            return [c for c in loaded if c is not None]
        return await repo.list(limit=1000)

    async def _evaluate_all(
        self, candidates: list[Candidate], job_payload: dict[str, Any]
    ) -> list[tuple[Candidate, EvaluationResult]]:
        semaphore = asyncio.Semaphore(self._concurrency)

        async def evaluate_one(
            candidate: Candidate,
        ) -> tuple[Candidate, EvaluationResult]:
            async with semaphore:
                result = await self._eval.evaluate(
                    candidate={
                        "name": candidate.name,
                        "email": candidate.email,
                        "profile": candidate.profile,
                    },
                    job=job_payload,
                )
                return candidate, result

        # Tolerate per-candidate failures (e.g. provider throttling) so a bad
        # apple doesn't fail the whole batch — return the successes.
        outcomes = await asyncio.gather(
            *(evaluate_one(c) for c in candidates), return_exceptions=True
        )
        pairs: list[tuple[Candidate, EvaluationResult]] = []
        for candidate, outcome in zip(candidates, outcomes, strict=True):
            if isinstance(outcome, BaseException):
                logger.warning("Evaluation failed for %s: %s", candidate.id, outcome)
            else:
                pairs.append(outcome)
        return pairs

    async def _persist(self, job: Job, pairs: list[tuple[Candidate, EvaluationResult]]) -> None:
        existing = {
            e.candidate_id: e for e in await EvaluationRepository(self._session).for_job(job.id)
        }
        for candidate, result in pairs:
            record = existing.get(candidate.id)
            if record is None:
                self._session.add(
                    Evaluation(
                        candidate_id=candidate.id,
                        job_id=job.id,
                        overall_score=result.overall_score,
                        fit_level=result.fit_level.value,
                        result=result.model_dump(mode="json"),
                    )
                )
            else:
                record.overall_score = result.overall_score
                record.fit_level = result.fit_level.value
                record.result = result.model_dump(mode="json")
        await self._session.commit()
