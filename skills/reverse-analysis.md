# Reverse Analysis

Reusable skill for recovering program behavior in firmware/embedded targets, EXE/PE/ELF, BIOS/UEFI, libraries and drivers. This governs **reverse engineering**, not agent orchestration or independent review. Project authority selects the target, analyzer/MCP, permissions and acceptance scope.

## Canonical model

- **The saved analyzer project is the source of truth:** original bytes, memory map, analyzed instructions/functions, references, names, prototypes, structures, types, comments and confirmed contracts. Keep one canonical project per target/version; do not re-import duplicates or repeat proven work.
- **Decompiled C is a generated view, not stored source.** Ghidra produces it on request from bytes plus the saved project state. Decompiler process caches are transient; a restart does not erase saved annotations. Reopen the project and program, then request the current function's C-like pseudocode. Neither a full new analysis nor a bulk decompilation is needed to recover that view.
- **High-level first, not high-level only.** Use analyzer-generated C-like code as the primary reading surface when supported. Target instructions, P-code, registers and observed effects resolve specific doubts and override a wrong high-level interpretation. Continuous hex/assembly-first exploration is not the default.
- **Reconstruction is distinct from decompilation.** When asked to produce working replacement software, write separate clean source based on recovered behavior contracts and available execution evidence. This is allowed and useful; it does not supersede the canonical analyzer project. Do not manually transcribe entire binaries into a second pseudocode database or pretend generated C is original compilable source.
- **Evidence over guesses.** Successful parsing, function discovery, decompilation, external symbols or a plausible name does not by itself prove an algorithm or runtime behavior.

## Whole-program first pass

On normal tractable firmware and modest binaries, do the **complete initial analyzer pass**, even for thousands of functions. It saves repeated agent discovery work, identifies failures up front and gives a navigable program. It does **not** establish persistent precomputed C or oblige agents to read every body. For exceptionally large, malformed or unsupported targets, record a scoped exception rather than repeatedly failing.

1. **Identify target and mapping.** Record hash/version, format, ISA/sub-ISA, endianness, compiler/ABI, load base/relocations and code/data ranges. For embedded targets identify reset/interrupt vectors, flash/RAM, banks/overlays, address units and MMIO as applicable. For Windows binaries inspect imports/exports and debug symbols when present. Map embedded bytecode/ACPI separately. Fix/integrate the loader, SLEIGH language or processor model if support is missing; do not infer unsupported instruction meaning from hex.
2. **Run and repair automatic discovery.** Finish applicable auto-analyzers and reuse saved output. Classify executable vs data regions. Inspect gaps, orphan instruction/function candidates, vector/callback targets, indirect calls/jumps, tables and disconnected code. Repair only evidenced boundaries/references; a lack of XREF does not imply padding, and apparent bytes do not automatically justify a function.
3. **Identify known code before deep tracing.** Reuse exact symbol/type information (PDB/DWARF, SDKs, headers, device/register descriptions) and Function ID, BSim, Version Tracking, hashes or fuzzy/structural matching **when available**. Verify target identity, ABI/layout and actual behavior before importing suggested names; do not re-search exhausted external references without a new exact lead.
4. **Run a bounded, resumable bulk decompilation** of **all discovered native functions** on the tractable target, preferably server-side rather than thousands of individual MCP calls. Record program/function identifiers, counts of successful, failed, timed-out and unsupported cases, plus unresolved executable gaps. This establishes decompiler readiness and coverage of *discovered functions*, not complete semantic recovery. After metadata edits or restart, request affected functions on demand; repeat the full pass only for a justified coverage/decoder change.
5. **Save the baseline.** Preserve a recoverable checkpoint with verified mapping, auto-analysis and discovered functions. Do not destroy known-good names/types/comments merely to regenerate pseudocode.

## Recover semantics

1. **Begin with a behavior question.** Navigate from entry points, strings/constants, commands, imports/exports, callbacks, state variables, device registers and externally visible effects. Traverse callers/callees, CFG, XREF, dispatch tables, error paths and state transitions. Close useful end-to-end control/data paths rather than randomly naming functions.
2. **Follow data across functions.** Establish parameters, returns, calling convention, pointer ownership, buffers, globals, read/write owners, producers/consumers, transformations and side effects. Use interprocedural call-site evidence and forward/backward P-code dataflow where useful. Keep indirect targets and aliases unresolved when evidence cannot establish them.
3. **Recover reusable types.** Infer signedness, widths, struct/union layout, field offsets, stride, padding, alignment, enum/bit masks, parameter and return types **across all relevant accessors**. For embedded targets map MMIO fields, vector tables and state structures as the target supports; advertised firmware capability is not proof of physical wiring. Propagate justified types/prototypes to related functions, check contradictory field uses, then regenerate their pseudocode.
4. **Write meaning back to the analyzer.** Apply semantic names, prototypes, data types, structures, labels, references and concise purpose/algorithm/input/output/side-effect comments. Use native **batch mutations** for compatible, evidenced edits instead of one call per variable; use small scoped changes when the premise is uncertain. Save and read back. Raw addresses remain evidence points, never substitutes for semantic names. No insight counts as materialized if it lives only in a report or agent context.
5. **Revisit changed decompilation.** Names, signatures, memory layout and structures can change C-like output. Read a fresh view for affected callers/callees rather than relying on older text. Move on once the behavior contract is supported or its remaining unknown is explicit.

