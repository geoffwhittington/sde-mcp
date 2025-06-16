# SD Elements MCP Server - Deployment Guide

This guide provides deployment options for the SD Elements MCP Server using modern Python tooling.

## Prerequisites

- SD Elements instance URL
- SD Elements API key (generate in SD Elements under Settings > API Tokens)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed (recommended)
- Python 3.10+ (if using pip directly)

## Configuration

All deployment methods require setting environment variables:

- `SDE_HOST`: Your SD Elements instance URL (e.g., `https://your-sdelements-instance.com`)
- `SDE_API_KEY`: Your SD Elements API key

## Deployment Options

### Option 1: uvx (Recommended)

The easiest way to run the server without installation:

```bash
# Set environment variables
export SDE_HOST="https://your-sdelements-instance.com"
export SDE_API_KEY="your-api-key-here"

# Run directly with uvx
uvx sde-mcp-server
```

### Option 2: uv pip Install

Install the package with uv:

```bash
# Install the package
uv pip install sde-mcp-server

# Set environment variables
export SDE_HOST="https://your-sdelements-instance.com"
export SDE_API_KEY="your-api-key-here"

# Run the server
sde-mcp-server
```

### Option 3: Traditional pip Install

```bash
# Install the package
pip install sde-mcp-server

# Set environment variables
export SDE_HOST="https://your-sdelements-instance.com"
export SDE_API_KEY="your-api-key-here"

# Run the server
sde-mcp-server
```

### Option 4: Development Installation

For development or local modifications:

```bash
# Clone the repository
git clone <repository-url>
cd sde-mcp-server

# Create virtual environment and install dependencies
uv sync

# Set environment variables
export SDE_HOST="https://your-sdelements-instance.com"
export SDE_API_KEY="your-api-key-here"

# Run in development mode
uv run python -m sde_mcp_server
```

## MCP Client Configuration

### Claude Desktop

