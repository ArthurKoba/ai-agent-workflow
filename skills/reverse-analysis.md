# Reverse Analysis

Self-contained skill for analyzer-driven examination of program behavior:
EXE/PE/ELF files, BIOS/UEFI, applications, libraries, drivers, firmware,
embedded binaries, and other programs supported by the selected analyzer.

Use this standalone skill file for terminology, trace methodology, semantic recovery,
confidence and proofs, Ghidra/Analysis project lifecycle, Java/GhidraScript,
persistent scripts and monitored jobs. Its rules do not require hardware,
a board, or a low-level target. Keep related analysis rules in this same
file, not in subdirectories or further skill modules. Project-owned target scope,
tool access, and validation criteria take precedence.

## Evidence-first

- Check existing analysis, names and proof before re-tracing a closed behavior.
- Prefer one canonical indexed project and preserved target bytes/source over
  extracting or importing duplicate mutable copies.
- Record the target's identity where relevant: version, binary hash, PE/ELF
  section layout, firmware/BIOS region, platform, CPU/language, image base,
  address mapping, relocations, loader/compiler and ABI assumptions.
- Define the observable question and the next evidence boundary before
  starting a broad scan.

## External reference stopping rule

External SDKs, symbols, PDB/DWARF data, libraries, protocol documents,
vendor information and related builds are possible clues, **not proof of
the target's behavior**. Use them when they materially reduce uncertainty.

For a poorly documented program, chipset or proprietary application,
once broad searches for sources and documentation have been exhausted,
do not repeat them as a ritual on each session. Reopen research only with
a new concrete lead (exact version, hash, symbol server, vendor SDK,
artifact locator, document or direct user request). Preserve useful and
negative search results. Target code and observed behavior take precedence
over analogies to another version or platform.

## Mandatory high-level-first analysis after import

1. **Identify and enable the architecture.** Inspect the imported program's
   format, processor/bytecode ISA, ABI, loader and address mapping. Attach the
   correct analyzer language/processor/loader. If support is absent, implement
   or integrate the needed decoder/language/loader and decompiler support;
   record any remaining unsupported scope explicitly, never guess an ISA.
2. **Analyze before tracing.** Run the analyzer's applicable automatic analysis
   for executable code and confirm it completed: function boundaries, CFG,
   references and data flow. Reuse valid saved analysis rather than rerunning
   it each session; do not treat data-only regions as machine code.
3. **Decompile and work at a high level.** Generate and read C-like pseudocode
   for the relevant native functions and their callers/callees. This is the
   mandatory **primary** representation wherever supported. Recover semantic
   names, prototypes, structures, field types and constants in the canonical
   analyzer; regenerate pseudocode after corrections, then save and read back.
   Do not maintain a hand-written C mirror as a second source of truth.
4. **Use low-level evidence only when necessary.** Decompilers may misread an
   ABI, argument width, indirect call, branch, register or side effect. For a
   *specific, bounded* ambiguity, inspect instructions/registers/IR/raw bytes,
   correct supported metadata and return to pseudocode. Such inspection is
   permitted and authoritative, but continuous assembly/register/hex-first
   analysis is **not** the default while a usable high-level view exists.
5. **Use the right representation.** For ACPI AML inspect decompiled ASL;
   for VM/bytecode or unusual packet formats attach/implement the appropriate
   decoder and high-level model. Do not force data tables into a native C
   decompiler or substitute raw hexadecimal reading for available structure.

## Trace and recovery process

Trace program behavior through actual control and data dependencies,
not by naming isolated functions or repeatedly proving known facts.

1. **Locate anchors:** program entry, exports/imports, callbacks, event or
   command handlers, API calls, literals, strings, objects/vtables, types,
   exception handlers, device registers (when present), or external inputs.
2. **Trace control:** callers/callees, CFG, XREF, dispatch tables, indirect
   branches/calls, state-machine transitions and error/cleanup/retry paths.
   Distinguish *code present* from *reachable or observed executing*.
3. **Trace data:** inputs, return values, calling convention/ABI, object
   fields, globals, buffers, producers/consumers, transforms and
   externally visible effects (files, network, UI, services, peripherals).
4. **Reconstruct behavior:** identify the algorithm/contract, parameters,
   preconditions, outputs, modes, limits, errors, resource ownership and
   interaction with other modules. Work from the high-level representation
   above; verify disputed claims with targeted instructions/IR or observations.
5. **Materialize:** apply defensible semantic names, types, structures,
   transitions, references, evidence comments and uncertainty to the
   canonical Analysis project. Save, then read back the changed objects.
6. **Move to a new gap:** avoid repeated proof of closed branches; track
   uncertain edges and meaningful work needed to close the feature.

A PE/EXE application, BIOS/UEFI boot path, library function, driver,
DSP algorithm or firmware service can all follow this workflow. Hardware
registers, pin routing and board acceptance are optional target-specific
concerns, **not requirements for ordinary program analysis**.

## Program identity and environment

Before mutation identify the canonical project, selected program and
actual mapped code/data. Related program versions can suggest semantics,
but do not assume identical API/ABI, offsets, structures, callbacks,
device registers or lifecycle. The examined target wins.

