# MCP DDI

MCP server for Infoblox DDI focused on read-only DNS operations.

## Overview

This project exposes Infoblox DDI data through MCP tools designed for LLM-oriented operations instead of direct endpoint mirroring.

Current capabilities:

- `list_zones`
- `list_records`
- `list_grid_members`
- `search_dns_record`
- `check_ip_usage`
- `get_zone_summary`
- `get_grid_status`
- `get_dns_overview`

## Principles

- Read-only in V1
- Operation-oriented
- Designed for LLM usage

## Project Structure

- [main.py](/Users/luizmeier/Projetos/mcp-ddi/main.py): MCP tool layer
- [services/dns_operations.py](/Users/luizmeier/Projetos/mcp-ddi/services/dns_operations.py): business logic and operational summaries
- [client/infoblox_client.py](/Users/luizmeier/Projetos/mcp-ddi/client/infoblox_client.py): Infoblox WAPI integration
- [models.py](/Users/luizmeier/Projetos/mcp-ddi/models.py): Pydantic models
- [config.py](/Users/luizmeier/Projetos/mcp-ddi/config.py): environment-based configuration

## Requirements

- Python 3.10+
- Access to an Infoblox WAPI endpoint

## Configuration

Set the following environment variables before running the server:

- `WAPI_URL`
- `WAPI_USER`
- `WAPI_PASS`
- `WAPI_VERIFY_SSL`

Example:

```bash
export WAPI_URL="https://infoblox.example.com/wapi/v2.13.7"
export WAPI_USER="your-user"
export WAPI_PASS="your-password"
export WAPI_VERIFY_SSL="true"
```

Keep `WAPI_VERIFY_SSL="false"` only for temporary lab scenarios with a known self-signed certificate.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
python3 main.py
```

The server uses FastMCP with `streamable-http` transport.

This project returns internal DNS and grid data. Do not expose this MCP endpoint directly to the internet.

Recommended minimum exposure model:

- bind it only to localhost or a private network
- place it behind an authenticated reverse proxy if remote access is required
- restrict source IPs to trusted clients only
- avoid publishing screenshots or examples with real hostnames, IPs, refs, or VIP addresses

By default, the MCP endpoint is exposed at:

```text
http://localhost:8000/mcp
```

## MCP Client Configuration

This server is not configured as a stdio MCP process. It runs as an HTTP server using `streamable-http`.

That means you must start the server manually before connecting your LLM client to it:

```bash
python3 main.py
```

Once the server is running, configure your MCP client with an HTTP entry similar to:

```json
{
  "mcpServers": {
    "DDI": {
      "type": "http",
      "url": "http://localhost:8000/mcp",
      "description": "DDI MCP Server"
    }
  }
}
```

If your client supports environment variables only for local process launches, note that in HTTP mode those variables must already be available in the shell or environment where `main.py` is started.

## Tool Summary

### DNS

- `list_zones`: lists authoritative zones
- `list_records`: lists DNS A records in a zone
- `search_dns_record`: searches DNS A records by IP, host name, or FQDN
- `check_ip_usage`: checks whether an IP is unused, in use, or shared
- `get_zone_summary`: returns a compact summary of a zone
- `get_dns_overview`: returns a general DNS panorama

### Grid

- `list_grid_members`: lists members
- `get_grid_status`: summarizes member health based on hosted services

## Development Notes

- The public MCP contract uses `ref`
- The Infoblox payload uses `_ref`, mapped internally through Pydantic aliases
- Grid member health is derived from per-service status, not from a single node status field

## Validation

Basic syntax validation can be done with:

```bash
python3 -m py_compile main.py client/infoblox_client.py services/dns_operations.py models.py config.py
```

## Roadmap

The current implementation covers weeks 1 through 5 of the working plan tracked in [docs/context.md](/Users/luizmeier/Projetos/mcp-ddi/docs/context.md). Next planned work includes examples and public-facing content.

## Examples

Practical tool examples are available in [docs/examples.md](/Users/luizmeier/Projetos/mcp-ddi/docs/examples.md).
