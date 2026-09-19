# Role Map

Role describes responsibility; skill describes task domain.

- implementation → `IMPLEMENTER.md`
- independent verification → `REVIEWER.md`
- multi-agent/multi-repo coordination → `ORCHESTRATOR.md`

## Separate Reviewer is expected for serious changes

At minimum when a change:
- alters architecture or ownership;
- spans multiple repositories;
- affects boot/kernel/storage/hardware-critical paths;
- is destructive or recovery-sensitive;
- changes infrastructure/security/permissions;
- is prepared for release/upstream contribution;
- replaces a known-good hardware-proven contract;
- closes a major milestone as production-ready/complete.

Small local changes may use self-review unless the Project requires otherwise.

Reviewer and Implementer may use the same skill/domain docs, but their responsibility and mutation permissions differ.
