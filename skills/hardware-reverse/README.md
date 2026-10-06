# Hardware Reverse / Embedded Bring-up

## Sub-map
- behavior-analysis vocabulary, evidence states and proof levels → `behavior-analysis.md`
- persistent analysis project/session/program lifecycle → `analysis-project-lifecycle.md`

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
