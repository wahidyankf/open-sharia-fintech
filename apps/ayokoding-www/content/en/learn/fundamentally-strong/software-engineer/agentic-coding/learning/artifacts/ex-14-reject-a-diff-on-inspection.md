---
title: "Artifact: Diff Rejection on Inspection"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 54
---

> A unified diff with one unrelated hunk, plus a written rejection reason naming that hunk
> specifically -- exercises co-15.

```diff
diff --git a/src/orders/discount.py b/src/orders/discount.py
--- a/src/orders/discount.py
+++ b/src/orders/discount.py
@@
-    return min(amount * 0.1, cap)
+    return min(amount * 0.10, 500)

diff --git a/.eslintrc.json b/.eslintrc.json
--- a/.eslintrc.json
+++ b/.eslintrc.json
@@
-  "no-console": "warn"
+  "no-console": "off"
```

**Rejection reason, as written down**: "Reject the `.eslintrc.json` hunk -- it silently disables
the repo-wide `no-console` lint rule and has nothing to do with the discount-cap fix this diff was
asked for. Splitting it into its own, separately-justified change (or dropping it entirely) before
accepting the `discount.py` hunk."

**Verify**: the written rejection reason names the exact unrelated hunk (`.eslintrc.json`'s
`no-console` change) by file and states specifically what it does (silently disables a lint rule)
-- satisfying ex-14's rule that the rejection is written down with a reason tied to the unrelated
hunk.
