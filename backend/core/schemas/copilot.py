"""Recruiter copilot schemas."""

from __future__ import annotations

import uuid

from pydantic import BaseModel, Field


class CopilotRequest(BaseModel):
    question: str = Field(min_length=1)
    candidate_ids: list[uuid.UUID] = Field(default_factory=list)


class CopilotResponse(BaseModel):
    answer: str
