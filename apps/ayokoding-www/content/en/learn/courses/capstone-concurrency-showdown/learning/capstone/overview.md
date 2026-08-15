---
title: "Same Workload, Two Models"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

1. Implement bounded fan-out/fan-in in Go with channels, `select`, cancellation, and a failing worker.
2. Run `go test -race`; verify cancellation stops producers and no result is silently dropped.
3. Implement the identical contract using an Elixir GenServer and supervision tree.
4. Crash a worker deliberately; verify supervision restores service without losing the coordinator.
5. Write `comparison.md` from observed behavior: coordination, backpressure, failure, testability, and
   observability, with a concrete selection rule.

```go
select { case out <- job: case <-ctx.Done(): return }
```

Do not claim one model is universally superior; bind every recommendation to workload and failure shape.
