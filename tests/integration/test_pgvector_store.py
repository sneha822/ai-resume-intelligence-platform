"""pgvector store integration test.

Requires a live Postgres with the pgvector extension and migrations applied.
Skipped unless RUN_DB_TESTS=1. See tests/integration/test_repositories.py.
"""

from __future__ import annotations

import os

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.adapters.vectorstore.pgvector_store import PgVectorStore
from backend.core.config import settings
from backend.db.models import Candidate, Resume

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1",
    reason="Set RUN_DB_TESTS=1 with a live Postgres to run DB integration tests.",
)


@pytest.fixture
async def session() -> AsyncSession:
    engine = create_async_engine(settings.database_url)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as s:
        yield s
        await s.rollback()
    await engine.dispose()


async def test_upsert_and_query_nearest(session: AsyncSession) -> None:
    dim = settings.embedding_dim
    candidate = Candidate(email="vec@example.com", profile={})
    session.add(candidate)
    await session.flush()

    resume = Resume(
        candidate_id=candidate.id,
        filename="r.pdf",
        content_text="python ml",
        embedding=[1.0] + [0.0] * (dim - 1),
    )
    session.add(resume)
    await session.flush()

    store = PgVectorStore(session)
    matches = await store.query([1.0] + [0.0] * (dim - 1), top_k=5)

    assert any(m.doc_id == str(resume.id) for m in matches)
