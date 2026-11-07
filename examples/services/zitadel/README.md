# ZITADEL infrastructure presets

Two alternative Git-backed patterns. In Coolify they use **Coolify's integrated Traefik proxy** directly: **no Caddy, no gateway sidecar**. The ZITADEL API requires h2c for HTTP/2/gRPC traffic, while Login V2 is normal HTTP; the Coolify entrypoint supplies two explicit Traefik routers for one operator-configured domain.

| Variant | Services | Dependencies |
| --- | --- | --- |
| `standalone/` | `postgres`, `valkey`, `zitadel-api`, `zitadel-login` | Own private volumes / network |
| `shared/` | `zitadel-api`, `zitadel-login` | Existing private PostgreSQL or PgBouncer and Valkey, separate identities / cache indexes |

**Verified deployment pattern:** The standalone topology and direct Traefik routes reached `running:healthy` in Koba Coolify v4.5.3 on 2026-11-02, with public OIDC discovery, JWKS and Login V2 HTTP 200; **the shared-dependency variant has not been runtime deployed**. `SERVICE_URL_ZITADEL_API_8080: /` remains the only Coolify public domain mapping. Because Coolify 4.5.3 did not supply `SERVICE_FQDN_ZITADEL_API_8080` to Compose build interpolation even when Domains contained a DNS-valid hostname, the portable presets require a single explicit `ZITADEL_PUBLIC_DOMAIN` input (hostname without `https://` or port) in their Resource ENV, matching the real `zitadel-api:8080` Coolify HTTPS domain. Never use the SigNoz or another app host as identity issuer. The explicit API router has priority 100 and uses Traefik `h2c` to port 8080; the Login route matches `/ui/v2/login` with priority 200 to port 3000. Coolify generates additional routers; verify the priority, routing labels, proxy networks, TLS certificate handling, and effective hostname on the **actual** version. Two deployments sharing a Docker provider must not reuse the same custom Traefik router/service names; isolate or uniquely namespace the labels before co-deploying instances on one proxy.

**Coolify-version caveat:** Some versions materialize the port-suffixed `SERVICE_FQDN_ZITADEL_API_8080` as `host:8080`, not a bare host. Never use it as the ZITADEL issuer, forwarded `Host`, Login URL or Traefik `Host()` matcher. On a version that supplies a correct, current `SERVICE_FQDN_ZITADEL_API` matching Domains, an owning deployment may derive the hostname automatically while retaining the `*_8080` mapping for routing. First verify actual Deployable Compose and issuer; do not silently replace the explicit domain input in this 4.5.3-validated example.

Unlike the former embedded gateway, there is no rewrite of `/api/*`, no root redirect, and no implicit public diagnostic-path filter. Verify public API route compatibility, ensure internal diagnostics are not accessible, and implement a reviewed narrow deny mechanism if necessary before using this for real identities. Do not assume the external Traefik proxy sanitizes application routes. A bare Docker Compose deployment now requires an independently configured public ingress satisfying the same h2c and path routing; Coolify-specific labels stay in the Coolify entrypoint.

ZITADEL's Redis-compatible cache (beta) is enabled for `Instance`, `Milestones` and `Organization`. `DBOffset` selects logical DB indexes (a Redis URL ending in `/0` does not); never share those indexes with other consumers. ZITADEL may execute `FLUSHDB`. Shared Valkey requires non-overlapping reserved indexes, correct ACL and actual network evidence.

Keep ZITADEL master key, bootstrap administrator credential, login session secret and PostgreSQL/Valkey credentials in restricted, independent bootstrap/recovery storage, not in Git. A single identity root must not depend on its own login for recovery. Copy an approved variant into the owning infrastructure repository and watch only its owned files; do not attach production to the public catalog's moving HEAD.

See `standalone/README.md`, `shared/README.md` and `VALIDATION.md` for operator inputs, parser gates and acceptance.
