"""Resilient LLM provider decorator: rate limiting + circuit breaking.

Wraps any ``LLMProvider`` (Tenacity retries already live inside the concrete
providers) so callers get throttling and fail-fast behaviour transparently.
"""

from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

from backend.core.ports.llm import LLMProvider
from backend.core.resiliency.circuit_breaker import CircuitBreaker
from backend.core.resiliency.rate_limiter import TokenBucketRateLimiter

T = TypeVar("T", bound=BaseModel)


class ResilientLLMProvider:
    """Implements the ``LLMProvider`` port around an inner provider."""

    def __init__(
        self,
        inner: LLMProvider,
        rate_limiter: TokenBucketRateLimiter | None = None,
        breaker: CircuitBreaker | None = None,
    ) -> None:
        self._inner = inner
        self._rate_limiter = rate_limiter
        self._breaker = breaker

    async def generate(self, prompt: str, system: str | None = None) -> str:
        if self._rate_limiter is not None:
            await self._rate_limiter.acquire()
        if self._breaker is not None:
            return await self._breaker.call(self._inner.generate, prompt, system)
        return await self._inner.generate(prompt, system)

    async def structured(
        self, prompt: str, response_model: type[T], system: str | None = None
    ) -> T:
        if self._rate_limiter is not None:
            await self._rate_limiter.acquire()
        if self._breaker is not None:
            return await self._breaker.call(self._inner.structured, prompt, response_model, system)
        return await self._inner.structured(prompt, response_model, system)
