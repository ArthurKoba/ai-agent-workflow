# ZITADEL acceptance — before deployment or production use

These are **source-level presets** until the target Coolify parser, container images, Caddy routing and ZITADEL/Valkey integration are tested.

- **Structure:** standalone Compose resolves `postgres`, `valkey`, `zitadel-api`, `zitadel-login`, `gateway` and three volumes; shared resolves API/Login/gateway only with the `zitadel-bootstrap` volume. No Postgres or Valkey host ports in either.
- **Coolify:** parser preserves `extends`, volumes and repository-backed `Caddyfile`; one generated gateway FQDN; no manually entered public URL. Effective `ZITADEL_EXTERNALDOMAIN`, HTTPS issuer/login redirects, `CUSTOM_REQUEST_HEADERS` and `ExternalSecure` must match the actual generated route. Blank or unresolved generated values are a release blocker.
- **Readiness:** PostgreSQL and Valkey healthcheck pass before standalone API; login starts only after API ready. For shared, the external DB/pooler/Valkey must be reachable and provisioned before starting the ZITADEL resource. Exercise cold and repeated deployment, not just one container restart.
- **Caching:** check `ZITADEL_CACHES_CONNECTORS_REDIS_ENABLED=true`, Redis cache URL reachable and the `Instance`, `Milestones`, `Organization` connectors truly serving requests. Test cache invalidation and temporary Valkey failure/circuit breaker. Inspect the configured `DBOffset`, actual selected DB indexes, ACL permissions and absence of conflicts with Infisical/VPN Core; `FLUSHDB` must not touch another application's keys.
- **Identity:** complete initial admin setup, reach issuer discovery/JWKS/login via HTTPS, perform a real OIDC login and logout with a test client, and test API calls requiring h2c routing. Console loading alone is not proof of correct integration.
- **Recovery:** back up/restore actual PostgreSQL physical volume/DB, bootstrap Login PAT material and master key. In shared mode coordinate backup with the dependency owner. Upgrades can migrate schema; a Git revert is not a data rollback. Never print or save private keys, secrets or PAT plaintext as test evidence.

Document real runtime results in the private deployment repository. Publication of these files is **not** evidence of runtime or production readiness.
