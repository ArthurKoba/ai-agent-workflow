#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$ROOT/bootstrap-host.sh"
COMPOSE="$ROOT/docker-compose.yaml"
ENTRYPOINT="$ROOT/bootstrap/entrypoint.sh"
DOCKERFILE="$ROOT/bootstrap/Dockerfile"
TMP="$(mktemp -d)"
PID=""

cleanup() {
  [[ -z "$PID" ]] || kill "$PID" 2>/dev/null || true
  rm -rf "$TMP"
}
trap cleanup EXIT

bash -n "$SCRIPT"
sh -n "$ENTRYPOINT"

# Regression: the old controller-volume shared path is known Zoomies cache
# state and may be retired, while unknown content must still fail closed.
LEGACY_OK="$TMP/controller-ok"
mkdir -p "$LEGACY_OK/shared/cache/pools" "$LEGACY_OK/shared/cache/tools"
touch "$LEGACY_OK/shared/cache/pools/cache-entry"
ZOOMIES_BOOTSTRAP_ENTRYPOINT_LIBRARY_ONLY=1 sh -c '
  . "$1"
  retire_legacy_controller_shared "$2"
  [ ! -e "$2/shared" ]
' _ "$ENTRYPOINT" "$LEGACY_OK"

LEGACY_BAD="$TMP/controller-bad"
mkdir -p "$LEGACY_BAD/shared/secrets"
touch "$LEGACY_BAD/shared/secrets/keep"
if ZOOMIES_BOOTSTRAP_ENTRYPOINT_LIBRARY_ONLY=1 sh -c '
  . "$1"
  retire_legacy_controller_shared "$2"
' _ "$ENTRYPOINT" "$LEGACY_BAD" >/dev/null 2>&1; then
  exit 1
fi
[[ -f "$LEGACY_BAD/shared/secrets/keep" ]]

export ZOOMIES_BOOTSTRAP_LIBRARY_ONLY=1
source "$SCRIPT"
unset ZOOMIES_BOOTSTRAP_LIBRARY_ONLY

RUNTIME_SOCKET="$TMP/empty.sock"
mkdir -p "$RUNTIME_SOCKET"
prepare_socket_path
[[ ! -e "$RUNTIME_SOCKET" ]]

RUNTIME_SOCKET="$TMP/nonempty.sock"
mkdir -p "$RUNTIME_SOCKET"
touch "$RUNTIME_SOCKET/keep"
if prepare_socket_path >/dev/null 2>&1; then
  exit 1
fi
[[ -f "$RUNTIME_SOCKET/keep" ]]

SOCK="$TMP/runtime.sock"
python3 - "$SOCK" <<'PY' &
import socket
import sys
import time
s = socket.socket(socket.AF_UNIX)
s.bind(sys.argv[1])
time.sleep(20)
PY
PID=$!
for _ in $(seq 1 40); do
  [[ -S "$SOCK" ]] && break
  sleep 0.05
done

RUNTIME_SOCKET="$SOCK"
RUNTIME_UID="$(id -u)"
RUNTIME_GID=7777
RUNTIME_USER="$(id -u)"
as_runtime() {
  if [[ "$1" == "systemctl" ]]; then
    return 0
  fi
  if [[ "$1" == "env" ]]; then
    shift
    [[ "$1" == DOCKER_HOST=* ]] && shift
    [[ "$1" == "docker" && "$2" == "info" ]]
    case "$4" in
      "{{json .SecurityOptions}}") printf '["name=rootless"]' ;;
      "{{.CgroupVersion}}") printf '2' ;;
      "{{.CgroupDriver}}") printf 'systemd' ;;
      "{{.DockerRootDir}}") printf '/home/test/.local/share/docker' ;;
      *) return 98 ;;
    esac
    return 0
  fi
  return 97
}
cat() {
  if [[ "$1" == /sys/fs/cgroup/user.slice/user-* ]]; then
    printf 'cpu cpuset io memory pids'
    return 0
  fi
  command cat "$@"
}
verify_rootless_docker
kill "$PID" 2>/dev/null || true
wait "$PID" 2>/dev/null || true
PID=""

grep -q 'Delegate=cpu cpuset io memory pids' "$SCRIPT"
grep -q '/etc/modules-load.d/99-zoomies-rootless-docker.conf' "$SCRIPT"
grep -q 'loginctl enable-linger' "$SCRIPT"
grep -q 'systemctl --user enable docker.service' "$SCRIPT"
grep -q 'docker-ce-rootless-extras=\$docker_ce_version' "$SCRIPT"
! grep -q 'chown -R.*SHARED_DIR' "$SCRIPT"
grep -q 'only Ubuntu 24.04 is qualified' "$SCRIPT"
grep -q 'SHARED_DIR=' "$SCRIPT"
grep -q 'native zoomies-agent.service exists' "$SCRIPT"
! grep -q 'ZOOMIES_JOIN_TOKEN' "$SCRIPT"
! grep -q 'agent join' "$SCRIPT"
! grep -q 'disable --now zoomies-agent.service' "$SCRIPT"
! grep -q 'get.docker.com/rootless' "$SCRIPT"
! grep -q 'BASH_SOURCE' "$SCRIPT"
grep -q 'findutils' "$DOCKERFILE"

