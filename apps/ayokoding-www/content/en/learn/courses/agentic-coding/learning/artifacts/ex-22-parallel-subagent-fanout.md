---
title: "Artifact: Parallel Subagent Fan-Out on Two Unrelated Subtasks"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 62
---

> Two independent subagents, both summaries merging without cross-contaminating context --
> exercises co-10.

```text
[main session] -> dispatch subagent A(
  task: "audit test coverage of carrier_adapter/retry.py's backoff logic"
)
[main session] -> dispatch subagent B(
  task: "check whether the Notification Worker's idempotency-cache TTL is documented anywhere"
)

[subagent A, isolated context -- reads retry.py and its test file, WITHHELD from main session]
[subagent B, isolated context -- greps the docs tree and the ADR folder, WITHHELD from main session]

[subagent A -> main session, summary]:
"test_retry.py covers the 503-then-200 retry path and the exhausted-retries case; it does
NOT cover a network-timeout-mid-retry case."

[subagent B -> main session, summary]:
"The idempotency-cache TTL (48 hours) is documented in ADR-0006's Consequences section; no
other document restates it."
```
