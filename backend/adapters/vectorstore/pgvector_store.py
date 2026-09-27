"""pgvector-backed vector store over the ``resumes.embedding`` column."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.ports.vector_store import ScoredMatch
from backend.db.models import Resume


class PgVectorStore:
    """Implements the ``VectorStore`` port using Postgres + pgvector.

    ``doc_id`` is the resume UUID (string). Scores are cosine similarity in
    ``[-1, 1]`` derived from pgvector's cosine distance.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert(self, doc_id: str, vector: list[float], payload: dict[str, object]) -> None:
        resume = await self._session.get(Resume, uuid.UUID(doc_id))
        if resume is not None:
            resume.embedding = vector
            await self._session.flush()

    async def query(self, vector: list[float], top_k: int = 20) -> list[ScoredMatch]:
        distance = Resume.embedding.cosine_distance(vector)
        stmt = (
            select(Resume.id, distance.label("distance"))
            .where(Resume.embedding.is_not(None))
            .order_by(distance)
            .limit(top_k)
        )
        rows = (await self._session.execute(stmt)).all()
        return [ScoredMatch(doc_id=str(row.id), score=1.0 - float(row.distance)) for row in rows]

    async def delete(self, doc_id: str) -> None:
        resume = await self._session.get(Resume, uuid.UUID(doc_id))
        if resume is not None:
            resume.embedding = None
            await self._session.flush()
