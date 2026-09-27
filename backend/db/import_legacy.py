"""One-shot importer: legacy SQLite candidate rows -> Postgres candidates.

The old schema is ``candidates(id, email, phone, skills)`` in
``legacy/data/candidate_database.db``. Skills are folded into the new JSONB
``profile``.

Run with the Postgres stack up and migrations applied::

    python -m backend.db.import_legacy --sqlite legacy/data/candidate_database.db
"""

from __future__ import annotations

import argparse
import asyncio
import sqlite3
from pathlib import Path

from backend.db.base import async_session_factory
from backend.db.repositories import CandidateRepository


def _read_legacy_rows(sqlite_path: Path) -> list[dict[str, str]]:
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute("SELECT email, phone, skills FROM candidates")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def _split_skills(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [s.strip() for s in raw.replace(";", ",").split(",") if s.strip()]


async def import_candidates(sqlite_path: Path) -> int:
    rows = _read_legacy_rows(sqlite_path)
    imported = 0
    async with async_session_factory() as session:
        repo = CandidateRepository(session)
        for row in rows:
            await repo.upsert_by_email(
                email=row.get("email") or None,
                phone=row.get("phone") or None,
                profile={"skills": _split_skills(row.get("skills"))},
            )
            imported += 1
        await session.commit()
    return imported


def main() -> None:
    parser = argparse.ArgumentParser(description="Import legacy SQLite candidates.")
    parser.add_argument(
        "--sqlite",
        default="legacy/data/candidate_database.db",
        help="Path to the legacy SQLite database.",
    )
    args = parser.parse_args()

    path = Path(args.sqlite)
    if not path.exists():
        raise SystemExit(f"SQLite database not found: {path}")

    count = asyncio.run(import_candidates(path))
    print(f"Imported {count} candidate(s) from {path}")


if __name__ == "__main__":
    main()
