# Behavior Analysis Vocabulary and Evidence

Use this module when reverse/embedded work is expressed as recovered behavior rather than ordinary source-level implementation.

## Vocabulary

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

### Scope boundary

`action node` and related action terminology apply to analyzed code/control structure. Do not use them as generic replacements for hardware parts, PCB routes, pins, buses, protocols, connectors or physical functions. A component identification is not an action node; a UART pin mux is not an action node; a protocol boundary is not an action node unless the statement is specifically about the code structure implementing it.

## Evidence states

Use explicit evidence states when a conclusion is not self-evident:

- **CONFIRMED** — reproducible target evidence directly supports the claim: bytes/instructions, low-level behavior, runtime output, package marking, continuity/scope measurement, hardware observation or equivalent primary evidence;
- **LIKELY** — multiple independent clues support the claim but direct target proof is incomplete;
- **UNKNOWN** — available evidence is insufficient;
- **CONTRADICTION** — authoritative observations disagree and the affected conclusion cannot be treated as settled.

Capability evidence is not topology proof. A datasheet feature, SDK option or firmware code path does not prove that a product PCB routes or uses that capability.

## Validation levels

Keep these levels separate:

- **implementation proof** — the target behavior/contract is recovered or implemented at source/static/native-analysis level;
- **execution proof** — the relevant path has been observed executing;
- **board proof** — target-board ownership, routing or physical behavior is established;
- **integration proof** — the modified/rebuilt implementation has been accepted on the target system with the required surrounding contracts and recovery path.

Never promote one level into another. A decoded path is not execution proof; a successful command is not board routing proof; a build is not integration proof.

## Coverage and progress

- Any percentage must name its denominator.
- Action-node naming coverage is not equivalent to feature, behavior or product completion.
- A control-path estimate must say which paths/contracts it includes and excludes.
- Prefer semantic route/contract closure over exhaustive naming of unrelated library code.
- When reporting progress, distinguish recovered behavior, unresolved routes, runtime evidence, board evidence and integration evidence.
- In ordinary user-facing progress, prefer semantic action names over raw addresses; exact addresses remain valid evidence in repository documentation and tool arguments.

## Evidence workflow

- Prefer narrow read-only evidence queries over broad speculative analysis.
- If one exact query/address/path fails or is blocked, do not blindly repeat it; switch to another legitimate evidence path.
- Keep evidence collection and semantic mutation separate when the next conclusion depends on the read result.
- Semantic mutations should be small and attributable: one name/comment/type/boundary change at a time, followed by a stable save/checkpoint as appropriate.
- Raw instruction/byte behavior is authoritative when a higher-level representation conflicts with it.
- Record contradictions explicitly and stop relying on the contradicted edge until resolved.
- Preserve known-good analysis state; do not stack speculative repairs on top of broken state.

## Provider / safety tool blocks

A provider, policy, safety or pre-tool block is infrastructure evidence, not target evidence. Do not interpret a blocked invocation as a firmware/hardware failure or as proof about the analyzed target.

On every such block during behavior analysis:

1. Re-read this behavior-analysis module from the current authority before the next reverse-analysis invocation. This is a narrow re-bootstrap step intended to restore the active terminology, evidence model and routing constraints; it does not require rereading the whole workflow library.
2. Record the incident while the exact invocation is still available. Preserve the tool/provider surface, operation or method name, sanitized arguments sufficient to identify the request shape, intended evidence goal, exact block/error text, whether the backend was reached, and the result of any legitimate alternate evidence path. Never copy credentials, secrets or unnecessary sensitive payloads into an issue.
3. Check the configured infrastructure/provider incident tracker for an existing issue with the same failure class. If one exists, append the current invocation and result as a new evidence point. Otherwise open a new issue. Repeated occurrences belong in the same issue when they share the same root symptom so the evidence base grows instead of fragmenting.
4. Continue through a narrower or otherwise legitimate evidence path when one exists. Do not blindly repeat the same blocked call and do not use another tool merely to evade the safety/policy decision.
5. If the same class blocks again later, repeat the terminology re-read and append the new occurrence. Treat recurrence count and invocation diversity as useful diagnostic evidence.

The project/infrastructure layer owns the concrete incident repository or provider tracker. The reverse skill owns the requirement to make these blocks observable and deduplicated.

## Completion

Behavior analysis is not complete merely because every discovered action node has a name. Completion is defined by the project's actual acceptance surface: the required behavior/control contracts, implementation path, execution evidence, board ownership and integration/recovery gates.
