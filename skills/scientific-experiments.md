# Scientific Experiments, Reproducibility and Comparison

Use when planning, running, interpreting or reviewing experimental,
simulation or computational evidence for a scientific hypothesis.
The task's declared outcome determines whether a controlled physical
experiment, theoretical proof or computational study is appropriate.

## Before execution

1. State the question and falsifiable outcome, baseline/controls,
   measured quantities and units. Define what an experiment can
   actually establish; testing a component does not prove a system.
2. Define the dataset/sample selection, partitioning, exclusions,
   preprocessing, reference or ground-truth construction, versions,
   operating conditions, parameter ranges, seeds and repetition
   protocol when applicable. Distinguish measured, simulated,
   calculated, illustrative and claimed external values.
3. Specify the **unit of evaluation** for every metric:
   samples, events, frames, devices, runs, subjects or other
   comparable units. For a percentage specify numerator,
   denominator and aggregation; distinguish percentage points
   from relative percentage improvement.
4. Choose a comparable scenario and input for every baseline.
   When an implementation adapts a published method, identify
   changes and avoid claiming a comparison to the full original
   method. Record memory, throughput, latency, accuracy,
   robustness or resource trade-offs as relevant to the claim.

## Evidence and analysis

- Preserve input provenance and executable calculation or
  notebook/script/workbook when supported. Avoid manual
  transcription of derived numbers that cannot be recomputed.
- Separate **computation time**, **end-to-end latency**, memory
  allocation, storage cost, accuracy and availability. A p99
  observation does not establish a hard deadline guarantee.
- Use repeated measurements and uncertainty/statistical treatment
  where warranted by the model and claims. Explicitly identify
  sample size, variability, exclusions, confidence assumptions
  and limits on generalization. Do not invent statistical
  significance or the missing raw observations.
- When optimizing weighted criteria or normalizing scores,
  justify weights and the reference scale; disclose sensitivity
  and avoid making general superiority claims from a
  selected favorable scenario.
- Reconcile every important number with its source data,
  equations, table, graph and surrounding explanation. A figure
  is a view of evidence, not a replacement for data provenance.
- When shortening a manuscript, preserve the minimum reproducible
  method (data IDs, baseline, measurement scope, preprocessing,
  tolerance, parameters, repeats) in the text or an accessible
  cited appendix; do not conceal unfavorable conditions.

## Stopping and reporting

An observed failure or negative result can be valid scientific
evidence. A simulation doesn't prove device performance, a build
doesn't prove runtime behavior, and an untested experiment protocol
is still a plan. Before rerunning a failed/missing result, check
the actual status and whether a prior run has finished; don't
repeat non-idempotent experiments blindly.

Report: exact tested configuration, result and unit, comparison,
uncertainty/limitations, cost of improvement and reproducible
artifact location. If unavailable, report the missing evidence
rather than a plausible estimate.

**Completion:** a reader can reconstruct the stated measurement
and see why the conclusion applies to **these** conditions.
