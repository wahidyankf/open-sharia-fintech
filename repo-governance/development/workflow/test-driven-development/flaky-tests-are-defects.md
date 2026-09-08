---
description: Requires every intermittent test failure to be fixed at its root cause, and forbids the masking remedies.
when_to_use: Use the moment a test passes and fails on the same code, before deciding what to do about it.
---

# Flaky tests are defects

A test that passes and fails on the same code is a **defect in the test or in the code under
test**. It is never noise to tolerate, and never a reason to re-run the job.

## Required response

Always fix an intermittent failure at its root cause:

1. Reproduce it, repeating or stressing the suspect test until the failure is observable on demand.
2. Identify what makes it nondeterministic — ordering, timing, shared state, real clocks,
   randomness, uncleaned fixtures, or a network or filesystem dependence.
3. Remove that source, then confirm the test is stable under the same repetition that reproduced
   it.

## Forbidden remedies

None of the following resolves an intermittent failure; each hides it:

- retrying the test, the job, or the workflow until it passes;
- adding a sleep, or widening a timeout, to outlast the race;
- loosening, removing, or narrowing an assertion so the unstable value stops mattering;
- reordering, isolating, or serialising tests so the interaction stops surfacing;
- skipping, quarantining, marking as expected-failure, or deleting the test; and
- filing it as accepted infrastructure flake without evidence identifying the infrastructure cause.

Adding retry, sleep, or timeout tolerance is legitimate only when it models a real external
behaviour the subject genuinely has, and the reason is recorded at the change.

## When the flake is production behaviour

Where the nondeterminism lives in the code under test rather than the test, it is a **production
defect** and is fixed in production code. A flake that hides a genuine race does not become
acceptable because it surfaced in a test first; it is the earliest evidence available of a bug
users will eventually hit.

## Enforcement

**Unenforced by decision.** No validator can distinguish a timeout raised to model real latency
from one raised to outlast a race, and intent is not mechanically observable. The nearest
mechanical support is the pre-push and CI gate set, which fails on a red test rather than
tolerating one; the judgement about how it is made green stays with the author and reviewer.
Complementary review coverage lives in the
[CI blocker resolution convention](../../quality/ci-blocker-resolution.md) and the
[pr-review integrity discipline](../../quality/pr-review-disciplines.md).

## Related Documentation

- [The Red-Green-Refactor Cycle](./the-red-green-refactor-cycle.md) — the loop a flake fix runs inside.
- [Picking the right level](./picking-the-right-level.md) — flakiness never reduces the required adapters.
- [CI Blocker Resolution](../../quality/ci-blocker-resolution.md) — investigating a red check at its root cause.
