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
    # Name should be extracted from the top line.
    assert result.metadata.get("name") == "Jane Doe"


async def test_parse_extracts_name_with_contact_header() -> None:
    body = "aryan.mehta.dev@example.com\nAryan Mehta\nSkills\nPython"
    result = await PyMuPDFParser().parse("aryan.pdf", _make_pdf(body))
    # First line is an email (skipped); name is the next qualifying line.
    assert result.metadata.get("name") == "Aryan Mehta"


async def test_all_caps_name_is_normalized() -> None:
    result = await PyMuPDFParser().parse("x.pdf", _make_pdf("ROHAN VERMA\nExperience"))
    assert result.metadata.get("name") == "Rohan Verma"


def test_extract_name_edge_cases() -> None:
    extract = PyMuPDFParser._extract_name
    assert extract("Jean-Luc O'Brien\nSkills") == "Jean-Luc O'Brien"
    assert extract("John Q. Public\nExperience") == "John Q. Public"
    # No plausible name -> None (contact only).
    assert extract("+1 555 123 4567\ninfo@example.com") is None
    # Section word alone is not a name.
    assert extract("Curriculum Vitae\nSummary") is None
