---
title: "Capstone: Local Tool and MCP Boundary"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

Build a local, deterministic capability service with a typed tool registry, schema validation,
discovery, and structured results. A small client discovers only the tools authorized for a task,
performs a call, and returns a result shape designed for the next agent-loop decision.

## Acceptance criteria

- The server advertises a named tool with a strict argument schema and a compact result schema.
- The client discovers and invokes only an allowed tool; it never hard-codes an unvalidated call.
- Invalid arguments and unavailable tools return typed, model-readable errors.
- A resource or prompt is discoverable without becoming an executable action.
- The whole trace runs locally with a fake model and no live provider, browser, or `remotebrowser`
  dependency.

The later implementation will compose examples already taught in the learning track; it will not add a
new capability outside the course's tool and MCP boundary.
