# Scientific Implementation and Practical Validation

Use when implementing a proposed research method in code, hardware,
a system prototype or an operational environment, or when reporting
**practical significance and adoption**. This is about linking a
research proposition to a faithful, demonstrated realization; it does
not prescribe a language, framework, platform or deployment provider.

## Map method to execution

1. Identify the research problem, mathematical model and algorithm;
   determine inputs/outputs, assumptions, domain, states and expected
   behavior. Do not substitute a software component diagram for a
   model or an executable algorithm with branches and terminal states.
2. Separate general method parameters from *chosen test-system*
   parameters (device, runtime, channel count, data format,
   sample rate, threshold, tool version). Do not silently present
   a particular rig as a universal requirement.
3. Trace each significant method stage to its actual implemented
   module/function/data transformation and configuration. Verify
   the executed path, not merely the existence of files, classes
   or a planned architecture. Identify known library contributions
   and the author's own modifications.
4. Preserve the exact tested revision, build/run prerequisites,
   dependencies, initialization, sample data and operation scope
   when these affect the reproducibility of the claim.
5. Plan measurements with Scientific Experiments rather than
   treating compilation or static inspection as empirical proof.

## Claim only the achieved verification level

Classify every component and integrated behavior separately:
**proposed → specified → implemented → built → executed →
experimentally evaluated → deployed/adopted and evidenced**.

- Source code reviewed proves a specific implementation is present.
- A passing build proves that build in the stated environment.
- A unit test proves only the tested behavior under its conditions.
- End-to-end tests measure the named path, not unspecified features.
- A calculation of a memory budget does not prove device RAM use.
- A prototype demonstration does not certify routine field adoption.
- A product deployment is not automatically a scientific method
  contribution or a measured improvement.
- Absence of operational evidence must stay marked unverified.

When practical adoption, economic value, a registered implementation
or institutional use is claimed, look for a genuine evidence
artifact (deployment record, acceptance report, use-case result,
authorized certificate, reproducible operating trace, or other
appropriate primary proof) and check its exact scope, date and
origin. Never create fake adoption certificates or imply that
a published paper proves implementation in practice.

## Interpretation and handoff

Connect measured effects to the research criteria and competing
methods, including negative outcomes, accuracy/latency/resource
trade-offs, portability and known failure modes. Separate theoretical,
implementation-specific and operational limitations.

For every claimed impact report: method contribution, particular
implementation, proven running configuration, evidence level,
limitations, and next acceptance test. A theoretical work can
be complete without a prototype when implementation was not
part of its defined scope; do not fabricate hardware acceptance.

**Completion:** an independent reader can locate the actual
realization, establish its executed behavior and see exactly
which scientific and practical claims are supported.
