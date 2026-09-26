"""RFC 7807 (problem+json) error handling."""

from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

PROBLEM_JSON = "application/problem+json"


def _problem(status_code: int, title: str, detail: str, instance: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        media_type=PROBLEM_JSON,
        content={
            "type": "about:blank",
            "title": title,
            "status": status_code,
            "detail": detail,
            "instance": instance,
        },
    )


async def _http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return _problem(
        status_code=exc.status_code,
        title=str(exc.detail),
        detail=str(exc.detail),
        instance=str(request.url.path),
    )


async def _validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        media_type=PROBLEM_JSON,
        content={
            "type": "about:blank",
            "title": "Validation error",
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "detail": "Request validation failed.",
            "instance": str(request.url.path),
            "errors": jsonable_encoder(exc.errors()),
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(StarletteHTTPException, _http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(
        RequestValidationError, _validation_exception_handler  # type: ignore[arg-type]
    )
