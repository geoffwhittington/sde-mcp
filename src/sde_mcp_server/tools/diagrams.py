"""Diagram-related tools"""
import json
from typing import Any, Dict, Optional

from fastmcp import Context

from ..server import mcp, api_client, init_api_client


@mcp.tool()
async def list_project_diagrams(ctx: Context, project_id: int) -> str:
    """List diagrams for a project"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    result = api_client.list_project_diagrams(project_id)
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_diagram(ctx: Context, diagram_id: int) -> str:
    """Get details of a specific diagram"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    result = api_client.get_project_diagram(diagram_id)
    return json.dumps(result, indent=2)


@mcp.tool()
async def create_diagram(ctx: Context, project_id: int, name: str, diagram_data: Optional[Dict[str, Any]] = None) -> str:
    """Create a new diagram"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    data = {"project": project_id, "name": name}
    if diagram_data:
        data["diagram_data"] = diagram_data
    result = api_client.create_project_diagram(data)
    return json.dumps(result, indent=2)


@mcp.tool()
async def update_diagram(ctx: Context, diagram_id: int, name: Optional[str] = None, diagram_data: Optional[Dict[str, Any]] = None) -> str:
    """Update a diagram"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    data = {}
    if name:
        data["name"] = name
    if diagram_data:
        data["diagram_data"] = diagram_data
    result = api_client.update_project_diagram(diagram_id, data)
    return json.dumps(result, indent=2)


@mcp.tool()
async def delete_diagram(ctx: Context, diagram_id: int) -> str:
    """Delete a diagram"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    result = api_client.delete_project_diagram(diagram_id)
    return json.dumps(result, indent=2)

