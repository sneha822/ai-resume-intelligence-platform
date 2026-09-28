"""Seed the database with demo data for a populated live demo.

Inserts one job, a few candidates (with real embeddings so search works), and
pre-computed evaluations (crafted, schema-valid — no LLM calls, no quota used) so
the UI shows competency radars and scorecards immediately.

Idempotent: re-running replaces the seed candidates (matched by email).

    python -m backend.db.seed
"""

from __future__ import annotations

import asyncio

from sqlalchemy import delete, select

from backend.adapters.embeddings.factory import get_embedder
from backend.core.schemas.evaluation import (
    EvaluationResult,
    FitLevel,
    GapAnalysis,
    RubricScore,
)
from backend.db.base import async_session_factory
from backend.db.models import Candidate, Evaluation, Job, Resume

JOB_TITLE = "Senior Machine Learning Engineer"
JOB_DESCRIPTION = (
    "Build production RAG and NLP systems. Requirements: Python, transformers, "
    "vector search, LLM fine-tuning, and strong software engineering."
)

_RUBRIC_CRITERIA = [
    "Technical Proficiency",
    "Domain Alignment",
    "Experience Depth",
    "Leadership Signal",
]


def _evaluation(scores: list[float], fit: FitLevel, summary: str) -> EvaluationResult:
    overall = round(sum(scores) / len(scores) * 10, 1)
    return EvaluationResult(
        candidate_id="seed",
        job_id="seed",
        overall_score=overall,
        fit_level=fit,
        rubric=[
            RubricScore(
                criterion=c,
                score=s,
                reasoning=f"{c}: evidence found in the resume supports a score of {s}/10.",
                evidence=["See resume experience and skills sections."],
            )
            for c, s in zip(_RUBRIC_CRITERIA, scores, strict=True)
        ],
        strengths=["Relevant hands-on experience", "Clear technical depth"],
        gaps=GapAnalysis(
            missing_skills=[] if overall >= 70 else ["production LLM deployment"],
            experience_gaps=[] if overall >= 70 else ["limited large-scale systems work"],
            recommendation=(
                "Advance to interview" if overall >= 70 else "Consider with reservations"
            ),
        ),
        summary=summary,
    )


# (name, email, phone, profile, resume_text, scores, fit, summary)
SEED = [
    (
        "Aisha Khan",
        "aisha.khan.ml@example.com",
        "+1-555-0101",
        {
            "current_title": "Machine Learning Engineer",
            "location": "Bengaluru",
            "skills": ["Python", "PyTorch", "Transformers", "RAG", "NLP", "vector search"],
        },
        "Machine Learning Engineer with 5 years building NLP and RAG systems using "
        "Python, PyTorch, transformers, and vector databases. Fine-tuned LLMs and shipped "
        "semantic search to production.",
        [9.0, 9.0, 8.0, 7.0],
        FitLevel.STRONG,
        "Strong fit: deep NLP/RAG experience directly matching the role.",
    ),
    (
        "Diego Torres",
        "diego.torres.ds@example.com",
        "+1-555-0102",
        {
            "current_title": "Data Scientist",
            "location": "Madrid",
            "skills": ["Python", "scikit-learn", "pandas", "SQL", "NLP", "statistics"],
        },
        "Data Scientist with 4 years in predictive modeling and NLP text classification "
        "using Python, scikit-learn, and pandas. Some experience with transformers.",
        [7.0, 7.0, 6.0, 6.0],
        FitLevel.MODERATE,
        "Moderate fit: solid DS foundation, lighter on production LLM/RAG.",
    ),
    (
        "Sam Patel",
        "sam.patel.swe@example.com",
        "+1-555-0103",
        {
            "current_title": "Backend Software Engineer",
            "location": "Toronto",
            "skills": ["Java", "Spring Boot", "PostgreSQL", "Microservices", "REST"],
        },
        "Backend Software Engineer with 6 years building Java Spring Boot microservices "
        "and REST APIs on PostgreSQL. Limited machine learning exposure.",
        [5.0, 3.0, 6.0, 6.0],
        FitLevel.WEAK,
        "Weak fit for an ML role: strong engineer but little ML/NLP background.",
    ),
]


async def seed() -> None:
    embedder = get_embedder()
    emails = [row[1] for row in SEED]

    async with async_session_factory() as session:
        # Idempotency: remove any previous seed candidates (cascades resumes/evals).
        await session.execute(delete(Candidate).where(Candidate.email.in_(emails)))

        # Get-or-create the job.
        job = (
            await session.execute(select(Job).where(Job.title == JOB_TITLE))
        ).scalar_one_or_none()
        if job is None:
            job = Job(title=JOB_TITLE, description=JOB_DESCRIPTION)
            session.add(job)
            await session.flush()

        for name, email, phone, profile, resume_text, scores, fit, summary in SEED:
            candidate = Candidate(name=name, email=email, phone=phone, profile=profile)
            session.add(candidate)
            await session.flush()

            embedding = await embedder.embed(resume_text)
            session.add(
                Resume(
                    candidate_id=candidate.id,
                    filename=f"{name.split()[0].lower()}_resume.pdf",
                    content_text=resume_text,
                    embedding=embedding,
                )
            )
            result = _evaluation(scores, fit, summary)
            session.add(
                Evaluation(
                    candidate_id=candidate.id,
                    job_id=job.id,
                    overall_score=result.overall_score,
                    fit_level=result.fit_level.value,
                    result=result.model_dump(mode="json"),
                )
            )

        await session.commit()
    print(f"Seeded 1 job + {len(SEED)} candidates with resumes and evaluations.")


if __name__ == "__main__":
    asyncio.run(seed())
