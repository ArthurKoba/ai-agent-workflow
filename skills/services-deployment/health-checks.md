# Service Health, Readiness and Functional Acceptance

**Load for all new long-running services**, and when evaluating deployment health, restart loops or missing consumer-facing results. For Coolify Compose Applications and Services, define checks in each relevant `docker-compose.yaml` service or its Dockerfile, **not** the non-Compose Coolify Healthcheck page. Include them in the effective Coolify `extends` output. Do not require always-running health for one-shot bootstrap/migrations; gate their successful completion instead, and confirm whether Coolify supports `exclude_from_hc: true` for their lifetime.

## Three independent signals

1. **Liveness:** the process is alive and can make forward progress. A running container, open port or HTTP 200 from a trivial endpoint is weak evidence by itself. Fail sustained unrecoverable process deadlocks; avoid restart storms on transient remote outages.
2. **Readiness:** required local configuration and dependencies permit the component to serve its real consumers. Check relevant service-specific prerequisites without depending on optional or flaky external systems. When a dependency is required, represent startup/order with a supported health/completion gate and verify fresh and repeated deploy.
3. **Functional delivery:** a scoped operation or observed output proves the service's mission. For telemetry, a healthy collector/exporter is not proof of successful remote_write or fresh samples in the destination. Check bounded delivery errors/backlog and query recent expected samples from the authorized backend. For other systems use a consumer-visible API, queue receipt, DB query or authorization flow. This acceptance test may be external and need not be encoded as a rapid container healthcheck.

## Compose probe example

Use an **existing** checker supplied by the image or application; the following is a shape, not a working command for arbitrary images:

```yaml
healthcheck:
  test: ["CMD", "/app/bin/healthcheck"]
  interval: 30s
  timeout: 5s
  start_period: 30s
  retries: 3
```

## Probe contract

- For each long-running Compose service, define an executable `healthcheck` when the image/runtime supports it. The checked binary/endpoint **must exist inside the final image** and return failure on genuine unhealthy state. Choose documented `interval`, `timeout`, `retries` and `start_period` based on startup and expected recovery; never apply one arbitrary default to everything.
- Probe without credentials in URLs, response bodies, logs or world-readable scripts. Use least-privileged internal endpoints. Healthchecks must be bounded, lightweight and side-effect-free; never execute a migration, register a user or mutate durable state to test health.
- Distinguish optional/degraded downstreams from mandatory readiness; use separate operational alerts for missed telemetry or external delivery rather than killing a healthy collector every time the network blips. Review restart policies and avoid `unhealthy` loops that erase diagnostics.
- Compose `depends_on: condition: service_healthy` / `service_completed_successfully` gates startup only where the deployed parser/runtime supports them; they do not prove continuous multi-service readiness. Do not invent cross-resource `depends_on` guarantees.
- Test healthy, intentionally failing and recovering states; verify effective Docker health status, Coolify routing/readiness behavior and real-consumer acceptance separately. `running:unknown` means health is **unverified**, not success or failure. Record unsupported probes and require another observable acceptance signal; do not silently omit checks.

## Ownership and scope

Document probe owner, condition, check frequency/recovery budget and where functional-delivery evidence is collected in the deployment README. Checks are part of the base Compose/image so deployments remain portable; Coolify-specific overrides only when the parser requires them. Include the probe in tested presets for future AI Agent Workflow examples. This skill does not authorize changes to already deployed resources; add probes with reviewed rollout and rollback.
