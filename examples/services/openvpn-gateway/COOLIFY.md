# Deploy OpenVPN Gateway through Coolify

Use a **Git-backed Docker Compose Application**.

## Git-backed resource

When deploying this preset directly from `ai-agent-workflow`:

```text
Base directory: /examples/services/openvpn-gateway
Docker Compose location: /docker-compose.yaml
Watch paths: examples/services/openvpn-gateway/**
```

If the preset is copied into another infrastructure repository, change the base
directory and Watch paths to that service directory. Keep the Compose location
relative to the base directory.

For Git-backed Coolify resources the Watch paths value is mandatory. It should
be repository-relative and narrow enough that unrelated commits do not rebuild
this gateway.

No public domain is required.

## Managed OpenVPN profile

After Coolify parses the Compose file, verify that File Storage contains:

```text
/etc/openvpn/client.ovpn
```

Replace the bootstrap placeholder with the private client profile.

Do not put the real profile in Git, a Docker image layer, README text or a normal
non-secret environment variable.

Existing Coolify File Storage content at the same mount path takes precedence
over the Git inline bootstrap content on later reparses. Treat the inline
`content:` block as recovery/bootstrap material, not continuous file
synchronization.

## Environment variables

The reusable defaults are:

```text
TZ=UTC
OPENVPN_TUN_DEVICE=openvpn0
OPENVPN_GATEWAY_LAN_CIDR=
OPENVPN_USERNAME=
OPENVPN_PASSWORD=
```

Recommended Coolify handling:

- `TZ`: Runtime only; optionally point it at the appropriate shared variable.
- `OPENVPN_TUN_DEVICE`: Runtime only; keep `openvpn0` unless the host requires another name.
- `OPENVPN_GATEWAY_LAN_CIDR`: Runtime only; leave empty unless LAN forwarding is intentionally enabled.
- `OPENVPN_USERNAME`: Runtime only and Secret when used.
- `OPENVPN_PASSWORD`: Runtime only and Secret when used.
- Buildtime: disable for all of the above; none is required to build the image.
- Preview: configure only if preview deployments are actually used.

Coolify may initially materialize Compose variables with broader flags than the
consumer needs. Verify the persisted flags after the first parse instead of
accepting generated defaults blindly.

## Host requirements

The target host must provide:

- Linux TUN support and `/dev/net/tun`;
- Docker host-network mode;
- permission for the container to receive `NET_ADMIN`;
- IPv4 forwarding only when LAN gateway mode is enabled.

This preset intentionally uses host networking because the VPN routes must be
visible to host workloads and other containers using ordinary Docker egress.

## LAN routing

For host-only use, leave `OPENVPN_GATEWAY_LAN_CIDR` empty.

For LAN gateway mode:

1. set the source LAN CIDR;
2. confirm `net.ipv4.ip_forward=1` on the host;
3. connect the VPN and discover/verify the intended private destination routes;
4. on the LAN router, add only those private destination routes with the Docker
   host as next hop.

Do not add a default route through this service.

## Deployment sequence

1. Create/parse the Git-backed resource.
2. Set the mandatory narrow Watch paths.
3. Verify the managed file mount exists.
4. Store the private OpenVPN profile in File Storage.
5. Review variable values and disable unnecessary Buildtime flags.
6. Deploy.
7. Wait for `CONNECTED,SUCCESS` health.
8. Inspect host routes and confirm the default route did not change.
9. Validate the real private-service consumer path.
10. Only then enable optional LAN forwarding/routing.

## Rollback

Because the container shares the host network namespace, preserve normal host
access and a way to stop the Coolify resource independently of the VPN path.

Stopping the container terminates OpenVPN and removes the forwarding/NAT rules
that the entrypoint added for `OPENVPN_GATEWAY_LAN_CIDR`.
