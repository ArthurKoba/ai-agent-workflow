# Engineering workflow

This is the default lifecycle for substantial technical work.

## 1. Bootstrap

- Read project authority and current state.
- Resolve required local context.
- Verify the real execution/tool surface before assuming capabilities.

## 2. Define the decision boundary

Identify:
- current known-good state;
- exact task/acceptance criteria;
- next meaningful unknown;
- evidence needed to resolve it.

## 3. Implement or investigate

Use the smallest appropriate scope. Reuse existing artifacts/contracts instead of recreating them.

## 4. Synchronize state

If refs, ownership, targets, validation gates or architecture changed, update the project authority in the same working iteration.

## 5. Validate by level

Do not collapse these into one status:

`OBSERVATION → SOURCE/REVERSE_CONFIRMED → BUILD_PASS → HARDWARE_PASS → PRODUCT/UPSTREAM_READY`

Only claim the highest level actually demonstrated.

## 6. Review

For significant changes, hand the exact diff/state to an independent Reviewer. The Reviewer does not silently mutate the implementation while reviewing it.

## 7. Complete

Before `DONE`, compare the result with the original acceptance criteria and unresolved findings. A solved central mechanism is not automatically task completion.
