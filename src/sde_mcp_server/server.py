#!/usr/bin/env python3
"""
SD Elements MCP Server

A Model Context Protocol (MCP) server for SD Elements API integration.
This server provides tools to interact with SD Elements through the MCP protocol.
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional, Sequence

from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    TextContent,
    Tool,
    GetPromptRequest,
    GetPromptResult,
    Prompt,
    PromptMessage,
    ListPromptsRequest,
)
from pydantic import BaseModel, ValidationError

from .api_client import SDElementsAPIClient, SDElementsAPIError, SDElementsAuthError, SDElementsNotFoundError

# Load environment variables
load_dotenv()

# Server instance
server = Server("sdelements-mcp")

# Global API client
api_client: Optional[SDElementsAPIClient] = None


class ToolError(Exception):
    """Custom exception for tool execution errors"""
    pass


def init_api_client() -> SDElementsAPIClient:
    """Initialize the SD Elements API client with configuration from environment variables"""
    host = os.getenv("SDE_HOST")
    api_key = os.getenv("SDE_API_KEY")
    
    if not host:
        raise ValueError("SDE_HOST environment variable is required")
    if not api_key:
        raise ValueError("SDE_API_KEY environment variable is required")
    
    return SDElementsAPIClient(host=host, api_key=api_key)


def format_error_response(error: Exception) -> str:
    """Format error response for tool calls"""
    if isinstance(error, SDElementsAuthError):
        return f"Authentication Error: {str(error)}"
    elif isinstance(error, SDElementsNotFoundError):
        return f"Not Found: {str(error)}"
    elif isinstance(error, SDElementsAPIError):
        return f"API Error: {str(error)}"
    elif isinstance(error, ValidationError):
        return f"Validation Error: {str(error)}"
    else:
        return f"Error: {str(error)}"


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List all available tools for SD Elements API interaction"""
    return [
        # Project tools
        Tool(
            name="list_projects",
            description="List all projects in SD Elements",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_size": {
                        "type": "integer",
                        "description": "Number of results per page (optional)"
                    },
                    "include": {
                        "type": "string",
                        "description": "Additional fields to include (comma-separated)"
                    },
                    "expand": {
                        "type": "string",
                        "description": "Fields to expand (comma-separated)"
                    }
                }
            }
        ),
        Tool(
            name="get_project",
            description="Get detailed information about a specific project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "The ID of the project to retrieve",
                        "minimum": 1
                    },
                    "include": {
                        "type": "string",
                        "description": "Additional fields to include (comma-separated)"
                    },
                    "expand": {
                        "type": "string",
                        "description": "Fields to expand (comma-separated)"
                    }
                },
                "required": ["project_id"]
            }
        ),
        Tool(
            name="create_project",
            description="Create a new project in SD Elements",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Project name"
                    },
                    "description": {
                        "type": "string",
                        "description": "Project description"
                    },
                    "application_id": {
                        "type": "integer",
                        "description": "ID of the application this project belongs to"
                    },
                    "phase_id": {
                        "type": "integer",
                        "description": "ID of the project phase"
                    }
                },
                "required": ["name", "application_id"]
            }
        ),
        Tool(
            name="update_project",
            description="Update an existing project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "The ID of the project to update",
                        "minimum": 1
                    },
                    "name": {
                        "type": "string",
                        "description": "Updated project name"
                    },
                    "description": {
                        "type": "string",
                        "description": "Updated project description"
                    },
                    "status": {
                        "type": "string",
                        "description": "Project status"
                    }
                },
                "required": ["project_id"]
            }
        ),
        Tool(
            name="delete_project",
            description="Delete a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "The ID of the project to delete",
                        "minimum": 1
                    }
                },
                "required": ["project_id"]
            }
        ),
        
        # Application tools
        Tool(
            name="list_applications",
            description="List all applications in SD Elements",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_size": {
                        "type": "integer",
                        "description": "Number of results per page (optional)"
                    },
                    "include": {
                        "type": "string",
                        "description": "Additional fields to include (comma-separated)"
                    },
                    "expand": {
                        "type": "string",
                        "description": "Fields to expand (comma-separated)"
                    }
                }
            }
        ),
        Tool(
            name="get_application",
            description="Get detailed information about a specific application",
            inputSchema={
                "type": "object",
                "properties": {
                    "application_id": {
                        "type": "integer",
                        "description": "The ID of the application to retrieve",
                        "minimum": 1
                    },
                    "include": {
                        "type": "string",
                        "description": "Additional fields to include (comma-separated)"
                    },
                    "expand": {
                        "type": "string",
                        "description": "Fields to expand (comma-separated)"
                    }
                },
                "required": ["application_id"]
            }
        ),
        Tool(
            name="create_application",
            description="Create a new application in SD Elements",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Application name"
                    },
                    "description": {
                        "type": "string",
                        "description": "Application description"
                    },
                    "business_unit_id": {
                        "type": "integer",
                        "description": "ID of the business unit this application belongs to"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="update_application",
            description="Update an existing application",
            inputSchema={
                "type": "object",
                "properties": {
                    "application_id": {
                        "type": "integer",
                        "description": "The ID of the application to update",
                        "minimum": 1
                    },
                    "name": {
                        "type": "string",
                        "description": "Updated application name"
                    },
                    "description": {
                        "type": "string",
                        "description": "Updated application description"
                    }
                },
                "required": ["application_id"]
            }
        ),
        
        # Countermeasure tools
        Tool(
            name="list_countermeasures",
            description="List countermeasures for a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "The ID of the project",
                        "minimum": 1
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by countermeasure status"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of results per page (optional)"
                    }
                },
                "required": ["project_id"]
            }
        ),
        Tool(
            name="get_countermeasure",
            description="Get detailed information about a specific countermeasure",
            inputSchema={
                "type": "object",
                "properties": {
                    "countermeasure_id": {
                        "type": "integer",
                        "description": "The ID of the countermeasure to retrieve",
                        "minimum": 1
                    }
                },
                "required": ["countermeasure_id"]
            }
        ),
        Tool(
            name="update_countermeasure",
            description="Update a countermeasure status or details",
            inputSchema={
                "type": "object",
                "properties": {
                    "countermeasure_id": {
                        "type": "integer",
                        "description": "The ID of the countermeasure to update",
                        "minimum": 1
                    },
                    "status": {
                        "type": "string",
                        "description": "New status for the countermeasure"
                    },
                    "notes": {
                        "type": "string",
                        "description": "Notes about the countermeasure"
                    }
                },
                "required": ["countermeasure_id"]
            }
        ),
        
        # User tools
        Tool(
            name="list_users",
            description="List all users in SD Elements",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_size": {
                        "type": "integer",
                        "description": "Number of results per page (optional)"
                    },
                    "active": {
                        "type": "boolean",
                        "description": "Filter by active users only"
                    }
                }
            }
        ),
        Tool(
            name="get_user",
            description="Get detailed information about a specific user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user to retrieve",
                        "minimum": 1
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="get_current_user",
            description="Get information about the currently authenticated user",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # Business Unit tools
        Tool(
            name="list_business_units",
            description="List all business units",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_size": {
                        "type": "integer",
                        "description": "Number of results per page (optional)"
                    }
                }
            }
        ),
        Tool(
            name="get_business_unit",
            description="Get detailed information about a specific business unit",
            inputSchema={
                "type": "object",
                "properties": {
                    "business_unit_id": {
                        "type": "integer",
                        "description": "The ID of the business unit to retrieve",
                        "minimum": 1
                    }
                },
                "required": ["business_unit_id"]
            }
        ),
        
        # Generic API tool
        Tool(
            name="api_request",
            description="Make a custom API request to any SD Elements endpoint",
            inputSchema={
                "type": "object",
                "properties": {
                    "method": {
                        "type": "string",
                        "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"],
                        "description": "HTTP method for the request"
                    },
                    "endpoint": {
                        "type": "string",
                        "description": "API endpoint (e.g., 'projects/', 'applications/123/')"
                    },
                    "params": {
                        "type": "object",
                        "description": "URL parameters as key-value pairs"
                    },
                    "data": {
                        "type": "object",
                        "description": "Request body data as key-value pairs"
                    }
                },
                "required": ["method", "endpoint"]
            }
        ),
        
        # Test connection tool
        Tool(
            name="test_connection",
            description="Test the connection to SD Elements API",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls for SD Elements API operations"""
    global api_client
    
    try:
        # Initialize API client if not already done
        if api_client is None:
            api_client = init_api_client()
        
        # Helper function to build params
        def build_params(args: Dict[str, Any]) -> Dict[str, Any]:
            params = {}
            if "page_size" in args:
                params["page_size"] = args["page_size"]
            if "include" in args:
                params["include"] = args["include"]
            if "expand" in args:
                params["expand"] = args["expand"]
            return params
        
        # Project tools
        if name == "list_projects":
            params = build_params(arguments)
            result = api_client.list_projects(params)
            
        elif name == "get_project":
            project_id = arguments["project_id"]
            params = build_params(arguments)
            result = api_client.get_project(project_id, params)
            
        elif name == "create_project":
            data = {k: v for k, v in arguments.items() if k in ["name", "description", "application_id", "phase_id"]}
            result = api_client.create_project(data)
            
        elif name == "update_project":
            project_id = arguments.pop("project_id")
            data = arguments  # Remaining arguments are the update data
            result = api_client.update_project(project_id, data)
            
        elif name == "delete_project":
            project_id = arguments["project_id"]
            result = api_client.delete_project(project_id)
            
        # Application tools
        elif name == "list_applications":
            params = build_params(arguments)
            result = api_client.list_applications(params)
            
        elif name == "get_application":
            app_id = arguments["application_id"]
            params = build_params(arguments)
            result = api_client.get_application(app_id, params)
            
        elif name == "create_application":
            data = {k: v for k, v in arguments.items() if k in ["name", "description", "business_unit_id"]}
            result = api_client.create_application(data)
            
        elif name == "update_application":
            app_id = arguments.pop("application_id")
            data = arguments  # Remaining arguments are the update data
            result = api_client.update_application(app_id, data)
            
        # Countermeasure tools
        elif name == "list_countermeasures":
            project_id = arguments["project_id"]
            params = {}
            if "status" in arguments:
                params["status"] = arguments["status"]
            if "page_size" in arguments:
                params["page_size"] = arguments["page_size"]
            result = api_client.list_countermeasures(project_id, params)
            
        elif name == "get_countermeasure":
            countermeasure_id = arguments["countermeasure_id"]
            result = api_client.get_countermeasure(countermeasure_id)
            
        elif name == "update_countermeasure":
            countermeasure_id = arguments.pop("countermeasure_id")
            data = arguments  # Remaining arguments are the update data
            result = api_client.update_countermeasure(countermeasure_id, data)
            
        # User tools
        elif name == "list_users":
            params = {}
            if "page_size" in arguments:
                params["page_size"] = arguments["page_size"]
            if "active" in arguments:
                params["is_active"] = arguments["active"]
            result = api_client.list_users(params)
            
        elif name == "get_user":
            user_id = arguments["user_id"]
            result = api_client.get_user(user_id)
            
        elif name == "get_current_user":
            result = api_client.get_current_user()
            
        # Business Unit tools
        elif name == "list_business_units":
            params = build_params(arguments)
            result = api_client.list_business_units(params)
            
        elif name == "get_business_unit":
            bu_id = arguments["business_unit_id"]
            result = api_client.get_business_unit(bu_id)
            
        # Generic API tool
        elif name == "api_request":
            method = arguments["method"]
            endpoint = arguments["endpoint"]
            params = arguments.get("params")
            data = arguments.get("data")
            result = api_client.api_request(method, endpoint, params, data)
            
        # Test connection tool
        elif name == "test_connection":
            success = api_client.test_connection()
            result = {
                "connection_successful": success,
                "host": api_client.host,
                "message": "Connection successful" if success else "Connection failed"
            }
            
        else:
            raise ToolError(f"Unknown tool: {name}")
        
        # Format the response
        response_text = json.dumps(result, indent=2, default=str)
        return [TextContent(type="text", text=response_text)]
        
    except Exception as e:
        error_message = format_error_response(e)
        return [TextContent(type="text", text=error_message)]


@server.list_prompts()
async def list_prompts() -> List[Prompt]:
    """List available prompts"""
    return [
        Prompt(
            name="project_summary",
            description="Generate a summary of projects in SD Elements",
        ),
        Prompt(
            name="security_status",
            description="Get security status overview for applications and projects",
        )
    ]


@server.get_prompt()
async def get_prompt(name: str, arguments: Dict[str, str] | None = None) -> GetPromptResult:
    """Get a specific prompt"""
    if name == "project_summary":
        return GetPromptResult(
            description="Generate a summary of projects in SD Elements",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text="Please provide a summary of all projects in SD Elements, including their status, applications, and key security metrics."
                    )
                )
            ]
        )
    elif name == "security_status":
        return GetPromptResult(
            description="Get security status overview",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text="Please provide an overview of the security status across all applications and projects, highlighting any critical countermeasures that need attention."
                    )
                )
            ]
        )
    else:
        raise ValueError(f"Unknown prompt: {name}")


async def main():
    """Main entry point for the MCP server"""
    # Validate configuration
    try:
        init_api_client()
        print("SD Elements MCP Server starting...", file=sys.stderr)
        print(f"Host: {os.getenv('SDE_HOST')}", file=sys.stderr)
        print("Configuration validated successfully", file=sys.stderr)
    except Exception as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        print("Please set SDE_HOST and SDE_API_KEY environment variables", file=sys.stderr)
        sys.exit(1)
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main()) 