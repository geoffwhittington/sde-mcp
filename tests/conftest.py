"""
Pytest configuration and fixtures for SD Elements MCP Server CSV tests
"""
import os
import sys
from pathlib import Path
import pytest
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


@pytest.fixture
def llm_api_key() -> Optional[str]:
    """Get OpenAI API key from environment for integration tests"""
    return os.getenv("OPENAI_API_KEY")


@pytest.fixture
def skip_if_no_llm(llm_api_key):
    """Skip test if no LLM API key is available"""
    if not llm_api_key:
        pytest.skip("No OpenAI API key found. Set OPENAI_API_KEY to run integration tests")

