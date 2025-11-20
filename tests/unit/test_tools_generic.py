"""
Unit tests for generic/utility tools
"""
import json
import pytest
from unittest.mock import patch

from sde_mcp_server.tools.generic import test_connection


@pytest.mark.asyncio
async def test_test_connection(mock_api_client, mock_context):
    """Test test_connection tool"""
    with patch("sde_mcp_server.tools.generic.api_client", mock_api_client):
        result = await test_connection(mock_context)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert data["status"] == "ok"
        mock_api_client.test_connection.assert_called_once()

