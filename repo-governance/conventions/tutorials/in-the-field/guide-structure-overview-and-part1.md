---
title: "Guide Structure Overview"
description: The six-part recommended guide structure and the requirements for Part 1, which establishes production relevance.
when_to_use: Use when starting to write a new In-the-Field guide and need the overall structure and Part 1 requirements.
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - in-the-field
  - education
  - production-ready
created: 2026-02-04
---

# Guide Structure Overview

Every in-the-field guide follows a **recommended structure**:

## Part 1: Why It Matters (2-3 paragraphs)

**Purpose**: Establish production relevance and motivation

**Must answer**:

- What production problem does this solve?
- What are consequences of NOT following this practice?
- What are core benefits in real systems?

**Example**:

```markdown
## Why Test-Driven Development Matters

Test-Driven Development (TDD) is critical for financial and enterprise systems because it prevents costly bugs, ensures correctness, enables confident refactoring, and documents behavior through executable specifications.

**Core Benefits**:

- Prevents costly bugs: Catch calculation errors before production
- Ensures correctness: Test-first forces thinking about requirements
- Enables refactoring: Tests provide safety net for improvements
- Documents behavior: Tests serve as executable specifications
- Builds confidence: High test coverage reduces deployment risk

**Problem**: Without TDD, bugs reach production causing incorrect calculations and financial losses.

**Solution**: Write tests first to catch bugs in seconds, never in production.
```
