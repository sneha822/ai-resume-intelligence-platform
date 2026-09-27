"""Celery tasks for heavy, non-blocking work.

Tasks are synchronous entry points that drive the async services via
``asyncio.run`` (a fresh event loop per task). File bytes are passed base64-encoded
so they survive the JSON serializer.
"""

from __future__ import annotations

import asyncio
import base64

from backend.workers.celery_app import celery_app


async def _ingest(filename: str, content: bytes) -> str:
    from backend.adapters.embeddings.factory import get_embedder
    from backend.adapters.parsing.pymupdf_parser import PyMuPDFParser
    from backend.db.base import async_session_factory
    from backend.services.ingestion_service import IngestionService

    async with async_session_factory() as session:
        service = IngestionService(session, PyMuPDFParser(), get_embedder())
        return await service.ingest(filename, content)


@celery_app.task(name="ingest_resume")  # type: ignore[untyped-decorator]
def ingest_resume(filename: str, content_b64: str) -> str:
    content = base64.b64decode(content_b64)
    return asyncio.run(_ingest(filename, content))


async def _batch_evaluate(candidate_ids: list[str], job_id: str) -> list[str]:
    import uuid

    from backend.adapters.llm.factory import get_llm_provider
    from backend.adapters.llm.resilient import ResilientLLMProvider
    from backend.core.resiliency.circuit_breaker import CircuitBreaker
    from backend.core.resiliency.rate_limiter import TokenBucketRateLimiter
    from backend.db.base import async_session_factory
    from backend.db.models import Evaluation
    from backend.db.repositories import CandidateRepository, JobRepository
    from backend.services.evaluation_service import EvaluationService

    llm = ResilientLLMProvider(
        get_llm_provider(),
        rate_limiter=TokenBucketRateLimiter(rate=2.0, capacity=5.0),
        breaker=CircuitBreaker(failure_threshold=5, reset_timeout=30.0),
    )
    service = EvaluationService(llm)
    written: list[str] = []

    async with async_session_factory() as session:
        job = await JobRepository(session).get(uuid.UUID(job_id))
        if job is None:
            return written
        candidate_repo = CandidateRepository(session)
        for cid in candidate_ids:
            candidate = await candidate_repo.get(uuid.UUID(cid))
            if candidate is None:
                continue
            result = await service.evaluate(
                candidate={"name": candidate.name, "profile": candidate.profile},
                job={"title": job.title, "description": job.description},
            )
            evaluation = Evaluation(
                candidate_id=candidate.id,
                job_id=job.id,
                overall_score=result.overall_score,
                fit_level=result.fit_level.value,
                result=result.model_dump(mode="json"),
            )
            session.add(evaluation)
            written.append(str(candidate.id))
        await session.commit()
    return written


@celery_app.task(name="batch_evaluate")  # type: ignore[untyped-decorator]
def batch_evaluate(candidate_ids: list[str], job_id: str) -> list[str]:
    return asyncio.run(_batch_evaluate(candidate_ids, job_id))
