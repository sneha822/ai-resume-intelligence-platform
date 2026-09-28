"""FastAPI dependency wiring."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.base import get_session
from backend.services.retrieval_service import RetrievalService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_retrieval_service(session: SessionDep) -> RetrievalService:
    """Assemble a hybrid retrieval service from the current DB session.

    Heavy imports (embedding model, pgvector store) are deferred to call time so
    module import stays cheap and the ONNX model loads lazily on first search.
    """
    from backend.adapters.embeddings.factory import get_embedder
    from backend.adapters.retrieval.bm25 import Bm25Retriever
    from backend.adapters.vectorstore.pgvector_store import PgVectorStore
    from backend.db.models import Resume

    rows = (await session.execute(select(Resume.id, Resume.content_text))).all()
    corpus = {str(row.id): row.content_text for row in rows}

    return RetrievalService(
        embedder=get_embedder(),
        vector_store=PgVectorStore(session),
        sparse=Bm25Retriever(corpus),
    )


RetrievalServiceDep = Annotated[RetrievalService, Depends(get_retrieval_service)]


def _resilient_llm() -> object:
    """Build a rate-limited, circuit-broken LLM provider from settings."""
    from backend.adapters.llm.factory import get_llm_provider
    from backend.adapters.llm.resilient import ResilientLLMProvider
    from backend.core.resiliency.circuit_breaker import CircuitBreaker
    from backend.core.resiliency.rate_limiter import TokenBucketRateLimiter

    return ResilientLLMProvider(
        get_llm_provider(),
        rate_limiter=TokenBucketRateLimiter(rate=2.0, capacity=5.0),
        breaker=CircuitBreaker(failure_threshold=5, reset_timeout=30.0),
    )


def _require_llm_configured() -> None:
    from fastapi import HTTPException, status

    from backend.adapters.llm.factory import is_llm_configured

    if not is_llm_configured():
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM not configured (set the provider's API key, " "or LLM_PROVIDER=ollama).",
        )


def get_evaluation_service() -> EvaluationService:
    from backend.services.evaluation_service import EvaluationService

    _require_llm_configured()
    return EvaluationService(_resilient_llm())  # type: ignore[arg-type]


def get_copilot_service() -> CopilotService:
    from backend.services.copilot_service import CopilotService

    _require_llm_configured()
    return CopilotService(_resilient_llm())  # type: ignore[arg-type]


if TYPE_CHECKING:
    from backend.services.copilot_service import CopilotService
    from backend.services.evaluation_service import EvaluationService

EvaluationServiceDep = Annotated["EvaluationService", Depends(get_evaluation_service)]
CopilotServiceDep = Annotated["CopilotService", Depends(get_copilot_service)]
