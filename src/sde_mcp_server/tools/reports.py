"""Advanced report tools"""
import json
from typing import Any, Dict, Optional

from fastmcp import Context

from ..server import mcp, api_client, init_api_client


@mcp.tool()
async def list_advanced_reports(ctx: Context) -> str:
    """List all advanced reports"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    result = api_client.list_advanced_reports()
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_advanced_report(ctx: Context, report_id: int) -> str:
    """Get details of a specific advanced report"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    result = api_client.get_advanced_report(report_id)
    return json.dumps(result, indent=2)


@mcp.tool()
async def run_advanced_report(ctx: Context, report_id: int, format: Optional[str] = None) -> str:
    """Run an advanced report"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    params = {}
    if format:
        params["format"] = format
    result = api_client.run_advanced_report(report_id, params)
    return json.dumps(result, indent=2)


@mcp.tool()
async def create_advanced_report(
    ctx: Context,
    title: str,
    chart: str,
    query: str,
    description: Optional[str] = None,
    chart_meta: Optional[Dict[str, Any]] = None,
    type: Optional[str] = None,
) -> str:
    """Create a new advanced report"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    data = {"title": title, "chart": chart, "query": query}
    if description:
        data["description"] = description
    if chart_meta:
        data["chart_meta"] = chart_meta
    if type:
        data["type"] = type
    result = api_client.create_advanced_report(data)
    return json.dumps(result, indent=2)


@mcp.tool()
async def execute_cube_query(ctx: Context, query: str) -> str:
    """Execute a cube query"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    result = api_client.execute_cube_query(query)
    return json.dumps(result, indent=2)

