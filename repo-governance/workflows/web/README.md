---
title: "Web Workflows"
description: "Orchestrated workflows that test a live running website and turn the findings into a fix plan — combined spec-aware exploratory, spec-blind usability, and design-aware design-fidelity testing."
category: explanation
subcategory: workflows
tags: []
created: 2026-06-20
---

# Web Workflows

Use these workflows when a live site needs to be experienced as a real visitor would experience it. They turn observed behavior, usability, and design findings into an actionable delivery plan.

## Purpose

These workflows define **WHEN and HOW to test a running site and act on the result**, orchestrating the three live-site testing agents (`web-exploratory-tester`, `web-usability-tester`, `web-design-tester`) and the planning agents (`plan-maker`, `plan-checker`, `plan-fixer`) so that a single run yields one combined, fix-ready plan.

## Scope

**✅ Workflows Here:**

- Spec-aware exploratory testing of a live site (functional, behavioural-consistency, responsive, accessibility, URL/IA, passive security)
- Spec-blind heuristic usability evaluation of the same live site (Nielsen heuristics, cognitive walkthrough, information scent)
- Design-aware design-fidelity evaluation of the same live site (mockup fidelity, runtime tokens, design-system primitives, hierarchy, spacing/density, typography, colour)
- Combining all three perspectives into one fix-planning deliverable in `plans/`

**❌ Not Included:**

- Public-web information gathering / research (that is the `web-researcher` agent, invoked directly)
- UI component quality validation of source components (that is `ui/`)
- Implementing the fixes themselves (that is `plan/plan-execution`, run later after promotion)

## Workflows

- [Web UX Test-Fixing Planning](./web-ux-test-fixing-planning.md) - Run the three live-site testers — `web-exploratory-tester` (spec-aware correctness), `web-usability-tester` (spec-blind usability), and `web-design-tester` (design-aware fidelity) — against the same live URL(s) and goal **sequentially** — integrating each result set into the plan before the next runs — then solidify one plan whose findings section keeps the three sources clearly separated (EWT-### vs UWT-### vs DWT-###) and which carries `tech-docs.md` (root-cause + fix approach), a TDD-shaped `delivery.md`, and — when the plan is UI-bearing — an `assets/` folder of both-tier (lo-fi + hi-fi) UI mockups. Grills the user hard on every material decision. Produces a new plan in `plans/in-progress/` by default; can merge into an existing plan on request. Deliverable is the plan, not the fixes. This is the near-end three-tester round web-UI feature-change plans must run (User-Facing Delivery Hardening Rule 15).

## Related Documentation

- [Workflows Index](../README.md) - All orchestrated workflows
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model these workflows enforce
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) - Core workflow pattern
- [Core Principles](../../principles/README.md) - Layer 1 governance
