"""SQLAlchemy 2.0 ORM models.

Tables cover user management, job postings, the candidate pool, parsed resumes
(with a pgvector embedding column), evaluation results, and an execution audit
trail.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.config import settings
from backend.db.base import Base


def _uuid() -> uuid.UUID:
    return uuid.uuid4()


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=_uuid)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32), default="recruiter")

    jobs: Mapped[list[Job]] = relationship(back_populates="created_by")


class Job(TimestampMixin, Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=_uuid)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text)
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )

    created_by: Mapped[User | None] = relationship(back_populates="jobs")
    evaluations: Mapped[list[Evaluation]] = relationship(back_populates="job")


class Candidate(TimestampMixin, Base):
    __tablename__ = "candidates"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=_uuid)
    email: Mapped[str | None] = mapped_column(String(320), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(64))
    profile: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)

    resumes: Mapped[list[Resume]] = relationship(
        back_populates="candidate", cascade="all, delete-orphan"
    )
    evaluations: Mapped[list[Evaluation]] = relationship(back_populates="candidate")


class Resume(TimestampMixin, Base):
    __tablename__ = "resumes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=_uuid)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"), index=True
    )
    filename: Mapped[str] = mapped_column(String(512))
    content_text: Mapped[str] = mapped_column(Text)
    # Dense embedding for hybrid retrieval; dim comes from the embedding model.
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(settings.embedding_dim), nullable=True
    )

    candidate: Mapped[Candidate] = relationship(back_populates="resumes")


class Evaluation(TimestampMixin, Base):
    __tablename__ = "evaluations"
    __table_args__ = (UniqueConstraint("candidate_id", "job_id", name="candidate_job"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=_uuid)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"), index=True
    )
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), index=True)
    overall_score: Mapped[float] = mapped_column(Float)
    fit_level: Mapped[str] = mapped_column(String(32))
    result: Mapped[dict[str, Any]] = mapped_column(JSONB)

    candidate: Mapped[Candidate] = relationship(back_populates="evaluations")
    job: Mapped[Job] = relationship(back_populates="evaluations")


class AuditLog(TimestampMixin, Base):
    __tablename__ = "audit_log"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=_uuid)
    action: Mapped[str] = mapped_column(String(128), index=True)
    entity_type: Mapped[str] = mapped_column(String(64))
    entity_id: Mapped[str | None] = mapped_column(String(64))
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
