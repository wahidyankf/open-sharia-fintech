---
title: "Acceptance Criteria Convention"
description: Writing testable acceptance criteria using Gherkin format for clarity and automation
category: explanation
subcategory: development
tags:
  - acceptance-criteria
  - gherkin
  - testing
  - requirements
created: 2025-12-07
when_to_use: Use when writing or reviewing acceptance criteria for a plan, feature spec, or test scenario.
---

# Acceptance Criteria Convention

This convention defines testable acceptance criteria using Gherkin for plans, specifications, and
requirements. It covers syntax, coherent user journeys, common patterns, anti-patterns, and test
automation.

## Documents

- [Purpose, Principles, and Conventions](./acceptance-criteria/purpose-principles-and-conventions.md) — Why acceptance criteria matter and which core principles and documentation conventions they implement. Use when orienting to why this convention exists or checking which principles and conventions acceptance criteria are expected to implement.
- [Gherkin Format and Journey Coherence](./acceptance-criteria/gherkin-format-and-step-keyword-cardinality.md) — Keyword syntax and when repeated primary steps form one continuous journey.
- [Best Practices](./acceptance-criteria/best-practices.md) — Six best practices for writing concrete, testable Gherkin scenarios, each with a PASS/FAIL example. Use when drafting a Gherkin scenario and wanting to check it against the specific-values, single-behaviour, present-tense, behaviour-focused, testable, and data-table best practices.
- [Common Patterns](./acceptance-criteria/common-patterns.md) — Reusable Gherkin scenario patterns for CRUD operations, authentication and authorization, and error handling. Use when writing acceptance criteria for a CRUD feature, an auth-gated route, or an error-handling path and want a starting scenario shape.
- [Real-World Examples, Anti-Patterns, and When to Use](./acceptance-criteria/real-world-examples-anti-patterns-and-when-to-use.md) — Full worked Gherkin examples, common anti-patterns to avoid, and the four categories of documentation where acceptance criteria belong. Use when you need a full worked scenario to copy from, want to check a draft scenario against known anti-patterns, or are deciding whether a document needs acceptance criteria at all.
- [Integration with Test Automation](./acceptance-criteria/integration-with-test-automation.md) — Mapping canonical Gherkin scenarios to owner-local Vitest Cucumber Unit and Playwright BDD E2E bindings. Use when wiring a canonical scenario to the repository's current TypeScript or F# test adapters.
- [Mermaid Diagram, Related Conventions, and Summary](./acceptance-criteria/mermaid-diagram-related-conventions-and-summary.md) — The Gherkin-to-automation workflow diagram, links to related conventions, and an overall summary of the acceptance-criteria convention. Use when you need a visual overview of the Gherkin workflow, links to related conventions, or a quick summary of this convention's guidance.
