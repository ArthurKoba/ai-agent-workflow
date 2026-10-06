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
   - Show only active directions whose progress changed since the previous report.
   - Use `before -> after`, for example `50% -> 70%`.
   - Do not report percentage ranges such as `50-70%`.
   - When progress is approximate, use one scalar estimate derived with the same scope/method as the previous report.
   - If no defensible percentage exists, use an exact count or state transition instead of inventing a number, for example `3/8 -> 5/8` or `LIKELY -> CONFIRMED`.
   - If the denominator/scope changed, say so explicitly; do not compare incompatible percentages as if they were the same metric.

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

Use scalar percentages or exact counters, not min/max ranges. Preserve validation-level distinctions; implementation proof, execution proof, board proof and integration proof are not interchangeable.

## Progress metric discipline

A report percentage is a communication metric, not objective truth by itself.

- Scope the percentage to a named direction or denominator.
- Reuse the same denominator/estimation basis across successive compact reports so `before -> after` remains meaningful.
- Prefer exact `closed / total` when a real checklist exists.
- When no exact denominator exists but a project intentionally tracks approximate progress, use one scalar approximation and keep the estimation method stable.
- Never show a range merely to avoid choosing a usable scalar. If the estimate cannot be made responsibly, report a state/count transition instead.
- Do not revive an old percentage after its denominator was retired or redefined.

## Report checkpoint continuity

For long-running work, the previous report baseline must not depend only on fragile chat memory.

When the task already maintains durable Task Context, status, handoff or structured state, keep enough report-checkpoint information there to recover:
- the active goal;
- the last reported progress values/counters;
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
- repeat the same unchanged findings in every compact report;
- show every project area when only one or two changed;
- mix current progress with historical ranges;
- use `50-70%` style ranges in place of a usable scalar;
- silently change the denominator behind a `before -> after` comparison;
- claim completion merely because one direction reached 100%;
- omit the immediate next path when the goal remains open;
- continue technical work after a report-only request unless the user also asked to continue.
