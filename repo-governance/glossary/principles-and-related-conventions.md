---
description: Which principles the glossary implements and which conventions authoritatively define the terms it names.
when_to_use: Use when tracing a glossary entry upward to the principle it serves or downward to the convention that governs it.
---

# Principles and Related Conventions

## Principles Implemented/Respected

- **[Explicit Over Implicit](../principles/software-engineering/explicit-over-implicit.md)**: A term
  each reader scopes differently is an implicit contract. Writing the boundary down converts an
  assumption into something checkable.
- **[Simplicity Over Complexity](../principles/general/simplicity-over-complexity.md)**: One shared
  definition costs less than re-litigating a rule's reach every time it is applied.
- **[Progressive Disclosure](../principles/content/progressive-disclosure.md)**: The headline
  definition sits in the index; full boundary tables sit in the children.
- **[Documentation First](../principles/content/documentation-first.md)**: Vocabulary is settled
  before the rules depending on it are argued.

## Related Conventions

- [Repository Governance Architecture](../repository-governance-architecture.md) — the six-layer
  hierarchy these terms sit inside.
- [Governance Vendor-Independence](../conventions/structure/governance-vendor-independence.md) —
  the vendor-neutral vocabulary this glossary uses for bindings and coding agents.
- [Governance Word-Budget](../conventions/structure/governance-word-budget.md) — the thresholds
  that make "surface" a measurable term rather than a metaphor.
- [Plans Organization Convention](../conventions/structure/plans.md) — the authoritative source for
  plan, phase, delivery unit, and delivery mode.
- [AI Agents Convention](../development/agents/ai-agents.md) — the authoritative source for agent,
  agent skill, and the maker/checker/fixer roles.
- [Programming Language Docs Separation](../conventions/structure/programming-language-docs-separation.md)
  — why the language style guides live outside `repo-governance/` while still binding.

## Why These Definitions Live Together

Each term below has an authoritative convention that defines it in full. The glossary exists for a
different question: not "what does this convention say" but "does this rule reach my file". That
question is answered by comparing terms against each other, which is why they are collected in one
place rather than left distributed across the conventions that own them.

The glossary therefore states scope and points onward. When it and an owning convention disagree,
the convention wins and the glossary entry is the defect.
