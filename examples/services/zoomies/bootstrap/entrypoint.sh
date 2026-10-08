#!/bin/sh
set -eu

runtime_uid="${ZOOMIES_RUNTIME_UID:-1001}"
runtime_gid="${ZOOMIES_RUNTIME_GID:-1001}"

fail() {
  echo "[zoomies-host-bootstrap] ERROR: $*" >&2
  return 1
}

case "$runtime_uid:$runtime_gid" in
  *[!0-9:]*|:*|*:)
    fail 'runtime uid/gid must be numeric'
    exit 1
    ;;
esac

retire_legacy_controller_shared() {
  controller_root="$1"
  legacy="$controller_root/shared"

  [ -e "$legacy" ] || return 0
  [ -d "$legacy" ] || fail "$legacy exists but is not a directory"

  unexpected="$(find "$legacy" -mindepth 1 -maxdepth 1 ! -name cache -print -quit 2>/dev/null || true)"
  [ -z "$unexpected" ] || fail "legacy controller shared directory contains unexpected top-level data: $unexpected"

  if [ -e "$legacy/cache" ]; then
    [ -d "$legacy/cache" ] && [ ! -L "$legacy/cache" ] || fail "$legacy/cache is not a normal directory"
    unexpected="$(find "$legacy/cache" -mindepth 1 -maxdepth 1 ! -name pools ! -name tools -print -quit 2>/dev/null || true)"
    [ -z "$unexpected" ] || fail "legacy controller cache contains unexpected data: $unexpected"

    for cache_dir in "$legacy/cache/pools" "$legacy/cache/tools"; do
      if [ -e "$cache_dir" ]; then
        [ -d "$cache_dir" ] && [ ! -L "$cache_dir" ] || fail "$cache_dir is not a normal directory"
      fi
    done
  fi

  echo "[zoomies-host-bootstrap] removing known legacy cache path $legacy"
  rm -rf -- "$legacy"
}

prepare_volume() {
  path="$1"
  label="$2"

  [ -d "$path" ] || fail "expected mounted volume $path"

  owner="$(stat -c '%u:%g' "$path")"
  if [ "$owner" != "$runtime_uid:$runtime_gid" ]; then
    if find "$path" -mindepth 1 -maxdepth 1 -print -quit | grep -q .; then
      fail "$label is non-empty and owned by $owner, expected $runtime_uid:$runtime_gid; refusing implicit data migration"
    fi
    chown "$runtime_uid:$runtime_gid" "$path"
  fi
  chmod 0750 "$path"

  unexpected="$(find "$path" -xdev -mindepth 1 \( ! -uid "$runtime_uid" -o ! -gid "$runtime_gid" \) -print -quit 2>/dev/null || true)"
  [ -z "$unexpected" ] || fail "$label contains data not owned by $runtime_uid:$runtime_gid: $unexpected"
}

main() {
  retire_legacy_controller_shared /bootstrap/controller-state
  prepare_volume /bootstrap/controller-state controller-state
  prepare_volume /bootstrap/agent-state agent-state

  [ -r /proc/1/ns/mnt ] || fail 'host PID namespace is not visible'

  if ! nsenter --target 1 --mount --uts --ipc --net --pid --cgroup -- /bin/sh -c 'test -x /bin/bash'; then
    fail 'host /bin/bash is required'
  fi

  exec nsenter --target 1 --mount --uts --ipc --net --pid --cgroup -- /bin/bash -s < /opt/zoomies/host-bootstrap.sh
}

if [ "${ZOOMIES_BOOTSTRAP_ENTRYPOINT_LIBRARY_ONLY:-0}" != "1" ]; then
  main "$@"
fi
