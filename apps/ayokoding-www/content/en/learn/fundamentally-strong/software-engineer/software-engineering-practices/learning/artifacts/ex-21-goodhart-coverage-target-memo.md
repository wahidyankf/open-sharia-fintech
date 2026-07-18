---
title: "Artifact: Memo -- Why 100% Coverage as a Merge Gate Backfires"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 61
---

> ex-21 &middot; exercises co-12 &middot; a short memo against mandating 100% coverage as a required
> check.

```text
To: Engineering leads
Re: proposal to require 100% line coverage on every merge

Recommendation: do not adopt this as a required check.

Coverage is a PROXY for testedness, not proof of correctness -- it measures whether a line executed
during a test run, not whether the test checked the line did the right thing. Example 20 shows this
concretely: a function with a real bug reaches 100% line coverage under a test that calls it but
asserts nothing about the result.

The moment a metric becomes a merge-blocking TARGET, Goodhart's law predicts (and we should expect
in practice) that people optimize the metric instead of the underlying goal. Concretely, a 100%
mandate produces:

  - Assertion-free tests written purely to touch a line ("coverage padding"), exactly the failure
    mode Example 20 demonstrates.
  - Deleted or skipped edge-case handling, because an unreachable defensive branch is easier to
    remove than to cover.
  - Time spent covering trivial getters/setters instead of the actually-risky logic nearby.

Alternative: treat coverage as a SIGNAL, reviewed as a trend (is it dropping on this PR?) and spot-
checked for suspicious patterns (a new file at exactly 100% with no meaningful assertions), rather
than a single number gating every merge.
```

**Verify**: the memo explicitly names the assertion-free-test failure mode (and cross-references the
concrete example that demonstrates it) as its central argument against the mandate, not a vague
"coverage isn't everything" objection.

**Key takeaway**: any metric that becomes a hard merge gate invites the cheapest way to satisfy the
gate, and for line coverage the cheapest way is a test that runs the code without checking it.

**Why It Matters**: this is Goodhart's law applied to a concrete engineering practice -- the same
caution that applies to velocity-as-a-target (a project-management pitfall) applies here: measuring
something useful, then rewarding the number itself instead of the thing it was proxying for, reliably
degrades exactly the property you were trying to protect.
