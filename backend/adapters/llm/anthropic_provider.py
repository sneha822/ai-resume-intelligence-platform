"""Anthropic (Claude) LLM provider with Instructor-enforced structured output."""

from __future__ import annotations

import time
from typing import TypeVar

import instructor
from anthropic import AsyncAnthropic
from anthropic.types import TextBlock
from opentelemetry.trace import Span
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential

from backend.core.config import settings
from backend.observability.llm_tracing import set_llm_span_attributes
from backend.observability.telemetry import get_tracer

T = TypeVar("T", bound=BaseModel)

_TRACER = get_tracer("backend.adapters.llm.anthropic")

_RETRY = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=20),
    reraise=True,
)


class AnthropicProvider:
    """Implements the ``LLMProvider`` port using Claude.

    ``structured`` routes through Instructor, which validates the model's output
    against the Pydantic ``response_model`` and retries on schema failure. Each
    call emits a span with model, token usage, estimated cost, and latency.
    """

    def __init__(self, model: str | None = None, api_key: str | None = None) -> None:
        self._raw = AsyncAnthropic(api_key=api_key or settings.anthropic_api_key)
        self._instructor = instructor.from_anthropic(self._raw)
        self._model = model or settings.llm_model
        self._max_tokens = 4096

    def _record(self, span: Span, usage: object, started: float) -> None:
        set_llm_span_attributes(
            span,
            model=self._model,
            input_tokens=int(getattr(usage, "input_tokens", 0) or 0),
            output_tokens=int(getattr(usage, "output_tokens", 0) or 0),
            latency_seconds=time.perf_counter() - started,
        )

    @_RETRY
    async def generate(self, prompt: str, system: str | None = None) -> str:
        with _TRACER.start_as_current_span("llm.generate") as span:
            started = time.perf_counter()
            message = await self._raw.messages.create(
                model=self._model,
                max_tokens=self._max_tokens,
                system=system or "",
                messages=[{"role": "user", "content": prompt}],
            )
            self._record(span, message.usage, started)
            return "".join(b.text for b in message.content if isinstance(b, TextBlock))

    @_RETRY
    async def structured(
        self, prompt: str, response_model: type[T], system: str | None = None
    ) -> T:
        with _TRACER.start_as_current_span("llm.structured") as span:
            started = time.perf_counter()
            raw, completion = await self._instructor.messages.create_with_completion(
                model=self._model,
                max_tokens=self._max_tokens,
                system=system or "You are a precise assistant that returns valid data.",
                messages=[{"role": "user", "content": prompt}],
                response_model=response_model,
            )
            result: T = raw
            self._record(span, getattr(completion, "usage", None), started)
            return result
