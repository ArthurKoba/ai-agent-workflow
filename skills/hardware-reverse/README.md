# Hardware Reverse / Embedded Bring-up

## Evidence-first
- Do not restart reverse if an existing corpus/contract answers the question.
- Prefer one authoritative searchable corpus over repeated target extraction.
- Capture once; analyze offline.

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
