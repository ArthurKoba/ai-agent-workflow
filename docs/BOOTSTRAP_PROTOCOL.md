# Bootstrap Protocol

Single owner of startup routing, required-source completeness, and recovery
boundaries for substantial technical work. `AGENTS.md` is the entry map;
account/project instructions govern authority and task-specific constraints.
Do not turn startup into a fixed full-library reading ritual.

## 1. Select the minimal mandatory context

Before substantial implementation, repository mutation, governed review,
side-effecting operations or human-operated command blocks:

1. Identify the active Project, repository, authority, branch/ref, and task.
2. Read the repository entry map **in full**: `AGENTS.md`, otherwise
   `CLAUDE.md`, otherwise `README.md` and relevant contribution rules.
3. Follow that map to the **selected** role, task skill and current
   project/domain/contract sources. The role/skill indexes are optional
   routing aids when the entry map already selects the correct files.
   Read each selected authority in full before its decision boundary.
   If a new source becomes mandatory later, load that source before proceeding
   into its domain; prior selection does not grandfather it in.
4. If the task requires this universal workflow library, use its declared
   authoritative connector. Its root map need not be read twice when it
   *is* the active repository map. Read its README only when selected by
   the map or needed for the decision. Project/account prompt source
   templates are not runtime prerequisites; read their actual current text
   when designing, auditing or changing those prompts.
5. Recover the task's current state and acceptance from its designated
   Issue/work-item/project authority; identify the local known-good revision,
   unfinished delta, applicable validation and immediate blocker. Preserve
   a technical recovery checkpoint only where the tracker cannot own it.

Select files by the decision they protect, not by an unconditional inventory.
Ordinary work needs the map, one relevant skill/role where applicable,
and directly affected source/contracts. Load neighboring specialist rules
only when the task crosses their boundary. No staged reads of unrelated
language, architecture or service skills.

Reading and non-destructive discovery needed to **locate** authority can
precede its full load. An unverified authority never licenses dependent
implementation.

## 2. Full, model-visible reading

**Selection is conditional; completeness is mandatory.** A selected document
is LOADED only if its entire current text was actually presented to the
model through its authoritative source, or injected completely by the harness.
Tool success, file paths, search previews, summaries, metadata, hashes and
prior-chat recollections are not substitutes.

Read selected files individually by default. Batch at most two only if their
estimated serialized output fits a **measured** safe budget with headroom;
do not bulk-emit authorities. Confirm (1) the returned UTF-8 byte count
against source metadata where available and (2) the complete, gap-free text
**actually exposed to the model**, through the final section/chunk. Byte
counts computed only inside a tool script do not prove model-visible reading.

If a response is truncated or a batch omits content, retry missing files
individually; then use labelled contiguous chunks with source/ref, offsets,
total length (when available) and continuity checks. Shrink chunk sizes
after truncation, read the final chunk, and never combine different source
revisions. A missing or unverifiable chunk leaves that source **unloaded**.
Track source identity, requested/returned/fully-read files, observed byte
sizes and truncation/cutoff **only when measured**; a warning without an
offset does not establish a numerical cutoff. Keep a compact loaded/unloaded
checkpoint in existing task state, not duplicated rules or raw outputs.
Do not silently replace an incomplete authoritative read with a local
clone, summary or alternate transport.

For this workflow library the configured GitHub MCP owns the current
published library authority. A local checkout owns the **working draft**:
inspect and validate its changes separately, but never use it to replace
missing or incomplete required GitHub context. Recheck the published ref
after a material update or publication. Other Projects may select a different
primary connector; do not override their source authority.

## 3. Missing sources and permission boundaries

If a **selected** mandatory file or primary connector is unavailable or
incompletely visible, attempt only bounded, authorized read-only recovery:
check the connection and retrieve missing chunks. Then:

- 🛑 Stop **dependent** implementation, mutation, reviews relying on the
  missing authority, side-effecting operations and operator command blocks. Name the missing
  document/portion and the affected decision; do not guess its contents.
- Continue only genuinely independent, authorized read-only investigation or
  other work that does not need the missing authority. This is not a way to
  bypass a globally mandatory source.
- Offer restoration and a complete reread. An explicitly scoped degraded-mode
  exception is possible only where governing rules permit it. Request an
  unambiguous user decision for this task; the original work request,
  silence or an unrelated approval is not consent. Record the exception
  and risks in existing task state. No exception overrides higher-priority
  policy, tool permissions or safety constraints.

For missing **local execution context**, use
`../context/LOCAL_CONTEXT_CONTRACT.md`: block the environment-dependent
actions, not unrelated repository/source analysis. If a Project explicitly
sets a stricter gate, follow it.

## 4. Recoverable task checkpoint

Before substantial action, know objective, acceptance, authority,
active role/skills, repository/ref, last known-good state, unfinished
patch/commit/artifact identity, validation level, contradictions and the
next decision. Do not depend on conversation memory alone.

Issues/work items own the mutable goal, assignments, acceptance and task
lifecycle where a tracker exists. The optional `../templates/TASK_CONTEXT.md`
is only a technical checkpoint for facts not already recoverable there.
Do not build a second Markdown backlog or repeat issue commentary.

Before a handoff, branch change or risky long-running operation, preserve
repository/ref, exact affected files, applied/not-applied delta locator,
completed validation and remaining checks in the owning state surface.
If delta identity is lost, reconstruct it from actual evidence before
stacking more changes. Keep secrets and unnecessary execution logs out
of task state.

## 5. Focused re-bootstrap

Refresh only the owning subset when the task domain or repository changes,
a source revision changes materially, agent/handoff context becomes stale,
a user reports a violated command/routing rule (even once), or repeated
mistakes/corrections indicate acceptance drift. Reload the terminal skill
before emitting another operator command block after a command-format
violation.

On a correction, compare the latest user requirements and acceptance against
actual state; find the mismatched assumption or contract, reload its owning
map/skill/source, update the existing task checkpoint, and resume only safe
work. Do not read the full library on each call or infer technical facts
from emotional tone.

An explicit context-refresh request means **actually re-open** the relevant
entry map, active phase authority/skill and current source checkpoint (and
the reporting owner when a governed report is requested). It is not permission
to expand scope or resume implementation unless the user also requests it.
A refresh alone does not require a full report.

## 6. Specialized boundary and pre-send gate

Before giving human-operated shell/SSH/PowerShell/UART commands, load
`../skills/terminal-operations.md` fully. Its real execution lane and
command-block constraints override generic answer-completeness preferences.
Do not emit an operator command block while its mandatory context is missing.

Check proposed actions and outputs against every active STOP/MUST/permission
rule **before** sending or executing. Loading a skill is not proof that the
action complies. Report only what evidence establishes, not assumed success.
