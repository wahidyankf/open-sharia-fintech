---
title: "Purpose, Principles, and Conventions"
description: Why acceptance criteria matter and which core principles and documentation conventions they implement.
category: explanation
subcategory: development
tags:
  - acceptance-criteria
  - gherkin
  - testing
  - requirements
created: 2025-12-07
when_to_use: Use when orienting to why this convention exists or checking which principles and conventions acceptance criteria are expected to implement.
---

# Purpose, Principles, and Conventions

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: Writing acceptance criteria forces explicit definition of success before implementation. Gherkin's Given-When-Then structure surfaces assumptions (Given), clarifies actions (When), and makes expected outcomes explicit (Then) - preventing vague requirements that hide confusion.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Gherkin syntax (Given-When-Then) explicitly states preconditions, actions, and expected outcomes. No ambiguous requirements like "should work well" - everything is concrete and verifiable.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: Gherkin scenarios translate directly to automated tests (BDD frameworks). Requirements become executable specifications. Machines verify correctness automatically instead of manual testing.

## Conventions Implemented/Respected

**REQUIRED SECTION**: All development practice documents MUST include this section to ensure traceability from practices to documentation standards.

This practice implements/respects the following conventions:

- **[Plans Organization Convention](../../../conventions/structure/plans.md)**: Acceptance criteria are written in `prd.md` within plan folders (or the condensed PRD section of a single-file plan's `README.md`) following the Gherkin format defined by this convention.

- **[Content Quality Principles](../../../conventions/writing/quality.md)**: Gherkin scenarios use active voice, clear structure, and concrete examples - aligning with content quality standards for clarity and testability.

- **[Diagrams Convention](../../../conventions/formatting/diagrams.md)**: When visualizing acceptance criteria workflows, use Mermaid diagrams with accessible colors as demonstrated in this document's Gherkin workflow diagram.

## Purpose

Acceptance criteria define the conditions that must be met for a feature, story, or requirement to be considered complete. Using structured Gherkin format provides:

- **Clear communication**: Unambiguous requirements understood by all stakeholders
- **Test automation**: Direct translation to automated tests (BDD frameworks)
- **Living documentation**: Scenarios serve as executable specifications
- **Testability**: Forces concrete, verifiable conditions
- **Shared language**: Business and technical teams use same terminology
