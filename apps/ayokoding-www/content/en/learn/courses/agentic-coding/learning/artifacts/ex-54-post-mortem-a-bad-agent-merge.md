---
title: "Artifact: Post-Mortem — an Unverified Agent Diff Broke the Build"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 94
---

> A constructed incident where an unverified agent diff reached the build and broke it, plus the
> process fix that closes the specific verification-loop gap that let it through -- exercises
> co-13, co-16, co-22.

```text
[Incident timeline]
14:02  Agent generates a diff refactoring parse_csv_row() to use
       csv.Row.from_line() -- a plausible-sounding but NONEXISTENT stdlib
       method (co-16: a hallucinated API).
14:03  Reviewer skims the diff (treats it as boilerplate-level, low-review --
       a co-17 miscalibration): "looks like an obvious stdlib API," approves
       without running it.
14:04  CI reports green -- but the CI run reused a 40-minute-old cached test
       result; the cache key did not include this file's content hash, so
       the new, broken code was never actually executed by CI.
14:06  Merged.
09:15 (next day)  Production ingest job crashes:
       AttributeError: module 'csv' has no attribute 'Row'.
```

**Root cause**: two independent verification-loop gaps compounded. First, a hallucinated API
(co-16) went unnoticed because the review was a skim, not a run -- co-13's "run it before you
trust it" discipline was skipped. Second, CI's stale cache masked the fact that the new code was
never actually executed pre-merge, so even a diligent "check CI is green" step gave false
confidence -- the green checkmark reflected a 40-minute-old run of the OLD code, not the new diff.

**Process fix, as written down**: "No merge without a fresh, from-scratch test run whose cache key
includes every changed file's content hash -- 'CI is green' must mean 'CI actually executed the
new code,' not 'a cached prior result happened to be green.' Additionally, any diff calling a
standard-library method must be run once locally before being accepted, closing the specific gap
that let this hallucinated API through: a skim-level review is not sufficient for code that has
never actually executed."

**Verify**: the fix names two specific, distinct gaps -- the stale test cache masking unexecuted
new code, and a skim-level review substituting for actually running the diff -- rather than a
generic "run more tests," and each gap maps to a concrete process change (cache keys include
content hashes; sensitive/novel-API diffs get run locally before acceptance) -- satisfying ex-54's
rule that the fix closes the specific verification-loop gap that let the diff through.
