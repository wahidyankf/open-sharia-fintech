---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Follow the examples in order: channels first make ownership transfer visible; `select` and context
make waiting and cancellation explicit; pipelines and worker pools then compose those boundaries.
Use `go test -race` whenever a claim depends on concurrent memory access.

## Concept route

- Beginner: goroutines, directional/buffered/nil channels, select, and `sync` basics.
- Intermediate: cancellation, pipeline stages, fan-out/fan-in, bounded pools, and shutdown.
- Advanced: memory ordering, race/leak/deadlock diagnosis, remediation, and the CSP/actor contrast.

## Scope guard

These examples teach Go CSP design. They do not turn every operation into a goroutine: simple local
state stays local, and actor-style identity/mailbox semantics belong to the companion actor course.
