# Reporting Protocol

Purpose: make progress reports concise, comparable across turns, and useful during long-running technical work.

This protocol defines how to interpret plain report requests versus full/detailed report requests. Project-specific vocabulary and evidence rules still apply.

## Report modes

### Plain / compact report

A plain report request means a **delta report**.

Typical triggers include:
- `report`, `status report`;
- `отчёт`, `короткий отчёт`, `упрощённый отчёт`;
- equivalent wording that asks for the current progress without explicitly asking for a full reconstruction of all known state.

The reference point is the **previous user-facing report for the same active goal**. Do not repeat facts, closed areas, unchanged progress, unchanged blockers or historical context that were already reported and did not materially change.

If there was no previous report for the active goal, use the task start or last explicit durable checkpoint as the baseline and treat the response as the first report.

A compact report must contain only the following information that is useful now:

1. **Changed progress**
   - Start the report with an explicit progress block; do not bury progress inside prose.
   - Show only active directions whose progress changed since the previous report.
   - Every changed direction must have a progress indicator.
   - If that direction was previously reported as a percentage, percentage reporting is **sticky**: continue with the same scoped `before% -> after%` metric unless the denominator/scope genuinely changed. An exact counter or state transition may supplement that percentage, but must not silently replace it.
   - If percentage reporting is established but the previous numeric percentage cannot be reliably recovered after a context switch, do not downgrade the metric to a counter/status. Report the current scoped `≈N%` and explicitly mark the previous numeric baseline as unavailable; restore `before -> after` once a reliable checkpoint exists again.
   - If no previous percentage exists but the direction is meaningfully estimable, provide one scoped scalar percentage. Use `before -> after` when the baseline is recoverable; otherwise show the current `≈N%` and state that the prior percentage baseline is unavailable.
   - Do not report percentage ranges such as `50-70%`.
   - When progress is approximate, use one scalar estimate derived with a stable scope/method.
   - Use an exact count or state transition **instead of** a percentage only when percentage progress would be materially misleading or undefined (for example a binary external approval, one unresolved decision, or a single pass/fail gate). In that case say briefly why a percentage is not meaningful.
   - If the denominator/scope changed, say so explicitly; do not compare incompatible percentages as if they were the same metric.
   - For a multi-direction active goal, include one scoped overall-goal percentage when an overall estimate is defensible. Once an overall-goal percentage has appeared in this workstream, it is sticky under the same rule as direction percentages. If an aggregate is genuinely not defensible, say so instead of inventing precision.

2. **Unique new results**
   - Report only findings, decisions, fixes, artifacts, semantic closures, contradictions or blockers discovered since the previous report.
   - Prefer semantic names and project vocabulary over raw coordinates when possible.
   - Do not restate stable baseline facts merely to make the report look complete.

3. **Goal status**
   - State whether the active goal is reached.
   - If not reached, state the remaining decision boundary in one concise sentence.
   - If reached, state that the goal is closed at the actually validated level and that another available goal/context may be selected next.

4. **Next path**
   - State the immediate next action or the small set of viable next paths.
   - Do not enumerate distant hypothetical work.

Keep a compact report short. Its purpose is to show **what changed since the last report**, not to reconstruct the whole project.

### Full / detailed report

A full report request means a **comprehensive current-state snapshot**.

Typical triggers include:
- `full report`, `detailed report`, `comprehensive report`;
- `полный отчёт`, `детализированный отчёт`, `подробный отчёт`;
- equivalent wording that explicitly asks for the whole current picture.

A full report may repeat previously reported information because its purpose is different. It should reconstruct the current state of the active objective across all meaningful directions.

A full report should include, as applicable:

1. active objective and acceptance boundary;
2. current progress for each meaningful direction;
3. accumulated confirmed results and material likely/unknown items;
4. completed, open and externally gated directions;
5. current contradictions/blockers and their effect;
6. current artifact/branch/validation state when relevant;
7. what remains before the active goal can be called complete;
8. next viable paths in priority order.

The same sticky-progress rules apply to full reports: if percentages are established or meaningfully estimable for an active direction/workstream, include them; exact counters may supplement them but do not silently replace them. Use state/counter-only reporting only when percentage progress is genuinely undefined or misleading, and say why. Never use min/max percentage ranges. Preserve validation-level distinctions; implementation proof, execution proof, board proof and integration proof are not interchangeable.

## Progress metric discipline

A report percentage is a communication metric, not objective truth by itself.

- Scope the percentage to a named direction or denominator.
- Reuse the same denominator/estimation basis across successive compact reports so `before -> after` remains meaningful.
- Exact `closed / total` counters are useful evidence and may accompany a percentage, but they do not automatically replace an established percentage metric.
- If the user or previous reports established percentage-based progress for the active workstream, preserve that format across subsequent reports unless the user changes it or the denominator becomes invalid.
- When no exact denominator exists but progress is still meaningfully estimable, use one scalar approximation and keep the estimation method stable.
- Never show a range merely to avoid choosing a usable scalar. If percentage progress is genuinely undefined or misleading, report a state/count transition and say why no percentage is shown.
- Do not revive an old percentage after its denominator was retired or redefined.

## Report checkpoint continuity

For long-running work, the previous report baseline must not depend only on fragile chat memory.

When the task already maintains durable Task Context, status, handoff or structured state, keep enough report-checkpoint information there to recover:
- the active goal;
- the last reported progress values/counters, including the active percentage denominator/estimation basis when percentages are in use;
- the last reported material findings;
- the next decision boundary at that report.

Do not create a second planning database only for reports. Reuse the project's existing durable task/state authority.

## Interaction semantics

- `report` by itself means: provide the report and stop there.
- `report and continue` means: provide the report, then continue the active work.
- `full/detailed report` by itself means: provide the comprehensive snapshot and stop there.
- If the user explicitly asks for another format or level of detail, that instruction overrides these defaults.

## Anti-patterns

Do not:
- omit percentages merely because an exact counter or state transition is also available when percentage reporting is already established or meaningfully estimable;
- silently switch a direction from percentage reporting to counters/status without explaining that the old denominator became invalid;
- repeat the same unchanged findings in every compact report;
- show every project area when only one or two changed;
- mix current progress with historical ranges;
- use `50-70%` style ranges in place of a usable scalar;
- silently change the denominator behind a `before -> after` comparison;
- claim completion merely because one direction reached 100%;
- omit the immediate next path when the goal remains open;
- continue technical work after a report-only request unless the user also asked to continue.
