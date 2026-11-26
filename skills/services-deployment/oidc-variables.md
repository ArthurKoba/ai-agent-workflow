# OIDC / OAuth Client and Resource Server Configuration

Load for OAuth/OIDC clients, login, token verification and deployment keys. Standards define protocol fields, not ENV names. Apply [ENV ownership](environment-policy.md), [credential naming](credential-variables.md) and [scope](variable-glossary.md); preserve upstream SDK/image names. Provider deployment → [identity scenario](scenario-identity.md).

## Operator inputs

| Key | Purpose / condition | Placement |
| --- | --- | --- |
| `OIDC_ISSUER_URL` | Exact trusted HTTPS issuer, including realm/path | Non-secret; Shared if common, explicit reference per consumer |
| `OIDC_CLIENT_ID` | Registered client | Non-secret; client owner/resource |
| `OIDC_CLIENT_SECRET` | Confidential client using secret authentication | Protected secret |
| `OIDC_CLIENT_PRIVATE_KEY` | Client authentication (`private_key_jwt`), not provider signing | Protected secret/file |
| `OIDC_AUDIENCE` | Independent API audience, not necessarily login client ID | Resource server, non-secret |
| `OIDC_ROLES_ORGANIZATION_ID` | External organization ID if authorization is organization-bound | Resource-specific, non-secret |

Pure OAuth: `OAUTH_ISSUER_URL`, `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET` or `OAUTH_CLIENT_PRIVATE_KEY` as applicable. No parallel OIDC/OAUTH aliases for one identity/issuer. Non-discoverable providers may need explicit endpoints. Name credentials by registered identity, not OAuth operations (introspection, exchange, revocation). One client uses `OIDC_CLIENT_ID` and its selected credential, even for introspection only. Qualify independent identities when they coexist in a resource or Shared scope. Never merge registrations or privileges for naming. Required inputs have no fabricated defaults. Admin/provisioning credentials are independently scoped, not reused from login/introspection.

## Scenarios

| Scenario | Minimal inputs, subject to provider contract |
| --- | --- |
| Public web/SPA/native, code + PKCE or supported device grant | Issuer + client ID; no secret |
| Confidential web/BFF, code + PKCE | Issuer + client ID + secret/private key |
| API/Gateway/MCP, JWT validation | Issuer + independent audience if needed; no secret for JWKS |
| API, RFC 7662 introspection | Issuer + audience policy + client ID and credential if required |
| OAuth machine-to-machine | OAuth issuer/endpoint + client ID + credential; client credentials, not user login |
| Generic multi-provider integrations | Per-connection registration, scopes, credentials and tokens |

## Application-owned, derived and runtime values

- Scopes are request policy, **not standard deployment ENV**. Do not expose `OIDC_SCOPES`/`OAUTH_SCOPES` by default. Build minimal scopes per operation; OIDC login requires `openid`; request `profile`, `email`, `offline_access` only for actual consumers. Provider adapters derive audience/role scopes from approved external IDs. Verify granted scopes; seek additional authorization when needed. Store configurable scopes per connection; ENV overrides require genuine operator ownership.
- Discover supported authorization, token, JWKS, UserInfo, introspection, revocation, logout, registration and device endpoints from trusted metadata. Verify issuer equality and TLS. Endpoint overrides require documented interoperability need.
- Derive redirect and post-logout URIs from verified public origin and owned routes; separate ENV only for independent addresses. Register exact URIs. Distinguish local logout from provider session termination.
- Grant type, PKCE S256, auth method, JWT algorithm allowlist, verification strategy, claim paths and role formats belong to reviewed code/configuration or provider adapters. Deployment selectors require supported alternatives with actual operator lifecycle. No production TLS/auth bypass or test HTTP switch.
- Generate state, nonce, PKCE verifier and client assertions at runtime. Access, refresh and ID tokens and sessions belong in protected runtime storage, not static ENV.

## Acceptance

Use maintained libraries. Verify discovery, issuer/redirects, state/nonce/PKCE, signature, audience, lifetime and authorization. Never authorize APIs with ID tokens. Introspection requires active tokens and resource checks. MCP: publish protected resource metadata and verify resource-bound access tokens. Test refresh, logout and denied cases as applicable. Migrate keys, consumers and secret references together; remove aliases after verified cutover. No live rename without approval.

References: [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html), [Discovery](https://openid.net/specs/openid-connect-discovery-1_0.html), [OAuth security BCP](https://www.rfc-editor.org/rfc/rfc9700), [scopes](https://www.rfc-editor.org/rfc/rfc6749#section-3.3), [introspection](https://www.rfc-editor.org/rfc/rfc7662), [resource metadata](https://www.rfc-editor.org/rfc/rfc9728).
