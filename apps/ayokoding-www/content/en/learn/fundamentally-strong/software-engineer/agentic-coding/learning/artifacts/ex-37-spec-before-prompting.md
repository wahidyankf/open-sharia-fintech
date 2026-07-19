---
title: "Artifact: Writing the Spec Before Writing the Prompt"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 77
---

> An acceptance-criteria spec, mapped bullet by bullet to the resulting diff -- exercises co-21.

**Spec document** (`specs/carrier-adapter-retry.md`):

```markdown
## Carrier Adapter Retry -- Acceptance Criteria

- AC1: `CarrierAdapter.get_status()` retries a failed call up to 3 times on HTTP 503.
- AC2: retry delays follow exponential backoff: 200ms, then 400ms, then 800ms.
- AC3: a non-503 response (success or a different error) returns immediately, no retry.
- AC4: if all 3 retries are exhausted, the last response is returned as-is (no exception
  raised by the retry wrapper itself).
```

**Review table mapping each spec bullet to the diff**:

| Spec bullet                         | Diff line(s)                                                  |
| ----------------------------------- | ------------------------------------------------------------- |
| AC1: retries up to 3 times on 503   | `for attempt, delay in enumerate([0, *self.RETRY_DELAYS_MS])` |
| AC2: 200/400/800ms backoff          | `RETRY_DELAYS_MS = [200, 400, 800]`                           |
| AC3: non-503 returns immediately    | `if response.status_code != 503: return response`             |
| AC4: exhausted retries return as-is | `return response` (the final line, outside the loop)          |
