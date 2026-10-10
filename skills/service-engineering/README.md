# Service Engineering

Use for services, deployment, networking, hosts, runtime maintenance and infrastructure-facing work.

## Sub-map
- Docker/Compose/container packaging → `docker-compose.md`
- Coolify-parsed Docker Compose → `coolify-compose.md` (mandatory when Coolify owns parsing/deployment)
- Git-backed infrastructure / orchestrator-owned deployments → `git-backed-infrastructure.md`
- reusable service deployment presets/examples → `../../examples/services/README.md`
- terminal/remote execution → `../terminal-operations.md`
- infrastructure/tooling architecture → `../../docs/MCP_STRATEGY.md`
- source/config changes → `../software-engineering/README.md`
- independent review → `../code-review.md`

## Principles
- Discover actual runtime/service topology before changing it.
- Prefer the existing service manager/orchestrator over a second control path.
- Keep environment-specific hosts/paths/credentials in project/local context.
- Make operational changes reversible when practical.
- Distinguish source/config change from deployment/runtime change.
- Validate the service from the same surface the real consumer uses.
- Before a substantial deployment redesign, freeze the acceptance invariants: deployment entrypoint, steady-state topology, privilege/trust boundary, persistence/backup authority, allowed manual steps and required validation level.
- Model materially different lifecycle states before rollout: clean install, repeat deploy, partial/stale state, restart/reboot, upgrade/migration and rollback. A local deployment failure may change implementation, not silently redefine the accepted architecture.
- When integrating a third-party service, inspect its supported installer/runtime/source ownership before reproducing enrollment, service lifecycle, backend probing, persistence or upgrade policy in custom bootstrap code.
