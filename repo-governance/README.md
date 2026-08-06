---
title: "Repository Governance"
description: How open-sharia-enterprise turns its mission and values into consistent ways of working
category: explanation
subcategory: governance
tags:
  - index
  - governance
  - principles
  - conventions
  - development
  - workflows
created: 2026-01-04
---

# Repository Governance

Governance helps open-sharia-enterprise make consistent, purposeful decisions as the repository grows. It connects the project's mission to the principles, standards, development practices, automated agents, and workflows that put that mission into practice.

This directory is a map, not a replacement for the documents it links to. Start with the layer closest to the question you have, then follow its links for the full rule or procedure.

## Start Here

- To understand the whole model and how the layers relate, read the [Repository Governance Architecture](./repository-governance-architecture.md).
- To learn why the project exists, begin with the [Vision](./vision/README.md).
- To find a rule for writing or organizing documentation, use [Conventions](./conventions/README.md).
- To find a software practice, quality gate, or engineering workflow, use [Development](./development/README.md).
- To run a defined multi-step process, use [Workflows](./workflows/README.md).

## Navigate the Layers

The governance model has six layers. Each answers a different question and gives the layers below it a clear foundation.

| Layer          | Question it answers                               | Where to go                                  |
| -------------- | ------------------------------------------------- | -------------------------------------------- |
| 0. Vision      | Why does the project exist?                       | [Vision](./vision/README.md)                 |
| 1. Principles  | Why do we value this approach?                    | [Principles](./principles/README.md)         |
| 2. Conventions | What rules shape our documentation?               | [Conventions](./conventions/README.md)       |
| 3. Development | How do we build and maintain software?            | [Development](./development/README.md)       |
| 4. AI Agents   | Who carries out defined checks and tasks?         | [Agent catalog](../.claude/agents/README.md) |
| 5. Workflows   | When do we use a coordinated, multi-step process? | [Workflows](./workflows/README.md)           |

The layers flow from enduring intent to day-to-day execution:

```text
Vision → Principles → Conventions and Development → AI Agents → Workflows
```

The [Repository Governance Architecture](./repository-governance-architecture.md) explains the relationships, traceability, and change impact in detail.

## Choose the Right Home

Use the question below to decide where a new governance document belongs.

| If the document answers…                          | Put it in…                                |
| ------------------------------------------------- | ----------------------------------------- |
| Why does the project exist?                       | [`vision/`](./vision/README.md)           |
| Why do we value an approach?                      | [`principles/`](./principles/README.md)   |
| What documentation rule should we follow?         | [`conventions/`](./conventions/README.md) |
| How should we develop, test, or operate software? | [`development/`](./development/README.md) |
| When should a multi-step process run?             | [`workflows/`](./workflows/README.md)     |

Keep governance prose vendor-neutral. Details that apply only to a particular tool or platform belong in its platform-binding documentation, as described by the [Governance Vendor-Independence Convention](./conventions/structure/governance-vendor-independence.md).

## Follow the Trace

When a rule feels arbitrary, trace it upward. A development practice should be grounded in relevant principles; a convention should support the project's purpose. When a higher layer changes, review the lower layers that depend on it.

For example, the [Accessibility First principle](./principles/content/accessibility-first.md) informs documentation conventions, development practices, agent checks, and workflows that verify accessible outcomes. This traceability keeps local decisions aligned with the project's broader purpose.

## Read by Situation

- **New to the repository:** read the [Vision](./vision/README.md), then the [Principles](./principles/README.md), followed by the [Repository Governance Architecture](./repository-governance-architecture.md).
- **Writing documentation:** start with [Conventions](./conventions/README.md), especially its formatting, linking, and writing guidance.
- **Changing code or delivery practices:** start with [Development](./development/README.md), then use the relevant [Workflows](./workflows/README.md).
- **Working with automated agents:** use the [Agent catalog](../.claude/agents/README.md) to understand available roles and the governance documents they enforce.

This structure keeps the repository's decisions discoverable: begin with the question at hand, use the matching layer, and follow links only as far as the work requires.
