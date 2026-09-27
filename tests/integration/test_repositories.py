"""Repository integration tests.

These require a live Postgres (with the pgvector extension) reachable at
``DATABASE_URL``. They are skipped automatically when it is not available, so
the default CI unit run stays green without infrastructure. To run them::

    docker compose up -d postgres
    alembic upgrade head
    RUN_DB_TESTS=1 pytest tests/integration
"""

from __future__ import annotations

import os

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.core.config import settings
from backend.db.models import Candidate
from backend.db.repositories import CandidateRepository

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


async def test_upsert_by_email_creates_then_updates(session: AsyncSession) -> None:
    repo = CandidateRepository(session)

    created = await repo.upsert_by_email(
        email="jane@example.com", name="Jane", profile={"skills": ["Python"]}
    )
    assert isinstance(created, Candidate)
    assert created.name == "Jane"

    updated = await repo.upsert_by_email(email="jane@example.com", phone="555-0100")
    assert updated.id == created.id
    assert updated.phone == "555-0100"
    assert updated.name == "Jane"  # unchanged
