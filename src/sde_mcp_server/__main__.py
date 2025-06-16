"""Entry point for python -m sde_mcp_server."""

import asyncio
from .server import main


def main_entry():
    """Entry point for the sde-mcp-server command."""
    asyncio.run(main())


if __name__ == "__main__":
    main_entry() 