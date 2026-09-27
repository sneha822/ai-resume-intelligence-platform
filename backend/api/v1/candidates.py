"""Candidate read endpoints."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException, status

from backend.api.deps import SessionDep
from backend.core.schemas import CandidateDetail, CandidateSummary
from backend.db.repositories import CandidateRepository

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("", response_model=list[CandidateSummary])
async def list_candidates(
    session: SessionDep, limit: int = 100, offset: int = 0
) -> list[CandidateSummary]:
    repo = CandidateRepository(session)
    rows = await repo.list_summaries(limit=limit, offset=offset)
    return [
        CandidateSummary(id=c.id, name=c.name, email=c.email, resume_count=count)
        for c, count in rows
    ]


@router.get("/{candidate_id}", response_model=CandidateDetail)
async def get_candidate(candidate_id: uuid.UUID, session: SessionDep) -> CandidateDetail:
    repo = CandidateRepository(session)
    candidate = await repo.get_detail(candidate_id)
    if candidate is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return CandidateDetail.model_validate(candidate)
