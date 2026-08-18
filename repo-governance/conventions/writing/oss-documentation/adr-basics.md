---
title: "ADRs: When to Create and Structure"
description: "When an architectural decision warrants an ADR and the required Status/Context/Decision/Consequences structure"
category: explanation
subcategory: conventions
tags:
  - conventions
  - documentation
  - open-source
  - repository-standards
created: 2026-04-04
when_to_use: "Read this before deciding whether a decision needs an ADR, or when starting to write one."
---

# ADRs: When to Create and Structure

## When to Create an ADR

Create an ADR for **architecturally significant decisions**:

- **Technology Choices** - Selecting frameworks, libraries, databases, cloud providers
- **Architectural Patterns** - Monorepo vs. polyrepo, microservices vs. monolith, state management
- **Infrastructure Decisions** - Deployment strategy, CI/CD approach, monitoring tools
- **Design Patterns** - Authentication approach, caching strategy, API design
- **Trade-offs** - Performance vs. simplicity, flexibility vs. standardization

**Do NOT create ADRs for:**

- Routine implementation details
- Temporary experimental code
- Decisions easily reversed without impact
- Minor library version updates

## ADR Structure

All ADRs must follow this structure:

```markdown
# [Number]. [Short Title]

Date: YYYY-MM-DD

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context

What is the issue we're facing? What factors are relevant?
Describe the forces at play (technical, political, social, project).
This section is value-neutral - present facts and constraints.

## Decision

What decision did we make?
State the decision clearly and concisely.
Use active voice: "We will use Nx for monorepo management."

## Consequences

What becomes easier or more difficult because of this decision?
Include both positive and negative consequences.
Be honest about trade-offs.

## Positive Consequences

- Benefit 1
- Benefit 2

## Negative Consequences

- Trade-off 1
- Trade-off 2

## Neutral Consequences

- Other impacts
```
