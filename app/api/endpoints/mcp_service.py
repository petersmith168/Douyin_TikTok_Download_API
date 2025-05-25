from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

router = APIRouter()

_app: Optional[FastAPI] = None


def set_app(app: FastAPI) -> None:
    """Attach the FastAPI app instance for schema generation."""
    global _app
    _app = app


def _get_schema() -> dict:
    if _app is None:
        raise RuntimeError("FastAPI app not initialized")
    return get_openapi(
        title=_app.title,
        version=_app.version,
        description=_app.description,
        routes=_app.routes,
    )


@router.get("/schema", summary="获取MCP总文档/Get full MCP schema")
async def get_full_schema() -> dict:
    """Return the full OpenAPI schema used for MCP."""
    return _get_schema()


@router.get("/schema/{path:path}", summary="获取指定接口MCP文档/Get schema for specific API")
async def get_schema_by_path(path: str) -> dict:
    """Return schema details for a specific API path."""
    schema = _get_schema()
    full_path = "/" + path.lstrip("/")
    if full_path not in schema.get("paths", {}):
        raise HTTPException(status_code=404, detail="Interface not found")
    return schema["paths"][full_path]
