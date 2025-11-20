# Testing Guide for SD Elements MCP Server

This directory contains CSV-driven integration tests that verify prompts trigger the correct tools using a real LLM.

**Important**: Test dependencies (including OpenAI library) are **NOT** required to run the MCP server. They are only needed for running tests. See [Installation](#installation) below.

## Test Structure

```
tests/
├── conftest.py                         # Shared fixtures and configuration
├── prompts_tool_mapping.csv            # CSV file for managing prompt-to-tool mappings
├── test_prompt_mapping_from_csv.py    # CSV-driven prompt-to-tool tests
├── validate_csv.py                     # CSV validation utility
├── show_tested_tools.py                # Tool coverage analysis utility
├── README_PROMPT_MAPPING.md            # Guide for managing the CSV file
└── README.md                           # This file
```

## Installation

### For Local Development/Testing

**You must install the project first, then add test dependencies:**

```bash
# 1. Install the project (includes main dependencies: fastmcp, python-dotenv, etc.)
pip install -e .

# 2. Install test dependencies on top
pip install -e ".[test-all]"  # Includes pytest and OpenAI for CSV-driven tests
```

**Or use uv (recommended):**
```bash
uv sync --all-extras
```

### For Production/Server Only

**Server only (no tests):**
```bash
pip install sde-mcp-server
```

**With tests (from PyPI):**
```bash
pip install sde-mcp-server[test-all]   # Includes pytest and OpenAI for CSV-driven tests
```

**Setup for CSV-driven prompt tests:**
1. Copy `tests/.env.example` to `.env` (in project root or tests directory)
2. Add your OpenAI API key: `OPENAI_API_KEY=your-key-here`
3. Run tests from project root: `pytest tests/test_prompt_mapping_from_csv.py -m 'integration and not unit' -v`

See `README_INSTALLATION.md` for details.

## Running Tests

**IMPORTANT:** 
- **Always run tests from the project root directory** (not from `tests/`)
- The project must be installed first (see [Installation](#installation) above)
- Test dependencies are isolated - they're in optional dependencies (`[test]`, `[integration]`), so they don't pollute the server installation. The server only installs 5 core dependencies.

### Running CSV-Driven Prompt Tests

```bash
# Make sure you're in the project root directory
cd /path/to/sde-mcp

# Run CSV-driven prompt-to-tool tests
pytest tests/test_prompt_mapping_from_csv.py -m 'integration and not unit' -v
```

**Note:** Tests are marked as `@pytest.mark.integration`, so you need `-m 'integration and not unit'` to run them.

**Why from root?** 
- Tests import `sde_mcp_server` which needs to be installed/importable
- Pytest configuration in `pyproject.toml` sets `pythonpath = ["src"]` 
- This ensures tests can find the server package

### CSV-Driven Prompt Tests

CSV-driven prompt tests require an OpenAI API key. They test that prompts actually trigger the correct tools using a real LLM.

**Setup:**

1. Install integration test dependencies (see [Installation](#installation) above)

2. Set OpenAI API key (via .env file or environment variable):
   ```bash
   # Option 1: .env file (recommended)
   # Copy tests/.env.example to .env and add your key
   cp tests/.env.example .env
   # Edit .env and set: OPENAI_API_KEY=your-key-here
   
   # Option 2: Environment variable
   export OPENAI_API_KEY="your-key-here"
   ```

3. Run integration tests with pytest:
   ```bash
   pytest -m 'integration and not unit'  # Run CSV-driven prompt tests
   # or
   pytest tests/test_prompt_mapping_from_csv.py -v
   ```

### Run All Tests

```bash
pytest -m ""
```

### Run Specific Test File

```bash
pytest tests/test_prompt_mapping_from_csv.py -m 'integration and not unit' -v
```

## Test Types

### CSV-Driven Prompt Tests

CSV-driven prompt tests use a real LLM to verify:
- Prompts trigger the correct tools
- Tool descriptions are clear enough for LLMs
- The actual user experience works as expected

**How it works:**
- Test cases are managed in `prompts_tool_mapping.csv`
- Tests automatically run for each CSV row
- Easy to add/modify test cases without code changes
- See `README_PROMPT_MAPPING.md` for details on managing the CSV

**Example CSV row:**
```csv
prompt,expected_tools,category,description,priority,persona
Show me all the projects in SD Elements,list_projects,projects,User wants to see all projects,high,generic
```

Each row becomes a test case that verifies the prompt triggers the expected tool(s).

## Adding New Test Cases

To add a new prompt test case, simply add a row to `prompts_tool_mapping.csv`:

```csv
prompt,expected_tools,category,description,priority,persona
Your new prompt here,tool_name,category,Description,medium,generic
```

Then run the tests:
```bash
pytest tests/test_prompt_mapping_from_csv.py -m 'integration and not unit' -v
```

See `README_PROMPT_MAPPING.md` for detailed instructions on managing the CSV file.

## Continuous Integration

In CI/CD:
- Run CSV-driven tests: `pytest tests/test_prompt_mapping_from_csv.py -m 'integration and not unit' -v`
- Requires `OPENAI_API_KEY` to be set in CI secrets
- Tests may be flaky due to LLM variability

## Troubleshooting

**Tests fail with "No OpenAI client available":**
- Install `openai` package: `pip install openai`
- Set `OPENAI_API_KEY` environment variable

**Integration tests are flaky:**
- LLM responses can vary - assertions should check for tool mentions, not exact text
- Consider using more lenient assertions or multiple test runs

**Import errors:**
- Ensure you're running tests from the project root
- Check that `src/` is in Python path (pytest should handle this)

