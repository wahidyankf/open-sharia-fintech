---
title: "Capstone: Service Readiness"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Build and run this light consolidation program from `learning/capstone/code/`:

```sh
cargo run
cargo test
```

`Service` is a struct, `Readiness` and `ServiceError` are enums, and `match` handles every
readiness state. `Named` is implemented for `Service`; `report<T: Named>` is constrained by that
trait. The capstone turns an optional port into a `Result` with `ok_or(...)` and propagates the
possible failure through `?`. The two tests prove its ready and missing-port outcomes.

This is intentionally a short language consolidation, not an application: it prepares the Rust
surface needed by [Modern System Programming](../../../../modern-system-programming/overview.md).
