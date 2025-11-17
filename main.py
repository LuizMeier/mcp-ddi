"""Main application module for Infoblox MCP Connector."""
import logging
import os
import json
from fastapi import FastAPI, Query, HTTPException, Body
from fastapi.responses import JSONResponse

from infoblox_client import InfobloxClient
from models import Zone, DNSRecord, GridMember

# ---------------------------------------------------------------------
# App Setup
# ---------------------------------------------------------------------

app = FastAPI(title="Infoblox MCP Connector", version="1.0")

client = InfobloxClient()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp")


# ---------------------------------------------------------------------
# Public API Endpoints
# ---------------------------------------------------------------------

@app.get("/zones", response_model=list[Zone])
async def list_zones():
    """List all authoritative DNS zones."""
    try:
        logger.info("Tool: list_zones() called")
        return await client.get_zones()
    except Exception as e:
        logger.error(f"Error in list_zones: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/records", response_model=list[DNSRecord])
async def list_records(zone: str = Query(..., description="Zone name")):
    """List all A records in a specific zone."""
    try:
        logger.info(f"Tool: list_records(zone={zone}) called")
        return await client.get_records(zone)
    except Exception as e:
        logger.error(f"Error in list_records: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/grid-members", response_model=list[GridMember])
async def list_grid_members():
    """List all Grid Members and their statuses."""
    try:
        logger.info("Tool: list_grid_members() called")
        return await client.get_grid_members()
    except Exception as e:
        logger.error(f"Error in list_grid_members: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------
# MCP Endpoints
# ---------------------------------------------------------------------

@app.get("/mcp/")
async def mcp_root():
    """Health check endpoint required by MCP."""
    return {"status": "ok", "message": "Infoblox MCP Connector is running"}


@app.get("/mcp/manifest")
async def manifest():
    """Returns the MCP manifest file that describes the available tools."""
    manifest_path = os.path.join(
        os.path.dirname(__file__),
        "mcp_manifest.json"
    )

    if not os.path.exists(manifest_path):
        raise HTTPException(status_code=500, detail="Manifest file not found")

    with open(manifest_path, "r") as f:
        return json.load(f)


# ---------------------------------------------------------------------
# MCP Tool Execution Endpoint
# ---------------------------------------------------------------------

@app.post("/mcp/call")
async def mcp_call(payload: dict = Body(...)):
    """
    Executed by the LLM when asking to use a tool.
    
    Payload example:
    {
        "tool": "list_records",
        "arguments": { "zone": "example.com" }
    }
    """

    tool = payload.get("tool")
    args = payload.get("arguments", {})

    logger.info(f"MCP call received: tool={tool}, args={args}")

    if not tool:
        raise HTTPException(status_code=400, detail="Missing 'tool' field")

    # Map tool name → internal API function
    try:
        if tool == "list_zones":
            result = await list_zones()

        elif tool == "list_records":
            zone = args.get("zone")
            if not zone:
                raise HTTPException(status_code=400, detail="Missing argument: zone")
            result = await list_records(zone)

        elif tool == "list_grid_members":
            result = await list_grid_members()

        else:
            raise HTTPException(status_code=400, detail=f"Unknown tool '{tool}'")

        logger.info(f"Tool '{tool}' executed successfully")

        return JSONResponse(
            content={"success": True, "data": result},
            status_code=200
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Unhandled error during tool execution: {e}")
        raise HTTPException(status_code=500, detail=str(e))
