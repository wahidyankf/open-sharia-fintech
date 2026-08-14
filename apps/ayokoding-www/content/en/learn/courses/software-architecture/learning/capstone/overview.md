---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: true
weight: 1
---

## Goal

Re-architect a small tangled order service into ports and adapters around a functional core. Keep a
characterization test before moving behavior, then demonstrate that an in-memory store and a durable
store satisfy the same port without changing core policy.

## Deliverables

1. A characterization test for the original order behavior.
2. A domain core with no framework, database, or transport import.
3. Two adapters that satisfy one port and contract checks for their observable behavior.
4. Context, container, and component diagrams that match the implementation.
5. An ADR recording the key trade-off and a fitness function that rejects forbidden imports.

## Acceptance criteria

- The core has no infrastructure import.
- Both adapters pass the same behavior checks.
- The diagrams name the same boundaries that code enforces.
- The ADR states context, decision, and consequences.

## Reflection

Describe one boundary that reduced the change blast radius and one cost the new boundary introduced.
If the answer names no cost, revisit the trade-off before calling the design complete.
