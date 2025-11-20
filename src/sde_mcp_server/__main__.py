"""Entry point for python -m sde_mcp_server."""

from .server import main


def main_entry():
    """Entry point for the sde-mcp-server command."""
    # FastMCP's run() is synchronous and manages its own event loop
    # The nest_asyncio is applied inside main() if needed
    main()


if __name__ == "__main__":
    main_entry() 