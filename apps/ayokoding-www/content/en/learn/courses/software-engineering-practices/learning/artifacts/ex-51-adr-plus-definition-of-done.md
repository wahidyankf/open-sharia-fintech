---
title: "Artifact: A Linked ADR as a Definition-of-Done Item"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 91
---

> ex-51 &middot; exercises co-18, co-21 &middot; an architecturally significant PR that fails its
> own checklist without a linked ADR.

**Definition of Done, v3** (extends Example 38's checklist):

```text
[ ] Tests pass locally AND in CI
[ ] Code reviewed and approved
[ ] Docs updated in the same PR, if behavior changed
[ ] Changelog entry added, if user-facing
[ ] IF this PR is architecturally significant (per Example 32's two-question test): a linked ADR
    is present, referencing the actual change
```

**Applied to PR #150 (refactor(payments): switch to async settlement)** -- architecturally
significant (changes the settlement consistency model, hard to reverse once live traffic depends on
it):

```text
[x] Tests pass locally AND in CI
[x] Code reviewed and approved
[x] Docs updated in the same PR
[ ] Changelog entry added           -- N/A, internal refactor, not user-facing
[ ] Linked ADR present               -- MISSING -- checklist FAILS here
```

**Verify**: PR #150 is correctly marked NOT done -- four of five applicable items are checked, but
the missing ADR item (the one this PR's own architectural-significance test triggers) fails the
whole checklist, satisfying co-21's gating rule applied to co-18's ADR criterion.

**Key takeaway**: making "a linked ADR" a conditional Definition-of-Done item (conditional on
Example 32's own significance test) turns "we should write an ADR for big decisions" from a norm
into an enforced gate.

**Why It Matters**: without this DoD line, an architecturally significant change can merge, ship,
and be forgotten-about-the-why within a quarter -- exactly the gap co-18's whole practice exists to
close, now backed by a checklist that actually blocks "done" until the record exists.
