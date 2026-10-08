# Hardware Reverse / Embedded Bring-up

Single authoritative skill for hardware/firmware behavior recovery:
terminology, evidence levels, semantic naming, project lifecycle, programmable
Ghidra analysis and monitored script jobs. Read this one file; do not require
additional hardware-reverse skill documents. Keep future terminology,
tracing, scripting, job orchestration and project lifecycle rules **in this
same README**; do not split them into sibling Markdown skill modules.

## Evidence-first
- Do not restart reverse if an existing corpus/contract answers the question.
- Prefer one authoritative searchable corpus over repeated target extraction.
- Capture once; analyze offline.

## Public-research stopping rule

For legacy, obscure or poorly documented silicon, generic public research is a bounded evidence path, not a mandatory startup ritual.

- If the current project already records that broad searches for datasheets, SDKs, vendor source trees, mirrors, chip-family examples or secondary-controller documentation were exhausted without producing an authoritative artifact, do **not** restart the same generic search in a new chat/session.
- After that boundary is recorded, the default path is target evidence: preserved firmware, canonical Analysis state, instruction-level behavior, runtime traces, board observations and other project-owned artifacts.
- Reopen external research only when there is a **new concrete lead**: a newly identified part number/revision, document title, archive filename/hash, vendor SDK/version, leaked/source repository reference, package marking that changes the search space, newly available dump, or another specific artifact locator. A direct user request to research externally is also sufficient.
- A vague hope that another search engine/query/session might find something is not a new lead. Do not spend another analysis cycle enumerating the same chip family, decoding the same top mark, or looking for generic source code after the project has already classified that route as exhausted.
- When a bounded external search is attempted, record the useful artifact or record that the path remained exhausted so later agents inherit the stop condition. Do not report generic family material as target proof.

This rule applies equally to the primary processor, audio DSP, secondary controller and other legacy companion silicon. Target reverse remains the authority when public material is absent.

## Semantic reverse
Use decompiler, CFG, callers/callees, XREF, globals/strings, types/structures and unresolved indirect flow.

Pseudocode is for understanding. Instruction/ASM evidence is required for critical proof.

## Canonical project
Before mutating reverse state, identify the canonical project/program. Do not create competing mutable projects for the same binary.

## Cross-platform references
A related SoC/platform may be a semantic oracle, but never assume identical ioctl numbers, structures, callbacks, MMIO or lifecycle. Target evidence wins.

## Runtime evidence
When static evidence is exhausted, define the exact runtime observation needed instead of broad further reverse.

## Hardware experiments
`baseline → action → observation → rollback → postcondition`

Physical/visual evidence outranks software success flags when they conflict.

## Stateful stacks
Stateful media/hardware pipelines need an explicit owner. Avoid competing processes/opens unless proven safe.

## Feature parity
A feature is complete only if a target contract is implemented, a compatible retained provider is proven, or the feature is explicitly unsupported. Silent no-op is not implementation.

## Terminology, semantic contracts and evidence

Use this section when reverse/embedded work is expressed as recovered behavior rather than ordinary source-level implementation.

### Vocabulary

Use these terms consistently in progress updates, handoffs and explanatory documentation:

- **behavior analysis** / **behavior recovery** — the overall activity;
- **action node**, **action boundary**, **action map**, **action route** — analyzed code/control structures;
- **transition**, **action link**, **inbound action**, **outbound action** — control-flow relationships;
- **high-level behavior view** / **low-level action view** — semantic/pseudocode vs instruction-level inspection;
- **behavior contract** / **control contract** — recovered semantics required for implementation or integration;
- **semantic coverage** / **behavior coverage** — progress over a named analysis denominator;
- **state**, **handler**, **dispatcher**, **chain**, **route**, **evidence point** — preferred neutral structural nouns;
- **implementation proof**, **execution proof**, **board proof**, **integration proof** — distinct validation levels.

Exact architecture names, instruction mnemonics, registers, addresses, protocol fields, control IDs and API identifiers remain exact evidence and should not be renamed merely to fit the vocabulary.

#### Scope boundary

`action node` and related action terminology apply to analyzed code/control structure. Do not use them as generic replacements for hardware parts, PCB routes, pins, buses, protocols, connectors or physical functions. A component identification is not an action node; a UART pin mux is not an action node; a protocol boundary is not an action node unless the statement is specifically about the code structure implementing it.

