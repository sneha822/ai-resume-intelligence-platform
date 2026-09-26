"""OpenTelemetry setup.

Idempotent. Configures a tracer provider that exports via OTLP/HTTP (point
``OTEL_EXPORTER_OTLP_ENDPOINT`` at Phoenix, Jaeger, or any collector) and/or the
console. When ``otel_enabled`` is false the app uses OTel's no-op tracer, so
instrumented code paths stay zero-cost.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.trace import Tracer

from backend.core.config import settings

if TYPE_CHECKING:
    from fastapi import FastAPI

_configured = False


def setup_telemetry(app: FastAPI | None = None) -> None:
    global _configured

    if not settings.otel_enabled:
        return

    if not _configured:
        provider = TracerProvider(
            resource=Resource.create({SERVICE_NAME: settings.otel_service_name})
        )
        if settings.otel_exporter_otlp_endpoint:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                OTLPSpanExporter,
            )

            provider.add_span_processor(
                BatchSpanProcessor(
                    OTLPSpanExporter(endpoint=f"{settings.otel_exporter_otlp_endpoint}/v1/traces")
                )
            )
        if settings.otel_console_export:
            provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

        trace.set_tracer_provider(provider)
        _configured = True

    if app is not None:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        FastAPIInstrumentor.instrument_app(app)


def get_tracer(name: str) -> Tracer:
    """Return a tracer; a no-op tracer if telemetry is disabled."""
    return trace.get_tracer(name)
