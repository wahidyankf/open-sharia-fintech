---
title: "Simplicity Over Complexity"
description: Favor minimum viable abstraction and avoid over-engineering - start simple, add complexity only when proven necessary
category: explanation
subcategory: principles
tags:
  - principles
  - simplicity
  - kiss
  - yagni
  - over-engineering
created: 2025-12-15
when_to_use: Use when deciding how much abstraction, configuration, or structure a solution needs before writing it.
---

# Simplicity Over Complexity

Favor **minimum viable abstraction** and avoid over-engineering. Start simple and add complexity **only when proven necessary** through actual use and pain points.

## Foundations

- [Vision Supported](./simplicity-over-complexity/01-vision-supported.md) — How simplicity over complexity serves the Open Sharia Enterprise vision of accessibility and low maintenance cost. Use when explaining why simplicity matters to the project's mission.
- [What](./simplicity-over-complexity/02-what.md) — Defines simplicity and complexity in this repository's terms. Use when you need the working definitions this convention uses.
- [Why](./simplicity-over-complexity/03-why.md) — Benefits of simplicity and problems with complexity, plus KISS, YAGNI, and Rule of Three. Use when justifying a simpler solution over a complex one.

## Worked Contrasts

- [How It Applies](./simplicity-over-complexity/04-how-it-applies.md) — Five worked contrasts (structure, agents, frontmatter, docs, conventions) of simple versus complex choices. Use when you need a concrete before/after example for a specific decision.
- [Anti-Patterns](./simplicity-over-complexity/05-anti-patterns.md) — Four code-level anti-patterns - premature abstraction, config explosion, deep inheritance, over-generic code. Use when reviewing code for these anti-patterns.
- [PASS: Best Practices](./simplicity-over-complexity/06-pass-best-practices.md) — Five best practices - start concrete, composition, flat over nested, one job per component, wait for pain. Use when choosing how to structure new code.
- [Implementation Guidelines](./simplicity-over-complexity/07-implementation-guidelines.md) — Five rules for minimum code with maximum clarity, plus the senior engineer test. Use when writing new code and avoiding speculative features.
- [Application Examples](./simplicity-over-complexity/08-application-examples.md) — Three worked examples (dark mode, API errors, utilities) contrasting over-engineered and minimal solutions. Use when you need a worked feature-request example.

## Reference

- [Relationship to Other Principles](./simplicity-over-complexity/09-relationship-to-other-principles.md) — Cross-references to deliberate-problem-solving, root-cause-orientation, explicit-over-implicit, automation-over-manual, progressive-disclosure. Use when tracing connections to the repo's other principles.
- [For AI Agents](./simplicity-over-complexity/10-for-ai-agents.md) — Five agent-specific obligations for simplicity, including avoiding premature abstraction. Use when auditing agent behavior against this principle.
- [Common Violations](./simplicity-over-complexity/11-common-violations.md) — Three before/after examples of common simplicity violations. Use when identifying whether a behavior violates this principle.
- [Summary](./simplicity-over-complexity/12-summary.md) — One-paragraph recap - minimal, no speculation, trust, inline first, question complexity. Use for the shortest possible recap of this principle.
- [Related Conventions](./simplicity-over-complexity/13-related-conventions.md) — Links to implementation workflow, monorepo structure, AI agents, and Diátaxis framework. Use when looking for related conventions.
- [References](./simplicity-over-complexity/14-references.md) — External references - KISS, YAGNI, Rule of Three, books, and articles. Use when looking for external sources backing this principle.
