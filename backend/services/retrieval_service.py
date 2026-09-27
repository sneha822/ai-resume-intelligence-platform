"""Hybrid retrieval: dense (pgvector) + sparse (BM25) fused with RRF."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from backend.core.ports.embedder import Embedder
from backend.core.ports.vector_store import VectorStore
from backend.core.schemas.search import SearchResult


@runtime_checkable
class SparseRetriever(Protocol):
    def search(self, query: str, top_k: int = 20) -> list[str]: ...


class RetrievalService:
    def __init__(
        self,
        embedder: Embedder,
        vector_store: VectorStore,
        sparse: SparseRetriever,
    ) -> None:
        self._embedder = embedder
        self._vector_store = vector_store
        self._sparse = sparse

    async def search(self, query: str, k: int = 20, rrf_k: int = 60) -> list[SearchResult]:
        query_vector = await self._embedder.embed(query)
        dense = await self._vector_store.query(query_vector, top_k=k)
        dense_ids = [match.doc_id for match in dense]
        sparse_ids = self._sparse.search(query, top_k=k)

        fused = self._reciprocal_rank_fusion([dense_ids, sparse_ids], k=rrf_k)
        return [SearchResult(candidate_id=doc_id, score=score) for doc_id, score in fused[:k]]

    @staticmethod
    def _reciprocal_rank_fusion(rankings: list[list[str]], k: int) -> list[tuple[str, float]]:
        scores: dict[str, float] = {}
        for ranking in rankings:
            for rank, doc_id in enumerate(ranking):
                scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
        return sorted(scores.items(), key=lambda item: item[1], reverse=True)
