---
title: "How It Applies — Documentation Hierarchy, Convention Documents, and the Word Budget"
description: Progressive structure in document sections, convention documents, and the governance word budget.
category: explanation
subcategory: principles
tags:
  - principles
  - progressive-disclosure
  - complexity-management
created: 2025-12-15
when_to_use: Use when structuring a document's sections or trimming a governance file to fit its word budget.
---

# How It Applies — Documentation Hierarchy, Convention Documents, and the Word Budget

## Documentation Hierarchy

**Context**: Structuring documentation.

**Progressive Layers**:

```markdown
# Document Title

## Overview

Brief 2-3 sentence summary.

## Quick Start

Get running in 5 minutes.

## Basic Usage

Common use cases (80% of users).

## Advanced Usage

Edge cases and optimization.

## Reference

Complete API/configuration details.
```

**Why this works**:

- PASS: Beginners read Overview + Quick Start
- PASS: Practitioners read Basic Usage
- PASS: Experts jump to Advanced Usage
- PASS: All levels served

## Convention Documents

**Context**: Explaining repository standards.

**Progressive Structure**:

```markdown
# Convention Name

## What

Simple explanation of the convention.

## Why

Benefits and rationale.

## How It Applies

Basic examples and patterns.

## Advanced Patterns

Edge cases and complex scenarios.

## Anti-Patterns

What to avoid (for advanced users).
```

**Why this works**:

- PASS: "What" and "Why" for beginners
- PASS: "How It Applies" for practitioners
- PASS: "Advanced Patterns" for experts
- PASS: Each level optional

## Governance Word Budget

**Context**: Governance instruction files (`AGENTS.md`, `CLAUDE.md`, harness-specific surfaces)
auto-loaded by coding-agent harnesses. Harnesses impose hard limits, measured in words (a raw
whole-file `split_whitespace()` count — see the
[Governance Word-Budget Convention](../../../conventions/structure/governance-word-budget.md));
content past the limit is silently truncated or ignored.

**Progressive Structure**:

When an instruction file exceeds its budget, the mandated fix is progressive disclosure — not
deletion, dense compression, or splitting into another auto-loaded file:

```markdown
<!-- BEFORE: 2,700 bytes for a single app block -->

### ose-www

- **URL**: https://oseplatform.com
- **Production branch**: `prod-ose-www`
- **Framework**: Next.js 16 (App Router, TypeScript, tRPC)
- **Deployment**: Vercel
- **Dev port**: 3100

<!-- AFTER: ~60 bytes; detail moves to app README -->

| `ose-www` | oseplatform.com | 3100 | `prod-ose-www` |
```

Detail remains fully accessible via `apps/ose-www/README.md` — it is just no longer inlined.

**Why this works**:

- PASS: Every rule still reachable via a `See` link
- PASS: Harness loads the full instruction file (under budget)
- PASS: No governance content deleted

**Alternative** (what we avoid):

FAIL: **Delete the rule** — agent behaviour becomes undefined for the deleted case.
FAIL: **Dense compression** — strips line breaks, degrades readability.
FAIL: **Split into another auto-loaded file** — moves bytes, does not reduce resolved-tree total.

**See**: [Governance Word-Budget Convention](../../../conventions/structure/governance-word-budget.md)
