#!/bin/sh
set -eu

CONFIG_PATH="${OPENVPN_CONFIG_PATH:-/etc/openvpn/client.ovpn}"
RUNTIME_CONFIG="/run/openvpn/client.ovpn"
TUN_DEVICE="${OPENVPN_TUN_DEVICE:-openvpn0}"
LAN_CIDR="${OPENVPN_GATEWAY_LAN_CIDR:-}"
AUTH_FILE="/run/openvpn/auth.txt"
MANAGEMENT_SOCKET="/run/openvpn/management.sock"
OPENVPN_PID=""
DEFAULT_ROUTE_BEFORE="$(ip -4 route show default 2>/dev/null || true)"

log() {
    printf '%s\n' "[openvpn-gateway] $*"
}

cleanup_rules() {
    if [ -n "$LAN_CIDR" ]; then
        while iptables -D FORWARD -s "$LAN_CIDR" -o "$TUN_DEVICE" -j ACCEPT 2>/dev/null; do :; done
        while iptables -D FORWARD -i "$TUN_DEVICE" -d "$LAN_CIDR" -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT 2>/dev/null; do :; done
        while iptables -t nat -D POSTROUTING -s "$LAN_CIDR" -o "$TUN_DEVICE" -j MASQUERADE 2>/dev/null; do :; done
    fi
}

cleanup() {
    trap - INT TERM EXIT
    cleanup_rules
    if [ -n "$OPENVPN_PID" ]; then
        kill -TERM "$OPENVPN_PID" 2>/dev/null || true
        wait "$OPENVPN_PID" 2>/dev/null || true
    fi
}

trap cleanup INT TERM EXIT

if [ ! -s "$CONFIG_PATH" ]; then
    log "OpenVPN profile is missing or empty: $CONFIG_PATH"
    exit 1
fi

if ! grep -Eq '^[[:space:]]*remote[[:space:]]+' "$CONFIG_PATH"; then
    log "OpenVPN profile does not contain a remote directive."
    exit 1
fi

mkdir -p /run/openvpn

# Keep the private profile outside Git, normalize the host-facing tunnel name,
# and prevent a direct redirect-gateway directive from replacing the host route.
awk '
    /^[[:space:]]*dev([[:space:]]|$)/ { next }
    /^[[:space:]]*dev-type([[:space:]]|$)/ { next }
    /^[[:space:]]*redirect-gateway([[:space:]]|$)/ { next }
    { print }
' "$CONFIG_PATH" > "$RUNTIME_CONFIG"

set -- openvpn \
    --config "$RUNTIME_CONFIG" \
    --dev-type tun \
    --dev "$TUN_DEVICE" \
    --auth-nocache \
    --management "$MANAGEMENT_SOCKET" unix \
    --pull-filter ignore redirect-gateway

if [ -n "${OPENVPN_USERNAME:-}" ] || [ -n "${OPENVPN_PASSWORD:-}" ]; then
    if [ -z "${OPENVPN_USERNAME:-}" ] || [ -z "${OPENVPN_PASSWORD:-}" ]; then
        log "OPENVPN_USERNAME and OPENVPN_PASSWORD must be set together."
        exit 1
    fi
    umask 077
    printf '%s\n%s\n' "$OPENVPN_USERNAME" "$OPENVPN_PASSWORD" > "$AUTH_FILE"
    set -- "$@" --auth-user-pass "$AUTH_FILE"
fi

cleanup_rules

log "Starting OpenVPN on tunnel $TUN_DEVICE."
"$@" &
OPENVPN_PID="$!"

i=0
while ! ip link show "$TUN_DEVICE" >/dev/null 2>&1; do
    if ! kill -0 "$OPENVPN_PID" 2>/dev/null; then
        wait "$OPENVPN_PID"
        exit $?
    fi
    i=$((i + 1))
    if [ "$i" -ge 60 ]; then
        log "Tunnel $TUN_DEVICE was not created within 60 seconds."
        exit 1
    fi
    sleep 1
done

DEFAULT_ROUTE_AFTER="$(ip -4 route show default 2>/dev/null || true)"
if [ "$DEFAULT_ROUTE_AFTER" != "$DEFAULT_ROUTE_BEFORE" ] || \
   ip -4 route show dev "$TUN_DEVICE" | grep -Eq '^(default|0\.0\.0\.0/1|128\.0\.0\.0/1)([[:space:]]|$)'; then
    log "Refusing VPN routes that capture general Internet traffic."
    exit 1
fi

if [ -n "$LAN_CIDR" ]; then
    if [ "$(cat /proc/sys/net/ipv4/ip_forward 2>/dev/null || printf 0)" != "1" ]; then
        log "Host IPv4 forwarding is disabled. Enable net.ipv4.ip_forward=1 on the Docker host."
        exit 1
    fi

    iptables -I FORWARD 1 -s "$LAN_CIDR" -o "$TUN_DEVICE" -j ACCEPT
    iptables -I FORWARD 1 -i "$TUN_DEVICE" -d "$LAN_CIDR" -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
    iptables -t nat -A POSTROUTING -s "$LAN_CIDR" -o "$TUN_DEVICE" -j MASQUERADE
    log "LAN forwarding enabled for $LAN_CIDR via $TUN_DEVICE."
fi

wait "$OPENVPN_PID"
