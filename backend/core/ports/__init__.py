"""Abstract interfaces (ports) that the domain depends on.

Concrete implementations live in ``backend/adapters`` and are injected at the
edges, keeping ``core`` and ``services`` free of vendor-specific code.
"""

from backend.core.ports.embedder import Embedder
from backend.core.ports.llm import LLMProvider
from backend.core.ports.parser import DocumentParser
from backend.core.ports.vector_store import ScoredMatch, VectorStore

__all__ = [
    "DocumentParser",
    "Embedder",
    "LLMProvider",
    "ScoredMatch",
    "VectorStore",
]
