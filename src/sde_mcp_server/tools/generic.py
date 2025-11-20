"""Generic API and utility tools"""
import json
from typing import Any, Dict, Optional

from fastmcp import Context

from ..server import mcp, api_client, init_api_client


@mcp.tool()
async def api_request(ctx: Context, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> str:
    """Make a generic API request to a custom endpoint. Use when user says 'make a GET/POST/PUT/DELETE request', 'call API endpoint', or 'custom API call'. Do NOT use for specific operations - use dedicated tools like get_project instead."""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    result = api_client.api_request(method, endpoint, params, data)
    return json.dumps(result, indent=2)


@mcp.tool()
async def test_connection(ctx: Context) -> str:
    """Test the connection to SD Elements API. Use this to verify API connectivity and credentials, not for making API calls."""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    success = api_client.test_connection()
    result = {
        "connection_successful": success,
        "host": api_client.host,
        "message": "Connection successful" if success else "Connection failed"
    }
    return json.dumps(result, indent=2)

