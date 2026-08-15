---
title: "Build and Operate"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

1. Implement a bounded Go worker pool with `context` cancellation and graceful shutdown.
2. Add a justified systems component, such as a bounded binary queue with explicit allocation limits.
3. Containerize the service and run the same workload locally.
4. Expose latency, traffic, errors, and saturation; define an availability SLI, SLO, and error budget.
5. Inject a local latency or error condition; verify a symptom-based alert and dashboard reflect it.

```go
if err := ctx.Err(); err != nil { return err } // graceful shutdown is a contract
```

Record the load profile and SLO math with the dashboard artifact; a graph without an actionable
threshold is not observability.
