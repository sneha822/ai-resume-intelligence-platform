"""Candidate API schemas."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CandidateCreate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    phone: str | None = None
    profile: dict[str, Any] = Field(default_factory=dict)


class CandidateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str | None
    name: str | None
    phone: str | None
    profile: dict[str, Any]
    created_at: datetime
