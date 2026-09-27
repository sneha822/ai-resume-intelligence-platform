"""Cost estimation and LLM span attribute tests (isolated in-memory tracer)."""

from __future__ import annotations

import pytest
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)

from backend.observability.llm_tracing import estimate_cost, set_llm_span_attributes


def test_estimate_cost_known_model() -> None:
    # sonnet: $3/1M in, $15/1M out
    cost = estimate_cost("claude-sonnet-5", 1_000_000, 1_000_000)
    assert cost == pytest.approx(18.0)


def test_estimate_cost_unknown_model_is_zero() -> None:
    assert estimate_cost("some-other-llm", 1000, 1000) == 0.0


def test_span_attributes_are_recorded() -> None:
    provider = TracerProvider()
    exporter = InMemorySpanExporter()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("test")

    with tracer.start_as_current_span("llm.call") as span:
        set_llm_span_attributes(
            span,
            model="claude-sonnet-5",
            input_tokens=1000,
            output_tokens=500,
            latency_seconds=0.42,
        )

    (finished,) = exporter.get_finished_spans()
    attrs = finished.attributes
    assert attrs is not None
    assert attrs["gen_ai.request.model"] == "claude-sonnet-5"
    assert attrs["gen_ai.usage.total_tokens"] == 1500
    assert attrs["gen_ai.usage.cost_usd"] == pytest.approx(
        1000 / 1_000_000 * 3 + 500 / 1_000_000 * 15
    )
    assert attrs["gen_ai.latency_seconds"] == pytest.approx(0.42)
