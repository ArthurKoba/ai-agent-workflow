#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

# Verify the changed commit range when the mainline reference is available.
if git show-ref --verify --quiet refs/remotes/origin/main; then
  base="$(git merge-base HEAD origin/main)"
  git diff --check "$base" HEAD
fi
git diff --check

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
