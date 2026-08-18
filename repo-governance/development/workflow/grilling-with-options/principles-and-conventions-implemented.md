---
title: "Principles and Conventions Implemented"
description: The principles and companion conventions the Grilling-With-Options Convention implements and respects.
category: explanation
subcategory: development
tags:
  - planning
  - grill-me
  - user-interaction
  - plan-maker
  - design-decisions
  - interaction
  - agents
created: 2026-05-26
when_to_use: Use when tracing why structured multiple-choice grilling is required back to the principles and conventions it respects.
---

# Principles and Conventions Implemented

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**:
  Structured options force the agent to understand the design space before asking, and force
  the user to choose deliberately rather than free-associate. Reversible design branches are
  made explicit so users can reason about them.
- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**:
  Each option names its trade-off. The Recommended option names its rationale. Nothing is
  left to the user's imagination or to silent agent inference.
- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: A
  bounded list of options reduces cognitive load. The user selects from prepared choices
  rather than having to generate an answer from scratch.
- **[Progressive Disclosure](../../../principles/content/progressive-disclosure.md)**: Options
  start simple (2-3 choices covering 90% of cases) and expose complexity only when the
  user's prior answer opens a new branch. Unrelated decisions never appear in the same
  question.
- **[Accessibility First](../../../principles/content/accessibility-first.md)**: Users are never
  locked into a predefined set — the free-form "Other / write-in" path is always available.
  Questions are self-contained so screen-reader users and harness users without rich
  rendering experience the same choice surface.

## Conventions Implemented/Respected

- **[Convention Writing Convention](../../../conventions/writing/conventions.md)**: This document
  follows the standard Purpose / Standards / Examples / Validation structure.
- **[Plans Organization Convention](../../../conventions/structure/plans.md)**: This convention
  serves the plan creation lifecycle described there — grilling is the first gate before any
  plan files are written.
- **[Governance Vendor-Independence Convention](../../../conventions/structure/governance-vendor-independence.md)**:
  All vendor-specific tool names are confined to the Platform Binding Examples section.
- **[Linking Convention](../../../conventions/formatting/linking.md)**: All cross-references use
  GitHub-compatible markdown with `.md` extensions.
- **[Content Quality Principles](../../../conventions/writing/quality.md)**: Active voice, single
  H1, proper heading nesting.
