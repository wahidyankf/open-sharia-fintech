---
title: "Artifact: Test-Pyramid Shape Flagged in Review"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 59
---

> ex-19 &middot; exercises co-11 &middot; a review comment naming the pyramid shape a PR violates.

**PR under review**: "feat(checkout): add gift-card redemption" -- diffstat: `+10 new files under
e2e/`, `+0 files under unit/`.

**Review comment**:

```text
This PR adds 10 new end-to-end tests and 0 unit tests for gift-card redemption's own validation
logic (card-format check, balance check, expiry check). That inverts the test pyramid: e2e tests
here take ~45s each (full browser + checkout flow) versus <10ms for a unit test of the same
validation function in isolation.

Ask: move the card-format/balance/expiry logic itself into 3-4 fast unit tests, and keep ONE e2e
test that exercises the full redemption flow end to end (proving the pieces integrate). That is
"many fast, few slow" -- the shape this PR currently has backwards.
```

**Verify**: the comment names the specific violated shape ("many fast, few slow," inverted here to
few-fast/many-slow) and ties it to a concrete cost (~45s per e2e test vs. <10ms per unit test), not
a vague "add more unit tests" ask.

**Key takeaway**: the test pyramid is not an abstract diagram -- it is a reviewable property of a
diffstat, checkable by counting new files per test tier and comparing their typical run cost.

**Why It Matters**: a PR that only ever adds e2e tests eventually makes the whole suite too slow to
run on every commit, pushing teams toward running tests less often -- exactly the opposite of what
fast feedback is for. Flagging the shape at review time, before the suite grows past the point where
untangling it is a project of its own, is far cheaper than a later "rebalance the test suite" effort.
