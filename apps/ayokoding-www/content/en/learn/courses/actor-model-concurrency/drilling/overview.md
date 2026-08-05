---
title: "Overview"
date: 2026-08-04T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

1. What preserves an actor's state without sharing it with another process?
   <details><summary>Answer</summary>Its own receive loop owns the state and changes it by handling
   messages serially.</details>
2. When should a process be monitored instead of linked?
   <details><summary>Answer</summary>Monitor when the observer needs a `:DOWN` message but should not
   crash with the observed process.</details>

## Applied problems

1. A worker never replies to its caller. Carry the caller PID in the request and send an explicit
   reply after the work completes.
2. A coordinator must survive a worker failure. Monitor the worker, handle `:DOWN`, and make the
   restart or recovery decision in the coordinator.
3. Concurrent requests overwrite shared state. Move state behind one process and exchange messages
   rather than sharing mutable data.

## Code katas

- [Kata 1: Mailbox reply](./kata-01-mailbox/_index.md)
- [Kata 2: Monitor a worker](./kata-02-monitor/_index.md)
- [Kata 3: Isolated state](./kata-03-state/_index.md)
- [Kata 4: Minimal GenServer](./kata-04-genserver/_index.md)
- [Kata 5: Supervision](./kata-05-supervision/_index.md)

For each kata, run the `before/main.exs` program, describe the violated actor-model property, then
compare it with `after/main.exs`.

## Self-check checklist

- [ ] I can distinguish a process mailbox from shared mutable state.
- [ ] I can choose between links and monitors for a stated failure boundary.
- [ ] I can explain why a GenServer serializes state transitions.
- [ ] I can identify the supervision decision that belongs above a crashing worker.

## Elaborative interrogation and self-explanation

1. Why does exchanging messages make failure handling more explicit than sharing an object?
2. Why can a monitor be safer than a link for a coordinator and a worker?
3. Why is supervision a design boundary rather than a generic retry loop?
