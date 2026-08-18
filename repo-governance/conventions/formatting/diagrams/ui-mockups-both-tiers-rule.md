---
title: "UI Mockups in Plan Docs: The Both-Tiers Rule"
description: "Defines the required two-tier mockup rule: low-fidelity ASCII wireframes plus high-fidelity Excalidraw PNGs."
when_to_use: "Use when producing UI mockups for a plan and need to know both required fidelity tiers and their formats."
category: explanation
subcategory: conventions
tags:
  - diagrams
  - mermaid
  - ascii-art
  - visualization
  - conventions
  - accessibility
  - color-blindness
created: 2025-11-24
---

# UI Mockups in Plan Docs: The Both-Tiers Rule

Every screen in a UI-bearing plan MUST be documented at **both** fidelities, in **separate,
labelled subsections**. This is the **both-tiers rule**:

| Tier          | Format                                    | Role                                                    |
| ------------- | ----------------------------------------- | ------------------------------------------------------- |
| Low-fidelity  | ASCII / Unicode wireframe in fenced block | Structure, control placement, flow — diffable, inline   |
| High-fidelity | Excalidraw `.excalidraw.png` via `![]()`  | Spacing, color, typography, visual hierarchy — editable |

The two tiers are **complementary**, not alternatives. The low-fidelity tier is the diffable
structural source of truth that reviewers comment on line-by-line. The high-fidelity tier shows
what the screen actually looks like with real design-system spacing and color.

**Plain `.png` screenshot** is the high-fidelity fallback once a design is final and no longer
iterating — it renders everywhere but is binary and must be replaced on every change.

## Tier 1 — Low-Fidelity ASCII Wireframe (Required)

Zero dependencies. Renders identically in GitHub, VSCode, and terminals. Perfectly diffable.
Stays inline in the `.md` file. Captures layout, control placement, and flow.

Copy-paste example:

```markdown
### Low-Fidelity Wireframe — Compare-All Mode

\`\`\`
┌──────────────────────────────────────────────────────┐
│ Salary Savings Calculator │
├──────────────────────────────────────────────────────┤
│ [ Compare All ] ( Single City ) ← tab toggle │
├──────────────────────────────────────────────────────┤
│ Salary (USD/mo): [________________] │
│ Household: [ Single ▼] │
│ Area: ( ) Center (•) Rural │
├──────────────────────────────────────────────────────┤
│ City Savings/mo % of Salary │
│ ────────────── ─────────── ─────────── │
│ Singapore $1,200 30% │
│ Jakarta $2,100 52% │
│ Kuala Lumpur $1,800 45% │
└──────────────────────────────────────────────────────┘
\`\`\`
```

## Tier 2 — High-Fidelity Excalidraw PNG (Required)

Real spacing, grouping, color, typography, and visual hierarchy, while staying editable (embedded
scene). The PNG file lives beside the plan, for example
`plans/in-progress/<name>/ui-compare-all.excalidraw.png`.

**Tooling**: The Excalidraw VSCode extension (`pomdtr.excalidraw-editor`) is needed to **edit**
an `.excalidraw.png` but not to **view** it. ASCII needs nothing.

Copy-paste example:

```markdown
### High-Fidelity Mockup — Compare-All Mode

![Compare-All mode — high-fidelity mockup](./ui-compare-all.excalidraw.png)

_High-fidelity mockup. Edit with the Excalidraw VSCode extension — the PNG carries the scene._
```
