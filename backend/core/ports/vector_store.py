"""Vector store port (backed by pgvector in the default adapter)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel


class ScoredMatch(BaseModel):
    doc_id: str
    score: float


@runtime_checkable
class VectorStore(Protocol):
    async def upsert(self, doc_id: str, vector: list[float], payload: dict[str, object]) -> None:
        """Insert or update a single vector with its metadata payload."""
        ...

    async def query(self, vector: list[float], top_k: int = 20) -> list[ScoredMatch]:
        """Return the ``top_k`` nearest neighbours to ``vector``."""
        ...

    async def delete(self, doc_id: str) -> None:
        """Remove a vector by id."""
        ...
