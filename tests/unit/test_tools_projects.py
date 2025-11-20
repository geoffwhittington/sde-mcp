"""
Unit tests for project-related tools
"""
import json
import pytest
from unittest.mock import patch, AsyncMock

from sde_mcp_server.tools.projects import (
    list_projects,
    get_project,
    create_project,
    update_project,
    delete_project,
)


@pytest.mark.asyncio
async def test_list_projects(mock_api_client, mock_context):
    """Test list_projects tool"""
    with patch("sde_mcp_server.tools.projects.api_client", mock_api_client):
        result = await list_projects(mock_context)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "results" in data
        assert len(data["results"]) == 2
        mock_api_client.list_projects.assert_called_once()


@pytest.mark.asyncio
async def test_get_project(mock_api_client, mock_context):
    """Test get_project tool"""
    with patch("sde_mcp_server.tools.projects.api_client", mock_api_client):
        result = await get_project(mock_context, project_id=1)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert data["id"] == 1
        assert data["name"] == "Test Project"
        mock_api_client.get_project.assert_called_once_with(1, {})


@pytest.mark.asyncio
async def test_create_project(mock_api_client, mock_context):
    """Test create_project tool"""
    mock_api_client.list_profiles.return_value = {
        "results": [{"id": "profile1", "name": "Default"}],
        "count": 1,
    }
    
    with patch("sde_mcp_server.tools.projects.api_client", mock_api_client):
        result = await create_project(
            mock_context,
            name="New Project",
            application_id=1,
            description="Test description"
        )
        
        assert isinstance(result, str)
        data = json.loads(result)
        # Verify project creation was attempted
        mock_api_client.create_project.assert_called()


@pytest.mark.asyncio
async def test_update_project(mock_api_client, mock_context):
    """Test update_project tool"""
    with patch("sde_mcp_server.tools.projects.api_client", mock_api_client):
        result = await update_project(
            mock_context,
            project_id=1,
            name="Updated Name",
            description="Updated description"
        )
        
        assert isinstance(result, str)
        mock_api_client.update_project.assert_called_once()


@pytest.mark.asyncio
async def test_delete_project(mock_api_client, mock_context):
    """Test delete_project tool"""
    with patch("sde_mcp_server.tools.projects.api_client", mock_api_client):
        result = await delete_project(mock_context, project_id=1)
        
        assert isinstance(result, str)
        mock_api_client.delete_project.assert_called_once_with(1)

