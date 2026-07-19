---
title: "Artifact: Catching Silent Scope Creep in a Diff"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 70
---

> An out-of-scope hunk flagged and trimmed before merge -- exercises co-15.

**Diff under review** (asked for: add retry-with-backoff to `carrier_adapter/retry.py` only):

```diff
--- a/carrier_adapter/retry.py
+++ b/carrier_adapter/retry.py
@@ -10,6 +10,7 @@ class CarrierAdapter:
+    RETRY_DELAYS_MS = [200, 400, 800]
     def get_status(self, tracking_id: str) -> dict:
         ...

--- a/notification_worker/config.py
+++ b/notification_worker/config.py
@@ -3,4 +3,4 @@
-LOG_LEVEL = "INFO"
+LOG_LEVEL = "DEBUG"
```

**Reviewer note**: "The `carrier_adapter/retry.py` hunk matches the ask and is approved. The second
hunk, changing `notification_worker/config.py`'s `LOG_LEVEL` to `DEBUG`, is unrelated to the retry
task and was never requested -- trimming it before merge. If debug logging is genuinely needed
there, that's a separate, explicitly-scoped change."

**Result**: only the `carrier_adapter/retry.py` hunk merges; the `notification_worker/config.py`
hunk is dropped from the diff.