grep -q 'retire_legacy_controller_shared /bootstrap/controller-state' "$ENTRYPOINT"
grep -q 'legacy controller shared directory contains unexpected' "$ENTRYPOINT"
grep -q 'legacy controller cache contains unexpected' "$ENTRYPOINT"
grep -q 'prepare_volume /bootstrap/controller-state controller-state' "$ENTRYPOINT"
grep -q 'prepare_volume /bootstrap/agent-state agent-state' "$ENTRYPOINT"
grep -q 'refusing implicit data migration' "$ENTRYPOINT"
entry_nsenter_line="$(grep -n 'exec nsenter' "$ENTRYPOINT" | cut -d: -f1)"
entry_state_line="$(grep -n 'prepare_volume /bootstrap/controller-state' "$ENTRYPOINT" | cut -d: -f1)"
(( entry_state_line < entry_nsenter_line ))

grep -q '^  zoomies-bootstrap:$' "$COMPOSE"
grep -q '^  zoomies:$' "$COMPOSE"
[[ "$(grep -c 'privileged: true' "$COMPOSE")" -eq 1 ]]
grep -A40 '^  zoomies-bootstrap:$' "$COMPOSE" | grep -q 'restart: "no"'
grep -A40 '^  zoomies-bootstrap:$' "$COMPOSE" | grep -q 'pid: host'
grep -A65 '^  zoomies:$' "$COMPOSE" | grep -q 'condition: service_completed_successfully'

ZOOMIES_BLOCK="$(sed -n '/^  zoomies:$/,/^volumes:$/p' "$COMPOSE")"
grep -q 'user: "${ZOOMIES_RUNTIME_UID:-1001}:${ZOOMIES_RUNTIME_GID:-1001}"' <<<"$ZOOMIES_BLOCK"
grep -q 'ZOOMIES_STATE_DIR: /var/lib/zoomies' <<<"$ZOOMIES_BLOCK"
grep -q 'SERVICE_URL_ZOOMIES_8080: /' <<<"$ZOOMIES_BLOCK"
grep -q 'ZOOMIES_EXTERNAL_URL: ${ZOOMIES_EXTERNAL_URL:-${SERVICE_URL_ZOOMIES}}' <<<"$ZOOMIES_BLOCK"
grep -q 'ZOOMIES_AGENT_EMBEDDED: "true"' <<<"$ZOOMIES_BLOCK"
grep -q 'ZOOMIES_WORK_DIR: /var/lib/zoomies-agent/work' <<<"$ZOOMIES_BLOCK"
grep -q 'ZOOMIES_DOCKER_HOST: unix://' <<<"$ZOOMIES_BLOCK"
grep -q 'source: /run/user' <<<"$ZOOMIES_BLOCK"
grep -q 'target: /run/user' <<<"$ZOOMIES_BLOCK"
grep -q 'read_only: true' <<<"$ZOOMIES_BLOCK"
grep -q 'source: /var/lib/zoomies/shared' <<<"$ZOOMIES_BLOCK"
grep -q 'target: /var/lib/zoomies/shared' <<<"$ZOOMIES_BLOCK"
[[ "$(grep -c 'create_host_path: false' "$COMPOSE")" -eq 2 ]]
[[ "$(grep -c 'nocopy: true' "$COMPOSE")" -eq 4 ]]
grep -q 'cap_drop:' <<<"$ZOOMIES_BLOCK"
grep -q 'no-new-privileges:true' <<<"$ZOOMIES_BLOCK"
! grep -q '/var/run/docker.sock' "$COMPOSE"
! grep -q 'host-socket' "$COMPOSE"
grep -q 'ZOOMIES_ENCRYPTION_KEY: ${ZOOMIES_ENCRYPTION_KEY:?}' "$COMPOSE"
! grep -q 'ZOOMIES_ENCRYPTION_KEY: [A-Za-z0-9+/]' "$COMPOSE"
! grep -q 'ZOOMIES_JOIN_TOKEN' "$COMPOSE"
! grep -q 'zoomies-runner-work' "$COMPOSE"

printf 'zoomies reusable single-compose rootless contract tests: ok\n'

