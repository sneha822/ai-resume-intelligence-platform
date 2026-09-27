"""Resume parsing via PyMuPDF (fast, pure-CPU, no ML models).

Extracts full text and best-effort section splitting. The ``DocumentParser``
port lets a heavier parser (e.g. Docling) be swapped in later without touching
callers.
"""

from __future__ import annotations

import asyncio
import re

import pymupdf

from backend.core.ports.parser import ParsedDocument

# Common resume section headers used for light structural splitting.
_SECTION_HEADERS = (
    "summary",
    "experience",
    "work experience",
    "education",
    "skills",
    "projects",
    "certifications",
    "achievements",
)
_HEADER_RE = re.compile(
    r"^\s*(" + "|".join(_SECTION_HEADERS) + r")\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# Words that appear at the top of a resume but are not the person's name.
_NON_NAME_WORDS = set(_SECTION_HEADERS) | {
    "curriculum vitae",
    "resume",
    "cv",
    "profile",
    "contact",
    "contact information",
}
# A name token: alphabetic, allowing an internal apostrophe/hyphen or a trailing
# dot for a middle initial (e.g. "O'Brien", "Jean-Luc", "Q.").
_NAME_TOKEN_RE = re.compile(r"^[A-Za-z][A-Za-z'-]*\.?$")


class PyMuPDFParser:
    """Implements the ``DocumentParser`` port."""

    async def parse(self, filename: str, content: bytes) -> ParsedDocument:
        return await asyncio.to_thread(self._parse_sync, filename, content)

    def _parse_sync(self, filename: str, content: bytes) -> ParsedDocument:
        filetype = "pdf" if filename.lower().endswith(".pdf") else "txt"
        text_parts: list[str] = []
        with pymupdf.open(stream=content, filetype=filetype) as doc:
            for page in doc:
                text_parts.append(page.get_text())
        text = "\n".join(text_parts).strip()
        metadata = {"filename": filename, "parser": "pymupdf"}
        name = self._extract_name(text)
        if name:
            metadata["name"] = name
        return ParsedDocument(
            text=text,
            sections=self._split_sections(text),
            metadata=metadata,
        )

    @staticmethod
    def _extract_name(text: str) -> str | None:
        """Heuristic: the candidate's name is usually the first top line that is a
        short run of alphabetic words, without contact tokens or section words."""
        for raw in text.splitlines()[:8]:
            line = raw.strip()
            if not line:
                continue
            lowered = line.lower()
            if "@" in line or "http" in lowered or any(ch.isdigit() for ch in line):
                continue
            if lowered in _NON_NAME_WORDS:
                continue
            tokens = line.split()
            if not (2 <= len(tokens) <= 4):
                continue
            if not all(_NAME_TOKEN_RE.match(tok) for tok in tokens):
                continue
            # Normalize ALL-CAPS names ("JANE DOE" -> "Jane Doe").
            return line.title() if line.isupper() else line
        return None

    @staticmethod
    def _split_sections(text: str) -> dict[str, str]:
        matches = list(_HEADER_RE.finditer(text))
        sections: dict[str, str] = {}
        for i, match in enumerate(matches):
            name = match.group(1).lower()
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            body = text[start:end].strip()
            if body:
                sections[name] = body
        return sections
