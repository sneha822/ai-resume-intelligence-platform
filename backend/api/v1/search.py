"""Hybrid candidate search endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from backend.api.deps import RetrievalServiceDep
from backend.core.schemas import SearchQuery, SearchResult

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=list[SearchResult])
async def search_candidates(
    payload: SearchQuery, service: RetrievalServiceDep
) -> list[SearchResult]:
    return await service.search(payload.query, k=payload.top_k)
