"""Resume ingestion: parse -> extract identity -> persist -> embed -> index."""

from __future__ import annotations

import re

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.ports.embedder import Embedder
from backend.core.ports.parser import DocumentParser
from backend.db.models import Resume
from backend.db.repositories import CandidateRepository

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE_RE = re.compile(r"(?:\+?\d[\d\s().-]{7,}\d)")


class IngestionService:
    def __init__(self, session: AsyncSession, parser: DocumentParser, embedder: Embedder) -> None:
        self._session = session
        self._parser = parser
        self._embedder = embedder

    async def ingest(self, filename: str, content: bytes) -> str:
        parsed = await self._parser.parse(filename, content)
        email, phone = self._extract_contact(parsed.text)

        candidate = await CandidateRepository(self._session).upsert_by_email(
            email=email,
            phone=phone,
            profile={"sections": parsed.sections},
        )

        embedding = await self._embedder.embed(parsed.text)
        resume = Resume(
            candidate_id=candidate.id,
            filename=filename,
            content_text=parsed.text,
            embedding=embedding,
        )
        self._session.add(resume)
        await self._session.flush()
        await self._session.commit()
        return str(resume.id)

    @staticmethod
    def _extract_contact(text: str) -> tuple[str | None, str | None]:
        email_match = _EMAIL_RE.search(text)
        phone_match = _PHONE_RE.search(text)
        return (
            email_match.group(0) if email_match else None,
            phone_match.group(0).strip() if phone_match else None,
        )
