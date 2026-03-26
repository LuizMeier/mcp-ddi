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
        "operation": "list_zones",
        "success": True,
        "total": len(zones),
        "results": zones,
        "message": f"Retrieved {len(zones)} zones successfully."
    }

@mcp.tool()
async def list_records(zone: str):
    """List all DNS records in a zone"""
    records = await dns_service.list_records(zone)
    return {
        "operation": "list_records",
        "success": True,
        "total": len(records),
        "results": records,
        "message": f"Retrieved {len(records)} records successfully."
    }

@mcp.tool()
async def list_grid_members():
    """List all grid members"""
    members = await dns_service.list_grid_members()
    return {
        "operation": "list_grid_members",
        "success": True,
        "total": len(members),
        "results": members,
        "message": f"Retrieved {len(members)} grid members successfully."
    }

@mcp.tool()
async def search_dns_record(query: str, zone: str | None = None):
    """Search DNS A records by IP address, host name, or FQDN."""
    results = await dns_service.search_dns_record(query, zone)
    return {
        "operation": "search_dns_record",
        "success": True,
        "total": len(results),
        "results": results,
        "message": f"Retrieved {len(results)} matching record(s) successfully."
    }

@mcp.tool()
async def health():
    """Check if the MCP server is healthy"""
    return {
        "operation": "health",
        "success": True,
        "total": 1,
        "results": [{"status": "healthy"}],
        "message": "MCP server is healthy."
    }

@mcp.tool()
async def check_ip_usage(ip: str):
    """Check whether an IP address is currently used by DNS A records."""
    usage = await dns_service.check_ip_usage(ip)
    results = usage["results"]
    status = usage["status"]

    if status == "unused":
        message = "IP address is not currently used by any DNS A record."
    elif status == "in_use":
        message = "IP address is currently used by 1 DNS A record."
    else:
        message = f"IP address is currently used by {len(results)} DNS A records."

    return {
        "operation": "check_ip_usage",
        "success": True,
        "status": status,
        "total": len(results),
        "results": results,
        "message": message,
    }

@mcp.tool()
async def get_zone_summary(zone: str):
    """Get a summary of a DNS zone"""
    summary = await dns_service.get_zone_summary(zone)
    return {
        "operation": "get_zone_summary",
        "success": True,
        "total": 1,
        "results": [summary],
        "message": f"Retrieved summary for zone '{zone}' successfully."
    }

# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