When static evidence cannot settle behavior, define a bounded authorized
debugger/emulation/trace experiment and the required observation. Preserve
the known-good baseline. For hardware or other stateful targets use:
`baseline → action → observation → rollback → postcondition`.

Stateful software processes, drivers, media pipelines or hardware interfaces
need clear ownership. Do not launch competing sessions or change target
state speculatively. A static behavior contract is sufficient for an
analysis-only task; implementing a replacement or achieving system
integration is a separate acceptance level.

## Terminology, semantic contracts and evidence

Use this terminology for both high-level program behavior and native code.

### Vocabulary

Use stable names for concepts: **program**, **module**, **function/method**,
**callback**, **handler**, **state**, **input**, **output**, **side effect**,
**dispatcher**, **branch/transition**, **producer/consumer**, **behavior
contract**, **evidence point** and **semantic coverage**.

When using an analyzer that calls functions **action nodes**, the terms
`action node`, `action boundary`, `action map`, `action route`,
`action link` and `low/high-level action view` refer specifically to its
code/control representation. Do not label a device, data structure, external
process or protocol as an action node. Prefer the actual program's names when
they are known.

Raw instruction/register names, ABI/API signatures, imported symbols,
addresses and protocol IDs remain exact evidence even after semantic renaming.

### Evidence states

- **CONFIRMED**: primary target evidence directly supports the claim:
  instructions, control/data flow, source, runtime observations, or verified
  hardware evidence if applicable.
- **LIKELY**: multiple independent clues support a bounded hypothesis but
  the precise behavior is not fully proved.
- **UNKNOWN**: available information cannot establish the claim.
- **CONTRADICTION**: authoritative findings disagree; affected semantics
  must not be treated as settled.
- **WITHDRAWN**: a historical interpretation was invalidated; this is not
  a live confidence state.

An imported API, SDK feature or code path does not automatically prove that
it runs or is exposed. A firmware capability additionally does not prove
physical wiring. Keep capability, reachability, execution and topology
claims separate.

### Semantic naming lifecycle

Every recovered semantic object must track confidence: functions, methods, callbacks, imports, globals, structures, class/object fields, constants/enums, state machines, call links, addresses and (when present) device registers.

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
- types, prototypes, enum, class/structure fields or register bits only when size/layout/ABI evidence supports them;
- proven transitions, inbound/outbound action links and data relationships, repairing stale boundaries/links before naming through them;
- retirement of stale aliases, contradictory comments and superseded provisional names;
- a stable save/checkpoint after the coherent semantic mutation batch.

Reuse a single canonical semantic name for the same global, field, constant, state or register after proving its identity. Do not create per-function synonyms or merge unrelated objects just because they have the same numeric value.

Raw addresses and numbers are proof points, not semantic names. Do not encode an owner, algorithm, protocol or physical role in a name unless actual target evidence supports it.

If a required rename/type/boundary/link mutation is temporarily blocked by tooling, annotate the nearest stable object with the proven semantics, current evidence state and stale-metadata warning so the handoff surface does not silently preserve the wrong interpretation.

### Validation levels

- **Static/implementation proof** — source, instructions, references and
  analyzed data/control flow establish a behavior contract.
- **Execution proof** — the relevant target path and side effects were
  actually observed under identified conditions.
- **Integration proof** — behavior meets the actual surrounding system
  acceptance contract, when integration is part of the task.
- **Board proof** — physical device ownership/routing was observed, only
  when physical hardware is in scope.

Do not promote static results to execution proof, a build to integration
proof, or a documented capability to physical-wiring proof.

### Coverage and progress

- Every percent must state its scope and denominator; functions named,
  semantics recovered and feature coverage are separate quantities.
- Prefer completed control/data contracts to renaming unrelated functions.
- Report deltas: inspected/understood/renamed functions, traced control/data
  paths, new scripts executed, behavior contracts confirmed, objects saved
  and unresolved contradictions. Show `before → after` when measurable.
- If no useful fact was established, report zero confirmed results and the
  actual blocker. Do not invent percentages or count exploratory calls as
  proven recovered behavior.
- Keep addresses and numeric proof in annotations; prefer meaningful
  semantic names in user-facing reports.

### Evidence workflow

- Prefer narrow read-only evidence queries over broad speculative analysis.
- If one exact query/address/path fails or is blocked, do not blindly repeat it; switch to another legitimate evidence path.
- Keep evidence collection and semantic mutation separate when the next conclusion depends on the read result.
- Semantic mutations should be small and attributable: one name/comment/type/boundary change at a time, followed by a stable save/checkpoint as appropriate.
- Raw instruction/byte behavior is authoritative when a higher-level representation conflicts with it.
- Record contradictions explicitly and stop relying on the contradicted edge until resolved.
- Preserve known-good analysis state; do not stack speculative repairs on top of broken state.

### Provider / safety tool blocks

A provider, policy, safety or pre-tool block is infrastructure evidence, not evidence that the analyzed program failed. Preserve that distinction.

On every such block during behavior analysis:

