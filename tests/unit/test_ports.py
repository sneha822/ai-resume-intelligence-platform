"""Ports are importable and are runtime-checkable Protocols."""

from __future__ import annotations

from backend.core.ports import DocumentParser, Embedder, LLMProvider, VectorStore


def test_ports_are_protocols() -> None:
    for port in (LLMProvider, Embedder, VectorStore, DocumentParser):
        # runtime_checkable Protocols expose _is_runtime_protocol
        assert getattr(port, "_is_runtime_protocol", False) is True
