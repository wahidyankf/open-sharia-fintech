---
title: "Artifact: Refusing an Unverifiable Change Until a Test Exists"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 83
---

> A proposed change to a module with zero test coverage, refused until a test exists to verify it
> -- exercises co-22, co-13.

```text
[Agent]: Proposes a diff to legacy/pricing_calendar.py, changing how holiday
surcharges are computed for the December calendar.

[Reviewer check]: grep -rl "pricing_calendar" tests/
  -> (no output -- zero existing tests cover this module)

[Refusal, as written down]: "Refusing this diff. legacy/pricing_calendar.py has
no test coverage at all, and December holiday-surcharge logic is exactly the
kind of case-heavy code that LOOKS right on read-through but is easy to get
subtly wrong. There is no accompanying verification path -- I can confirm this
diff is plausible, not that it is correct. No merge until a test exists."

[Agent, second pass]: writes a characterization test first, pinning today's
actual (pre-diff) December-surcharge output for five known dates.

[Test run against pre-diff code]: pytest tests/test_pricing_calendar.py -q
  -> 5 passed  (the characterization test matches CURRENT behavior)

[Diff re-applied, characterization values updated to the intended new
surcharges, delta reviewed line by line, test rerun]:
  pytest tests/test_pricing_calendar.py -q -> 5 passed

[MERGED] -- only after tests/test_pricing_calendar.py existed and passed
against the diff.
```

The refusal did not block the change forever -- it blocked it until a verification path existed.
Writing the characterization test first (pinning the current, pre-diff behavior) gave the reviewer
something concrete to diff the intended change against, rather than relying on a read-through
alone for case-heavy calendar logic.

**Verify**: the transcript shows an explicit refusal citing the absence of any test, followed only
later by a merge that happens strictly after `tests/test_pricing_calendar.py` exists and passes --
satisfying ex-43's rule that no diff merges without an accompanying verification path.
