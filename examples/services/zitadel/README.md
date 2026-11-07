# ZITADEL infrastructure presets

Two alternative Git-backed patterns. In Coolify they use **Coolify's integrated Traefik proxy** directly: **no Caddy, no gateway sidecar**. The ZITADEL API requires h2c for HTTP/2/gRPC traffic, while Login V2 is normal HTTP; the Coolify entrypoint supplies two explicit Traefik routers for one operator-configured domain.

| Variant | Services | Dependencies |
| --- | --- | --- |
| `standalone/` | `postgres`, `valkey`, `zitadel-api`, `zitadel-login` | Own private volumes / network |
| `shared/` | `zitadel-api`, `zitadel-login` | Existing private PostgreSQL or PgBouncer and Valkey, separate identities / cache indexes |

**Historical deployment evidence:** On 2026-11-02, Koba Coolify v4.5.3 reached `running:healthy` with public OIDC discovery, JWKS and Login V2. That deployment used an explicit pinned hostname because its parser did not supply a working FQDN during Compose interpolation. The updated reusable manifests use Coolify's **portless** `SERVICE_FQDN_ZITADEL_API` for the issuer. This newer template has **not** been runtime-accepted on v4.5.3, and the shared-dependency variant has never been runtime deployed.

Both generic examples use `SERVICE_FQDN_ZITADEL_API_8080: /` only to declare the HTTPS route for `zitadel-api:8080`. Its generated value may include `:8080`; never pass that port-qualified value to `ZITADEL_EXTERNALDOMAIN`, Login V2 URLs, forwarded `Host` or Traefik `Host()` labels. Instead those fields consume `${SERVICE_FQDN_ZITADEL_API:?}`, matching the **same** domain assigned in Coolify Domains. Do not set another `ZITADEL_PUBLIC_DOMAIN` input. Fail closed if the portless FQDN is missing or stale: don't hardcode a hostname or invent another secret. The API router uses h2c on port 8080 (priority 100), and Login uses port 3000 for `/ui/v2/login` (priority 200); check proxy networks and TLS routing on the target Coolify version.

Unlike the former embedded gateway, there is no rewrite of `/api/*`, no root redirect, and no implicit public diagnostic-path filter. Verify public API route compatibility, ensure internal diagnostics are not accessible, and implement a reviewed narrow deny mechanism if necessary before using this for real identities. Do not assume the external Traefik proxy sanitizes application routes. A bare Docker Compose deployment now requires an independently configured public ingress satisfying the same h2c and path routing; Coolify-specific labels stay in the Coolify entrypoint.

ZITADEL's Redis-compatible cache (beta) is enabled for `Instance`, `Milestones` and `Organization`. `DBOffset` selects logical DB indexes (a Redis URL ending in `/0` does not); never share those indexes with other consumers. ZITADEL may execute `FLUSHDB`. Shared Valkey requires non-overlapping reserved indexes, correct ACL and actual network evidence.

Keep ZITADEL master key, bootstrap administrator credential, login session secret and PostgreSQL/Valkey credentials in restricted, independent bootstrap/recovery storage, not in Git. A single identity root must not depend on its own login for recovery. Copy an approved variant into the owning infrastructure repository and watch only its owned files; do not attach production to the public catalog's moving HEAD.

See `standalone/README.md`, `shared/README.md` and `VALIDATION.md` for operator inputs, parser gates and acceptance.
