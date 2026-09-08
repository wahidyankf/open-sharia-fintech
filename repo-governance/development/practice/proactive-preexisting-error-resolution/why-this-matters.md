---
description: The backlog problem, the monkey-patch problem, and the normalization problem that motivate fixing preexisting errors immediately rather than deferring them
when_to_use: Use when you need to justify why a preexisting error should be fixed now rather than noted for later.
---

# Why This Matters

## The Backlog Problem

Mentioning without fixing creates an ever-growing list of known-but-unresolved problems. Each item requires human triage to schedule, re-investigation to understand, and context-switching to execute. A codebase that accumulates acknowledged defects degrades trust and slows all contributors.

Every encounter with a preexisting error is a zero-cost opportunity: the relevant code is already open, the context is already loaded, the root cause is either understood or discoverable with minimal effort. That opportunity expires the moment the context window closes.

## The Monkey-Patch Problem

Working around a preexisting problem adds a second layer of code on top of a broken first layer. Both layers now exist in the codebase. The original problem is still there. Future contributors encounter both the workaround and the underlying defect without understanding the relationship between them.

Monkey-patches compound. A patch on a patch on a patch is a codebase that nobody can reason about safely.

## The Normalization Problem

Ignoring preexisting errors normalizes broken state. When broken tests, dead links, or failing configurations persist without resolution, they signal that degraded state is acceptable. That signal travels to every contributor who reads the code. Quality bars drift downward.
