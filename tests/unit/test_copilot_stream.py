"""Streaming copilot tests: service, resilient passthrough, and SSE endpoint."""

from __future__ import annotations

from collections.abc import AsyncIterator

from fastapi import FastAPI
from httpx import AsyncClient

from backend.adapters.llm.resilient import ResilientLLMProvider
from backend.api.deps import get_copilot_service
from backend.core.resiliency.rate_limiter import TokenBucketRateLimiter
from backend.services.copilot_service import CopilotService


class FakeStreamingLLM:
    def __init__(self, chunks: list[str]) -> None:
        self._chunks = chunks

    async def generate(self, prompt: str, system: str | None = None) -> str:
        return "".join(self._chunks)

    async def structured(self, prompt, response_model, system=None):  # type: ignore[no-untyped-def]
        raise NotImplementedError

    async def stream(self, prompt: str, system: str | None = None) -> AsyncIterator[str]:
        for c in self._chunks:
            yield c


async def test_copilot_service_streams_chunks() -> None:
    service = CopilotService(FakeStreamingLLM(["Hello ", "there ", "recruiter"]))
    out = [chunk async for chunk in service.answer_stream("hi", [])]
    assert "".join(out) == "Hello there recruiter"


async def test_resilient_provider_stream_passthrough() -> None:
    inner = FakeStreamingLLM(["a", "b", "c"])
    provider = ResilientLLMProvider(
        inner, rate_limiter=TokenBucketRateLimiter(rate=1000, capacity=10)
    )
    out = [chunk async for chunk in provider.stream("x")]
    assert out == ["a", "b", "c"]


class _FakeStreamCopilot:
    async def answer_stream(
        self, question: str, candidates: list[dict[str, object]]
    ) -> AsyncIterator[str]:
        for c in ["Ada ", "scores ", "highest."]:
            yield c


async def test_stream_endpoint_emits_sse(app: FastAPI, client: AsyncClient) -> None:
    app.dependency_overrides[get_copilot_service] = lambda: _FakeStreamCopilot()

    resp = await client.post(
        "/api/v1/copilot/stream",
        json={"question": "who is best?", "candidate_ids": []},
    )
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/event-stream")
    body = resp.text
    assert '"delta": "Ada "' in body
    assert '"delta": "highest."' in body
    assert "data: [DONE]" in body
