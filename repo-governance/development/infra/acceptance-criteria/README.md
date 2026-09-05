---
title: "Acceptance Criteria Convention"
description: "Writing testable acceptance criteria using Gherkin format for clarity and automation"
when_to_use: "Read this index to find the right Acceptance Criteria Convention child document."
---

# Acceptance Criteria Convention

- [Purpose, Principles, and Conventions](./purpose-principles-and-conventions.md) — Why acceptance criteria matter and which core principles and documentation conventions they implement. Use when orienting to why this convention exists or checking which principles and conventions acceptance criteria are expected to implement.
- [Gherkin Format and Journey Coherence](./gherkin-format-and-step-keyword-cardinality.md) — Keyword syntax and the continuous-journey rule for repeated primary steps.
- [Best Practices](./best-practices.md) — Six best practices for writing concrete, testable Gherkin scenarios, each with a PASS/FAIL example. Use when drafting a Gherkin scenario and wanting to check it against the specific-values, single-behaviour, present-tense, behaviour-focused, testable, and data-table best practices.
- [Common Patterns](./common-patterns.md) — Reusable Gherkin scenario patterns for CRUD operations, authentication and authorization, and error handling. Use when writing acceptance criteria for a CRUD feature, an auth-gated route, or an error-handling path and want a starting scenario shape.
- [Real-World Examples, Anti-Patterns, and When to Use](./real-world-examples-anti-patterns-and-when-to-use.md) — Full worked Gherkin examples, common anti-patterns to avoid, and the four categories of documentation where acceptance criteria belong. Use when you need a full worked scenario to copy from, want to check a draft scenario against known anti-patterns, or are deciding whether a document needs acceptance criteria at all.
- [Integration with Test Automation](./integration-with-test-automation.md) — Mapping canonical Gherkin scenarios to owner-local Vitest Cucumber Unit and Playwright BDD E2E bindings. Use when wiring a canonical scenario to the repository's current TypeScript or F# test adapters.
- [Mermaid Diagram, Related Conventions, and Summary](./mermaid-diagram-related-conventions-and-summary.md) — The Gherkin-to-automation workflow diagram, links to related conventions, and an overall summary of the acceptance-criteria convention. Use when you need a visual overview of the Gherkin workflow, links to related conventions, or a quick summary of this convention's guidance.
