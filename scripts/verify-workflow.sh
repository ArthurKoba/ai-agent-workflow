#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

# CI supplies the before/base commit. On a direct main push, origin/main
# may already equal HEAD: comparing HEAD with itself would miss changes.
base=""
if [[ -n "${VERIFY_BASE_SHA:-}" ]]; then
  if ! git cat-file -e "${VERIFY_BASE_SHA}^{commit}" 2>/dev/null; then
    echo "Unable to verify change range: base ${VERIFY_BASE_SHA} is missing" >&2
    exit 1
  fi
  base="${VERIFY_BASE_SHA}"
elif git show-ref --verify --quiet refs/remotes/origin/main; then
  base="$(git merge-base HEAD origin/main)"
  if [[ "$base" == "$(git rev-parse HEAD)" ]] && git rev-parse -q --verify HEAD^ >/dev/null; then
    base="$(git rev-parse HEAD^)"
  fi
fi
if [[ -n "$base" ]]; then
  git diff --check "$base" HEAD
fi
git diff --check
git diff --cached --check

# The canonical skill maps must not silently route to missing files.
python3 - <<'PY'
import re
from pathlib import Path

maps = (
    (Path('AGENTS.md'), Path('.')),
    (Path('skills/README.md'), Path('skills')),
)
missing = []
for map_file, base in maps:
    content = map_file.read_text(encoding='utf-8')
    for route in re.findall(r'→\s*`([^`]+)`', content):
        target = base / route
        if not target.is_file():
            missing.append(f'{map_file}: {route}')
if missing:
    raise SystemExit('Missing skill routes:\n' + '\n'.join(missing))
print('Workflow maps and changed-commit whitespace verified')
PY
