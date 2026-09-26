"""Search schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    query: str = Field(min_length=1, description="Natural-language recruiter query")
    top_k: int = Field(default=20, ge=1, le=100)


class SearchResult(BaseModel):
    candidate_id: str
    score: float
    snippet: str | None = None
