---
title: "Web Workflows"
description: "Orchestrated workflows that test a live running website and turn the findings into a fix plan — combined spec-aware exploratory, spec-blind usability, and design-aware design-fidelity testing."
when_to_use: Use when routing to a workflow that tests a live running site and turns findings into a fix plan.
category: explanation
subcategory: workflows
tags: []
created: 2026-06-20
---

# Web Workflows

Use these workflows when a live site needs to be experienced as a real visitor would experience it. They turn observed behaviour, usability, and design findings into an actionable delivery plan.

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

- [web-ux-test-fixing-planning](./web-ux-test-fixing-planning.md) — Run the three live-site UX-quality testers (exploratory, usability, design) sequentially against the same URL(s), then solidify one source-attributed fix plan with tech-docs.md and a TDD-shaped delivery.md. Use before hardening a user-facing feature, to get a combined correctness/usability/design-fidelity read on a running site, or to refresh an existing findings plan via plan-mode=merge.

## Related Documentation

- [Workflows Index](../README.md) - All orchestrated workflows
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model these workflows enforce
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) - Core workflow pattern
- [Core Principles](../../principles/README.md) - Layer 1 governance
