# Quick Start: Managing Prompt-to-Tool Mappings

## Setup

1. Copy `tests/.env.example` to `.env` (in project root or tests directory)
2. Add your OpenAI API key to `.env`: `OPENAI_API_KEY=your-key-here`

## For Product Team

### Add Test Case

1. Open `tests/prompts_tool_mapping.csv` in Excel/Sheets
2. Add row: `prompt,expected_tools,category,description,priority`
3. Validate: `python tests/validate_csv.py --summary`
4. Run tests: `pytest tests/test_prompt_mapping_from_csv.py -m 'integration and not unit' -v`
   (API key loaded from .env file or OPENAI_API_KEY env var)
   
   **Note:** Use `-m integration` to run the prompt-to-tool mapping tests (they're marked as integration tests)

### CSV Format

- `prompt`: User's prompt (quote if commas)
- `expected_tools`: Tool name(s), comma-separated
- `category`: Optional grouping
- `description`: Optional note
- `priority`: `high`, `medium`, or `low`

## For Developers

**Setup (one-time):**
```bash
# From project root - install project + test dependencies
pip install -e ".[test-all]"
# OR with uv:
uv sync --all-extras
```

**Run tests (always from project root):**
```bash
# Make sure you're in the project root directory
cd /path/to/sde-mcp

# CSV-driven prompt-to-tool mapping tests (needs API key in .env or OPENAI_API_KEY env var)
pytest tests/test_prompt_mapping_from_csv.py -m 'integration and not unit' -v
```

**Important:** 
- Run tests from project root, not from `tests/` directory
- Project must be installed first (`pip install -e .` or `uv sync`)
- Test dependencies are optional - they don't pollute the server installation. The server only has 5 core dependencies.

See `README_PROMPT_MAPPING.md` for full guide.
