# Service Engineering

Use for services, deployment, networking, hosts, runtime maintenance and infrastructure-facing work.

## Sub-map
- terminal/remote execution → `../terminal-operations/README.md`
- infrastructure/tooling architecture → `../../docs/MCP_STRATEGY.md`
- source/config changes → `../software-engineering/README.md`
- independent review → `../code-review/README.md`

## Principles
- Discover actual runtime/service topology before changing it.
- Prefer the existing service manager/orchestrator over a second control path.
- Keep environment-specific hosts/paths/credentials in project/local context.
- Make operational changes reversible when practical.
- Distinguish source/config change from deployment/runtime change.
- Validate the service from the same surface the real consumer uses.
