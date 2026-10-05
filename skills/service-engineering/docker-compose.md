# Docker / Compose Engineering

Use this module for Dockerfiles, Docker Compose manifests, container runtime configuration and registry-based deployment packaging.

## Ownership

- Follow the repository's established orchestrator first. Do not introduce Compose where Kubernetes, Nomad, Coolify-managed templates or another owner is already authoritative.
- Use Compose when the project already uses it or when one reproducible multi-container definition is the natural local/service contract.
- Keep environment-specific hosts, registry coordinates, secrets and deployment topology in project/local context.

## Compose files

- Prefer the repository's established filename and extension. If no convention exists, modern Compose commonly uses `compose.yaml` or `docker-compose.yaml`; do not rename an existing working convention merely for style.
- Define services, networks and persistent volumes declaratively when they are part of the reproducible runtime topology.
- Use named volumes for durable container-managed data when host-path ownership is not required.
- Use explicit networks only when topology/isolation requires them; do not add decorative networks.
- Parameterize environment-dependent values through the project's configuration contract instead of hard-coding production values.

## Environment and secrets

- Do not commit real `.env` files or plaintext secrets.
- A tracked `.env.example`/template may document required variable names and safe example values when that is the project's convention.
- Secret values should come from the declared secret/provider/runtime surface rather than being embedded in Compose, Dockerfile layers or image metadata.
- Validate required runtime variables explicitly when missing values would produce an unsafe or misleading deployment.

## Images and builds

- Production/release deployment should normally consume a reproducible published image rather than rebuilding source ad hoc on the target host.
- Pin image tags/digests according to the project's release policy; immutable digests are preferred where release provenance matters.
- Keep development `build:` flows separate from production image-selection semantics when both are supported.
- Multi-stage builds should keep build toolchains and unnecessary artifacts out of the runtime image.

## Runtime behavior

- Use health/readiness checks when another service/orchestrator needs a machine-readable availability contract.
- Make restart behavior explicit when process recovery semantics matter.
- Avoid privileged mode, host networking, broad device mounts or writable host paths unless the service contract requires them.
- Do not add a second reverse proxy/service manager/control path when the project already has one.

## Operations

Use the project's supported Compose/runner commands. Typical Compose operations are:

```text
docker compose up -d
docker compose down
docker compose logs -f <service>
docker compose pull
docker compose up -d --remove-orphans
```

These are examples, not commands to emit blindly. Human-operated commands still require `terminal-operations/README.md` and the active project/local execution contract.

## Validation

Before calling a container change ready, verify the level relevant to the change:

- manifest/config parses;
- image builds when build logic changed;
- declared mounts/networks/env resolve as intended;
- service starts under the real orchestrator/runtime;
- health/readiness and consumer-facing behavior work from the intended surface;
- rollback/redeployment remains possible for production-facing changes.
