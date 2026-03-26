# MCP DDI Examples

This document provides practical examples of the MCP tools exposed by the project.

## list_zones

Scenario: discover which authoritative zones are available.

Tool:

```text
list_zones
```

Input:

```json
{}
```

Expected response shape:

```json
{
  "operation": "list_zones",
  "success": true,
  "total": 2,
  "results": [
    {
      "fqdn": "example.com",
      "view": "default",
      "ref": "zone_auth/..."
    }
  ],
  "message": "Retrieved 2 zones successfully."
}
```

## list_records

Scenario: inspect DNS A records in a known zone.

Tool:

```text
list_records
```

Input:

```json
{
  "zone": "example.com"
}
```

Expected response shape:

```json
{
  "operation": "list_records",
  "success": true,
  "total": 3,
  "results": [
    {
      "name": "app01.example.com",
      "ipv4addr": "10.10.10.15",
      "ref": "record:a/..."
    }
  ],
  "message": "Retrieved 3 records successfully."
}
```

## search_dns_record

Scenario: search by IP address, host name, or FQDN.

Tool:

```text
search_dns_record
```

Input by IP:

```json
{
  "query": "10.10.10.15"
}
```

Input by host name:

```json
{
  "query": "app01",
  "zone": "example.com"
}
```

Input by FQDN:

```json
{
  "query": "app01.example.com"
}
```

Expected response shape:

```json
{
  "operation": "search_dns_record",
  "success": true,
  "total": 1,
  "results": [
    {
      "name": "app01.example.com",
      "ipv4addr": "10.10.10.15",
      "zone": "example.com",
      "ref": "record:a/..."
    }
  ],
  "message": "Retrieved 1 matching record(s) successfully."
}
```

## check_ip_usage

Scenario: verify whether an IP is already used before creating or reassigning a record.

Tool:

```text
check_ip_usage
```

Input:

```json
{
  "ip": "10.10.10.15"
}
```

Possible outcomes:

- `unused`: no A records found
- `in_use`: one A record found
- `shared`: multiple A records found

Expected response shape:

```json
{
  "operation": "check_ip_usage",
  "success": true,
  "status": "shared",
  "total": 2,
  "results": [
    {
      "name": "app01.example.com",
      "ipv4addr": "10.10.10.15",
      "zone": "example.com",
      "ref": "record:a/..."
    }
  ],
  "message": "IP address is currently used by 2 DNS A records."
}
```

## get_zone_summary

Scenario: get a quick operational summary of a zone.

Tool:

```text
get_zone_summary
```

Input:

```json
{
  "zone": "example.com"
}
```

Expected response shape:

```json
{
  "operation": "get_zone_summary",
  "success": true,
  "total": 1,
  "results": [
    {
      "zone": "example.com",
      "total_records": 25,
      "total_unique_ips": 18,
      "sample_records": [
        {
          "name": "app01.example.com",
          "ipv4addr": "10.10.10.15",
          "zone": "example.com",
          "ref": "record:a/..."
        }
      ]
    }
  ],
  "message": "Retrieved summary for zone 'example.com' successfully."
}
```

## list_grid_members

Scenario: inspect which Infoblox grid members are available.

Tool:

```text
list_grid_members
```

Input:

```json
{}
```

Expected response shape:

```json
{
  "operation": "list_grid_members",
  "success": true,
  "total": 3,
  "results": [
    {
      "host_name": "infoblox.localdomain",
      "ref": "member/...",
      "ipv4_address": "10.253.0.132"
    }
  ],
  "message": "Retrieved 3 grid members successfully."
}
```

## get_grid_status

Scenario: understand grid health based on critical hosted services.

Tool:

```text
get_grid_status
```

Input:

```json
{}
```

Expected response shape:

```json
{
  "operation": "get_grid_status",
  "success": true,
  "total": 3,
  "results": [
    {
      "host_name": "infoblox.localdomain",
      "platform": "VNIOS",
      "vip_address": "10.253.0.132",
      "member_status": "healthy",
      "critical_services": {
        "DNS": {
          "status": "WORKING",
          "description": "DNS Service is working"
        },
        "DHCP": {
          "status": "WORKING",
          "description": "DHCP Service is working"
        }
      },
      "service_counts": {
        "WORKING": 3,
        "INACTIVE": 8,
        "UNKNOWN": 2
      },
      "ref": "member/..."
    }
  ],
  "summary": {
    "total_members": 3,
    "healthy_members": 1,
    "degraded_members": 2,
    "unknown_status_members": 0
  },
  "message": "Retrieved grid status for 3 members successfully."
}
```

## get_dns_overview

Scenario: get a high-level panorama of the DNS environment.

Tool:

```text
get_dns_overview
```

Input:

```json
{}
```

Expected response shape:

```json
{
  "operation": "get_dns_overview",
  "success": true,
  "total": 5,
  "results": {
    "overall_status": "degraded",
    "summary": {
      "overall_status": "degraded",
      "total_zones": 12,
      "total_grid_members": 3,
      "healthy_grid_members": 1,
      "degraded_grid_members": 2,
      "unknown_status_grid_members": 0
    },
    "results": {
      "zones": [
        {
          "fqdn": "example.com",
          "view": "default",
          "ref": "zone_auth/..."
        }
      ],
      "grid": {
        "total_members": 3,
        "healthy_members": 1,
        "degraded_members": 2,
        "unknown_status_members": 0
      }
    },
    "message": "DNS overview generated successfully. Some grid members require attention."
  },
  "message": "DNS overview generated successfully. Some grid members require attention."
}
```

## Notes

- The examples above illustrate response shapes and intent, not exact live values.
- Public MCP responses expose `ref`.
- Infoblox WAPI `_ref` values are mapped internally and surfaced as `ref` in the MCP contract.
