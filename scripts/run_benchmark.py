"""Run the role/resume retrieval benchmark and print a metrics table.

    python scripts/run_benchmark.py          # uses real fastembed embeddings

No LLM calls / no quota used — pure retrieval evaluation.
"""

from __future__ import annotations

import asyncio

from backend.adapters.embeddings.fastembed_embedder import FastEmbedEmbedder
from backend.eval.benchmark import evaluate_retrieval, load_benchmark


async def main() -> None:
    data = load_benchmark()
    n_pairs = len(data["labels"])
    print(
        f"Benchmark: {len(data['roles'])} roles, {len(data['resumes'])} resumes, "
        f"{n_pairs} labeled pairs (synthetic)\n"
    )
    results = await evaluate_retrieval(FastEmbedEmbedder())

    cols = ["recall@3", "recall@5", "precision@3", "MRR", "nDCG@5"]
    print(f"{'method':8}" + "".join(f"{c:>13}" for c in cols))
    for method in ("dense", "sparse", "hybrid"):
        row = results[method]
        print(f"{method:8}" + "".join(f"{row[c]:>13.2f}" for c in cols))


if __name__ == "__main__":
    asyncio.run(main())
