# OpenVPN Gateway Reference Preset

Status: **validated deployment pattern; endpoint-specific tunnel acceptance required**.

This preset runs a standard OpenVPN client in Docker host-network mode so routes
installed by the VPN are visible in the host network namespace. It is useful
when host workloads, sibling Docker applications, or selected LAN clients need
access to a private network without putting every consumer inside the VPN
container namespace.

The preset is intentionally small. The orchestrator remains the operator UI for
start/stop/redeploy/logs and for storing the private OpenVPN profile.

## Architecture

```text
host workloads / Docker workloads
              |
              v
       Linux host routing
              |
          openvpn0
              |
              v
       private network

optional LAN client
      |
      v
LAN router -> Linux host -> openvpn0
```

The service uses:

- `network_mode: host`;
- `NET_ADMIN`;
- `/dev/net/tun`;
- a Coolify/orchestrator-managed `.ovpn` file;
- a Unix-domain OpenVPN management socket for health reporting;
- optional forwarding/NAT for one LAN CIDR.

It does **not** expose a public HTTP endpoint or management TCP port.

## Files

- `docker-compose.yaml` — reusable service definition.
- `Dockerfile` — minimal Alpine/OpenVPN runtime.
- `entrypoint.sh` — profile normalization, auth-file support, route guard and optional LAN forwarding.
- `COOLIFY.md` — Git-backed Coolify deployment contract.
- `VALIDATION.md` — acceptance levels and lessons learned from the reference deployment.

## Private profile ownership

The real OpenVPN client profile is never stored in Git.

The Compose file declares a managed file at:

```text
/etc/openvpn/client.ovpn
```

The inline content is only a bootstrap placeholder. Replace it in the
orchestrator's managed file storage after the resource is parsed.

Profiles may contain certificates, private keys, tokens, remote addresses or
other sensitive/environment-specific values. Treat the complete file as a
secret-bearing runtime artifact.

## Authentication

The profile may be fully self-contained.

If it contains `auth-user-pass` and expects non-interactive credentials, set
both of these as runtime secrets:

```text
OPENVPN_USERNAME
OPENVPN_PASSWORD
```

The entrypoint writes them to a private temporary file under `/run` and passes
that file to OpenVPN. If the profile does not require separate credentials,
leave both variables empty.

## Route policy

The preset is a **split-tunnel gateway**, not a full-tunnel client.

It removes a local `redirect-gateway` directive and ignores a server-pushed
`redirect-gateway`. It also rejects an observed default route change or
default-equivalent `/1` routes through the configured tunnel device.

This is defense-in-depth, not a general route allowlist: non-default routes
pushed by the trusted VPN server are accepted. Runtime acceptance must inspect
the actual installed routes before other hosts depend on this gateway.

If a deployment requires a strict route allowlist, use an environment-specific
policy such as `route-nopull` plus explicit approved routes rather than silently
broadening this preset.

## Optional LAN gateway mode

Leave `OPENVPN_GATEWAY_LAN_CIDR` empty when only the host and its workloads need
the VPN.

To let LAN clients use the gateway:

1. set `OPENVPN_GATEWAY_LAN_CIDR` to the allowed source LAN;
2. ensure host IPv4 forwarding is enabled;
3. add only the required private destination route(s) on the LAN router with
   this Linux host as next hop.

The entrypoint adds source-limited forwarding rules and masquerades that LAN
traffic only when the variable is non-empty.

Do not make this host the LAN default gateway merely to reach one private
service.

## Health

A TUN interface can exist while OpenVPN is still reconnecting. Therefore the
healthcheck does not test only for `openvpn0`.

The service uses OpenVPN's management interface over a container-local Unix
socket and reports healthy only when the management state is
`CONNECTED,SUCCESS`. OpenVPN documents Unix-domain management sockets as an
appropriate local control surface and exposes the `state` command specifically
for connection-state inspection.

## Security boundary

Host networking plus `NET_ADMIN` means this container can modify the host
network namespace. That capability is intentional and should not be copied to
ordinary application containers.

The preset does not use `privileged: true`, does not mount the Docker socket,
and does not expose the OpenVPN management interface over TCP.

Because the container can affect host routes/firewall state, preserve a
known-good host-network recovery path before deploying it on a critical server.

## Acceptance

Do not call a deployment accepted until the relevant gates pass:

- Coolify/orchestrator parses the Compose resource correctly;
- the managed profile file is materialized at the intended path;
- the Watch paths contract is present for Git-backed deployment;
- runtime-only variables are not unnecessarily exposed at build time;
- the OpenVPN management state reaches `CONNECTED,SUCCESS`;
- the host default route remains unchanged;
- only intended private routes use the VPN tunnel;
- the real host workload can reach the intended private service;
- if LAN forwarding is enabled, a LAN client reaches only the intended private route through the gateway;
- restart/redeploy restores the same routing behavior.

## References

- OpenVPN 2.6 manual: https://openvpn.net/community-docs/community-articles/openvpn-2-6-manual.html
- OpenVPN management interface: https://openvpn.net/community-docs/management-interface.html
