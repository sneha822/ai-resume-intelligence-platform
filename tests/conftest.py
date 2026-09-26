"""Shared test fixtures.

The API tests run against an in-memory SQLite database so they need no external
infrastructure and stay in the default CI run. Only the relational tables
(``users``, ``jobs``) are created here — tables that use Postgres-only types
(JSONB, pgvector) are exercised in the ``tests/integration`` suite against a real
Postgres instead.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from backend.db.base import get_session
from backend.db.models import Job, User
from backend.main import create_app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        # Create only the tables that use portable column types.
        await conn.run_sync(User.__table__.create)
        await conn.run_sync(Job.__table__.create)

    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def _override_get_session() -> AsyncIterator[AsyncSession]:
        async with factory() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_session] = _override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    await engine.dispose()
