"""Recruiter copilot endpoint (non-streaming)."""

from __future__ import annotations

from fastapi import APIRouter

from backend.api.deps import CopilotServiceDep, SessionDep
from backend.core.schemas import CopilotRequest, CopilotResponse
from backend.db.repositories import CandidateRepository

router = APIRouter(prefix="/copilot", tags=["copilot"])


@router.post("", response_model=CopilotResponse)
async def ask_copilot(
    payload: CopilotRequest, session: SessionDep, service: CopilotServiceDep
) -> CopilotResponse:
    repo = CandidateRepository(session)
    candidates = []
    for cid in payload.candidate_ids:
        candidate = await repo.get(cid)
        if candidate is not None:
            candidates.append(
                {
                    "name": candidate.name,
                    "email": candidate.email,
                    "profile": candidate.profile,
                }
            )
    answer = await service.answer(payload.question, candidates)
    return CopilotResponse(answer=answer)
