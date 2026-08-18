---
title: "Principles, Conventions, and Core Rule"
description: The assumption that Vercel MCP is available, the principles and conventions behind it, and the two-gate rule that resolves it for a plan.
category: explanation
subcategory: development
tags:
  - vercel
  - mcp
  - planning
created: 2026-08-01
when_to_use: Use when you need the core assumed-availability rule and its two gates, or the principles/conventions this convention builds on.
---

# Principles, Conventions, and Core Rule

An MCP server for Vercel is **assumed available** to any plan whose surface includes a
Vercel-deployed project. Deployment state, runtime invocation counts, build logs, and deploy
provenance are therefore agent-readable, and steps that read them are tagged `[AI]` rather than
`[HUMAN]`.

The assumption is load-bearing, so it is **probed, never presumed** — once while planning, and again
at execution Phase 0 before any step depends on it.

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: a
  plan that tags a deployment-verification step `[AI]` is asserting a capability. The assertion is
  written down and checked, not assumed from the fact that a previous plan managed it.

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: the
  probe is cheap and runs before the work is shaped around its answer, rather than after an executor
  discovers mid-phase that a step it planned cannot be performed.

## Conventions Implemented/Respected

- **[Vercel Deployment Convention](../vercel-deployment.md)**: defines which projects deploy through
  Vercel and how their builds are configured. This convention governs what an agent may **observe**
  about those deployments; that one governs how they are **built**.
- **[Manual Behavioral Verification](../../quality/manual-behavioral-verification.md)**: the same
  shape — a capability an agent uses to verify real running behavior instead of asserting from
  source.
- **[Plans Organization Convention](../../../conventions/structure/plans.md)**: supplies the
  `[AI]` / `[HUMAN]` executor tags this convention shifts between.

## The Core Rule

**If a plan touches a Vercel-deployed surface, it MUST resolve Vercel MCP availability at both
gates, and record the answer.**

| Gate                                                   | Who         | What it decides                                                              |
| ------------------------------------------------------ | ----------- | ---------------------------------------------------------------------------- |
| **Planning** — before authoring the delivery checklist | plan author | whether deployment-verification steps are written `[AI]` or `[HUMAN]`        |
| **Execution** — Phase 0, before Phase 1 starts         | executor    | whether the checklist's `[AI]` assumption still holds, or must be downgraded |

A plan that touches no Vercel-deployed surface is **out of scope** — it neither probes nor records
anything. Do not add a vacuous check to plans that cannot use the answer.
