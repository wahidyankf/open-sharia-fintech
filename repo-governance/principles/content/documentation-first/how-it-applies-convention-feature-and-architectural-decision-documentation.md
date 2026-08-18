---
title: "How It Applies — Convention, Feature, and Architectural Decision Documentation"
description: Requirements for convention, feature, and architectural-decision documentation.
category: explanation
subcategory: principles
tags:
  - principles
  - documentation
created: 2025-12-28
when_to_use: Use when writing a convention, feature, or decision document.
---

# How It Applies — Convention, Feature, and Architectural Decision Documentation

## Convention Documentation

**Context**: All standards and conventions in `repo-governance/conventions/`.

**Requirements**:

PASS: **Every convention** has a document explaining:

- What the convention is (the rule)
- Why it exists (the rationale)
- How to apply it (examples)
- When exceptions are allowed (if any)
- Principles it implements (traceability)

FAIL: **Anti-pattern**: "We just follow this convention, everyone knows it"

**Example**: Instead of just enforcing file naming via checker agents, we have [File Naming Convention](../../../conventions/structure/file-naming.md) explaining:

- The pattern: descriptive kebab-case filenames with category implied by directory location
- The why: Readability, searchability, no prefix lookup required
- Examples: `getting-started.md`, `file-naming-convention.md`
- Principles: Explicit Over Implicit, Simplicity Over Complexity

**Why this works**: New contributors understand WHY the convention exists and can apply it correctly in new contexts.

## Feature Documentation

**Context**: All features in applications and libraries.

**Requirements**:

PASS: **Every feature** has documentation including:

- **How-to guide**: Step-by-step instructions for using the feature
- **Reference documentation**: Complete technical details (API, configuration, options)
- **Explanation**: Why the feature exists, what problem it solves, design decisions

FAIL: **Anti-pattern**: "The feature is live, users will figure it out"

**Example**: When adding a new Islamic finance calculation (e.g., Murabahah profit calculation), document:

- **How-to**: "How to Calculate Murabahah Profits" (step-by-step guide)
- **Reference**: API documentation for `calculateMurabahahProfit()` function
- **Explanation**: "Understanding Murabahah Profit Structures" (concepts, Shariah principles, design rationale)

**Why this works**: Users can use the feature independently. Developers can maintain and extend it confidently.

## Architectural Decision Documentation

**Context**: All major technical decisions (frameworks, patterns, architecture).

**Requirements**:

PASS: **Every architectural decision** is documented with:

- **Context**: What problem are we solving?
- **Decision**: What approach did we choose?
- **Rationale**: Why this approach over alternatives?
- **Consequences**: What trade-offs does this create?
- **Alternatives considered**: What did we NOT choose and why?

FAIL: **Anti-pattern**: "We chose Express because I like it"

**Example**: Decision to use Nx monorepo:

```markdown
## Decision: Nx Monorepo Architecture

**Context**: Multiple applications and libraries sharing code and conventions.

**Decision**: Use Nx monorepo with apps/ and libs/ structure.

**Rationale**:

- Task caching reduces build times
- Affected detection runs only changed projects
- Dependency graph visualizes relationships
- Consistent tooling across projects

**Consequences**:

- Single repository (simpler than multi-repo, but larger)
- Shared dependencies (version alignment required)
- Learning curve for Nx CLI

**Alternatives Considered**:

- Multi-repo: More complex versioning, harder to share code
- Lerna/Turborepo: Less integrated than Nx
- No monorepo: Code duplication, inconsistent tooling
```

**Why this works**: Future maintainers understand WHY this architecture was chosen. When requirements change, they can reconsider with full context.
