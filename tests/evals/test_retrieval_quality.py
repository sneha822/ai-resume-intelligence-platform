"""Retrieval-quality drift gate.

Runs the real RetrievalService (dense + BM25 + RRF) over a golden dataset and
asserts recall/MRR stay above thresholds. The default run uses a deterministic
lexical embedder (no model download, CI-safe). Set RUN_MODEL_EVALS=1 to also run
the same gate with real fastembed embeddings.
"""

from __future__ import annotations

import os
import re

import pytest

from backend.adapters.retrieval.bm25 import Bm25Retriever
from backend.eval.metrics import mean_reciprocal_rank, recall_at_k
from backend.services.retrieval_service import RetrievalService
from tests.evals.datasets import GOLDEN_CORPUS, GOLDEN_QUERIES
from tests.evals.inmem import InMemoryVectorStore

_TOKEN = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


class LexicalEmbedder:
    """Deterministic bag-of-words embedder over a fixed vocabulary."""

    def __init__(self, vocab: list[str]) -> None:
        self._vocab = vocab
        self._index = {term: i for i, term in enumerate(vocab)}

    @property
    def dimension(self) -> int:
        return len(self._vocab)

    def _vec(self, text: str) -> list[float]:
        vec = [0.0] * len(self._vocab)
        for tok in _tokenize(text):
            if tok in self._index:
                vec[self._index[tok]] += 1.0
        return vec

    async def embed(self, text: str) -> list[float]:
        return self._vec(text)

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self._vec(t) for t in texts]


async def _run_gate(embedder: object, *, min_recall: float, min_mrr: float) -> None:
    corpus_vectors = {
        cid: await embedder.embed_batch([text])  # type: ignore[attr-defined]
        for cid, text in GOLDEN_CORPUS.items()
    }
    store = InMemoryVectorStore({cid: v[0] for cid, v in corpus_vectors.items()})
    sparse = Bm25Retriever(GOLDEN_CORPUS)
    service = RetrievalService(embedder, store, sparse)  # type: ignore[arg-type]

    cases = []
    recalls = []
    for query, relevant in GOLDEN_QUERIES:
        results = await service.search(query, k=3)
        ranked = [r.candidate_id for r in results]
        recalls.append(recall_at_k(ranked, relevant, k=2))
        cases.append((ranked, relevant))

    mean_recall = sum(recalls) / len(recalls)
    mrr = mean_reciprocal_rank(cases)
    assert mean_recall >= min_recall, f"recall@2 {mean_recall:.3f} < {min_recall}"
    assert mrr >= min_mrr, f"MRR {mrr:.3f} < {min_mrr}"


async def test_retrieval_gate_lexical() -> None:
    vocab = sorted({tok for text in GOLDEN_CORPUS.values() for tok in _tokenize(text)})
    await _run_gate(LexicalEmbedder(vocab), min_recall=0.75, min_mrr=0.9)


@pytest.mark.skipif(
    os.getenv("RUN_MODEL_EVALS") != "1",
    reason="Set RUN_MODEL_EVALS=1 to run the gate with real fastembed embeddings.",
)
async def test_retrieval_gate_fastembed() -> None:
    from backend.adapters.embeddings.fastembed_embedder import FastEmbedEmbedder

    await _run_gate(FastEmbedEmbedder(), min_recall=0.75, min_mrr=0.9)