### Evidence states

Use explicit evidence states when a conclusion is not self-evident:

- **CONFIRMED** — reproducible target evidence directly supports the claim: bytes/instructions, low-level behavior, runtime output, package marking, continuity/scope measurement, hardware observation or equivalent primary evidence;
- **LIKELY** — multiple independent clues support the claim but direct target proof is incomplete;
- **UNKNOWN** — available evidence is insufficient;
- **CONTRADICTION** — authoritative observations disagree and the affected conclusion cannot be treated as settled.

Capability evidence is not topology proof. A datasheet feature, SDK option or firmware code path does not prove that a product PCB routes or uses that capability.

`WITHDRAWN` is a historical-status marker, not a live evidence state. Use it when a previous semantic interpretation has been invalidated and must remain visible only to prevent later reuse. The current claim itself must still be classified as `UNKNOWN`, `LIKELY`, `CONFIRMED` or `CONTRADICTION` as appropriate.

### Semantic naming lifecycle

Every recovered semantic object must track evidence strength and keep its persisted metadata at the same strength. This applies to action nodes and boundaries, states/globals, MMIO registers and fields, constants/enums, structures, protocol fields, addresses/labels, transitions and action links.

Use this lifecycle:

1. **UNKNOWN** — preserve exact raw identity and structure, but do not invent a semantic owner or product meaning. Keep a generic/structural name when that is all the evidence supports.
2. **LIKELY** — a conservative provisional semantic name is allowed when it improves navigation, but the name must assert no more than the evidence proves. Prefer observed behavior over vendor/component identity. When ambiguity would otherwise be hidden, use the project's provisional/candidate naming convention and record `LIKELY` plus the supporting evidence and unresolved condition in the comment.
3. **CONFIRMED** — when reproducible target evidence closes the behavior contract, promote the object to its precise semantic name. In the same coherent materialization pass, remove obsolete provisional markers and update the comment, type/prototype, enum/field names, boundary and proven links/relationships that depend on the stronger conclusion.
4. **CONTRADICTION** — stop relying on the affected semantic edge immediately. Demote or neutralize any name/type/comment that now asserts too much, record the conflicting evidence, and do not restore a strong name until the contradiction is resolved.
5. **WITHDRAWN interpretation** — retire or rename stale aliases and misleading semantic names. Keep a historical note only when it prevents a known-bad interpretation from being reintroduced.

Confidence is not monotonic. A semantic object may be promoted, demoted or withdrawn as new evidence appears. Persisted names must change with the evidence state; a stale strong name is itself a documentation defect.

#### Materialization checklist

For each recovered object, materialize as much of the following as the evidence supports:

- exact object identity: address, storage, action boundary or protocol location;
- current evidence state and the primary evidence point(s) that justify it;
- one canonical semantic name at the correct confidence level;
- a comment that states the recovered behavior/control contract and the remaining unknowns;
- type, prototype, enum, structure/field or register-bit semantics only when width/layout/ABI evidence supports them;
- proven transitions, inbound/outbound action links and data relationships, repairing stale boundaries/links before naming through them;
- retirement of stale aliases, contradictory comments and superseded provisional names;
- a stable save/checkpoint after the coherent semantic mutation batch.

When the same register, state, constant or protocol field appears in multiple actions, reuse one canonical semantic object/name after identity is established. Do not create per-action synonyms for the same recovered contract, and do not merge equal numeric values into one semantic object until references and lifecycle behavior prove that identity.

Raw addresses and numeric values remain exact evidence, but they are not semantic names by themselves. A precise-looking name must never encode a stronger owner, protocol, physical pin role, hardware block identity or product meaning than the current evidence state supports.

If a required rename/type/boundary/link mutation is temporarily blocked by tooling, annotate the nearest stable object with the proven semantics, current evidence state and stale-metadata warning so the handoff surface does not silently preserve the wrong interpretation.

### Validation levels

Keep these levels separate:

- **implementation proof** — the target behavior/contract is recovered or implemented at source/static/native-analysis level;
- **execution proof** — the relevant path has been observed executing;
- **board proof** — target-board ownership, routing or physical behavior is established;
- **integration proof** — the modified/rebuilt implementation has been accepted on the target system with the required surrounding contracts and recovery path.

