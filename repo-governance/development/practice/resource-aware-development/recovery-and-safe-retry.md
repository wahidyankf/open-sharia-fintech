---
title: "Recovery and Safe Retry"
description: What HIPPO exits 73, 75, and 78 require before a retry, and the corrections that are never allowed.
category: explanation
subcategory: development
tags:
  - resource-management
  - parallelism
  - development
  - tooling
created: 2026-09-05
when_to_use: Use when a guarded command exits non-zero and you are deciding whether and how to retry it.
---

# Recovery and Safe Retry

- Exit `73`: free storage safely, then retry.
- Exit `75`: let the capacity/FIFO/lease/rollout deferral exit before retrying the same invocation;
  never duplicate or loop retries.
- Exit `78`: correct configuration, reservation, mapping, or strict-profile planning before retry.

Never bypass HIPPO, weaken a gate, delete possibly live state, or raise mapped concurrency.
Unreadable or corrupt shared state fails closed and `status` reports that error instead of a
partial document; confirm all compatibility owners exited before correcting private state.
