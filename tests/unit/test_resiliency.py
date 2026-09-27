"""Rate limiter, circuit breaker, and resilient LLM wrapper tests."""

from __future__ import annotations

import asyncio
import time

import pytest

from backend.adapters.llm.resilient import ResilientLLMProvider
from backend.core.resiliency.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerOpenError,
    CircuitState,
)
from backend.core.resiliency.rate_limiter import TokenBucketRateLimiter


async def test_rate_limiter_throttles_when_bucket_empties() -> None:
    limiter = TokenBucketRateLimiter(rate=20.0, capacity=1.0)
    start = time.monotonic()
    await limiter.acquire()  # uses the one initial token immediately
    await limiter.acquire()  # must wait ~1/20s for a refill
    elapsed = time.monotonic() - start
    assert elapsed >= 0.03


async def test_circuit_breaker_opens_then_recovers() -> None:
    breaker = CircuitBreaker(failure_threshold=2, reset_timeout=0.05)

    async def boom() -> str:
        raise ValueError("fail")

    async def ok() -> str:
        return "ok"

    for _ in range(2):
        with pytest.raises(ValueError):
            await breaker.call(boom)
    assert breaker.state is CircuitState.OPEN

    with pytest.raises(CircuitBreakerOpenError):
        await breaker.call(ok)

    await asyncio.sleep(0.06)  # let it move to half-open
    assert await breaker.call(ok) == "ok"
    assert breaker.state is CircuitState.CLOSED


class _AlwaysFailProvider:
    async def generate(self, prompt: str, system: str | None = None) -> str:
        raise RuntimeError("upstream down")

    async def structured(self, prompt, response_model, system=None):  # type: ignore[no-untyped-def]
        raise RuntimeError("upstream down")


async def test_resilient_provider_opens_circuit() -> None:
    breaker = CircuitBreaker(failure_threshold=1, reset_timeout=5.0)
    provider = ResilientLLMProvider(_AlwaysFailProvider(), breaker=breaker)

    with pytest.raises(RuntimeError):
        await provider.generate("hi")
    # circuit now open -> fail fast
    with pytest.raises(CircuitBreakerOpenError):
        await provider.generate("hi")
