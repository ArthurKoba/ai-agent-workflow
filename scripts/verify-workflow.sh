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
# The fallback HEAD^ is for whitespace only. Do not treat an already
# published oversized skill as newly changed. CI supplies VERIFY_BASE_SHA;
# unpushed local commits are compared with origin/main.
size_base=""
if [[ -v VERIFY_BASE_SHA ]]; then
  size_base="$VERIFY_BASE_SHA"
elif git show-ref --verify --quiet refs/remotes/origin/main; then
  if [[ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]]; then
    size_base="$(git merge-base HEAD origin/main)"
  fi
fi
export WORKFLOW_VERIFY_BASE="$size_base"
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
# Deleted bootstrap must not return as an active startup dependency.
# Historical changelog entries are intentionally excluded.
active = [Path('AGENTS.md'), Path('README.md')]
for folder in ('context', 'docs', 'projects', 'prompts', 'roles', 'skills'):
    active.extend(Path(folder).rglob('*.md'))
dead = []
for path in active:
    if not path.is_file():
        continue
    body = path.read_text(encoding='utf-8')
    if 'BOOTSTRAP_PROTOCOL' in body or 'workflow_bootstrap' in body:
        dead.append(str(path))
if dead:
    raise SystemExit('Obsolete bootstrap references:' + chr(10) + chr(10).join(dead))

# Enforce a per-file 32 KiB UTF-8 cap for every new or changed skill.
# Pre-existing oversized files are reported as migration debt; editing one
# requires bringing that file under the cap.
import os
import subprocess

limit = 32 * 1024
def paths_from_git(args):
    return {
        x.decode('utf-8') for x in subprocess.check_output(
            ['git', *args, '--', 'skills/']).split(b'\0') if x
    }

changed = set()
base = os.environ.get('WORKFLOW_VERIFY_BASE', '')
if base:
    changed.update(paths_from_git(['diff', '--name-only', '-z',
                                   '--diff-filter=ACMRT', base, 'HEAD']))
changed.update(paths_from_git(['diff', '--name-only', '-z',
                               '--diff-filter=ACMRT']))
changed.update(paths_from_git(['diff', '--cached', '--name-only', '-z',
                               '--diff-filter=ACMRT']))
changed.update(paths_from_git(['ls-files', '--others', '--exclude-standard',
                               '-z']))
violations = []
legacy = []
for path in sorted(Path('skills').rglob('*.md')):
    size = path.stat().st_size
    if size > limit:
        (violations if path.as_posix() in changed else legacy).append(
            f'{path}: {size} > {limit} UTF-8 bytes')
if violations:
    raise SystemExit('Oversized new/changed skills (split or shorten):\n' +
                     '\n'.join(violations))
if legacy:
    print('Pre-existing oversized skills (unchanged; migration required):')
    print('\n'.join(legacy))
print('Workflow maps, skill byte limits, obsolete links and whitespace verified')
PY
