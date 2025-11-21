# Cursor MCP Configuration

This directory contains the MCP (Model Context Protocol) configuration for the SD Elements server.

## Setup

**IMPORTANT:** You need to add your SD Elements credentials to `.cursor/mcp.json`

1. Open `.cursor/mcp.json` in this directory
2. Replace the placeholder values:
   - `SDE_HOST`: Your SD Elements instance URL
   - `SDE_API_KEY`: Your API key from SD Elements Settings > API Tokens

Example:
```json
{
  "mcpServers": {
    "sde-elements": {
      "command": "python3",
      "args": ["-m", "sde_mcp_server"],
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/venv/lib/python3.10/site-packages",
        "SDE_HOST": "https://demo.sdelements.com",
        "SDE_API_KEY": "abc123def456..."
      }
    }
  }
}
```

## Security Note

**DO NOT commit `.cursor/mcp.json` with real credentials!**

The file `.cursor/mcp.json` is gitignored to prevent accidentally committing your API keys.
A template is provided at `.cursor/mcp.json.example`.

## After Setup

1. Save your changes to `.cursor/mcp.json`
2. Reload Cursor window (Cmd/Ctrl+Shift+P → "Developer: Reload Window")
3. Test with: `"List all projects in SD Elements"`

