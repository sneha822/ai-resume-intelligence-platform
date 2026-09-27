"""Recruiter copilot endpoints (non-streaming + SSE streaming)."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.api.deps import CopilotServiceDep, SessionDep
from backend.core.schemas import CopilotRequest, CopilotResponse
from backend.db.repositories import CandidateRepository

router = APIRouter(prefix="/copilot", tags=["copilot"])


async def _gather_context(session: SessionDep, request: CopilotRequest) -> list[dict[str, Any]]:
    repo = CandidateRepository(session)
    candidates: list[dict[str, Any]] = []
    for cid in request.candidate_ids:
        candidate = await repo.get(cid)
        if candidate is not None:
            candidates.append(
                {
                    "name": candidate.name,
                    "email": candidate.email,
                    "profile": candidate.profile,
                }
            )
    return candidates


@router.post("", response_model=CopilotResponse)
async def ask_copilot(
    payload: CopilotRequest, session: SessionDep, service: CopilotServiceDep
) -> CopilotResponse:
    candidates = await _gather_context(session, payload)
    answer = await service.answer(payload.question, candidates)
    return CopilotResponse(answer=answer)


@router.post("/stream")
async def stream_copilot(
    payload: CopilotRequest, session: SessionDep, service: CopilotServiceDep
) -> StreamingResponse:
    candidates = await _gather_context(session, payload)

    async def event_stream() -> AsyncIterator[str]:
        async for chunk in service.answer_stream(payload.question, candidates):
            yield f"data: {json.dumps({'delta': chunk})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
