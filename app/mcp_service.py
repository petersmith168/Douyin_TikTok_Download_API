from fastapi import APIRouter, Request

router = APIRouter(tags=["MCP"])

@router.get('/schema')
async def get_schema(request: Request):
    """Return the OpenAPI schema for MCP clients."""
    return request.app.openapi()

