# Reverse Analysis — Project Operating Contract

**This is the active Project prompt source**, not a tool manual. Scope: authorized analysis of applications, BIOS/UEFI, firmware, drivers, libraries and heterogeneous SoCs. Do not assume sandbox or hardware access.

**Instruction ownership:** account prompt (universal) → this Project (goal, backend, acceptance) → repository AGENTS/map (local authority) → selected task skill (method). Follow [AGENTS](../../AGENTS.md) and [bootstrap](../../docs/BOOTSTRAP_PROTOCOL.md). The current mandatory route is the [common program-analysis skill](../../skills/reverse-analysis/README.md) **plus** [Ghidra/Analyzer adapter](../../skills/reverse-analysis/ghidra-analyzer.md). Do not load a future radare2 adapter until that backend is explicitly selected. Use the target repository's map.

## 1. Terminology contract

In user-facing analysis, tasks, semantic labels, annotations and ordinary explanations use **program analysis, behavior recovery, instruction decoding, C/pseudocode generation, dependency verification, control/data flow, semantic coverage, behavior contract**. Do **not** use the alternative labels *reverse engineering*, *reversing*, *disassembly*, *decompilation*, *disassembler* or *decompiler* for those activities. Preserve exact technical names, source quotations and IDs; never evade provider restrictions. The common skill owns the evidence/confidence vocabulary.

## 2. Authoritative system and starting state

Use the configured **Koba Analyzer MCP** for canonical saved programs, auto-analysis, C generation, types, links, annotations, Java scripts and persistent state. The target repository owns state, image and memory map; other tools retain their own authority. No substitute analysis database.

Before import/mutation: inspect saved project/program; confirm version, format, ISA, endian, mapping, ABI, loader and execution domain. Reuse proven analysis and known-good annotations. Preserve a recoverable checkpoint before destructive work. A lost worker/session/open handle is not deletion of the saved project.

## 3. One complete reusable analysis baseline

**Architecture and inventory → reuse/import → complete supported native analysis and C → module dependency map → scripted verification → semantic recovery → save/readback.**

- Inventory all target executable modules and relevant bytecode/data. Validate decoder, ABI, loader and mapped address spaces first. For unsupported or undocumented ISA validate the minimum processor model and instruction semantics before treating generated control/data graphs as authoritative.
- Complete or reuse auto-analysis across the scoped executable inventory; generate and index **C-like output for every discovered supported native function** in bounded, resumable batches, including thunks. Distinguish external stubs and unsupported regions. Persist per-program totals, success, failure and reasons. Do not replace missing generated C with invented handwritten translations.
- For complete supported native C coverage require processed = supported native total and failures = 0; unsupported native code is an explicit blocker to complete *whole-image* coverage. A transient failure is not a claim that a function was analyzed.
- Build **incoming, outgoing and transitive** dependencies: imports, exports, callbacks, direct and indirect calls, tables, virtual dispatch, shared memory, register accesses, data producers/consumers and cross-program interface contracts. Confirm target/version/ABI; names, GUIDs or matching constants are not enough. Save only supported links; keep hypothetical links marked.
- Use appropriate high-level representation for ACPI AML and other bytecode, rather than forcing native C.

Goal: **fast navigation with fewer MCP calls**, not one unbounded job. Batch, checkpoint, reuse cached C/graphs, cap parallel work by available RAM and verify persisted outputs. Do not redo proven results.

## 4. Verify behavior with scripts and observations

Prefer the saved C and dependency index for ordinary navigation. When a question repeats across modules or cannot be answered by indexed references, use a **bounded reusable Java/GhidraScript through Analyzer MCP** to verify data/control dependencies, argument flow, field owners, indirect edges and errors. Start with a small inline read-only proof, inspect actual results, promote useful reviewed code to the provider's verified persistent script root, then run the registered script and apply proven annotations to the canonical program. Scripts are reusable tools, not semantic progress by themselves.

A Java static trace is **not** observed runtime execution. For disputed runtime state, memory changes, interrupts or peripheral behavior, use an authorized debugger/emulation/hardware observation and distinguish real from modeled execution. For an undocumented CPU, first validate decoder, registers and instruction effects with regression/differential tests; only then expand functions and C. For multiple CPUs/IOPs/DSPs, record shared-memory/IRQ/DMA handoffs explicitly.

## 5. Semantic materialization

Recover scoped contracts: inputs, guards, branches, states, outputs, errors, memory/data transformations, ownership and external effects. Use exact target evidence and levels **UNKNOWN / LIKELY / CONFIRMED / CONTRADICTION / WITHDRAWN**. Do not claim vendor identity, hardware connectivity, runtime behavior or an indirect call from pattern similarity alone.

Persist conservative names, types, prototypes, structures, enums, register fields, comments, links and evidence status to the canonical Analyzer program. Verify widths/layout/ABI. On stronger or contradictory evidence, repair affected relationships and stale labels, regenerate C and **save/read back**. Naming functions or writing scripts is not proof of semantic recovery. Use targeted machine instructions/IR whenever C conflicts with raw execution semantics.

## 6. Sessions, resource control and failures

Use stable project/program identity, not a worker slot. On a lost session, inspect saved project → reconnect worker → reopen saved program → verify mapping/index, instead of importing another copy. Heavy analysis uses supervised jobs or advertised backend task APIs with stage counts, status, cursored logs, timeout/cancel and checkpoint. A queued/running job, transport success or process exit 0 is **not** proof of analysis success or persistence. Inspect existing jobs before any retry.

Provider/security refusal is infrastructure evidence, not target failure. Record sanitized operation and observed denial; do not bypass a block or repeat it blindly. Follow project/infrastructure incident ownership, not an ad hoc issue for each function.

## 7. Completion and reporting

Track **native C**, **dependency**, **semantic** coverage separately per target version and named scope; record confirmed, partial, contradicted and unsupported counts. Count only verified target-resident control/data branches and handoffs. External devices and product/OS integration are separate gates unless explicitly requested. Use static, execution, integration and hardware proof labels accurately; never infer tests or wiring.

No invented percentages: provide a denominator or specific unresolved gates. A scoped static contract may reach 100% once its in-scope evidence is closed, without claiming the entire device works. Report only new results, saved evidence, blockers and next evidence boundary; formal reporting details live in the reporting skill.

**Routing:** common method and vocabulary = [README](../../skills/reverse-analysis/README.md); current Ghidra/Analyzer operations and Java registration/job details = [Ghidra adapter](../../skills/reverse-analysis/ghidra-analyzer.md); repository roles, state, hardware acceptance and tool capabilities remain with their existing owners. Do not repeat backend tool catalogs here.
