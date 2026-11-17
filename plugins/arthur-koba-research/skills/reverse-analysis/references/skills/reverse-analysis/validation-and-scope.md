### Validation levels

- **Static/implementation proof** — source, instructions, references and
  analyzed data/control flow establish a behavior contract.
- **Execution proof** — the relevant target path and side effects were
  actually observed under identified conditions.
- **Integration proof** — behavior meets the actual surrounding system
  acceptance contract, when integration is part of the task.
- **Board proof** — physical device ownership/routing was observed, only
  when physical hardware is in scope.

Do not promote static results to execution proof, a build to integration
proof, or a documented capability to physical-wiring proof.

### Coverage and progress

- For firmware/BIOS reverse engineering, define the assessed unit before assigning
  progress: the **specific target image/version** and a named interface, routine
  or behavior contract. Count recovery of the code, paths, data, decisions,
  errors and observable handoff **present in that target**. Distinguish
  an individual WMI/ACPI command contract from the whole device feature.
- A call from the target to an EC, chipset, driver or another firmware
  component is a boundary: recover its target-side inputs, outputs, guards
  and error handling. Do **not** subtract progress because the callee's
  internal firmware, on-device behavior, OS integration, or tests of another
  platform/BIOS are unknown, **unless they are expressly included in the
  current task's artifact and acceptance scope**. Track those as separate
  unknowns or tasks, without silently expanding the denominator.
- **100% of a scoped static contract** means every relevant target-resident
  branch, data transformation, call/handoff and failure behavior has been
  recovered or its provable boundary explicitly established, with no
  unresolved in-scope contradiction. It does **not** mean a complete
  subsystem, device execution, product readiness or a compatible OS driver.
  If target-resident code or semantics remain unresolved, name those exact
  gaps instead of declaring the contract complete.
- Reject pseudo-precise near-completion figures such as 95% or 98% when
  there is no traceable denominator or outstanding in-scope evidence.
  Close the bounded contract at 100% if its acceptance gates are met;
  otherwise state the concrete missing gates or use an honest qualitative
  estimate. If an older score mixed external requirements into this
  denominator, **withdraw and rebaseline** it explicitly rather than
  portraying the scope correction as newly recovered behavior.

- Every percent must state its scope and denominator; functions named,
  semantics recovered and feature coverage are separate quantities.
- Prefer completed control/data contracts to renaming unrelated functions.
- Report deltas: inspected/understood/renamed functions, traced control/data
  paths, new scripts executed, behavior contracts confirmed, objects saved
  and unresolved contradictions. Show `before → after` when measurable.
- If no useful fact was established, report zero confirmed results and the
  actual blocker. Do not invent percentages or count exploratory calls as
  proven recovered behavior.
- Keep addresses and numeric proof in annotations; prefer meaningful
  semantic names in user-facing reports.
