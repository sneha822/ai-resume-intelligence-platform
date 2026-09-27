"""Structured resume extraction contract (LLM response model)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ResumeExtraction(BaseModel):
    """Structured attributes an LLM extracts from raw resume text.

    Used as the Instructor ``response_model`` so the model returns validated JSON.
    Every field is optional/defaulted so a sparse resume still parses.
    """

    full_name: str | None = Field(
        default=None,
        description="The candidate's full name, even if it appears in a header, "
        "graphic caption, or before/after a job title. Null if truly absent.",
    )
    email: str | None = Field(default=None, description="Primary email address.")
    phone: str | None = Field(default=None, description="Primary phone number.")
    current_title: str | None = Field(default=None, description="Most recent or current job title.")
    location: str | None = Field(default=None, description="City/region, if stated.")
    years_of_experience: float | None = Field(
        default=None, ge=0, description="Total years of professional experience."
    )
    skills: list[str] = Field(
        default_factory=list, description="Distinct technical/professional skills."
    )
    summary: str | None = Field(default=None, description="One-sentence professional summary.")
