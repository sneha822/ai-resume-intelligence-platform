"""Search endpoint test with an overridden retrieval service (no infra)."""

from __future__ import annotations

from fastapi import FastAPI
from httpx import AsyncClient

from backend.api.deps import get_retrieval_service
from backend.core.schemas import SearchResult


class FakeRetrievalService:
    async def search(self, query: str, k: int = 20) -> list[SearchResult]:
        return [
            SearchResult(candidate_id="c2", score=0.033),
            SearchResult(candidate_id="c1", score=0.016),
        ]


async def test_search_endpoint_returns_ranked_results(app: FastAPI, client: AsyncClient) -> None:
    app.dependency_overrides[get_retrieval_service] = lambda: FakeRetrievalService()

    resp = await client.post("/api/v1/search", json={"query": "python ml engineer", "top_k": 5})
    assert resp.status_code == 200
    body = resp.json()
    assert [r["candidate_id"] for r in body] == ["c2", "c1"]


async def test_search_validation_error(app: FastAPI, client: AsyncClient) -> None:
    # Override the DB-backed dependency so validation (not infra) is exercised.
    app.dependency_overrides[get_retrieval_service] = lambda: FakeRetrievalService()

    resp = await client.post("/api/v1/search", json={"query": ""})
    assert resp.status_code == 422
    assert resp.headers["content-type"].startswith("application/problem+json")
