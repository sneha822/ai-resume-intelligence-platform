"""Hybrid retrieval + RRF tests using fakes and a real BM25 index."""

from __future__ import annotations

from backend.adapters.retrieval.bm25 import Bm25Retriever
from backend.core.ports.vector_store import ScoredMatch
from backend.services.retrieval_service import RetrievalService


class FakeEmbedder:
    dimension = 3

    async def embed(self, text: str) -> list[float]:
        return [1.0, 0.0, 0.0]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [[1.0, 0.0, 0.0] for _ in texts]


class FakeVectorStore:
    def __init__(self, matches: list[ScoredMatch]) -> None:
        self._matches = matches

    async def upsert(self, doc_id, vector, payload) -> None:  # type: ignore[no-untyped-def]
        return None

    async def query(self, vector, top_k=20) -> list[ScoredMatch]:  # type: ignore[no-untyped-def]
        return self._matches[:top_k]

    async def delete(self, doc_id) -> None:  # type: ignore[no-untyped-def]
        return None


def test_rrf_rewards_agreement_across_rankers() -> None:
    # doc "b" is top of both rankers -> must win after fusion.
    fused = RetrievalService._reciprocal_rank_fusion([["b", "a", "c"], ["b", "d", "e"]], k=60)
    ranked_ids = [doc_id for doc_id, _ in fused]
    assert ranked_ids[0] == "b"


async def test_hybrid_search_merges_dense_and_sparse() -> None:
    dense = FakeVectorStore(
        [ScoredMatch(doc_id="c1", score=0.9), ScoredMatch(doc_id="c2", score=0.8)]
    )
    # A corpus large enough that BM25 IDF for the query terms stays positive
    # (tiny corpora drive IDF to ~0 and every score collapses).
    sparse = Bm25Retriever(
        {
            "c2": "python machine learning engineer nlp",
            "c3": "java backend developer spring",
            "c4": "frontend react typescript developer",
            "c5": "devops kubernetes terraform aws",
            "c6": "product manager roadmap stakeholders",
        }
    )
    service = RetrievalService(FakeEmbedder(), dense, sparse)

    results = await service.search("python machine learning", k=10)
    ids = [r.candidate_id for r in results]

    assert "c2" in ids  # in both dense and sparse -> should rank first
    assert ids[0] == "c2"
    assert "c1" in ids  # dense-only still included
    assert all(r.score > 0 for r in results)
