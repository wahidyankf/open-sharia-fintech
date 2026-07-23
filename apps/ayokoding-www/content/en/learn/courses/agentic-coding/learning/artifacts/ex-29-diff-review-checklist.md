---
title: "Artifact: A Scope/Tests/Style Diff-Review Checklist"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 69
---

> A structured checklist applied to one agent diff before merge -- exercises co-15.

**Diff under review** (adds retry-with-backoff to `carrier_adapter/retry.py`):

```diff
--- a/carrier_adapter/retry.py
+++ b/carrier_adapter/retry.py
@@ -10,6 +10,7 @@ class CarrierAdapter:
+    RETRY_DELAYS_MS = [200, 400, 800]
+
     def get_status(self, tracking_id: str) -> dict:
-        return self._client.get(f"/tracking/{tracking_id}")
+        for attempt, delay in enumerate([0, *self.RETRY_DELAYS_MS]):
+            if delay:
+                time.sleep(delay / 1000)
+            response = self._client.get(f"/tracking/{tracking_id}")
+            if response.status_code != 503:
+                return response
+        return response
```

**Checklist applied before merge**:

- [x] **Scope**: touches only `carrier_adapter/retry.py` -- no unrelated files in the diff.
- [x] **Tests**: `test_retry_on_503` (new) passes; the full existing adapter suite still passes
      unchanged.
- [x] **Style**: matches the module's existing naming (`SCREAMING_SNAKE_CASE` for the class
      constant) and docstring conventions.

**Merge decision**: approved -- all three checklist items explicitly checked.
