"""Enterprise backend for the AI Resume Intelligence platform."""

from __future__ import annotations

import asyncio
import sys

# psycopg's async driver cannot run on Windows' default ProactorEventLoop.
# Select the SelectorEventLoop policy for every entry point (API, worker,
# alembic, scripts) that imports the backend package.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
