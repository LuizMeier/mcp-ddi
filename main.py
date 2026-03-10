"""
Infoblox MCP Server
"""

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from client.infoblox_client import InfobloxClient
from services.dns_operations import DNSOperationsService

load_dotenv()  # Load the .env file before anything else

ib_client = InfobloxClient()
dns_service = DNSOperationsService(ib_client)

# Create an MCP server
mcp = FastMCP("Infoblox", json_response=False)

@mcp.tool()
async def list_zones():
    """List all DNS zones"""
    zones = await dns_service.list_zones()
    return {
        "zones": zones,
        "total": len(zones)
    }

@mcp.tool()
async def list_records(zone: str):
    """List all DNS records in a zone"""
    records = await dns_service.list_records(zone)
    return {
        "records": records,
        "total": len(records),
        "zone": zone
    }

@mcp.tool()
async def list_grid_members():
    """List all grid members"""
    members = await dns_service.list_grid_members()
    return {
        "members": members,
        "total": len(members)
    }

# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
