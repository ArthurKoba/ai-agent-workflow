# Coolify Networking and Public Routing

Load when a deployment uses shared networks, domains or external access. For related frontend/backend/dependencies prefer a private shared network **per environment**, verifying actual membership. Keep a resource's private networks when they enforce a real trust boundary. The Destination label alone does not prove network attachment.

## Internal vs external networking

### Coolify destinations and Compose network ownership

- **Destination selection is not Compose attachment.** A Destination has a display **Name** and a separate, actual Docker **Network**. Git-backed Docker Compose applications use their resource-specific network by default; enable **Advanced → Docker Compose → Connect To Predefined Network** for each resource that must also join its selected Destination.
- Let Coolify inject the selected Destination's actual network into the generated deployment Compose. Do not hard-code the Destination's display name as an `external: true` Compose network or invent another shared network merely to mirror a UI selection. Explicit Compose network management needs a separate approved ownership reason.
- Verify the actual Docker Network exists on the target host, the enabled setting, generated network declarations, container membership and cross-resource DNS/port reachability. A Destination record alone does not prove that Docker created its network. On missing-network errors, diagnose the Destination/network provisioning path before modifying Compose; check health-gated startup behavior in the deployed parser version.

Internal traffic should stay internal.

Prefer:

```text
api -> postgres:5432
collector -> exporter:9550
frontend -> backend:8080
```

over host/LAN hairpins such as:

```text
api -> 192.168.x.x:5432
collector -> host-ip:9550
```

Rules:

- use Docker service DNS and fixed container ports for internal communication;
- use `expose:` to document/discover internal ports when useful;
- use `ports:` only when a host or external consumer really needs the port;
- do not publish metrics/admin/debug endpoints merely because another container consumes them;
- mutable remote hosts, cross-server targets, bind addresses and externally meaningful ports belong in required runtime variables.

## Public-route inventory before generating domains

Before supplying Coolify Application settings, derive the public/private route inventory from the **accepted product/API contract**, not from whichever containers happen to exist or which endpoints are currently mounted. For each intended route identify its owner Compose service, externally used hostname/protocol, internal listener port, consumer, and activation/security prerequisite. If OAuth and MCP use separate ingress, identify public issuer/discovery/login/token routes separately from the MCP gateway. A health-only stub does **not** satisfy the required OAuth route, and a not-yet-active public service must not be mistakenly classified as permanently internal. Do not expose the private identity/data owner merely because it participates in authentication.

## Generated domains

Coolify declares managed public routes with version-supported `SERVICE_FQDN_*` / `SERVICE_URL_*` ENV magic variables (for example `SERVICE_FQDN_APP_8080: /` for service `app` exposed on port 8080). Match the **actual service name**, normalize separators to underscores, and target the intended internal port. Declare under the owner service's `environment:` in Coolify-parsed Compose; `extends` may require an explicit override for discovery. Do not invent magic variants, manually populate managed keys or use conflicting ordinary `SERVICE_*` keys. Confirm behavior against the deployed parser.

Generated domains are **service-keyed**: two independently editable domains/ports may not coexist under one service. When the parser permits only one domain per service, expose separate lightweight ingress adapters mapping each public HTTP route to the appropriate private listener; never grant them unrelated capabilities. Validate domain count, owner, internal ports and stale state on a fresh parser resource.

### Generated application URL (preferred)
If the app's public origin **equals a Coolify-managed route**, prefer `SERVICE_URL_<SERVICE>_<PORT>` (scheme included) over a separate Required URL:

```yaml
environment:
  SERVICE_URL_APP_8080: /
  APP_EXTERNAL_URL: ${SERVICE_URL_APP_8080}
```

`SERVICE_FQDN_*` is hostname-only. Map to the app's actual key (e.g. `SITE_URL`) only if consumed; use a separate URL only if the origin differs or an approved fallback is required.

**Parser gate:** Git-backed Coolify 4.4.1 sometimes interpolated `${SERVICE_URL_*}` before generation, leaving the app URL empty despite a working domain. Verify generated route, Deployable Compose **and resolved container URL/issuer**; HTTP 200 alone is insufficient. If wrong or empty, stop and diagnose, then seek approval for a verified fallback—do not silently add a manual Required URL.
