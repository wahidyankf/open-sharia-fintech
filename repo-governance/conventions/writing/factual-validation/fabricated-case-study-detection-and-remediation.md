---
title: "Fabricated Corporate Case Study Rule — Detection and Remediation"
description: The suspension test authors should apply before citing a company metric, the sentence pattern checkers should flag, and a worked before/after fix.
when_to_use: Use when a checker needs a detection pattern for fabricated case studies, or when rewriting a flagged fabricated claim.
category: explanation
subcategory: conventions
tags:
  - factual-validation
  - verification
  - web-research
  - accuracy
  - quality-assurance
created: 2025-12-16
---

# Fabricated Corporate Case Study Rule — Detection and Remediation

Continues from [The Pattern and What's Allowed/Prohibited](./fabricated-case-study-pattern-and-allowed-content.md).

## Suspension Test

Before writing any company-attributed metric, ask: **"Can I link to the primary source right now?"**

- If yes: include the link, write the claim
- If no: rewrite using the general principle without the company name and metric

## Detection Pattern for Checkers

Flag any "Why It Matters" sentence matching this structure:

```
[Company] + [past-tense action verb] + [specific numeric outcome]
```

Examples that always require verification:

- "When Stripe implemented X, they reduced Y by Z%"
- "At Google, [system] handles N+ transactions with metric M"
- "After Facebook adopted X, deployment incidents dropped by Y%"

High-suspicion signals:

- Suspiciously round or precise numbers (73%, 95%, exactly 15 service classes)
- Claims about internal metrics (bugs/month, memory footprint, cost savings)
- No citation of an engineering blog post, paper, or conference talk
- Multiple companies named with similar precision in the same file

## How to Fix a Fabricated Claim

Replace the corporate anecdote with the underlying principle:

```markdown
# BEFORE (fabricated)

When Shopify refactored order processing from anemic to rich domain models,
they reduced order-related bugs by 73%. Business rules previously scattered
across 15 service classes were consolidated into domain objects.

# AFTER (accurate)

Anemic models lead to scattered business logic that's hard to maintain and test.
Martin Fowler identified the Anemic Domain Model as an anti-pattern in 2003,
noting that it violates object-oriented principles by separating data from the
behavior that operates on it. When business rules live in service classes rather
than domain objects, they become invisible to domain experts, harder to test in
isolation, and prone to duplication across services.
```

The rewrite keeps the technical insight while removing the fabricated evidence.
