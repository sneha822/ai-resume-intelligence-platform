"""Document parser port.

Concrete adapters (Docling / Unstructured / LlamaParse) turn raw resume bytes
into structured content the ingestion service can normalise into a candidate
profile.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel


class ParsedDocument(BaseModel):
    text: str
    sections: dict[str, str] = {}
    metadata: dict[str, str] = {}


@runtime_checkable
class DocumentParser(Protocol):
    async def parse(self, filename: str, content: bytes) -> ParsedDocument:
        """Parse raw document bytes into structured content."""
        ...
