---
title: "Parallel-by-Default Practice"
description: When doing work with independent sub-units (tool calls, file reads/edits, searches, or delegated agents), default to running them in parallel rather than serially, capped at three concurrent units of work
category: explanation
subcategory: development
tags:
  - parallelism
  - concurrency
  - performance
  - ai-agents
  - efficiency
created: 2026-06-23
when_to_use: Use whenever you have two or more independent units of work — tool calls, file reads, searches, or delegated agents — ready to launch.
---

# Parallel-by-Default Practice

When independent units of work are ready, run them in parallel. Serial execution of independent work wastes throughput and adds latency with no benefit. The deliberate cap of **three** simultaneous units preserves meaningful speedup while staying below the token-burn and Claude API per-minute rate-limit threshold.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: The declared N is a deliberate, pre-decided constraint — not a reactive limit set after hitting errors, and not a number an agent infers mid-batch from how fast things feel. Acting from a bounded model prevents speculative over-parallelism and the cascading failures it causes.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: One number — N, defaulting to three — governs all parallel work. No adaptive scheduling, no per-task caps, no context-dependent arithmetic. N is declared up front and may be adjusted per-plan or along the way when independent work, machine capacity, and budget headroom allow; what stays simple is that a single declared number governs, and an agent never self-promotes beyond it.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: Running independent tool calls in a single turn, or independent subagents in background, automates what would otherwise require manually sequenced round-trips. Parallel-by-default is the automated form of efficient execution.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: The cap and its rationale are stated explicitly in this document. Agents apply the value here — they do not infer limits from context or self-promote based on observed headroom.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Content Quality Principles](../../conventions/writing/quality.md)**: This document follows active voice, proper heading hierarchy, and accessible examples throughout.

- **[File Naming Convention](../../conventions/structure/file-naming.md)**: This document uses a lowercase kebab-case filename consistent with repository naming rules.

## Contents

- [Purpose and Scope](./parallel-by-default/purpose-and-scope.md) — the two failure modes this practice eliminates, and exactly what it covers.
- [Standards 1-2 — Parallel Unless Dependent, and the N+1 Model](./parallel-by-default/standards-1-to-2.md) — the default execution model and the adjustable concurrency cap.
- [Standards 3-4 — Background-Slot Preference and DAG-First Ordering](./parallel-by-default/standards-3-to-4.md) — keeping the main thread vacant, and declaring the dependency DAG.
- [Anti-Patterns and References](./parallel-by-default/anti-patterns-and-references.md) — four common failure patterns, related principles, practices, and agents.
