#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
umask 077

PROGRAM="zoomies-rootless-runtime-bootstrap"
ZOOMIES_USER="zoomies"

log() { printf '[%s] %s\n' "$PROGRAM" "$*"; }
die() { printf '[%s] ERROR: %s\n' "$PROGRAM" "$*" >&2; exit 1; }

[[ ${EUID:-$(id -u)} -eq 0 ]] || die "run this bootstrap as root"
[[ "$(uname -s)" == "Linux" ]] || die "Linux is required"
command -v systemctl >/dev/null 2>&1 || die "systemd is required"
[[ "$(stat -fc %T /sys/fs/cgroup 2>/dev/null || true)" == "cgroup2fs" ]] || \
  die "cgroup v2 is required by this hardened preset"

if ! command -v newuidmap >/dev/null 2>&1 || ! command -v newgidmap >/dev/null 2>&1; then
  log "installing rootless Docker prerequisites"
  if command -v apt-get >/dev/null 2>&1; then
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -y --no-install-recommends uidmap dbus-user-session slirp4netns fuse-overlayfs
  elif command -v dnf >/dev/null 2>&1; then
    dnf install -y shadow-utils dbus-daemon slirp4netns fuse-overlayfs
  elif command -v yum >/dev/null 2>&1; then
    yum install -y shadow-utils dbus-daemon slirp4netns fuse-overlayfs
  else
    die "unsupported package manager"
  fi
fi

command -v newuidmap >/dev/null 2>&1 || die "newuidmap is missing"
command -v newgidmap >/dev/null 2>&1 || die "newgidmap is missing"
command -v dockerd-rootless-setuptool.sh >/dev/null 2>&1 || \
  die "dockerd-rootless-setuptool.sh is missing"
command -v docker >/dev/null 2>&1 || die "Docker CLI is missing"

if ! id "$ZOOMIES_USER" >/dev/null 2>&1; then
  log "creating dedicated user $ZOOMIES_USER"
  useradd --create-home --shell /bin/bash --user-group "$ZOOMIES_USER"
fi

ZOOMIES_UID=$(id -u "$ZOOMIES_USER")
ZOOMIES_GID=$(id -g "$ZOOMIES_USER")
ZOOMIES_HOME=$(getent passwd "$ZOOMIES_USER" | awk -F: '{print $6}')
RUNTIME_DIR="/run/user/$ZOOMIES_UID"
DOCKER_SOCKET="$RUNTIME_DIR/docker.sock"
DOCKER_HOST_URI="unix://$DOCKER_SOCKET"

[[ "$ZOOMIES_UID" -ne 0 && "$ZOOMIES_GID" -ne 0 ]] || die "$ZOOMIES_USER must not be root"
passwd -l "$ZOOMIES_USER" >/dev/null 2>&1 || true

groups=" $(id -nG "$ZOOMIES_USER") "
for group in docker sudo wheel; do
  if getent group "$group" >/dev/null 2>&1 && [[ "$groups" == *" $group "* ]]; then
    log "removing forbidden group $group from $ZOOMIES_USER"
    gpasswd -d "$ZOOMIES_USER" "$group" >/dev/null
  fi
done

if command -v sudo >/dev/null 2>&1 && runuser -u "$ZOOMIES_USER" -- sudo -n true >/dev/null 2>&1; then
  die "$ZOOMIES_USER can sudo"
fi

awk -F: -v u="$ZOOMIES_USER" '$1 == u && $3 >= 65536 { ok=1 } END { exit !ok }' /etc/subuid || \
  die "$ZOOMIES_USER needs at least 65536 subordinate UIDs"
awk -F: -v u="$ZOOMIES_USER" '$1 == u && $3 >= 65536 { ok=1 } END { exit !ok }' /etc/subgid || \
  die "$ZOOMIES_USER needs at least 65536 subordinate GIDs"

as_zoomies() {
  runuser -u "$ZOOMIES_USER" -- env \
    HOME="$ZOOMIES_HOME" \
    USER="$ZOOMIES_USER" \
    LOGNAME="$ZOOMIES_USER" \
    XDG_RUNTIME_DIR="$RUNTIME_DIR" \
    DBUS_SESSION_BUS_ADDRESS="unix:path=$RUNTIME_DIR/bus" \
    PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin" \
    "$@"
}

log "enabling persistent user services"
loginctl enable-linger "$ZOOMIES_USER"
systemctl start "user@${ZOOMIES_UID}.service"

for _ in {1..20}; do
  [[ -d "$RUNTIME_DIR" ]] && break
  sleep 0.5
done
[[ -d "$RUNTIME_DIR" ]] || die "systemd did not create $RUNTIME_DIR"

if [[ ! -S "$DOCKER_SOCKET" ]]; then
  log "installing rootless Docker as $ZOOMIES_USER"
  as_zoomies dockerd-rootless-setuptool.sh install --force
fi

as_zoomies systemctl --user enable docker.service >/dev/null 2>&1 || true
as_zoomies systemctl --user start docker.service

for _ in {1..40}; do
  [[ -S "$DOCKER_SOCKET" ]] && break
  sleep 0.5
done
[[ -S "$DOCKER_SOCKET" ]] || die "rootless Docker socket did not appear at $DOCKER_SOCKET"

[[ "$(stat -c %u "$DOCKER_SOCKET")" -eq "$ZOOMIES_UID" ]] || \
  die "Docker socket is not owned by $ZOOMIES_USER"

security=$(as_zoomies env DOCKER_HOST="$DOCKER_HOST_URI" docker info --format '{{json .SecurityOptions}}')
[[ "$security" == *rootless* ]] || die "Docker daemon did not report rootless mode"

root_dir=$(as_zoomies env DOCKER_HOST="$DOCKER_HOST_URI" docker info --format '{{.DockerRootDir}}')
[[ "$root_dir" != "/var/lib/docker" ]] || die "Docker is using the rootful data root"

install -d -m 0755 /etc/zoomies
cat > /etc/zoomies/rootless-runtime.env <<EOF_RUNTIME
ZOOMIES_RUNTIME_UID=$ZOOMIES_UID
ZOOMIES_RUNTIME_GID=$(stat -c %g "$DOCKER_SOCKET")
ZOOMIES_RUNTIME_SOCKET=$DOCKER_SOCKET
ZOOMIES_DOCKER_HOST=$DOCKER_HOST_URI
EOF_RUNTIME
chmod 0644 /etc/zoomies/rootless-runtime.env

log "runtime accepted"
log "user: $ZOOMIES_USER uid=$ZOOMIES_UID gid=$ZOOMIES_GID"
log "Docker: rootless at $DOCKER_HOST_URI"
log "next: deploy agent-compose.yaml with a fresh one-time join token"
