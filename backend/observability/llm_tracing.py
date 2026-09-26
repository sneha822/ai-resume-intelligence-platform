"""LLM span helpers: token usage, cost estimation, and latency attributes.

Follows the OpenTelemetry GenAI semantic-convention attribute names where they
exist (``gen_ai.*``).
"""

from __future__ import annotations

from opentelemetry.trace import Span

# Approximate list price in USD per 1M tokens: (input, output). Update as needed.
_PRICING: dict[str, tuple[float, float]] = {
    "claude-opus": (15.0, 75.0),
    "claude-sonnet": (3.0, 15.0),
    "claude-haiku": (0.80, 4.0),
}


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    key = next((k for k in _PRICING if k in model.lower()), None)
    if key is None:
        return 0.0
    price_in, price_out = _PRICING[key]
    return input_tokens / 1_000_000 * price_in + output_tokens / 1_000_000 * price_out


def set_llm_span_attributes(
    span: Span,
    *,
    model: str,
    input_tokens: int,
    output_tokens: int,
    latency_seconds: float,
    system: str = "anthropic",
) -> None:
    span.set_attribute("gen_ai.system", system)
    span.set_attribute("gen_ai.request.model", model)
    span.set_attribute("gen_ai.usage.input_tokens", input_tokens)
    span.set_attribute("gen_ai.usage.output_tokens", output_tokens)
    span.set_attribute("gen_ai.usage.total_tokens", input_tokens + output_tokens)
    span.set_attribute("gen_ai.usage.cost_usd", estimate_cost(model, input_tokens, output_tokens))
    span.set_attribute("gen_ai.latency_seconds", latency_seconds)