Never promote one level into another. A decoded path is not execution proof; a successful command is not board routing proof; a build is not integration proof.

### Coverage and progress

- Any percentage must name its denominator.
- Action-node naming coverage is not equivalent to feature, behavior or product completion.
- A control-path estimate must say which paths/contracts it includes and excludes.
- Prefer semantic route/contract closure over exhaustive naming of unrelated library code.
- When reporting progress, distinguish recovered behavior, unresolved routes, runtime evidence, board evidence and integration evidence.
- In ordinary user-facing progress, prefer semantic action names over raw addresses; exact addresses remain valid evidence in repository documentation and tool arguments.

### Evidence workflow

- Prefer narrow read-only evidence queries over broad speculative analysis.
- If one exact query/address/path fails or is blocked, do not blindly repeat it; switch to another legitimate evidence path.
- Keep evidence collection and semantic mutation separate when the next conclusion depends on the read result.
- Semantic mutations should be small and attributable: one name/comment/type/boundary change at a time, followed by a stable save/checkpoint as appropriate.
- Raw instruction/byte behavior is authoritative when a higher-level representation conflicts with it.
- Record contradictions explicitly and stop relying on the contradicted edge until resolved.
- Preserve known-good analysis state; do not stack speculative repairs on top of broken state.

### Provider / safety tool blocks

A provider, policy, safety or pre-tool block is infrastructure evidence, not target evidence. Do not interpret a blocked invocation as a firmware/hardware failure or as proof about the analyzed target.

On every such block during behavior analysis:

1. Re-read this unified hardware-reverse skill from the current authority before the next reverse-analysis invocation. This is a narrow re-bootstrap step intended to restore the active terminology, evidence model and routing constraints; it does not require rereading the whole workflow library.
2. Record the incident while the exact invocation is still available. Preserve the tool/provider surface, operation or method name, sanitized arguments sufficient to identify the request shape, intended evidence goal, exact block/error text, whether the backend was reached, and the result of any legitimate alternate evidence path. Never copy credentials, secrets or unnecessary sensitive payloads into an issue.
3. Check the configured infrastructure/provider incident tracker for an existing issue with the same failure class. If one exists, append the current invocation and result as a new evidence point. Otherwise open a new issue. Repeated occurrences belong in the same issue when they share the same root symptom so the evidence base grows instead of fragmenting.
4. Continue through a narrower or otherwise legitimate evidence path when one exists. Do not blindly repeat the same blocked call and do not use another tool merely to evade the safety/policy decision.
5. If the same class blocks again later, repeat the terminology re-read and append the new occurrence. Treat recurrence count and invocation diversity as useful diagnostic evidence.

The project/infrastructure layer owns the concrete incident repository or provider tracker. The reverse skill owns the requirement to make these blocks observable and deduplicated.

### Completion

Behavior analysis is not complete merely because every discovered action node has a name. Completion is defined by the project's actual acceptance surface: the required behavior/control contracts, implementation path, execution evidence, board ownership and integration/recovery gates.

## Persistent Analysis project and worker lifecycle

Use this section when the analysis backend stores persistent projects/programs but exposes session-local worker/program handles.

### Distinguish project, session and open program

- The persistent **project** owns saved analysis state on durable storage.
- A **project/session handle** is a live backend attachment to that project.
- An **open program** is a session-local handle to one saved program/artifact.

Loss of a session or open-program handle is not evidence that the persistent project or program analysis was deleted.

### Recovery order

When a previously available program disappears or an operation reports that the program is not open:

1. Check project/session status and persistent project contents.
2. If the project exists, reacquire/open the project session.
3. Reopen only the required saved program by its project path.
4. Reuse the saved program; do not re-import the original binary unless the durable project artifact is genuinely absent or unusable.
5. Treat the program as missing/corrupt only after the persistent file is absent or opening it produces a concrete storage/backend diagnostic.

Do not abandon the active behavior route merely because a live handle was released.

### Worker pools

Worker capacity/assignment is infrastructure state, not project identity.

- A project may remain sticky to one worker while its session is active.
- After idle release/restart, the same project may reopen on another eligible worker.
- Never encode worker index as part of durable project identity or evidence.

