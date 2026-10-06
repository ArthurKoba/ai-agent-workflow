#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
umask 077

PROGRAM="zoomies-rootless-host-bootstrap"
ZOOMIES_USER="zoomies"
CONTROLLER_URL=""
JOIN_TOKEN=""
ZOOMIES_VERSION="v1.3.4"
BUILD_CACHE_MB="0"

log() { printf '[%s] %s\n' "$PROGRAM" "$*"; }
die() { printf '[%s] ERROR: %s\n' "$PROGRAM" "$*" >&2; exit 1; }
need_root() { [[ ${EUID:-$(id -u)} -eq 0 ]] || die "run this bootstrap as root"; }

usage() {
  cat <<'USAGE'
Usage: bootstrap-host.sh [options]

Creates a dedicated unprivileged Zoomies runner host with rootless Docker.
The bootstrap refuses to leave the Zoomies account with sudo, docker-group,
or rootful Docker-socket access.

Options:
  --user NAME            service account (default: zoomies)
  --controller URL       Zoomies controller URL
  --join-token TOKEN     one-time Zoomies host join token
  --version VERSION      Zoomies version for official installer (default: v1.3.4)
  --build-cache-mb N     agent Docker build-cache target (default: 0)
  -h, --help             show this help

When --controller and --join-token are supplied together, the script also runs
the official Zoomies agent installer after the rootless runtime is accepted.
USAGE
}

