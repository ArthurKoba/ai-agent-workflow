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

- exact object identity: address, storage, code boundary or protocol location;
- current evidence state and the primary evidence point(s) that justify it;
- one canonical semantic name at the correct confidence level;
- a comment that states the recovered behavior/control contract and the remaining unknowns;
- types, prototypes, enum, class/structure fields or register bits only when size/layout/ABI evidence supports them;
- proven transitions, inbound/outbound action links and data relationships, repairing stale control-flow boundaries and links before naming through them;
- retirement of stale aliases, contradictory comments and superseded provisional names;
- a stable save/checkpoint after the coherent semantic mutation batch.

Reuse a single canonical semantic name for the same global, field, constant, state or register after proving its identity. Do not create per-function synonyms or merge unrelated objects just because they have the same numeric value.

Raw addresses and numbers are proof points, not semantic names. Do not encode an owner, algorithm, protocol or physical role in a name unless actual target evidence supports it.

If a required rename/type/boundary/link mutation is temporarily blocked by tooling, annotate the nearest stable object with the proven semantics, current evidence state and stale-metadata warning so the handoff surface does not silently preserve the wrong interpretation.