Add this to your Claude Desktop configuration file (`~/.config/claude-desktop/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "sde-elements": {
      "command": "uvx",
      "args": ["sde-mcp-server"],
      "env": {
        "SDE_HOST": "https://your-sdelements-instance.com",
        "SDE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Cline (VS Code Extension)

Add this to your Cline MCP settings:

```json
{
  "mcpServers": {
    "sde-elements": {
      "command": "uvx",
      "args": ["sde-mcp-server"],
      "env": {
        "SDE_HOST": "https://your-sdelements-instance.com",
        "SDE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Continue (VS Code Extension)

Add this to your Continue configuration:

```json
{
  "mcpServers": {
    "sde-elements": {
      "command": "uvx",
      "args": ["sde-mcp-server"],
      "env": {
        "SDE_HOST": "https://your-sdelements-instance.com",
        "SDE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Cursor

To configure the SD Elements MCP server in Cursor:

#### Step 1: Open Cursor Settings
1. Open Cursor
2. Go to **Settings** (Ctrl/Cmd + ,)
3. Search for "MCP" or navigate to **Extensions** > **Model Context Protocol**

#### Step 2: Add Server Configuration

Choose one of the following configuration options:

#### Option 1: Using uvx (Recommended)
```json
{
  "mcpServers": {
    "sde-elements": {
      "command": "uvx",
      "args": ["sde-mcp-server"],
      "env": {
        "SDE_HOST": "https://your-sdelements-instance.com",
        "SDE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

#### Option 2: Using local installation
If you have installed the package locally with `pip` or `uv pip install`:
```json
{
  "mcpServers": {
    "sde-elements": {
      "command": "sde-mcp-server",
      "env": {
        "SDE_HOST": "https://your-sdelements-instance.com",
        "SDE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

#### Option 3: Using Python module directly
If you have the source code and want to run it directly:
```json
{
  "mcpServers": {
    "sde-elements": {
      "command": "python",
      "args": ["-m", "sde_mcp_server"],
      "env": {
        "SDE_HOST": "https://your-sdelements-instance.com",
        "SDE_API_KEY": "your-api-key-here"
      },
      "cwd": "/path/to/sde-mcp-server"
    }
  }
}
```

#### Step 3: Restart Cursor
After adding the configuration, restart Cursor for the changes to take effect.

#### Step 4: Verify Connection
1. Open a chat or use the AI assistant in Cursor
2. The SD Elements tools should now be available
3. You can ask questions like "List all projects in SD Elements" or "Show me countermeasures for project ID 123"

#### Troubleshooting Cursor Configuration

**Server not starting:**
- Ensure `uvx` is installed and in your PATH
- Verify your `SDE_HOST` and `SDE_API_KEY` are correct
- Check Cursor's output/logs for error messages

**Command not found errors:**
- If using Option 2, ensure the package is installed: `pip install sde-mcp-server`
- If using Option 3, ensure the correct path to your source code

**Environment variable issues:**
- Make sure your SD Elements instance URL doesn't have a trailing slash
- Verify your API key has the necessary permissions in SD Elements

## Environment Configuration

### Using .env File

Create a `.env` file in your working directory:

```env
SDE_HOST=https://your-sdelements-instance.com
SDE_API_KEY=your-api-key-here
```

The server will automatically load these variables if the file is present.

### Using System Environment Variables

#### Linux/macOS

```bash
# Add to ~/.bashrc, ~/.zshrc, or similar
export SDE_HOST="https://your-sdelements-instance.com"
export SDE_API_KEY="your-api-key-here"

# Reload your shell
source ~/.bashrc
```

#### Windows (PowerShell)

```powershell
# Set environment variables
$env:SDE_HOST="https://your-sdelements-instance.com"
$env:SDE_API_KEY="your-api-key-here"

# Or set permanently
[System.Environment]::SetEnvironmentVariable("SDE_HOST", "https://your-sdelements-instance.com", "User")
[System.Environment]::SetEnvironmentVariable("SDE_API_KEY", "your-api-key-here", "User")
```

## Testing Your Installation

### Basic Connection Test

```bash
# Test that the package can be imported
python -c "import sde_mcp_server; print('✓ Package imported successfully')"
```

### Full Integration Test

```bash
# Run with test environment variables
SDE_HOST=https://demo.sdelements.com SDE_API_KEY=test uvx sde-mcp-server
```

## Troubleshooting

### Common Issues

1. **"Command not found: uvx"**
   - Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Or use pip: `pip install uv`

2. **"Package not found: sde-mcp-server"**
   - The package isn't published yet. Use development installation instead.

3. **"Authentication failed"**
   - Verify your `SDE_HOST` URL is correct
   - Check that your `SDE_API_KEY` is valid
   - Ensure the API key has proper permissions

4. **"Connection timeout"**
   - Check network connectivity
   - Verify firewall settings
   - Ensure SD Elements instance is accessible

### Debug Mode

Run with debug logging:

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
uvx sde-mcp-server
```

## Production Deployment

### Systemd Service (Linux)

Create a systemd service file `/etc/systemd/system/sde-mcp-server.service`:

```ini
[Unit]
Description=SD Elements MCP Server
After=network.target

[Service]
Type=simple
User=sde-mcp
Environment=SDE_HOST=https://your-sdelements-instance.com
Environment=SDE_API_KEY=your-api-key-here
ExecStart=/usr/local/bin/uvx sde-mcp-server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable sde-mcp-server
sudo systemctl start sde-mcp-server
sudo systemctl status sde-mcp-server
```

### Process Manager (PM2)

```bash
# Install PM2
npm install -g pm2

# Create ecosystem file
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'sde-mcp-server',
    script: 'uvx',
    args: 'sde-mcp-server',
    env: {
      SDE_HOST: 'https://your-sdelements-instance.com',
      SDE_API_KEY: 'your-api-key-here'
    }
  }]
}
EOF

# Start with PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## Security Considerations

- Store API keys securely (use environment variables, not hardcoded values)
- Use HTTPS endpoints only
- Regularly rotate API keys
- Monitor API usage and access logs
- Run the server with minimal required permissions
- Use virtual environments or containers to isolate dependencies

## Monitoring

### Health Checks

The server provides basic health checking through successful import:

```bash
# Simple health check
python -c "import sde_mcp_server; print('Healthy')" || echo "Unhealthy"
```

### Logging

The server logs to stdout by default. Configure your deployment to capture and rotate logs appropriately.

---

For additional support, see the main [README.md](README.md) or open an issue in the repository. 