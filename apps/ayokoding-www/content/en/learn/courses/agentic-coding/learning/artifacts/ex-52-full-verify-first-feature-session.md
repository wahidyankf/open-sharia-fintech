---
title: "Artifact: A Full Verify-First Feature Session, Prompt to Merge"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 92
---

> One complete feature session -- specified prompt, plan-mode pass, act-mode diffs, tests run at
> each step, final review -- exercises co-05, co-09, co-13, co-15.

```text
[PROMPT] Goal: add a /health endpoint returning {"status": "ok"}.
Constraints: no new dependencies, must respond in under 50ms, must have a test.
Example: GET /health -> 200 {"status": "ok"}.
Acceptance criteria: AC1 route registered; AC2 returns exactly {"status":
"ok"}; AC3 covered by a test; AC4 no new third-party dependency added.

[PLAN MODE -- read-only]
1. read_file(path="src/api/router.py")
2. read_file(path="requirements.txt")
Proposed plan: add a handler to router.py, register the route, add one test.

[Human]: Plan approved -- proceed.

[ACT MODE]
--- Diff 1 ---
edit_file(path="src/api/router.py",
          diff="+  @app.get('/health')\n+  def health(): return {'status': 'ok'}")
[TEST RUN 1] pytest tests/ -q -> "12 passed"
  (no test for /health exists yet -- confirms diff 1 broke nothing pre-existing)
[REVIEW 1] scope: router.py only, matches the ask. style: consistent with
  adjacent routes. Approved to build on.

--- Diff 2 ---
edit_file(path="tests/test_health.py",
          diff="+  def test_health(): assert client.get('/health').json() == {'status': 'ok'}")
[TEST RUN 2] pytest tests/ -q -> "13 passed"
  (the new test itself now passes)
[REVIEW 2] scope: test file only. asserts the exact AC2 payload. Approved to
  build on.

--- Diff 3 ---
edit_file(path="requirements.txt", diff="(no change -- confirms AC4: nothing added)")
[TEST RUN 3] pytest tests/ -q -> "13 passed"
  (re-confirms nothing regressed after the no-op check)
[FINAL REVIEW] AC1-AC4 checklist: [x] route registered  [x] exact payload
  [x] test added, passing  [x] requirements.txt diff is empty -- no new
  dependency.

[MERGED]
```

Diff 1 is followed immediately by Test Run 1 and Review 1, before Diff 2 begins; the same holds
for Diff 2 and Diff 3 -- there is no point in the transcript where a second diff starts before the
prior one's own test run and review are both complete.

**Verify**: every one of the three diffs has its own `[TEST RUN N]` and `[REVIEW N]` entry
appearing directly after it and before the next diff or `[MERGED]` -- satisfying ex-52's rule that
no diff reached the final state without being run and reviewed.
