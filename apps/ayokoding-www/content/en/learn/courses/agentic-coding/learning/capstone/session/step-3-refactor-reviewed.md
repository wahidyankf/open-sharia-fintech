---
title: "Capstone Session Step 3: Refactor, Reviewed"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 40
---

A small, behavior-preserving refactor, requested after the fix went green: extract the per-token
seconds calculation into its own named function, purely for readability -- no behavior change, so
this step (co-12: small reversible steps) can be reverted on its own without touching the actual
bugfix from step 2.

```diff
--- attempt2.py
+++ attempt3_final.py
@@ -1,4 +1,4 @@
-"""Capstone attempt 2 (fixed): parse_duration -- "1h30m"-style duration string to total seconds."""
+"""Capstone final: parse_duration -- convert an "1h30m"-style duration string to total seconds."""
 from __future__ import annotations

 import re
@@ -8,16 +8,23 @@


 def parse_duration(s: str) -> int:
-    """Parse a duration string like "1h30m" or "45s" into total whole seconds."""
+    """Parse a duration string like "1h30m" or "45s" into total whole seconds.
+
+    Raises ValueError if `s` is empty, has no valid tokens, or has any
+    unmatched/malformed trailing content.
+    """
     if not s:
         raise ValueError("duration string must not be empty")
     total = 0
     consumed = 0
     for match in _TOKEN.finditer(s):
-        value = int(match.group(1))
-        unit = match.group(2)
-        total += value * _UNIT_SECONDS[unit]
+        total += _seconds_for_token(match.group(1), match.group(2))
         consumed += len(match.group(0))
     if consumed != len(s):
         raise ValueError(f"invalid duration string: {s!r}")
     return total
+
+
+def _seconds_for_token(digits: str, unit: str) -> int:
+    """Convert one (digits, unit) token into whole seconds."""
+    return int(digits) * _UNIT_SECONDS[unit]
```

**Review before accepting**: touches only the function body's internal structure (extract-method) and
docstrings -- no change to `parse_duration`'s signature, its `ValueError` conditions, or the
`_UNIT_SECONDS` table the previous step fixed. Diff-review checklist (co-15, mirroring
`ex-29 · diff-review-checklist`): scope -- confined to the one file, no unrelated hunk; tests --
rerun below, not assumed; style -- adds a docstring, consistent with the rest of the file.

**Run**: `python3 -m pytest test_parse_duration.py -q`

**Output** (genuine, captured transcript):

```text
.......                                                                  [100%]
7 passed in 0.00s
```

**Verify**: still all seven tests green after the refactor -- confirming the extract-method change
was genuinely behavior-preserving, not just assumed to be. This is the final state committed to
`learning/capstone/code/parse_duration.py`.

---

← Previous: [Step 2: Fix, Green](./step-2-fix-and-green.md) &middot; Next: [Trust/Verify Log](../trust-verify-log.md) →
