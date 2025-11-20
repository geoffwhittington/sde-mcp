"""Countermeasure-related tools"""
import json
from typing import Optional

from fastmcp import Context

from ..server import mcp, api_client, init_api_client


@mcp.tool()
async def list_countermeasures(ctx: Context, project_id: int, status: Optional[str] = None, page_size: Optional[int] = None, risk_relevant: bool = True) -> str:
    """List all countermeasures for a project. Use this to see countermeasures associated with a project, not get_project which returns project details."""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    params = {}
    if status:
        params["status"] = status
    if page_size:
        params["page_size"] = page_size
    params["risk_relevant"] = str(risk_relevant).lower()
    result = api_client.list_countermeasures(project_id, params)
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_countermeasure(ctx: Context, project_id: int, countermeasure_id: str) -> str:
    """Get details of a specific countermeasure"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    if not countermeasure_id.startswith(f"{project_id}-"):
        countermeasure_id = f"{project_id}-{countermeasure_id}"
    result = api_client.get_countermeasure(project_id, countermeasure_id)
    return json.dumps(result, indent=2)


@mcp.tool()
async def update_countermeasure(ctx: Context, project_id: int, countermeasure_id: str, status: Optional[str] = None, notes: Optional[str] = None) -> str:
    """Update a countermeasure (status or notes). Use when user says 'update status', 'mark as complete', or 'change status'. Do NOT use for 'add note', 'document', or 'note' - use add_countermeasure_note instead."""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    if not countermeasure_id.startswith(f"{project_id}-"):
        countermeasure_id = f"{project_id}-{countermeasure_id}"
    data = {}
    if status:
        data["status"] = status
    if notes:
        data["status_note"] = notes
    result = api_client.update_countermeasure(project_id, countermeasure_id, data)
    return json.dumps(result, indent=2)


@mcp.tool()
async def add_countermeasure_note(ctx: Context, project_id: int, countermeasure_id: str, note: str) -> str:
    """Add a note to a countermeasure. Use when user says 'add note', 'document', 'note that', 'record that', or wants to add documentation. Use update_countermeasure if user wants to change status."""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    if not countermeasure_id.startswith(f"{project_id}-"):
        countermeasure_id = f"{project_id}-{countermeasure_id}"
    result = api_client.add_task_note(project_id, countermeasure_id, note)
    return json.dumps(result, indent=2)

