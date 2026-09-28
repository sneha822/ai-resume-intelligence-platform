"""LLM-based structured resume extraction (Instructor/Claude JSON).

Extracts the candidate's full name and other attributes robustly, even when the
name sits in a header, a graphic caption, or beside a job title. Callers fall back
to the regex/heuristic path when this is unavailable or fails.
"""

from __future__ import annotations

from backend.core.ports.llm import LLMProvider
from backend.core.schemas.extraction import ResumeExtraction

# Cap prompt size — the identity/skills live near the top; this bounds token cost.
_MAX_CHARS = 6000

SYSTEM_PROMPT = (
    "You extract structured data from resume text. Return only what is present; "
    "use null for anything you cannot find. The full name may appear in a header, "
    "a logo/graphic caption, or next to a job title — capture it regardless. Never "
    "invent values."
)


class ResumeExtractor:
    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm

    async def extract(self, text: str) -> ResumeExtraction:
        prompt = f"Extract structured fields from this resume:\n\n{text[:_MAX_CHARS]}"
        return await self._llm.structured(
            prompt=prompt, response_model=ResumeExtraction, system=SYSTEM_PROMPT
        )


def build_default_extractor() -> ResumeExtractor | None:
    """Build an extractor from settings, or None when no LLM is configured.

    Wraps the provider in the resilient decorator (rate limit + circuit breaker),
    matching how evaluation/copilot call the LLM.
    """
    from backend.adapters.llm.factory import get_llm_provider, is_llm_configured

    if not is_llm_configured():
        return None

    from backend.adapters.llm.resilient import ResilientLLMProvider
    from backend.core.resiliency.circuit_breaker import CircuitBreaker
    from backend.core.resiliency.rate_limiter import TokenBucketRateLimiter

    provider = ResilientLLMProvider(
        get_llm_provider(),
        rate_limiter=TokenBucketRateLimiter(rate=2.0, capacity=5.0),
        breaker=CircuitBreaker(failure_threshold=5, reset_timeout=30.0),
    )
    return ResumeExtractor(provider)
