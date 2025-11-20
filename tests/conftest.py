"""
Pytest configuration and fixtures for SD Elements MCP Server tests
"""
import os
import sys
from pathlib import Path
import pytest
from unittest.mock import Mock, AsyncMock, MagicMock
from typing import Optional

# Add src directory to Python path so tests can import sde_mcp_server
# This allows tests to be run from either project root or tests directory
_tests_dir = Path(__file__).parent
_project_root = _tests_dir.parent
_src_dir = _project_root / "src"
if str(_src_dir) not in sys.path:
    sys.path.insert(0, str(_src_dir))

# Load .env file if it exists (for OpenAI API key and other test config)
try:
    from dotenv import load_dotenv
    # Load from project root or tests directory
    env_paths = [
        _project_root / ".env",  # Project root
        _tests_dir / ".env",  # Tests directory
    ]
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            break
except ImportError:
    pass  # dotenv not available, skip

# Set test environment variables before importing server modules
os.environ.setdefault("SDE_HOST", "https://test.sdelements.com")
os.environ.setdefault("SDE_API_KEY", "test-api-key")


@pytest.fixture
def mock_api_client():
    """Create a mocked SD Elements API client"""
    client = Mock()
    
    # Mock common API responses
    client.list_projects.return_value = {
        "results": [
            {"id": 1, "name": "Test Project 1", "status": "active"},
            {"id": 2, "name": "Test Project 2", "status": "active"},
        ],
        "count": 2,
    }
    
    client.get_project.return_value = {
        "id": 1,
        "name": "Test Project",
        "status": "active",
        "description": "A test project",
    }
    
    client.list_applications.return_value = {
        "results": [
            {"id": 1, "name": "Test App", "business_unit": {"id": 1, "name": "Test BU"}},
        ],
        "count": 1,
    }
    
    client.list_profiles.return_value = {
        "results": [
            {"id": "profile1", "name": "Default Profile"},
        ],
        "count": 1,
    }
    
    client.test_connection.return_value = {"status": "ok", "message": "Connection successful"}
    
    return client


@pytest.fixture
def mock_context():
    """Create a mocked FastMCP Context"""
    ctx = AsyncMock()
    
    # Mock elicitation response
    elicitation_response = Mock()
    elicitation_response.action = "accept"
    elicitation_response.data = "test_value"
    
    ctx.elicit = AsyncMock(return_value=elicitation_response)
    
    return ctx


@pytest.fixture
def mock_context_cancel():
    """Create a mocked Context that cancels elicitation"""
    ctx = AsyncMock()
    
    elicitation_response = Mock()
    elicitation_response.action = "cancel"
    elicitation_response.data = None
    
    ctx.elicit = AsyncMock(return_value=elicitation_response)
    
    return ctx


@pytest.fixture(autouse=True)
def reset_api_client(monkeypatch):
    """Reset the global api_client before each test"""
    import sde_mcp_server.server
    monkeypatch.setattr(sde_mcp_server.server, "api_client", None)


@pytest.fixture
def llm_api_key() -> Optional[str]:
    """Get OpenAI API key from environment for integration tests"""
    return os.getenv("OPENAI_API_KEY")


@pytest.fixture
def skip_if_no_llm(llm_api_key):
    """Skip test if no LLM API key is available"""
    if not llm_api_key:
        pytest.skip("No OpenAI API key found. Set OPENAI_API_KEY to run integration tests")