### Mapping and index state

Persistent bytes, program mapping and analysis/index state are different surfaces.

- A missing action/index entry does not prove the bytes are absent.
- A mapping/base mismatch can make valid bytes appear unavailable at the expected address.
- Before broad re-analysis, inspect the smallest known region and verify the expected mapping/load address.
- When a mapping/index repair is proven, save the corrected program state before relying on it across sessions.

### Known-good state

Before semantic mutation or repair:

- identify the canonical project/program;
- verify the current mapping/load assumptions;
- avoid creating competing mutable copies of the same binary without an explicit experiment boundary;
- preserve recoverable checkpoints when a mutation could invalidate existing references or analysis state.

### Backend defects

Keep session/transport/index defects separate from target-behavior findings. A project-open failure, dropped handle or stale index is tooling evidence, not firmware behavior. Record and fix the owning infrastructure layer when possible without rewriting target conclusions around a transient backend defect.

## Java/GhidraScript analysis and monitored jobs

Use this section before using programmable Analysis/Ghidra evidence tools or
designing a repeatable firmware-wide trace. It is the owner of the script
execution, promotion, persistence and monitored-job workflow.

### When to script

Use a bounded, read-only Ghidra Java/GhidraScript, P-code/SLEIGH pass or
controlled emulation when it is more reliable than repeated manual lookups,
especially for:

- cross-module MMIO/constant inventories and register owner searches;
- calculated/indirect addresses, data flow and control-flow traces;
- repeated checks of call/return edges, instruction/data classification and
  saved action boundaries;
- exhaustive writer/reader audits of a hardware field or protocol state;
- reproducible verification after a targeted metadata correction.

Do **not** write a new script for a straightforward question already answered
by instructions, XREF, CFG or a saved contract. Never redo confirmed reverse
work merely to increase script counts.

### Required two-stage script lifecycle

**Explore inline → verify evidence → register useful script in Analysis →
execute the registered script → retain findings in the canonical project.**

1. **Identify the target.** Confirm the canonical `project_id`, exact
   `program`, architecture, mapped addresses and existing metadata. One
   program must be selected explicitly when several are open. Bound the
   instruction/function count and the range being inspected.
2. **Probe online.** Submit a small Java `GhidraScript` source to
   `run_analysis_script_inline(project_id, program, code, args?, dry_run?)`.
   This is for early hypothesis tests and small, read-only surveys. Inspect
   the returned `success`, `console_output`, counters, instruction addresses
   and contradictions. A transport timeout is **not** proof of script failure
   or success. An inline execution uses an ephemeral server-side source/cache;
   it does **not** register the script for future sessions.
3. **Promote after useful proof.** Once the script produces a reproducible
   finding or is useful for follow-up/regression, store its **Java source in
   the Analysis/Ghidra server's configured persistent script root**, not as
   a permanent local file or a Git-tracked firmware artifact. Do not
   promote disposable failed experiments merely to keep everything.
4. **Prove registration.** Read back and compare the complete source bytes
   or digest; reject an existing same-name file with different contents
   rather than overwriting it silently. Run the registered script by its
   permanent path and verify its actual output. Only then discard any
   temporary local Java source. Preserve the script's stable name and
   purpose in the appropriate Analysis project knowledge.
5. **Materialize findings separately.** A stored script is a reusable tool,
   not semantic coverage. Write proven names, contracts, register fields,
   links and evidence to the canonical analysis program; save and read back
   those edits. Scripts and reverse annotations are different artifacts.

### How to register and run a persistent GhidraScript

First call `get_storage_info(project_id)` and read the **live**
`script_root.path`, existence and writeability. Where available, use the
Analysis provider's dedicated script upload/install API. Do not infer that
the Terminal workspace, an imported firmware `Program`, the temporary
inline compilation cache and the Ghidra script root are the same storage.

On an Analysis installation without a dedicated upload API, a **one-time,
narrowly scoped, authorized inline Java/GhidraScript bootstrap** may register
the reviewed source from inside the running Ghidra process:

- Resolve the configured `GHIDRA_MCP_SCRIPT_ROOT` and cross-check it with
  `get_storage_info.script_root.path`; refuse missing, unexpected or
  non-writable roots. Do not invent a mount path.
