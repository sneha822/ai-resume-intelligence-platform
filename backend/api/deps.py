"""FastAPI dependency wiring."""

from __future__ import annotations

from typing import Annotated

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
