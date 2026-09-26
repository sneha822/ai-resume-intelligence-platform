"""PyMuPDF parser round-trip test (generates a small PDF, then parses it)."""

from __future__ import annotations

import pymupdf

from backend.adapters.parsing.pymupdf_parser import PyMuPDFParser


def _make_pdf(text: str) -> bytes:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    data: bytes = doc.tobytes()
    doc.close()
    return data


async def test_parse_extracts_text_and_sections() -> None:
    body = "Jane Doe\nSkills\nPython, SQL\nExperience\nBuilt ML systems"
    pdf = _make_pdf(body)

    result = await PyMuPDFParser().parse("jane.pdf", pdf)

    assert "Jane Doe" in result.text
    assert "Python" in result.text
    assert result.metadata["parser"] == "pymupdf"
    # Section headers on their own line should be detected.
    assert "skills" in result.sections
