"""Business unit-related tools"""
import json
from typing import Optional

from fastmcp import Context

from ..server import mcp, api_client, init_api_client
from ._base import build_params


@mcp.tool()
async def list_business_units(ctx: Context, page_size: Optional[int] = None, include: Optional[str] = None, expand: Optional[str] = None) -> str:
    """List all business units"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    params = build_params({"page_size": page_size, "include": include, "expand": expand})
    result = api_client.list_business_units(params)
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_business_unit(ctx: Context, business_unit_id: int) -> str:
    """Get details of a specific business unit"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    result = api_client.get_business_unit(business_unit_id)
    return json.dumps(result, indent=2)