while (($#)); do
  case "$1" in
    --user) [[ $# -ge 2 ]] || die "--user needs a value"; ZOOMIES_USER=$2; shift 2 ;;
    --controller) [[ $# -ge 2 ]] || die "--controller needs a value"; CONTROLLER_URL=$2; shift 2 ;;
    --join-token) [[ $# -ge 2 ]] || die "--join-token needs a value"; JOIN_TOKEN=$2; shift 2 ;;
    --version) [[ $# -ge 2 ]] || die "--version needs a value"; ZOOMIES_VERSION=$2; shift 2 ;;
    --build-cache-mb) [[ $# -ge 2 ]] || die "--build-cache-mb needs a value"; BUILD_CACHE_MB=$2; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

[[ -z "$CONTROLLER_URL" && -z "$JOIN_TOKEN" ]] || \
  [[ -n "$CONTROLLER_URL" && -n "$JOIN_TOKEN" ]] || \
  die "--controller and --join-token must be supplied together"
[[ "$BUILD_CACHE_MB" =~ ^[0-9]+$ ]] || die "--build-cache-mb must be a non-negative integer"

need_root
[[ "$(uname -s)" == "Linux" ]] || die "Linux is required"
command -v systemctl >/dev/null 2>&1 || die "systemd is required"
[[ "$(stat -fc %T /sys/fs/cgroup 2>/dev/null || true)" == "cgroup2fs" ]] || \
  die "cgroup v2 is required by this hardened preset"

install_rootless_prereqs() {
  if command -v newuidmap >/dev/null 2>&1 && command -v newgidmap >/dev/null 2>&1; then
    return
  fi

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
    die "unsupported package manager; install newuidmap/newgidmap, dbus, slirp4netns and fuse-overlayfs"
  fi

  command -v newuidmap >/dev/null 2>&1 || die "newuidmap is still missing"
  command -v newgidmap >/dev/null 2>&1 || die "newgidmap is still missing"
}

ensure_user() {
  if ! id "$ZOOMIES_USER" >/dev/null 2>&1; then
    log "creating dedicated user $ZOOMIES_USER"
    useradd --create-home --shell /bin/bash --user-group "$ZOOMIES_USER"
  fi

  local uid gid home groups group
  uid=$(id -u "$ZOOMIES_USER")
  gid=$(id -g "$ZOOMIES_USER")
  home=$(getent passwd "$ZOOMIES_USER" | awk -F: '{print $6}')
  [[ -n "$home" && -d "$home" ]] || die "home directory for $ZOOMIES_USER is missing"
  [[ "$uid" -ne 0 && "$gid" -ne 0 ]] || die "$ZOOMIES_USER must not be root"

  # This is a dedicated automation account. Password login is not required.
  passwd -l "$ZOOMIES_USER" >/dev/null 2>&1 || true

  groups=" $(id -nG "$ZOOMIES_USER") "
  for group in docker sudo wheel; do
    if getent group "$group" >/dev/null 2>&1 && [[ "$groups" == *" $group "* ]]; then
      log "removing forbidden group $group from $ZOOMIES_USER"
      gpasswd -d "$ZOOMIES_USER" "$group" >/dev/null
    fi
  done

  if command -v sudo >/dev/null 2>&1 && runuser -u "$ZOOMIES_USER" -- sudo -n true >/dev/null 2>&1; then
    die "$ZOOMIES_USER still has passwordless sudo; remove its sudoers grant before continuing"
  fi

  awk -F: -v u="$ZOOMIES_USER" '$1 == u && $3 >= 65536 { ok=1 } END { exit !ok }' /etc/subuid || \
    die "$ZOOMIES_USER needs a subordinate UID range of at least 65536 IDs"
  awk -F: -v u="$ZOOMIES_USER" '$1 == u && $3 >= 65536 { ok=1 } END { exit !ok }' /etc/subgid || \
    die "$ZOOMIES_USER needs a subordinate GID range of at least 65536 IDs"

  ZOOMIES_UID=$uid
  ZOOMIES_GID=$gid
  ZOOMIES_HOME=$home
  RUNTIME_DIR="/run/user/$uid"
  DOCKER_SOCKET="$RUNTIME_DIR/docker.sock"
  DOCKER_HOST_URI="unix://$DOCKER_SOCKET"
}

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

setup_rootless_docker() {
  command -v dockerd-rootless-setuptool.sh >/dev/null 2>&1 || \
    die "dockerd-rootless-setuptool.sh is missing; install Docker rootless extras first"
  command -v docker >/dev/null 2>&1 || die "Docker CLI is missing"

  log "enabling persistent user services for $ZOOMIES_USER"
  loginctl enable-linger "$ZOOMIES_USER"
  systemctl start "user@${ZOOMIES_UID}.service"

  local i
  for i in {1..20}; do
    [[ -d "$RUNTIME_DIR" && -S "$RUNTIME_DIR/bus" ]] && break
    sleep 0.5
  done
  [[ -d "$RUNTIME_DIR" ]] || die "systemd did not create $RUNTIME_DIR"

  if [[ ! -S "$DOCKER_SOCKET" ]]; then
    log "installing rootless Docker service as $ZOOMIES_USER"
    as_zoomies dockerd-rootless-setuptool.sh install
  fi

  as_zoomies systemctl --user enable docker.service >/dev/null 2>&1 || true
  as_zoomies systemctl --user start docker.service

  for i in {1..40}; do
    [[ -S "$DOCKER_SOCKET" ]] && break
    sleep 0.5
  done
  [[ -S "$DOCKER_SOCKET" ]] || die "rootless Docker socket did not appear at $DOCKER_SOCKERT"

  local socket_uid security root_dir
  socket_uid=$(stat -c %u "$DOCKER_SOCKET")
  [[ "$socket_uid" -eq "$ZOOMIES_UID" ]] || die "Docker socket is not owned by $ZOOMIES_USER"

  security=$(as_zoomies env DOCKER_HOST="$DOCKER_HOST_URI" docker info --format '{{json .SecurityOptions}}')
  [[ "$security" == *rootless* ]] || die "Docker daemon did not report rootless security mode"

  root_dir=$(as_zoomies env DOCKER_HOST="$DOCKER_HOST_URI" docker info --format '{{.DockerRootDir}}')
  [[ "$root_dir" != "/var/lib/docker" ]] || die "Docker is using the rootful data root"

  install -d -m 0755 /etc/zoomies
  cat > /etc/zoomies/rootless-runtime.env <<EOF_RUNTIME
ZOOMIES_DOCKER_HOST=$DOCKER_HOST_URI
ZOOMIES_AGENT_DOCKER_BUILD_CACHE_MB=$BUILD_CACHE_MB
EOF_RUNTIMER
  chmod 0644 /etc/zoomies/rootless-runtime.env
}

assert_privilege_boundary() {
  local groups
  groups=" $(id -nG "$ZOOMIES_USER") "
  [[ "$groups" != *" docker "* ]] || die "$ZOOMIES_USER is in docker group"
  [[ "$groups" != *" sudo "* ]] || die "$ZOOMIES_USER" is in sudo group"
  [[ "$groups" != *" wheel "* ]] || die "$ZOOMIES_USER is in wheel group"

  if command -v sudo >/dev/null 2>&1 && runuser -u "$ZOOMIES_USER" -- sudo -n true >/dev/null 2>&1; then
    die "$ZOOMIES_USER …¸ÍÕ‘¼ˆ(€™¤((€ml€ˆ‘=-I}M=-Pˆ€„ô€ˆ½Ù…È½ÉÕ¸½‘½­•È¹Í½¬ˆutñð‘¥”€‰É½½Ñ™Õ°½­•ÈÍ½­•Ð¥Ì™½É‰¥‘‘•¸ˆ)ô()•¹É½±±}…•¹Ñ}¥™}É•ÅÕ•ÍÑ• ¤ì(€ml€µ¸€ˆ‘)=%9}Q=-8ˆutñðÉ•ÑÕÉ¸€À(€½µµ…¹€µØÕÉ°€ø½‘•Ø½¹Õ±°€Èø˜Äñð‘¥”€‰ÕÉ°¥ÌÉ•ÅÕ¥É•™½Èi½½µ¥•Ì•¹É½±±µ•¹Ðˆ((€±½œ€‰•¹É½±±¥¹œi½½µ¥•Ì…•¹ÐÝ¥Ñ Ñ¡”½™™¥¥…°¥¹ÍÑ…±±•Èˆ(€€ŒQ¡”½¹”µÑ¥µ”Ñ½­•¸•á¥ÍÑÌ½¹±ä¥¸Ñ¡¥ÌÁÉ½•ÍÌ•¹Ù¥É½¹µ•¹Ð½…ÉÕµ•¹ÐÍÑÉ•…´¸(€€ŒI½½Ð¥ÌÕÍ•Ñ¼¥¹ÍÑ…±°Ñ¡”Í•ÉÙ¥”°‰ÕÐÑ¡”É•ÍÕ±Ñ¥¹œÍ•ÉÙ¥”µÕÍÐÉÕ¸…Ì(€€ŒÑ¡”‘•‘¥…Ñ•i½½µ¥•Ì…½Õ¹Ð¸Q¡”É½½Ñ±•ÍÌÍ½­•Ð¥ÌÁ¥¹¹••áÁ±¥¥Ñ±ä¸(€•áÁ½ÉÐ=-I}!=MPôˆ‘=-I}!=MQ}UI$ˆ((€•áÁ½ÉÐi==5%M}=-I}!=MPôˆ‘=-I}!=MQ}UI$ˆ(€•áÁ½ÉÐi==5%M}9Q}=-I}	U%1}!}5ôˆ‘	U%1}!}5ˆ(€ÕÉ°€µ™ÍM0¡ÑÑÁÌè¼½é½½µ¥•Ì¹Í ½¥¹ÍÑ…±°¹Í ðÍ €µÌ€´´p(€€€€´µµ½‘”…•¹Ðp(€€€€´µ½¹ÑÉ½±±•È€ˆ‘=9QI=11I}UI0ˆp(€€€€´µ©½¥¸µÑ½­•¸€ˆ‘)=%9}Q=-8ˆp(€€€€´µÙ•ÉÍ¥½¸€ˆ‘i==5%M}YIM%=8ˆ((€¥˜ÍåÍÑ•µÑ°…Ðé½½µ¥•Ìµ…•¹Ð¹Í•ÉÙ¥”€ø½‘•Ø½¹Õ±°€Èø˜ÄìÑ¡•¸(€€€±½…°Í•ÉÙ¥•}ÕÍ•È(€€€Í•ÉÙ¥•}ÕÍ•Èô¡ÍåÍÑ•µÑ°Í¡½Üé½µ¥•Ìµ…•¹Ð¹Í•ÉÙ¥”€µÀUÍ•È€´µÙ…±Õ”¤(€€€ml€ˆ‘Í•ÉÙ¥•}ÕÍ•Èˆ€ôô€ˆ‘i==5%M}UMHˆutñðp(€€€€€‘¥”€‰é½µ¥•Ìµ…•¹Ð¹Í•ÉÙ¥”ÉÕ¹Ì…Ì€‘íÍ•ÉÙ¥•}ÕÍ•ÈèµÉ½½Ñô°•áÁ•Ñ•€‘i==5%M}UMHˆ(€™¤)ô()¥¹ÍÑ…±±}É½½Ñ±•ÍÍ}ÁÉ•É•ÅÌ)•¹ÍÕÉ•}ÕÍ•È)…ÍÍ•ÉÑ}ÁÉ¥Ù¥±••}‰½Õ¹‘…Éä)Í•ÑÕÁ}É½½Ñ±•ÍÍ}‘½­•È)…ÍÍ•ÉÑ}ÁÉ¥Ù¥±••}‰½Õ¹‘…Éä)•¹É½±±}…•¹Ñ}¥™}É•ÅÕ•ÍÑ•()±½œ€‰‰½½ÑÍÑÉ…À…•ÁÑ•ˆ)±½œ€‰ÕÍ•Èè€‘i==5%M}UMH€¡Õ¥ô‘i==5%M}U%¤°¹¼ÍÕ‘¼½‘½­•ÈµÉ½ÕÀ…•ÍÌˆ)±½œ€‰½­•ÈèÉ½½Ñ±•ÍÌ…Ð€‘=-I}!=MQ}UI$ˆ)±½œ€‰ÉÕ¹Ñ¥µ”•¹Øè€½•ÑŒ½é½½µ¥•Ì½É½½Ñ±•ÍÌµÉÕ¹Ñ¥µ”¹•¹Øˆ)¥˜ml€µè€ˆ‘)=%9}Q=-8ˆutìÑ¡•¸(€±½œ€‰ÉÕ¹Ñ¥µ”¥ÌÉ•…‘äìÉ•ÉÕ¸Ý¥Ñ €´µ½¹ÑÉ½±±•È…¹€´µ©½¥¸µÑ½­•¸Ñ¼•¹É½±°Ñ¡”…•¹Ðˆ)•±Í”(€±½œ€‰…•¹Ð•¹É½±±µ•¹ÐÉ•ÅÕ•ÍÑ•ìÙ•É¥™äÑ¡”¡½ÍÐ¥Ì=¹±¥¹”¥¸i½½µ¥•Ì‰•™½É”É•…Ñ¥¹œÁ½½±Ìˆ)™¤(