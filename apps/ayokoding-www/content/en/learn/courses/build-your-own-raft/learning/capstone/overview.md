---
title: "Capstone: Raft KV"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Run `go test ./...` in `code/`. The capstone models election, majority replication, partitions, restart state, and a replicated key-value map using an in-memory harness. It intentionally does not implement network transport, snapshots, or membership change.
