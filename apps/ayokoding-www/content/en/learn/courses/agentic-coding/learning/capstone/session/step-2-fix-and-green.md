---
title: "Capstone Session Step 2: Fix, Green"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 30
---

The fix, as a real diff against step 1 (one line):

```diff
--- attempt1.py
+++ attempt2.py
@@ -1,10 +1,10 @@
-"""Capstone attempt 1: parse_duration -- convert an "1h30m"-style duration string to total seconds."""
+"""Capstone attempt 2 (fixed): parse_duration -- "1h30m"-style duration string to total seconds."""
 from __future__ import annotations

 import re

 _TOKEN = re.compile(r"(\d+)([hms])")
-_UNIT_SECONDS: dict[str, int] = {"h": 3600, "m": 600, "s": 1}
+_UNIT_SECONDS: dict[str, int] = {"h": 3600, "m": 60, "s": 1}


 def parse_duration(s: str) -> int:
```

**Review before accepting**: a one-line diff, touching only the `"m"` value in `_UNIT_SECONDS` --
scoped exactly to the rejected bug from step 1, no unrelated hunks (co-15: this is the same
scope-check `ex-30 · catch-silent-scope-creep` teaches, applied here to the agent's own follow-up
diff). Accepted only after re-running the full suite, not on inspection alone.

**Run**: `python3 -m pytest test_parse_duration.py -q`

**Output** (genuine, captured transcript):

```text
.......                                                                  [100%]
7 passed in 0.00s
```

**Verify**: all seven acceptance-criteria tests from `prompt.md` now pass -- a real, captured green
run, following a real, captured red run (step 1) -- the red-to-green transition co-13/co-14 require
before any "done" claim.

---

← Previous: [Step 1: First Attempt, Rejected](./step-1-first-attempt-rejected.md) &middot; Next: [Step 3: Refactor, Reviewed](./step-3-refactor-reviewed.md) →
