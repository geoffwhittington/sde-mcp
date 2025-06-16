# SD Elements MCP Server

A Model Context Protocol server that provides **SD Elements API integration**. This server enables LLMs to interact with SD Elements security development lifecycle platform.

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

</div>

## Available Tools

### Project Management
* `list_projects` - List all projects with optional filtering
* `get_project` - Get detailed project information
* `create_project` - Create a new project
* `update_project` - Update project details
* `delete_project` - Delete a project

### Application Management
* `list_applications` - List all applications
* `get_application` - Get application details
* `create_application` - Create a new application
* `update_application` - Update application information

### Countermeasures
* `list_countermeasures` - List countermeasures for a project
* `get_countermeasure` - Get countermeasure details
* `update_countermeasure` - Update countermeasure status

### Tasks & Surveys
* `list_tasks` - List tasks for a project
* `get_task` - Get task details
* `list_surveys` - List surveys
* `get_survey` - Get survey details

### Phases & Milestones
* `list_phases` - List project phases
* `get_phase` - Get phase details
* `list_milestones` - List project milestones

## Quick Start

### Using uvx (recommended)

You can run the server directly using `uvx` without installing:

```bash
uvx sde-mcp-server
```

### Using uv pip

```bash
# Install the package
uv pip install sde-mcp-server

# Run the server
sde-mcp-server
```

### Using pip

```bash
pip install sde-mcp-server
sde-mcp-server
```

## Configuration

The server requires two environment variables:

- `SDE_HOST`: Your SD Elements instance URL (e.g., `https://your-sdelements-instance.com`)
- `SDE_API_KEY`: Your SD Elements API key

### Setting Environment Variables

#### Option 1: Environment Variables
```bash
export SDE_HOST="https://your-sdelements-instance.com"
export SDE_API_KEY="your-api-key-here"
```

#### Option 2: .env File
Create a `.env` file in your working directory:
```env
SDE_HOST=https://your-sdelements-instance.com
SDE_API_KEY=your-api-key-here
```

### Getting Your API Key

1. Log into your SD Elements instance
2. Go to **Settings** > **API Tokens**
3. Generate a new API token
4. Copy the token value for use as `SDE_API_KEY`

## MCP Client Configuration

### Claude Desktop

Add this to your Claude Desktop configuration file:

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

### Cline

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

### Continue

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

Add this to your Cursor configuration file:

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
If you have the package installed locally:
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
```json
{
  "mcpServers": {
    "sde-elements": {
      "command": "python",
      "args": ["-m", "sde_mcp_server"],
      "env": {
        "SDE_HOST": "https://your-sdelements-instance.com",
        "SDE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Development

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed
- Python 3.10 or higher

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd sde-mcp-server

# Create virtual environment and install dependencies
uv sync

# Run in development mode
uv run python -m sde_mcp_server
```

### Testing

```bash
# Run the import test
uv run python test_import.py

# Test with environment variables
SDE_HOST=https://demo.sdelements.com SDE_API_KEY=test uv run python -m sde_mcp_server
```

### Building

```bash
# Build the package
uv build

# Install locally for testing
uv pip install dist/*.whl
```

## Features

- **Full API Coverage**: Supports all major SD Elements API endpoints
- **Authentication**: Secure API key-based authentication
- **Error Handling**: Comprehensive error handling and validation
- **Environment Configuration**: Flexible configuration via environment variables
- **Modern Python**: Built with modern Python packaging (uv, pyproject.toml)
- **MCP Compliant**: Fully compatible with the Model Context Protocol

## API Coverage

This server provides access to:

- Projects and Applications
- Countermeasures and Tasks
- Surveys and Phases
- Milestones and Requirements
- Users and Teams
- Compliance and Reporting

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues and questions:

1. Check the [Issues](../../issues) page
2. Review the SD Elements API documentation
3. Ensure your API key has proper permissions

---

**Note**: This is an unofficial MCP server for SD Elements. For official SD Elements support, please contact Security Compass. 