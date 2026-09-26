"""Anthropic (Claude) LLM provider with Instructor-enforced structured output."""

from __future__ import annotations

from typing import TypeVar

import instructor
from anthropic import AsyncAnthropic
from anthropic.types import TextBlock
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential

from backend.core.config import settings

T = TypeVar("T", bound=BaseModel)

_RETRY = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=20),
    reraise=True,
)


class AnthropicProvider:
    """Implements the ``LLMProvider`` port using Claude.

    ``structured`` routes through Instructor, which validates the model's output
    against the Pydantic ``response_model`` and retries on schema failure.
    """

    def __init__(self, model: str | None = None, api_key: str | None = None) -> None:
        self._raw = AsyncAnthropic(api_key=api_key or settings.anthropic_api_key)
        self._instructor = instructor.from_anthropic(self._raw)
        self._model = model or settings.llm_model
        self._max_tokens = 4096

    @_RETRY
    async def generate(self, prompt: str, system: str | None = None) -> str:
        message = await self._raw.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            system=system or "",
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in message.content if isinstance(b, TextBlock))

    @_RETRY
    async def structured(
        self, prompt: str, response_model: type[T], system: str | None = None
    ) -> T:
        result: T = await self._instructor.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            system=system or "You are a precise assistant that returns valid data.",
            messages=[{"role": "user", "content": prompt}],
            response_model=response_model,
        )
        return result
