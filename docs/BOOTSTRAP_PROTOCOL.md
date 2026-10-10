# Bootstrap Protocol

Purpose: make workflow loading observable and resistant to prompt/context drift.

This protocol applies to substantial technical work.

## Hard startup gate

Before the first implementation/mutation/human-operated command block:

1. identify the active Project/repository/workspace;
2. read the local repository map:
   - `AGENTS.md` if present;
   - otherwise `CLAUDE.md`;
   - otherwise `README.md` + contribution/review docs;
3. read the universal workflow library root `AGENTS.md` and `README.md` in full through its designated authority; if unavailable, apply the mandatory STOP gate below;
4. select and read the relevant task skill(s);
5. identify the active role;
6. read current state/tasks/authority documents required by the repository map;
7. establish the current Task Context.

The repository map should keep this mandatory set intentionally small. Additional architecture/language/database/frontend/operations modules are loaded just in time when the task crosses their decision boundary; do not preload unrelated rule families merely because they exist.

Do not proceed past this gate by merely claiming that the files were read.

## Complete-document loading gate (mandatory)

**Selection is conditional; completeness is not.** Select the smallest relevant
set of required authorities using the repository map, role, active task and
skill router. Read **each selected required file from beginning to end** before
performing work governed by it. When a new skill/module or project contract
becomes mandatory later, read that whole document before crossing its decision
boundary. Do not preload unrelated skills or reread the whole library after
every tool call.

A document is **LOADED** only when its full current contents were actually
retrieved and read through the authoritative tool in this task context, or
were explicitly injected in full by the harness. Opening a file, obtaining its
path/metadata, reading a search snippet/preview/summary, reading just a
heading or section, trusting a prior chat recollection, or seeing an
incomplete/truncated tool response **does not count**.

- Use the Project's declared primary repository/connector authority. For
  `ArthurKoba/ai-agent-workflow`, retrieve the current GitHub repository
  through the **configured GitHub MCP**, not a stale local clone, a remembered
  excerpt, or an unapproved alternate HTTP/browser route.
- If the tool limits output, retry using supported pagination/chunked reads
  with complete start-to-end coverage and verified continuity. Inspect every
  chunk, including the final one; check completeness against available
  length/size/truncation metadata. A failed, missing or unverifiable chunk
  leaves the **entire required document unloaded**.
- For traceability keep the required file's locator/ref and whether full
  reading succeeded in the existing Task Context. Do not paste full rules,
  credentials or large tool outputs into a second tracked planning document.

## Unavailable mandatory context — STOP and ask

If any required file cannot be **fully** loaded, or the configured GitHub MCP
needed to read this library is absent, disconnected, denied or failing:

1. Attempt only bounded **read-only access recovery**, such as inspecting
   configured connector availability, reconnecting through an authorized
   interface or fetching the missing chunks. Do not bypass the declared tool
   authority or use a stale local checkout to claim success.
2. **STOP before substantial implementation, mutations, side-effecting
   tests/operations, reviews relying on that authority, or human-operated
   command blocks.** Do not continue another implementation slice on the
   unsupported assumption that the missing rules probably do not matter.
3. Tell the user exactly which required documents/MCP access are missing and
   why the context is incomplete. Offer to connect/restore the configured MCP
   and retry full loading, **or explicitly ask whether this specific task
   may start/continue in a degraded mode without those named documents**.
4. **Wait for an unambiguous, task-scoped user approval** before proceeding
   without them. Silence, an unrelated instruction, a generic earlier
   permission to work, or self-assessed low risk is not approval. Record the
   exception and its known risks in Task Context; it does not remove
   independent safety, security, permissions or correctness requirements.
   A new task or newly missing mandatory source needs its own decision.

If approval is refused or not given, stay stopped at this boundary. The
agent may still help diagnose/reconnect the missing access, but must not
describe the task as bootstrapped or approved for implementation.

## Task Context

Before substantial work, know at least:

- objective;
- acceptance criteria;
- active repository/workspace;
- active branch/ref when relevant;
- current known-good state;
- active role;
- loaded task skill(s);
- current patch/delta/artifact identity;
- latest observed result;
- next real decision boundary;
- blockers/contradictions.

This context may live in repository state, a task file, a durable artifact, or structured tool state.

Do not rely on chat memory alone for long or multi-turn technical work.

## Patch / delta continuity

An unfinished patch, generated file set, or important diff must not exist only as prose in chat.

Before a context switch, long investigation, agent handoff, or risky branch change, persist enough information to recover it:
- repository + branch/ref;
- affected files;
- diff/commit/patch artifact ID or exact locator;
- applied/not-applied state;
- validation already performed;
- remaining validation.

If the patch identity cannot be recovered, stop and reconstruct it from repository/artifact evidence before stacking new edits.

## Human-operated commands

If the task will emit commands for a human to run, `skills/terminal-operations.md` is mandatory.

Do not emit the first command block until the terminal skill is loaded or its rules are already injected in current context.

## Re-bootstrap triggers

Repeat only the relevant bootstrap subset when:
- repository/workspace changes;
- branch/state authority changes materially;
- a new task domain is entered;
- context/handoff/agent changes;
- a long task resumes after state uncertainty;
- the user reports that command/routing rules were violated;
- the user explicitly rejects the current technical direction, repeats the same correction, or expresses escalating frustration after a technical mismatch.

For a correction-triggered re-bootstrap, do not reread the whole library. Stop speculative mutation at the next safe boundary and recover only the context needed to explain the mismatch:

1. reread the latest explicit user requirements/corrections and the current durable Task Context;
2. compare the current implementation/architecture against the original acceptance contract;
3. identify the assumption, contradiction or ownership decision that drifted;
4. reload only the map/skill/source authority that owns that decision;
5. persist the corrected contract before continuing substantial implementation.

Strong negative feedback is not itself technical proof, but it is operational evidence that the current task model may be wrong. Do not dismiss repeated direct correction as tone or continue the same strategy without a bounded self-audit.

Do not reread everything mechanically after every tool call.

## Explicit context refresh

An explicit request to refresh/re-read context is a re-bootstrap trigger, not a
request to recite chat memory. Before the next technical decision, actually
re-open the active repository map and phase/task authority, the selected task
skill and any owning terminology/evidence module, the reporting protocol if a
report is requested, and the smallest current source/status checkpoint.

Re-read only the relevant authoritative subset; do not reload unrelated
modules. A context refresh does not authorize new work, a broader acceptance
scope or a full report by itself. Continue implementation only when the user
also requests continuation.

## User-visible startup signal

For substantial work, a short startup update may state:
- repository/workspace;
- selected skill/role;
- current decision boundary.

Do not dump the whole checklist or pretend verification that did not happen.


## Pre-send compliance

Loading the correct map/skill is necessary but not sufficient.

Before emitting an action governed by an active skill, perform a final compliance check against that skill's hard constraints.

Do not let a secondary response objective such as completeness, compactness, end-to-end planning, or convenience override an explicit STOP / MUST / decision-boundary rule.

If a draft response conflicts with an active hard constraint, the hard constraint wins and the draft must be rewritten before sending.
