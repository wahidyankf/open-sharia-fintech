---
title: "UI Mockups in Plan Docs: Responsive Design and Design-Review Heuristic"
description: "Covers the mobile/tablet/desktop responsive design requirement and the identical-DOM-per-breakpoint review heuristic."
when_to_use: "Use when a UI mockup needs to show responsive behaviour across breakpoints and you need the review heuristic."
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

# UI Mockups in Plan Docs: Responsive Design and Design-Review Heuristic

## Responsive Design — Mobile / Tablet / Desktop

Every UI-bearing screen MUST be designed for all three display classes, **mobile-first**. A
desktop-only mockup does not pass review.

| Display class | Breakpoint (Tailwind) | Reference width |
| ------------- | --------------------- | --------------- |
| Mobile        | base (`< sm`)         | ~360 px         |
| Tablet        | `md` (≥ 768 px)       | ~768 px         |
| Desktop       | `lg` (≥ 1024 px)      | ~1280 px        |

The mockups MUST make the responsive behaviour explicit rather than showing a single desktop width:

- **Low-fidelity (Tier 1)** — provide an ASCII wireframe (or an inline note) for at least the
  **mobile** and **desktop** layouts where they differ, showing how the layout reflows: e.g. a
  multi-column table collapses to stacked cards on mobile; a left control rail moves into a top
  sheet / drawer; a two-pane split becomes a single column.
- **High-fidelity (Tier 2)** — the selected design's record MUST state the **responsive strategy**
  per breakpoint: which components stack, collapse, hide, or change, grounded in the repo's UI-kit
  breakpoint tokens (Tailwind `sm` / `md` / `lg`).
- **Selection rationale** — each finalist MUST be evaluated on its **responsive behaviour
  (mobile-first)**, not only its desktop appearance; a layout that only works on desktop is not a
  valid finalist.

## Design-Review Heuristic — Identical DOM at Every Breakpoint

When a plan's responsive strategy proposes **identical DOM at every breakpoint** — for example, a
single SVG mockup with one `viewBox` scaled uniformly across mobile/tablet/desktop — the required
follow-up question is: **what is the responsive lever, and does it scale text?** Identical DOM
combined with a uniform-scale coordinate system leaves scale as the only responsive lever available,
which forces typography to become a function of viewport width — mutually exclusive with stable,
legible text sizes at every breakpoint. Reviewers and `plan-checker` should treat "same DOM at every
breakpoint" as a flag requiring an explicit, answered version of this question before the strategy is
accepted.
