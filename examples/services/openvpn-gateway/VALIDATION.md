# OpenVPN Gateway validation history

This preset preserves a deployment pattern that was exercised through a
Git-backed Coolify resource. The result is useful as a reusable reference, but
the private VPN endpoint and target-network acceptance are environment-specific
and are not part of this public preset.

## Demonstrated levels

The reference work demonstrated:

- source/config structure under `deploy/coolify/<service>/`;
- Git-backed Coolify parsing;
- Coolify-managed file materialization for `/etc/openvpn/client.ovpn`;
- narrow Watch paths triggering service-local redeploy;
- host-network OpenVPN startup;
- non-interactive `auth-user-pass` support through runtime secrets;
- OpenVPN management-socket health reporting.

It did **not** establish a portable claim that an arbitrary private VPN endpoint,
profile or downstream service will be reachable. That remains deployment
acceptance.

## Lesson 1 — TUN existence is not connection health

An early healthcheck treated the presence of the TUN device as healthy.

That is insufficient: a client may create or preserve a TUN device while it is
still polling/reconnecting and has not completed the OpenVPN initialization
sequence.

The final pattern uses the OpenVPN management interface and requires:

```text
CONNECTED,SUCCESS
```

This is why the image includes `socat` and the entrypoint exposes only a local
Unix-domain management socket.

## Lesson 2 — interactive auth fails in unattended containers

A profile containing bare `auth-user-pass` can cause OpenVPN to prompt for
credentials on a TTY. An unattended Coolify container has no interactive TTY, so
that configuration fails before a connection can be established.

The preset supports optional runtime-only `OPENVPN_USERNAME` and
`OPENVPN_PASSWORD` values and converts them into a temporary two-line auth file
under `/run`.

Profiles that already provide their own non-interactive authentication do not
need these variables.

## Lesson 3 — managed profile content belongs outside Git

The OpenVPN profile is treated as a secret-bearing runtime file. Coolify's
managed File Storage is the authority for its real content.

The Git inline file content exists only to make the mount parseable and
recoverable.

## Lesson 4 — Watch paths are deployment behavior

For a monorepo/multi-service infrastructure repository, a missing Watch paths
value couples unrelated commits to this service.

The validated pattern uses one repository-relative service path, for example:

```text
deploy/coolify/openvpn-gateway/**
```

When deploying the public preset directly:

```text
examples/services/openvpn-gateway/**
```

A webhook-triggered redeploy after a service-local commit is part of acceptance.

## Lesson 5 — host networking is a deliberate capability boundary

The gateway needs the VPN route in the host namespace so ordinary host/Docker
consumers can use it. Therefore host networking is intentional.

This also means `NET_ADMIN` and iptables changes operate on the host network
namespace. The preset avoids `privileged: true` and limits its own forwarding
rules to the configured LAN source CIDR, but the deployment must still be
treated as infrastructure code rather than an ordinary application container.

## Route acceptance

The preset blocks `redirect-gateway` and checks for an observed default route or
default-equivalent `/1` routes on the tunnel.

This is not a complete pushed-route allowlist. Before declaring a deployment
accepted, inspect the actual private routes installed by the connected profile.
If strict allowlisting is required, use a deployment-specific `route-nopull`
policy and explicit routes.

## Compatibility notes

OpenVPN 2.6 negotiates data-channel ciphers through `data-ciphers`; old profiles
that only specify `cipher` may emit compatibility/deprecation warnings or need
server/profile modernization. Do not globally rewrite crypto policy in this
preset because compatibility belongs to the specific VPN endpoint.

OpenVPN compression directives are also endpoint/profile policy and should be
reviewed independently rather than normalized automatically by this wrapper.

## Final acceptance checklist

A concrete deployment is accepted only when:

1. the Git-backed resource has the correct base directory, relative Compose
   location and mandatory Watch paths;
2. the private profile exists only in managed runtime storage;
3. runtime-only variables have Buildtime disabled;
4. the management state reaches `CONNECTED,SUCCESS`;
5. the host default route is unchanged;
6. the intended private routes are present;
7. the real host/Docker consumer reaches the target service;
8. optional LAN forwarding, when enabled, works through only the intended route;
9. stop/redeploy restores the expected host routing/firewall state.
