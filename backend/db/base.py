"""SQLAlchemy 2.0 async engine, session factory, and declarative base.

The whole stack is async (FastAPI endpoints, ports, services), so the DB layer
uses ``create_async_engine`` with the psycopg (v3) dialect. The same
``DATABASE_URL`` works for both async runtime and Alembic's async migrations.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from backend.core.config import settings

# Consistent constraint naming keeps Alembic autogenerate diffs stable.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


engine = create_async_engine(settings.database_url, echo=settings.debug, future=True)

async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency yielding a transactional async session."""
    async with async_session_factory() as session:
        yield session
