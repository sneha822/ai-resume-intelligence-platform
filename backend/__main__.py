"""Run the API: ``python -m backend``.

On Windows, uvicorn's own ``run()`` force-selects the Proactor event loop, which
async psycopg cannot use. We instead set the SelectorEventLoop policy ourselves
and drive ``uvicorn.Server.serve()`` under our own loop. On Linux (Docker) the
compose/Dockerfile uvicorn command is used instead.
"""

from __future__ import annotations

import asyncio
import os
import sys

import uvicorn

from backend.main import app


async def _serve() -> None:
    config = uvicorn.Config(
        app,
        host=os.getenv("API_HOST", "127.0.0.1"),
        port=int(os.getenv("API_PORT", "8000")),
        log_level=os.getenv("API_LOG_LEVEL", "info"),
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(_serve())
