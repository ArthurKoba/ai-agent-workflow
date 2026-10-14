# Program Analysis and Behavior Recovery

General skill for PE/ELF, BIOS/UEFI, firmware, drivers, libraries, bytecode and multi-processor SoCs. The Project selects the tool backend. Load only the applicable adapter: [Ghidra via Analyzer MCP](ghidra-analyzer.md) (current) or a future native CLI adapter (not yet included). Do not preload both without a comparison or migration task. This file owns common decisions, not backend commands.

## Terminology and proof

Use **program analysis**, **behavior recovery**, **dependency verification**, **machine-instruction decoding**, **Analyzer C/pseudocode generation**, **semantic coverage** in agent-authored tasks, annotations, reports and prose. Avoid the labels *reverse engineering*, *reversing*, *disassembly*, *decompilation*, *disassembler*, *decompiler* in those surfaces. Preserve exact names and spelling when essential for source, APIs, paths, tool calls, processor instructions, external quotations or identifiers. This changes vocabulary, not evidence requirements or authorization.

A *program* is an analyzed image/database item; a *module* is executable/data/bytecode unit; a *behavior contract* describes inputs, control decisions, data transformations, outputs, errors and effects. Analyzer **action nodes/links/maps** are code/control objects, not devices, physical buses or external processes.

Confidence: **UNKNOWN** (identity only); **LIKELY** (supported provisional hypothesis plus verification condition); **CONFIRMED** (precisely scoped target evidence); **CONTRADICTION** (conflicting facts, suspend affected claims); **WITHDRAWN** (retired disproved interpretation). Promote/demote stored names, comments, types and relationships when evidence changes. Static presence is not observed execution; reachability is not proof of runtime behavior. Distinguish static, execution, integration and hardware proofs. Vendor SDKs, symbols and similar builds are leads, not target proof.

## 1. Establish target and known-good state

Identify source/hash/version, sections and firmware containers, CPU/ISA, bit width, endian, image base, address spaces, mapping/relocations, ABI, loader, and code vs data. Inventory all executable and bytecode modules, including ACPI AML, DSP/IOP blocks, libraries and stubs. Confirm canonical saved project/program and reuse existing analysis; checkpoint before destructive reanalysis or semantic changes. Define target-resident behavior and its boundary to another chip, library, EC, OS or physical device. Keep exhausted public-reference searches as evidence; repeat only for a new specific lead.

## 2. Complete indexed C baseline

For validated, supported executable modules, the default is **one resumable bulk pass**, then fast navigation through persisted C and dependencies. A narrow diagnosis can precede the pass, but it is not completion.

1. Validate decoder, ISA, load mapping, ABI and code/data classification. For unknown ISA, pass section 3 first. Index unsupported regions; never invent C for them.
2. Reuse or complete native auto-analysis across the in-scope executable inventory. Enumerate functions/thunks, imports, exports, references, indirect tables and callbacks.
3. Generate analyzer-produced C-like output for **every discovered supported native function**. Save a searchable per-program index and counts: native total, C success, C failure, unsupported, external stubs. Log exact failures; retry only missing batches. Complete native C coverage requires all supported functions processed and zero failures, with unsupported separate.
4. Link direct/indirect calls, XRefs, relocations, imports, versions/ABI, callbacks, jump/dispatch tables, data producers/consumers and cross-program interfaces. Classify unproven edges rather than inventing CALL/XREF links. Do not assume matching symbol/GUID means matching implementation.
5. Use ASL or the appropriate representation for AML/other bytecode; do not force C on data.

**Resource rule:** completeness does not mean one uncontrolled job. Bound each module/function batch by RAM, duration and output size, checkpoint indexed progress, resume interrupted work, reuse prior C and graph results, and control heavy-worker concurrency. This minimizes later fine-grained MCP calls while preventing avoidable memory exhaustion.

## 3. Unknown ISA and multi-processor gate

Before trusting a whole-program graph for an undocumented CPU:
1. Identify execution domains, code/data, vectors/entry candidates, instruction size/encoding, endianness, address banks and memory spaces. Preserve competing hypotheses.
2. Validate a minimum decoder, register profile, branch/call/return targets and instruction side effects. Add ABI, loader and stack rules only as evidenced. Maintain deterministic instruction fixtures and regression cases.
3. Compare modeled register/memory transitions with real hardware or independent trusted traces when possible (**differential testing**); record input, register flags, RAM/MMIO and control transitions. Emulation is not equivalent to hardware execution.
4. Expand CFG and native C generation only for validated regions. Track unsupported instructions, ambiguous branches, interrupt modes and untested semantics separately.
5. For CPU/DSP/IOP and peripheral blocks, recover shared-memory layout, mailboxes, DMA, interrupts, timers and producer/consumer handoffs as explicit contracts. An ISA emulator alone is not a complete SoC.

