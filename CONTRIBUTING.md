# Contributing

## Scope

This project is currently focused on read-only MCP operations for Infoblox DDI.

Please prefer contributions that:

- keep the MCP surface operation-oriented
- preserve read-only behavior in V1
- improve clarity for LLM and human consumers
- keep integration concerns in the client and business rules in the service layer

## Development Flow

1. Create a branch for your work.
2. Make focused changes.
3. Run basic validation.
4. Open a pull request with a concise description of the change.

## Project Conventions

- Public MCP responses should expose `ref`, not `_ref`
- `_ref` should remain an integration detail handled by model aliases
- `main.py` should stay thin and delegate logic to the service layer
- `client/infoblox_client.py` should only contain Infoblox WAPI access logic
- `services/dns_operations.py` should contain operational logic and summaries

## Validation

Run at least:

```bash
python3 -m py_compile main.py client/infoblox_client.py services/dns_operations.py models.py config.py
```

If you change tool behavior, also verify:

- MCP response shape stays consistent
- `mcp_manifest.json` matches the exposed tools
- [docs/context.md](/Users/luizmeier/Projetos/mcp-ddi/docs/context.md) is updated

## Pull Request Notes

A good pull request should include:

- what changed
- why it changed
- any assumptions made
- any follow-up work still pending
