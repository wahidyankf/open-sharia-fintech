---
title: "Mermaid Diagram, Related Conventions, and Summary"
description: The Gherkin-to-automation workflow diagram, links to related conventions, and an overall summary of the acceptance-criteria convention.
category: explanation
subcategory: development
tags:
  - acceptance-criteria
  - gherkin
  - testing
  - requirements
created: 2025-12-07
when_to_use: Use when you need a visual overview of the Gherkin workflow, links to related conventions, or a quick summary of this convention's guidance.
---

# Mermaid Diagram, Related Conventions, and Summary

## Mermaid Diagram: Gherkin Workflow

<!-- Uses accessible colors: blue (#0173B2), orange (#DE8F05), teal (#029E73) -->

```mermaid
graph TD
 A[Write Gherkin Scenario] -- define behaviour --> B[Scenario: Login Success]
 B --> C[Given: Initial state]
 C --> D[When: User action]
 D --> E[Then: Expected outcome]
 E --> F{Implement Feature}
 F -- code written --> G[Write Step Definitions]
 G --> H[Run Automated Tests]
 H -- pass --> I[Feature Complete]
 H -- fail --> J[Fix & Re-run Tests]
 J --> I

 style A fill:#0173B2,stroke:#000,color:#fff
 style B fill:#DE8F05,stroke:#000,color:#000
 style I fill:#029E73,stroke:#000,color:#fff
 style J fill:#CC78BC,stroke:#000,color:#fff
```

## Related Conventions

- [Behaviour-Driven Development](../../behaviour-driven-development.md) - Mandatory 1:1 mapping between CLI commands and Gherkin specifications
- [Plans Organization Convention](../../../conventions/structure/plans.md) - Where to use acceptance criteria in plans
- [Tutorial Convention](../../../conventions/tutorials/general.md) - Acceptance criteria for tutorial quality
- [Content Quality Principles](../../../conventions/writing/quality.md) - Writing clear, testable content

## Summary

**Use Gherkin format for acceptance criteria to**:

- PASS: Ensure requirements are clear and unambiguous
- PASS: Enable direct translation to automated tests
- PASS: Create living documentation that stays up-to-date
- PASS: Facilitate communication between business and technical teams
- PASS: Force concrete, testable conditions

**Follow best practices**:

- Be specific with concrete values
- One scenario per behaviour
- Use present tense
- Focus on behaviour, not implementation
- Make it testable
- Use data tables for multiple inputs

**Apply to**:

- Project plans and requirements
- Feature specifications and RFCs
- API documentation
- Test documentation and QA checklists