### Targeted low-level and execution work

Descend to assembly, bytes, registers and P-code for a **specific ambiguity** (bad function boundary, ABI, flags, stack, bank mapping, indirect target, register alias, interrupt, side effect or decompiler artifact), repair metadata and return to high-level analysis.

For a custom SLEIGH processor distinguish **opcode decoding**, **correct P-code semantics**, **successful generation of C**, and **faithful machine behavior**. A userop, unsupported instruction, synthetic context, or incomplete status/loop/interrupt model may create believable yet wrong C. Record those gaps and do not assign confident semantics until corroborated. If static evidence is insufficient, use bounded authorized emulation/debugger/trace tests with explicit input, expected observation and actual result; for stateful targets use baseline → action → observation → rollback → postcondition.

## Evidence and semantic names

Use consistent evidence states for functions, globals, fields, registers, constants and transitions:

- **UNKNOWN:** exact address/structure known, behavior not established; retain a neutral name.
- **LIKELY:** conservative provisional name with evidence and the remaining unknown.
- **CONFIRMED:** reproducible target evidence establishes a particular contract; promote associated name, type, comments and proven links together.
- **CONTRADICTION:** conflicting evidence; stop relying on the disputed meaning, neutralize overconfident names/types and resolve before promotion.
- **WITHDRAWN:** historical hypothesis disproved and retired; preserve a note only when needed to prevent its reuse.

Evidence confidence can decrease. Give one proven object one canonical meaning; do not merge independent objects with equal constants. Link each important claim to target addresses/instructions, dataflow, a trace or observed effects. Distinguish **static**, **observed execution**, **integration** and **hardware** acceptance. A high documentation score or named-function percentage does not prove semantic correctness. Report meaningful deltas with the correct denominator: discovered/decompiled/understood functions, closed paths, confirmed vs unknown links, saved objects and blockers. Completion follows the actual scoped behavior question.

## Persistent project / worker lifecycle

A **saved project**, an active **worker/project session** and an **open program handle** are distinct. If a program disappears, first inspect persistent project contents and session status, reacquire the session, then reopen the **saved** program by project path. Do not infer corruption or re-import binary bytes from a dropped handle. If analysis seems missing, verify image base, address spaces and current index before a destructive reanalysis. Worker assignment does not define project ownership; save/checkpoint before significant fixes and preserve the known-good state.

## Native tools, GhidraScript and long tasks

- Use the project-selected analyzer MCP for decompilation, metadata, type inference, XREF/CFG, P-code/dataflow, renaming, comments, bulk edits and save. Inspect **actual** exposed tools/arguments; never assume a provider exposes a named operation. Prefer one bounded batch to hundreds of small round trips; do not batch speculative edits.
- Script only repetitive or heavy questions better handled **inside the analyzer**: comprehensive read/write owner scans, indirect references, uncovered code, constant maps and reproducible data/control-flow probes. Do not rewrite results already provided by native queries or saved analysis.
- **Short exploration:** run a bounded, preferably read-only Java/GhidraScript inline where authorized, and inspect success, precise addresses, counters and errors. Inline source/compilation is temporary; this does **not** register a durable script or save recovered semantic annotations.
- **Reusable script:** promote only a useful, reproducible probe. Resolve the live **persistent script root** via analyzer storage diagnostics; prefer the dedicated upload/install API. Do not guess filesystem mounts or confuse script root with temporary compile cache, original binary or project database. Register with no-clobber/exact-content verification, read back its source or digest, execute it by its actual path, and validate its results. Script persistence and program annotation persistence are separate.
- **Long analysis:** prefer genuine analyzer-native async task/status APIs if provided; do not invent job IDs for synchronous calls. Otherwise use the approved persistent job surface to run a bounded client against the **same canonical project**. Capture job ID, target/script/scope, progress counts and expected evidence; read status and incremental output by cursor until terminal completion. Confirm both runner exit and analyzer-level success. A live process or elapsed time is not proof of progress.
- **Timeout:** inspect the existing job, session and saved analysis before retrying; do not stack equivalent expensive scripts or replace a busy worker speculatively. Use bounded chunks/checkpoints, cancellation checks and only authorized scoped writes. Treat tool/provider/safety blocks as tooling incidents rather than evidence of target behavior; record sanitized invocation and error in the owning tracker, never bypass permission decisions.

Script output is evidence, **not** the recovered program. Commit supported semantics to the canonical analyzer project and read them back. If a necessary decoder, tool, script-storage or execution capability is absent, state that limitation instead of fabricating coverage or an alternative authority.
