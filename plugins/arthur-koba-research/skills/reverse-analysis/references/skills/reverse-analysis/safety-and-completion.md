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

1. Re-read [terminology and evidence](terminology.md) from the current authority before the next analysis invocation. This is a narrow re-bootstrap step intended to restore the active terminology, evidence model and routing constraints; it does not require rereading the whole workflow library.
2. Record the incident while the exact invocation is still available. Preserve the tool/provider surface, operation or method name, sanitized arguments sufficient to identify the request shape, intended evidence goal, exact block/error text, whether the backend was reached, and the result of any legitimate alternate evidence path. Never copy credentials, secrets or unnecessary sensitive payloads into an issue.
3. Check the configured project or infrastructure incident tracker for an existing issue with the same failure class. If one exists, append the current invocation and result as a new evidence point. Otherwise open a new issue. Repeated occurrences belong in the same issue when they share the same root symptom so the evidence base grows instead of fragmenting.
4. Continue through a narrower or otherwise legitimate evidence path when one exists. Do not blindly repeat the same blocked call and do not use another tool merely to evade the safety/policy decision.
5. If the same class blocks again later, repeat the terminology re-read and append the new occurrence. Treat recurrence count and invocation diversity as useful diagnostic evidence.

The project/infrastructure layer owns the incident tracker. This skill requires blocked analysis invocations to be observable and deduplicated.

### Completion

Program analysis is not complete because all functions have names. Completion follows the user's actual scoped acceptance criteria: recovered contracts and meaningful paths, plus execution, hardware, implementation or integration only when requested or necessary.
