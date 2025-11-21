"""Application-related tools"""
import json
from typing import Optional

from fastmcp import Context

from ..server import mcp, api_client, init_api_client
from ._base import build_params


@mcp.tool()
async def list_applications(ctx: Context, page_size: Optional[int] = None, include: Optional[str] = None, expand: Optional[str] = None) -> str:
    """List all applications"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    params = build_params({"page_size": page_size, "include": include, "expand": expand})
    result = api_client.list_applications(params)
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_application(ctx: Context, application_id: int, page_size: Optional[int] = None, include: Optional[str] = None, expand: Optional[str] = None) -> str:
    """Get details of a specific application"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    params = build_params({"page_size": page_size, "include": include, "expand": expand})
    result = api_client.get_application(application_id, params)
    return json.dumps(result, indent=2)


@mcp.tool()
async def create_application(ctx: Context, name: str, business_unit_id: int, description: Optional[str] = None) -> str:
    """Create a new application"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    data = {"name": name, "business_unit": business_unit_id}
    if description:
        data["description"] = description
    result = api_client.create_application(data)
    return json.dumps(result, indent=2)


@mcp.tool()
async def update_application(ctx: Context, application_id: int, name: Optional[str] = None, description: Optional[str] = None) -> str:
    """Update an existing application"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    data = {}
    if name:
        data["name"] = name
    if description:
        data["description"] = description
    result = api_client.update_application(application_id, data)
    return json.dumps(result, indent=2)