- Verify the expected canonical program and guard the target filename
  against directory traversal. Place only the intended `<ClassName>.java`
  under that root (not under a worker-specific temporary cache).
- Supply the reviewed source payload (for example as a bounded embedded
  UTF-8/Base64 payload), decode it **inside Ghidra**, and create the file
  with no-clobber semantics. If it exists, compare exact bytes and fail on
  a mismatch. Read back the resulting file; emit installed/identical counts.
- Do not patch firmware bytes, import the `.java` as a Ghidra `Program`,
  alter unrelated scripts or claim durable registration from a successful
  inline execution alone.

Run the registered source with
`run_analysis_script(project_id, program, script_name, args?,
timeout_seconds?, capture_output=true, dry_run?)`, setting `script_name`
to the **absolute source path in the discovered script root**. Prefer a
bounded but sufficiently long `timeout_seconds` for substantial audits.
Check the returned `success`, `script_path`, output and measured results.

**Headless caveat:** `list_scripts` may only describe desktop Script Manager
usage; it is not an authoritative inventory of headless installed sources.
Successful execution **by permanent absolute path**, with an exact source
readback, is stronger registration evidence. If the configured script root
is not persistent/shared across the intended worker restarts, fix that
storage contract before relying on the script across sessions.

### Long-running analyses as monitored jobs

Prefer an Analysis-native asynchronous task/status API if the current
provider exposes one. **Do not invent one:** on versions where
`run_analysis_script` is synchronous, it may expose an execution
`timeout_seconds` but no script task ID, while
`run_analysis_script_inline` may not expose a tool-level timeout.

For longer scripts use the project's approved **Terminal job surface** with
a small, bounded client/runner that submits a real Analysis MCP request
against the canonical project (not an alternate analysis database):

1. `job_start(workspace_id, command=<approved Analysis MCP client command>,
   label=<audit purpose>, timeout_seconds=<outer budget>)` returns `job_id`.
   The client calls `run_analysis_script` for a registered script (or
   `run_analysis_script_inline` for the initial proof), explicitly
   specifying `project_id` and `program`. Set the inner script timeout
   separately and make the outer job budget larger to allow setup/output.
2. Capture `job_id`, script name, program, intended scope and expected
   output. `job_status(job_id)` checks lifecycle; `job_read(job_id,
   cursor, max_bytes?, wait_seconds?)` retrieves only new output and returns
   `next_cursor`; `job_wait(job_id, timeout_seconds)` waits for an
   intermediate or terminal state. Advance the cursor instead of rereading
   old logs.
3. Interpret **terminal job exit**, Analysis tool `success` and script
   output together. An outer process that exited with `0` is not enough if
   the Analysis response reports failure or script output contains an
   execution error. Count a trace as proven only from its actual findings.
4. A running job proves only that the client process is alive; a synchronous
   Analysis call may buffer Java `println` output until completion. For
   meaningful intermediate progress use smaller bounded stages/checkpoints,
   explicit per-stage counts, or a provider-supported progress endpoint.
   Do not invent progress percentages from elapsed time.
5. On a client timeout or disconnect, **inspect the existing job and
   project/worker state before resubmitting**. Never stack identical heavy
   scripts on a busy program. Use `job_cancel` or worker recovery only at a
   real decision boundary, accounting for unsaved edits and the project's
   known-good state.

A transient runner may live in an approved orchestration workspace; it is
**not** the canonical home for promoted `.java` scripts. Never require the
user to operate a terminal when an authorized job tool can do so.

### Evidence and safety

- Default to read-only Java scripts. Mutation requires a scoped proof,
  known-good baseline, exact target verification and save/readback.
- Enforce bounded scans, cancellation checks, and a clear distinction
  between instruction-decoded hits and raw words that might be data.
- For every useful run, record *examined instructions/functions, distinct
  owners, new traced edges, confirmed vs likely claims, changes actually
  saved, script count, and remaining contradictions*. Report deltas rather
  than repeated worker/queue bookkeeping.
- Static script output is implementation/behavior evidence, not runtime
  execution proof, board proof, or completion of a whole hardware block.
- Respect script-execution permissions and provider security decisions.
  If installation/execution is unavailable, report the exact missing
  capability; do not silently replace the analyzer's script library with
  local or Git storage, or route around a security block.
