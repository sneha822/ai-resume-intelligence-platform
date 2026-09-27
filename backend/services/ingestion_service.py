"""Resume ingestion: parse -> extract identity -> persist -> embed -> index.

Identity/attributes come from an optional LLM extractor; when it is absent or
fails, we fall back to the regex + parser-heuristic path so ingestion never breaks.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.ports.embedder import Embedder
from backend.core.ports.parser import DocumentParser, ParsedDocument
from backend.core.schemas.extraction import ResumeExtraction
from backend.db.models import Resume
from backend.db.repositories import CandidateRepository
from backend.services.extraction_service import ResumeExtractor

logger = logging.getLogger(__name__)

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE_RE = re.compile(r"(?:\+?\d[\d\s().-]{7,}\d)")


class IngestionService:
    def __init__(
        self,
        session: AsyncSession,
        parser: DocumentParser,
        embedder: Embedder,
        extractor: ResumeExtractor | None = None,
    ) -> None:
        self._session = session
        self._parser = parser
        self._embedder = embedder
        self._extractor = extractor

    async def ingest(self, filename: str, content: bytes) -> str:
        parsed = await self._parser.parse(filename, content)
        extraction = await self._safe_extract(parsed.text)
        name, email, phone, profile = self._resolve_identity(parsed, extraction)

        candidate = await CandidateRepository(self._session).upsert_by_email(
            email=email, name=name, phone=phone, profile=profile
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

    async def _safe_extract(self, text: str) -> ResumeExtraction | None:
        """Run the LLM extractor, returning None if unavailable or it fails."""
        if self._extractor is None:
            return None
        try:
            return await self._extractor.extract(text)
        except Exception as exc:  # noqa: BLE001 - degrade gracefully to heuristics
            logger.warning("LLM resume extraction failed, using heuristics: %s", exc)
            return None

    @staticmethod
    def _resolve_identity(
        parsed: ParsedDocument, extraction: ResumeExtraction | None
    ) -> tuple[str | None, str | None, str | None, dict[str, Any]]:
        """Merge LLM extraction with regex/heuristic fallbacks (LLM wins per-field)."""
        regex_email, regex_phone = _extract_contact(parsed.text)
        heuristic_name = parsed.metadata.get("name")
        profile: dict[str, Any] = {"sections": parsed.sections}

        if extraction is None:
            profile["extracted_by"] = "heuristic"
            return heuristic_name, regex_email, regex_phone, profile

        profile["extracted_by"] = "llm"
        profile["skills"] = extraction.skills
        for key, value in (
            ("current_title", extraction.current_title),
            ("location", extraction.location),
            ("years_of_experience", extraction.years_of_experience),
            ("summary", extraction.summary),
        ):
            if value is not None:
                profile[key] = value

        return (
            extraction.full_name or heuristic_name,
            extraction.email or regex_email,
            extraction.phone or regex_phone,
            profile,
        )


def _extract_contact(text: str) -> tuple[str | None, str | None]:
    email_match = _EMAIL_RE.search(text)
    phone_match = _PHONE_RE.search(text)
    return (
        email_match.group(0) if email_match else None,
        phone_match.group(0).strip() if phone_match else None,
    )
