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

This convention defines how to write testable acceptance criteria using **Gherkin format** for plans, specifications, and requirements documentation. It covers the Gherkin keyword syntax, the step-keyword cardinality rule, best practices, common scenario patterns, real-world examples, anti-patterns, when to use acceptance criteria, and test-automation integration in the child documents below.

## Documents

- [Purpose, Principles, and Conventions](./acceptance-criteria/01-purpose-principles-and-conventions.md) — Why acceptance criteria matter and which core principles and documentation conventions they implement. Use when orienting to why this convention exists or checking which principles and conventions acceptance criteria are expected to implement.
- [Gherkin Format and Step-Keyword Cardinality](./acceptance-criteria/02-gherkin-format-and-step-keyword-cardinality.md) — The Gherkin keyword syntax used to write scenarios, plus the HARD rule limiting every scenario to one primary Given/When/Then line. Use when looking up the Gherkin Given-When-Then keyword syntax, or checking that a scenario follows the one-primary-keyword-per-Scenario rule.
- [Best Practices](./acceptance-criteria/03-best-practices.md) — Six best practices for writing concrete, testable Gherkin scenarios, each with a PASS/FAIL example. Use when drafting a Gherkin scenario and wanting to check it against the specific-values, single-behavior, present-tense, behavior-focused, testable, and data-table best practices.
- [Common Patterns](./acceptance-criteria/04-common-patterns.md) — Reusable Gherkin scenario patterns for CRUD operations, authentication and authorization, and error handling. Use when writing acceptance criteria for a CRUD feature, an auth-gated route, or an error-handling path and want a starting scenario shape.
- [Real-World Examples, Anti-Patterns, and When to Use](./acceptance-criteria/05-real-world-examples-anti-patterns-and-when-to-use.md) — Full worked Gherkin examples, common anti-patterns to avoid, and the four categories of documentation where acceptance criteria belong. Use when you need a full worked scenario to copy from, want to check a draft scenario against known anti-patterns, or are deciding whether a document needs acceptance criteria at all.
- [Integration with Test Automation](./acceptance-criteria/06-integration-with-test-automation.md) — Mapping Gherkin scenarios to step definitions in Cucumber.js, Jest-Cucumber, and cucumber-rs. Use when wiring a Gherkin scenario to a BDD test framework in TypeScript, Rust, or F#.
- [Mermaid Diagram, Related Conventions, and Summary](./acceptance-criteria/07-mermaid-diagram-related-conventions-and-summary.md) — The Gherkin-to-automation workflow diagram, links to related conventions, and an overall summary of the acceptance-criteria convention. Use when you need a visual overview of the Gherkin workflow, links to related conventions, or a quick summary of this convention's guidance.
