"""Candidate repository."""

from __future__ import annotations

from sqlalchemy import select

from backend.db.models import Candidate
from backend.db.repositories.base import BaseRepository


class CandidateRepository(BaseRepository[Candidate]):
    model = Candidate

    async def get_by_email(self, email: str) -> Candidate | None:
        result = await self.session.execute(select(Candidate).where(Candidate.email == email))
        return result.scalar_one_or_none()

    async def upsert_by_email(
        self,
        email: str | None,
        name: str | None = None,
        phone: str | None = None,
        profile: dict[str, object] | None = None,
    ) -> Candidate:
        """Insert a candidate, or update the existing one with the same email."""
        existing = await self.get_by_email(email) if email else None
        if existing is not None:
            if name is not None:
                existing.name = name
            if phone is not None:
                existing.phone = phone
            if profile is not None:
                existing.profile = profile
            await self.session.flush()
            return existing

        candidate = Candidate(email=email, name=name, phone=phone, profile=profile or {})
        return await self.add(candidate)