1. Re-read the terminology/evidence section of this reverse-analysis skill from the current authority before the next analysis invocation. This is a narrow re-bootstrap step intended to restore the active terminology, evidence model and routing constraints; it does not require rereading the whole workflow library.
2. Record the incident while the exact invocation is still available. Preserve the tool/provider surface, operation or method name, sanitized arguments sufficient to identify the request shape, intended evidence goal, exact block/error text, whether the backend was reached, and the result of any legitimate alternate evidence path. Never copy credentials, secrets or unnecessary sensitive payloads into an issue.
3. Check the configured infrastructure/provider incident tracker for an existing issue with the same failure class. If one exists, append the current invocation and result as a new evidence point. Otherwise open a new issue. Repeated occurrences belong in the same issue when they share the same root symptom so the evidence base grows instead of fragmenting.
4. Continue through a narrower or otherwise legitimate evidence path when one exists. Do not blindly repeat the same blocked call and do not use another tool merely to evade the safety/policy decision.
5. If the same class blocks again later, repeat the terminology re-read and append the new occurrence. Treat recurrence count and invocation diversity as useful diagnostic evidence.

The project/infrastructure layer owns the incident tracker. This skill requires blocked analysis invocations to be observable and deduplicated.

### Completion

Program analysis is not complete because all functions have names. Completion follows the user's actual scoped acceptance criteria: recovered contracts and meaningful paths, plus execution, hardware, implementation or integration only when requested or necessary.

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

Keep session/transport/index defects separate from target behavior. A project-open failure, dropped handle or stale index is tooling evidence, not target-code proof. Record and fix the owning infrastructure layer when possible without rewriting target conclusions around a transient backend defect.

## Java/GhidraScript analysis and monitored jobs

Use this section when a repeatable analysis script or broad control/data-flow audit improves target evidence. It is the owner of the script
execution, promotion, persistence and monitored-job workflow.

### When to script

Use a bounded, read-only Ghidra Java/GhidraScript, P-code/SLEIGH pass or
controlled emulation when it is more reliable than repeated manual lookups,
especially for:

- cross-module call/import maps, constants, global owners, and MMIO/register maps where applicable;
- calculated/indirect addresses, data flow and control-flow traces;
- repeated checks of call/return edges, instruction/data classification and
  saved action boundaries;
- exhaustive writer/reader audits of a program field, global, protocol state or hardware register when present;
- reproducible verification after a targeted metadata correction.

Do **not** script questions already answered by XREF/CFG/instructions or a saved contract. Rewriting confirmed behavior to increase script counts is not progress.

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
   a permanent local file or a Git-tracked target artifact. Do not
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

### Project-owned Java script libraries

Every canonical Analysis project owns a **distinct persistent script library**,
keyed by its stable project identity rather than worker number. Script listing,
installation and execution must show and accept only that project's scripts,
including after worker reassignment. Another project's scripts must not appear
in its Script Manager/search results or be executable through its project API.
An explicitly authorized shared library is a separate opt-in exception.

Confirm the project's effective `get_storage_info(project_id).script_root`
and enforce root containment on both reads and writes. A common global root,
filename prefix or subdirectory **without server-side project scoping** is not
isolation: treat it as an infrastructure blocker, not as completed migration.
Do not move scripts through a different target's project session.

For migration, inventory and hash all sources, stage no-clobber copies in
distinct project-owned roots, then verify listing, allowed execution and
cross-project denial **for each affected project**. Preserve the old library
until the new route and rollback are proven; never silently delete, overwrite,
relabel ownership or count a migrated file as a newly recovered behavior.

### How to register and run a persistent GhidraScript

First call `get_storage_info(project_id)` and read the **live**
`script_root.path`, existence and writeability. Where available, use the
Analysis provider's dedicated script upload/install API. Do not infer that
the Terminal workspace, an imported firmware `Program`, the temporary
inline compilation cache and the Ghidra script root are the same storage.

On an Analysis installation without a dedicated upload API, a **one-time,
narrowly scoped, authorized inline Java/GhidraScript bootstrap** may register
the reviewed source from inside the running Ghidra process:

- Resolve the **project-specific** script root reported by
  `get_storage_info(project_id)`, check it is writable and confined to the
  configured storage parent, and refuse a global/shared effective root.
  `GHIDRA_MCP_SCRIPT_ROOT` alone may identify only that parent; do not
  infer the project's own directory from it without backend confirmation.
- Verify the expected canonical program and guard the target filename
  against directory traversal. Place only the intended `<ClassName>.java`
  under that root (not under a worker-specific temporary cache).
- Supply the reviewed source payload (for example as a bounded embedded
  UTF-8/Base64 payload), decode it **inside Ghidra**, and create the file
  with no-clobber semantics. If it exists, compare exact bytes and fail on
  a mismatch. Read back the resulting file; emit installed/identical counts.
- Do not patch target bytes, import the `.java` as a Ghidra `Program`,
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
- Static script output is behavior evidence, not proof of runtime execution or completion of an entire subsystem.
- Respect script-execution permissions and provider security decisions.
  If installation/execution is unavailable, report the exact missing
  capability; do not silently replace the analyzer's script library with
  local or Git storage, or route around a security block.