## 4. Recover the requested behavior

Use indexed C and graph results to locate anchors: entries, callbacks, command handlers, symbols, objects/vtables, strings, constants, register access and external inputs. Follow callers/callees, conditional paths, state transitions, errors/retries and indirect branches. Trace value origins, parameters, return values, buffers, structures, globals, imports and side effects. Bound each question: *what decision or contract will this trace establish?*

Generated C is the **primary navigation and annotation representation** for supported ISA, but not proof of actual execution. If generated C, ABI, widths, pointers, jump targets, register effects or memory accesses are uncertain, inspect targeted raw instructions/IR/bytes or run bounded observation; correct metadata and regenerate C. Do not hand-maintain substitute C as recovered source; a separate model is allowed only for a clearly labeled, narrowly unsupported construct.

When static evidence cannot distinguish hypotheses, conduct an **authorized** debugger, modeled-execution or hardware experiment. Preserve baseline → action → observation → rollback → postcondition for stateful/physical targets; include concrete inputs and observed state. Distinguish code present, path reachable, simulation successful and runtime observed.

## 5. Annotate and persist conclusions

For each relevant function, constant, structure, global, state, cross-program edge or MMIO register:
- Preserve exact identity/address/space, supporting evidence and confidence; use conservative names with one canonical identity per actual object.
- Add concise contract and unknowns; apply types, enum/masks, prototypes, field layouts, and ABI only at evidenced widths/offsets.
- Correct wrong control boundaries, references and aliases before strengthening interpretations. Promote/demote dependent names, comments, types and regenerated C together.
- Save/checkpoint coherent, attributable annotation batches and **read back** mutations; a script output or successful MCP call alone does not mean state was saved. If mutation is blocked, preserve the evidence at the nearest stable object plus missing capability.
- Avoid recreating already verified work. Naming density, script count and raw call volume are **not** semantic coverage.

## 6. Reusable scripted verification

Precompute reusable call/dependency maps, indirect-call candidates, writer/reader inventories, C indexes and register access patterns once; later agents should query stored results. Select bounded read-only scripts for questions repeated across many functions, and retain parameterized scripts after a successful small probe. Separate **static control/data trace**, **emulated instruction execution**, and **instrumented runtime trace**; each supports different proof levels. Keep input, tool/version, program, tested range, output, error, evidence and repeatability.

Use provider-supported background jobs for heavyweight passes; otherwise use the project's approved supervised runner that invokes the *same canonical backend*. Track real job completion and saved data, not guessed percentages. Distinguish failed transport, tool rejection and actual target result. Check existing jobs/sessions before retrying a timeout; never stack identical heavy work on a mutable program. Scripts live under backend-specific ownership rules rather than as arbitrary copies.

## 7. Coverage and stop condition

Maintain separate **native C**, **dependency mapping**, and **behavior contract** inventories: discovered, partial, confirmed, contradicted, failed, unsupported. Every percentage needs a named target/version, unit and traceable denominator. A new discovery may enlarge the denominator without reversing completed work.

For register maps distinguish observed window, actual accessed addresses, confirmed registers, verified fields and implemented slots. Do not derive hardware coverage by dividing a window by an assumed stride. Avoid double-counting shared IRQ/register/route contracts across CPU/DSP/peripheral aggregates; if no stable denominator exists, state concrete gaps without invented percentages.

A scoped static contract is complete only when in-scope branches, data transformations, errors and target-side handoffs are evidenced; this does **not** certify external callee internals, runtime execution, physical wiring or product readiness. Report newly established conclusions, saved changes, remaining contradictions and next evidence boundary. Detailed report format belongs to [REPORTING_PROTOCOL](../../docs/REPORTING_PROTOCOL.md).

## Backend selection and blocked operations

Read the selected adapter for session/script/storage/tool behavior. A lost program handle, stale mapping or analysis index is a **backend issue**, not proof that saved bytes or target behavior disappeared. On provider/security blocks, preserve sanitized operation and refusal, do not blindly retry or evade restrictions with another transport; incident ownership belongs to infrastructure. Recover valid independent analysis only where permitted.
