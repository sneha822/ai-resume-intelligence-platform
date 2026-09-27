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
        return ParsedDocument(
            text=text,
            sections=self._split_sections(text),
            metadata={"filename": filename, "parser": "pymupdf"},
        )

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
