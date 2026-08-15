---
title: "Intermediate Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

Examples 27–52 make cross-thread ownership explicit. Channels transfer messages; `Arc` is shared
ownership and `Mutex` controls the one-writer portion. The examples never claim that `Rc` is
thread-safe: its rejection is an important compiler guarantee. The last section puts generic traits,
dynamic dispatch, iterator pipelines, and explicit error conversions beside the concurrency work.
