"""LLM structured extraction + heuristic-fallback tests (no real LLM)."""

from __future__ import annotations

from typing import TypeVar, cast

from pydantic import BaseModel

from backend.core.ports.parser import ParsedDocument
from backend.core.schemas.extraction import ResumeExtraction
from backend.services.extraction_service import ResumeExtractor
from backend.services.ingestion_service import IngestionService

T = TypeVar("T", bound=BaseModel)


class FakeLLM:
    """Returns a canned model and records the requested response_model."""

    def __init__(self, canned: BaseModel) -> None:
        self._canned = canned
        self.requested_model: type[BaseModel] | None = None

    async def generate(self, prompt: str, system: str | None = None) -> str:
        return ""

    async def structured(
        self, prompt: str, response_model: type[T], system: str | None = None
    ) -> T:
        self.requested_model = response_model
        return cast(T, self._canned)


class RaisingLLM:
    async def generate(self, prompt: str, system: str | None = None) -> str:
        raise RuntimeError("upstream down")

    async def structured(
        self, prompt: str, response_model: type[T], system: str | None = None
    ) -> T:
        raise RuntimeError("upstream down")


def _doc(text: str = "", *, name: str | None = None) -> ParsedDocument:
    meta = {"filename": "r.pdf", "parser": "pymupdf"}
    if name is not None:
        meta["name"] = name
    return ParsedDocument(text=text, sections={"skills": "Python"}, metadata=meta)


def _svc(extractor: ResumeExtractor | None) -> IngestionService:
    # session/parser/embedder are unused by the methods under test.
    return IngestionService(
        cast("object", None),  # type: ignore[arg-type]
        cast("object", None),  # type: ignore[arg-type]
        cast("object", None),  # type: ignore[arg-type]
        extractor=extractor,
    )


# --- ResumeExtractor requests the right schema -------------------------------


async def test_extractor_requests_resume_extraction_schema() -> None:
    fake = FakeLLM(ResumeExtraction(full_name="Ada Lovelace"))
    result = await ResumeExtractor(fake).extract("some resume text")
    assert fake.requested_model is ResumeExtraction
    assert result.full_name == "Ada Lovelace"


# --- identity resolution (LLM wins per-field, heuristics fill gaps) ----------


def test_llm_name_preferred_over_heuristic() -> None:
    extraction = ResumeExtraction(
        full_name="Grace Hopper",
        email="grace@navy.mil",
        skills=["COBOL"],
        current_title="Rear Admiral",
    )
    doc = _doc("Contact grace2@old.example", name="Wrong Heuristic")
    name, email, phone, profile = IngestionService._resolve_identity(doc, extraction)
    assert name == "Grace Hopper"
    assert email == "grace@navy.mil"
    assert profile["extracted_by"] == "llm"
    assert profile["skills"] == ["COBOL"]
    assert profile["current_title"] == "Rear Admiral"


def test_llm_null_name_falls_back_to_heuristic() -> None:
    extraction = ResumeExtraction(full_name=None, email=None)
    doc = _doc("jane@example.com +1 555 222 3333", name="Jane Roe")
    name, email, phone, _ = IngestionService._resolve_identity(doc, extraction)
    assert name == "Jane Roe"  # heuristic name
    assert email == "jane@example.com"  # regex fallback since LLM gave None
    assert phone is not None


def test_no_extraction_uses_heuristic_path() -> None:
    doc = _doc("john@example.com", name="John Doe")
    name, email, _, profile = IngestionService._resolve_identity(doc, None)
    assert name == "John Doe"
    assert email == "john@example.com"
    assert profile["extracted_by"] == "heuristic"


# --- graceful degradation ----------------------------------------------------


async def test_safe_extract_returns_none_without_extractor() -> None:
    assert await _svc(None)._safe_extract("text") is None


async def test_safe_extract_swallows_llm_failure() -> None:
    extractor = ResumeExtractor(RaisingLLM())
    assert await _svc(extractor)._safe_extract("text") is None
