"""Golden retrieval dataset for the evaluation gate.

A small, hand-labeled corpus + queries with known-relevant candidate ids. Used
to assert retrieval quality does not regress (drift gate).
"""

from __future__ import annotations

GOLDEN_CORPUS: dict[str, str] = {
    "ml1": "Machine learning engineer specializing in NLP, transformers, and RAG "
    "pipelines with PyTorch and Hugging Face.",
    "ml2": "Data scientist with deep experience in natural language processing, "
    "text classification, and large language model fine-tuning.",
    "be1": "Backend software engineer building Java Spring Boot microservices and "
    "REST APIs with PostgreSQL.",
    "fe1": "Frontend developer focused on React, TypeScript, and accessible design "
    "systems for web applications.",
    "de1": "DevOps engineer managing Kubernetes clusters, Terraform infrastructure, "
    "and CI/CD pipelines on AWS.",
    "pm1": "Product manager leading roadmap planning, stakeholder alignment, and "
    "agile delivery for SaaS products.",
}

# (query, set of relevant candidate ids)
GOLDEN_QUERIES: list[tuple[str, set[str]]] = [
    ("nlp machine learning engineer with transformers", {"ml1", "ml2"}),
    ("java spring boot backend microservices", {"be1"}),
    ("react typescript frontend developer", {"fe1"}),
    ("kubernetes terraform aws devops", {"de1"}),
]
