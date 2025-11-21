# Test Dependencies Installation Guide

## Quick Summary

**The server does NOT require test dependencies to run.** Test libraries (like OpenAI) are only needed if you want to run tests.

**Test dependencies are isolated** - they're in optional dependency groups (`[test]`, `[integration]`), so installing the server alone (`pip install sde-mcp-server`) only installs 5 core dependencies. Test dependencies are completely separate.

## Installation

### Run Server Only (No Tests)

```bash
pip install sde-mcp-server
```

Installs only the server and its 5 runtime dependencies. No test libraries.

### Run Tests

**Unit tests only:**
```bash
pip install sde-mcp-server[test]
```

**Integration tests (requires OpenAI API key):**
```bash
pip install sde-mcp-server[integration]

# Set OpenAI API key in .env file (recommended):
# Copy tests/.env.example to .env and add your key
cp tests/.env.example .env
# Then edit .env and add your OPENAI_API_KEY

# Or via environment variable:
export OPENAI_API_KEY="your-key-here"
```

**All test dependencies:**
```bash
pip install sde-mcp-server[test-all]
```

### Development

```bash
pip install sde-mcp-server[dev-all]
```

Includes all test dependencies plus dev tools (black, isort, mypy).

## For Contributors / Local Development

**Step 1: Install the project (includes main dependencies)**
```bash
git clone <repo>
cd sde-mcp
pip install -e .
```

**Step 2: Install test dependencies on top**
```bash
pip install -e ".[test-all]"  # All tests
# OR
pip install -e ".[dev-all]"   # Tests + dev tools (black, isort, mypy)
```

**Or use uv (does both steps):**
```bash
uv sync --all-extras
```

**Why two steps?**
- The project needs to be installed first so tests can import `sde_mcp_server`
- Then test dependencies are added on top
- This ensures the server package is available to the test suite

