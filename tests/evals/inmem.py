"""In-memory cosine vector store for evaluation (no Postgres needed)."""

from __future__ import annotations

import math

from backend.core.ports.vector_store import ScoredMatch


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


class InMemoryVectorStore:
    """Implements the VectorStore protocol over an in-memory dict of vectors."""

    def __init__(self, vectors: dict[str, list[float]]) -> None:
        self._vectors = vectors

    async def upsert(self, doc_id: str, vector: list[float], payload: dict[str, object]) -> None:
        self._vectors[doc_id] = vector

    async def query(self, vector: list[float], top_k: int = 20) -> list[ScoredMatch]:
        scored = [
            ScoredMatch(doc_id=doc_id, score=_cosine(vector, vec))
            for doc_id, vec in self._vectors.items()
        ]
        scored.sort(key=lambda m: m.score, reverse=True)
        return scored[:top_k]

    async def delete(self, doc_id: str) -> None:
        self._vectors.pop(doc_id, None)
