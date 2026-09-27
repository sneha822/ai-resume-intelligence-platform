"""Unit tests for the legacy importer's pure helpers."""

from __future__ import annotations

from backend.db.import_legacy import _split_skills


def test_split_skills_handles_commas_and_semicolons() -> None:
    assert _split_skills("Python, SQL; Docker") == ["Python", "SQL", "Docker"]


def test_split_skills_empty() -> None:
    assert _split_skills(None) == []
    assert _split_skills("") == []


def test_split_skills_strips_whitespace() -> None:
    assert _split_skills("  Go ,  Rust ") == ["Go", "Rust"]
