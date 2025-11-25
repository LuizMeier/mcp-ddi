"""
FastMCP quickstart example.

Run from the repository root:
    uv run examples/snippets/servers/fastmcp_quickstart.py
"""

import json
import logging
from mcp.server.fastmcp import FastMCP
from fastapi import HTTPException
from dotenv import load_dotenv
from infoblox_client import InfobloxClient

load_dotenv()  # Load the .env file before anything else

# Create an MCP server
mcp = FastMCP("Demo", json_response=False)

# Create an Infoblox client
ibClient = InfobloxClient()

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add Infoblox tools
@mcp.tool()
async def list_zones():
    """List all DNS zones"""
    data = await ibClient.get_zones()
    zones = [{"fqdn": z.fqdn, "view": z.view, "ref": z.ref} for z in data]
    return {"zones": zones, "total": len(zones)}

@mcp.tool()
async def list_records(zone: str):
    """List all DNS records in a zone"""
    data = await ibClient.get_records(zone)
    records = [{"name": r.name, "ipv4addr": r.ipv4addr, "ref": r.ref} for r in data]
    return {"records": records, "total": len(records), "zone": zone}

@mcp.tool()
async def list_grid_members():
    """List all grid members"""
    data = await ibClient.get_grid_members()
    members = [{"host_name": m.host_name, "ref": m.ref} for m in data]
    return {"members": members, "total": len(members)}

@mcp.tool()
async def list_breeds():
    """List all Dog Breeds."""
    try:
        data = await ibClient.get_breeds()
        # New structure: breed names are in data[i]['attributes']['name']
        breeds = [breed['attributes']['name'] for breed in data.get('data', [])]
        return breeds
    except Exception as e:
        logger.error("Error in list_breeds: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e

# Add a test tool that fetches data from an external API
logger = logging.getLogger("mcp")


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
