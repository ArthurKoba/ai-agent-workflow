# Code / Engineering Review

Reviewer is independent from the implementation pass.

## Reviewer does
- inspect exact diff/commits;
- verify ownership and architecture;
- check claims against source/evidence;
- look for regressions, hidden dependencies and missing gates;
- verify validation level is not overstated;
- produce approval or actionable findings.

## Reviewer does not
- silently fix implementation during the same review pass;
- use the same mutation identity to make the reviewed change;
- accept “tests passed” without understanding what they prove.

If fixes are required, return findings to Implementer or start a new explicit implementation cycle.

For serious work check ownership, state/doc sync, dependency closure, rollback, provenance, validation level, unrelated files and branch/history hygiene.
