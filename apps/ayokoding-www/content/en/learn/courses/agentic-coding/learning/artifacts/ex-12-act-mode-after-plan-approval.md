---
title: "Artifact: Act-Mode After Plan Approval"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 52
---

> Continuing the ex-11 plan-mode pass: an explicit approval line, then edits appear only after it
> -- exercises co-09.

```text
[Human]: Plan approved -- proceed.

[ACT MODE ENABLED]
5. edit_file(path="src/api/middleware/rate_limit.py", diff="+class RateLimitMiddleware: ...")
6. edit_file(path="src/api/router.py", diff="+  app.add_middleware(RateLimitMiddleware)")
7. edit_file(path="src/api/settings.py", diff="+  RATE_LIMIT_RPM = 60")
8. edit_file(path="tests/test_rate_limit.py", diff="+def test_under_limit(): ...")
9. run_shell(command="pytest tests/test_rate_limit.py -q")
```

**Verify**: ex-11's steps 1-4 (the plan-mode pass) contain zero edits; the explicit
`[Human]: Plan approved -- proceed.` line sits immediately before `[ACT MODE ENABLED]`; every
`edit_file` call (steps 5-8) occurs strictly after that approval line -- satisfying ex-12's rule
that edits appear in the log only after the explicit approval step.
