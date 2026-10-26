# Service Presets

Reusable, sanitized service deployment templates owned by AI Agent Workflow. This catalog is an upstream **example source**, not a mutable production deployment repository. Use `../../skills/services-deployment/README.md` to select relevant deployment rules.

## New preset contract

Each new Compose-based preset should provide both platform-neutral `docker-compose.yaml` and Coolify-aware `docker-compose.coolify.yaml` (`.yaml`, four letters). The owning README (which may cover several nested service directories) explains product/setup, prerequisites, required inputs, network/storage ownership, bootstrap and recovery; add `COOLIFY.md` or `VALIDATION.md` only when complexity justifies them. Compose inheritance / `include` / `extends` must be tested with the targeted parser; a filename alone does not prove effective merge or generated Coolify state. No real credentials, private domains, IPs, host paths, tokens or resource IDs.

Classify presets by ownership and lifecycle: a shared infrastructure identity provider and a dedicated application identity provider are separate reusable scenarios. Group stable dependencies where their lifecycle permits; do not prescribe a container-per-resource split.

## Distribution and improvement

Copy a vetted preset into the owning infrastructure or application repository's `deploy/` hierarchy; record its source revision, make environment-specific adaptations there and point Coolify Watch Paths at those **owned copies**. Never have production follow this catalog's moving HEAD. Changes to the catalog must not implicitly redeploy a dependent infrastructure. Upstream updates are deliberate diffs with review, migration and runtime acceptance. When project work reveals a reusable improvement, contribute a generalized, non-sensitive correction and evidence back here.

Existing proven presets below remain supported in their established, **single-Compose** form until each is separately migrated and validated. Do not bulk-rename or force a second Compose file into a validated deployment merely to satisfy the new-preset layout.

## Existing presets

- `jenkins/` — Jenkins controller with dedicated inbound builder and isolated TLS-protected Docker-in-Docker daemon.
- `openvpn-gateway/` — host-network OpenVPN client gateway with orchestrator-managed profile storage and connection health.
- `zoomies/` — Zoomies 1.3.4 rootless controller + embedded-agent preset, with verified clean deployment and DinD behavior.

## Candidate examples (not yet validated or published)

- Shared infrastructure ZITADEL and service-owned ZITADEL, each with its own resource, network, secrets and upgrade/rollback contract.
