"""
FastMCP quickstart example.

Run from the repository root:
    uv run examples/snippets/servers/fastmcp_quickstart.py
"""

import logging
from mcp.server.fastmcp import FastMCP
from fastapi import HTTPException
from infoblox_client import InfobloxClient

# Create an MCP server
mcp = FastMCP("Demo", json_response=True)

# Create an Infoblox client
ibClient = InfobloxClient()

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add Infoblox tools
@mcp.tool()
def list_zones():
    """List all DNS zones"""
    return [z.name for z in ibClient.get_zones()]

@mcp.tool()
def list_records(zone: str):
    """List all DNS records in a zone"""
    return [r.model_dump() for r in ibClient.get_records(zone)]

@mcp.tool()
def list_grid_members():
    """List all grid members"""
    return [m.model_dump() for m in ibClient.get_grid_members()]

# Add a test tool that fetches data from an external API
logger = logging.getLogger("mcp")


@mcp.tool()
async def list_breeds():
    """List all Dog Breeds."""
    try:
        data = await ibClient.get_breeds()
        # Nova estrutura: nomes das raças estão em data[i]['attributes']['name']
        breeds = [breed['attributes']['name'] for breed in data.get('data', [])]
        return breeds
    except Exception as e:
        logger.error("Error in list_breeds: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
