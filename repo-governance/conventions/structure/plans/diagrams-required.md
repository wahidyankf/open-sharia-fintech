---
title: "Diagrams in Plans"
description: Requires Mermaid as the primary diagram format in plans/ and lists the architectural concerns that must each get their own diagram.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when deciding whether a plan section needs its own Mermaid diagram.
---

# Diagrams in Plans

Files in `plans/` folder MUST use **Mermaid diagrams** as the primary format (same as all markdown files in the repository).

**Diagram Standards**:

- **Primary Format**: Mermaid diagrams for all flowcharts, architecture diagrams, sequences
- **ASCII Art**: Optional for general diagrams (simple directory trees or rare edge cases), but **Required** as the low-fidelity wireframe tier for **UI-bearing plans** — see [UI Mockups in Plan Docs](../../formatting/diagrams/ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope) for the both-tiers rule, design funnel, and grounding rule
- **Orientation**: Default to left-to-right (`flowchart LR` / `graph LR`) per the [Diagram and Schema Convention](../../formatting/diagrams.md); use top-down only when semantically required
- **Colors**: Use color-blind friendly palette from [Color Accessibility Convention](../../formatting/color-accessibility.md)

**Why Mermaid**:

- Renders properly in GitHub and most markdown viewers
- Version-controllable (text-based)
- Easy to update and maintain
- Supports multiple diagram types (flowchart, sequence, class, ER, etc.)

## When a Plan MUST Include a Diagram

A plan MUST include extensive Mermaid diagrams where appropriate: every distinct architectural concern the plan touches that a reader would otherwise have to reconstruct mentally from prose SHOULD receive its own dedicated diagram. This means one diagram per concern, not one diagram total.

The concerns that warrant their own diagram when present in a plan:

- **Component interactions** — which services, agents, apps, or libraries call which, and through what contract (flowchart or C4-style diagram)
- **Sequence or flow between agents or systems** — order-of-operations across processes, including async hand-offs and timeouts (sequenceDiagram)
- **State transitions** — lifecycle of an entity (plan folder, request, deployment, entitlement) with named states and triggered transitions (stateDiagram-v2)
- **Decision branches** — non-trivial conditional logic with more than two outcomes or nested decisions (flowchart with labelled edges)
- **Dependency position** — upstream and downstream plan or system dependencies showing where this plan sits relative to sibling plans, services, or libraries it depends on or that depend on it (flowchart)
- **Phase/delivery flow** — the phased delivery progression with gates, showing how phases sequence and what conditions govern transitions (flowchart or stateDiagram-v2)

**Prefer multiple focused diagrams over one overloaded diagram.** A plan covering N distinct architectural concerns should generally carry N diagrams — one per concern — rather than forcing all concerns into a single crowded chart.

If unsure whether a diagram is warranted for a given concern, add it. A redundant diagram costs less than a missed architectural ambiguity.

See [Diagrams in Plans — Skipping, Accessibility, and Example](./diagrams-skip-accessibility-and-example.md) for the escape hatch, the accessibility rules, and a worked example.
