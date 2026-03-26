# MCP DDI Assistant

## Goal
Build a DNS Operations Assistant using MCP and Infoblox DDI.

## Current State
- MCP server working
- Tools:
  - list_zones
  - list_records
  - list_grid_members
  - search_dns_record
  - check_ip_usage
  - get_zone_summary
  - get_grid_status
  - get_dns_overview
- Week 1 status: completed
- Week 2 status: completed
- Week 3 status: completed
- Week 4 status: completed
- Week 5 status: completed
- Week 6 status: in progress
- Ref modeling status: corrected to use internal `ref` with DDI alias `_ref`
- MCP response contract: use `ref` externally, not `_ref`
- Response format status: standardized across current MCP tools
- Grid member payload note: `service_status` is a list of per-service status objects; `vip_setting` is a single nested object
- Architecture:
  - main.py → MCP layer
  - services → business logic
  - client → Infoblox API

## Principles
- Read-only (V1)
- Operation-oriented (not endpoint-oriented)
- Designed for LLM usage

---

## Weekly Plan (2 sessions of 1h)

### Week 1 — Architecture
- Session 1: Separate DNSOperationsService from main.py
- Session 2: Remove quickstart/example tools

### Week 2 — First Operation
- Session 3: Implement search_dns_record
- Session 4: Standardize response format

### Week 3 — Troubleshooting
- Session 5: Implement check_ip_usage
- Session 6: Implement get_zone_summary

### Week 4 — Infra Awareness
- Session 7: Improve get_grid_status
- Session 8: Implement get_dns_overview

### Week 5 — Open Source Readiness
- Session 9: Improve README
- Session 10: Add LICENSE and CONTRIBUTING

### Week 6 — Content
- Session 11: Create examples

---

## Next Steps
- TBD