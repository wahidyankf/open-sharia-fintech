---
title: "Principles Implemented/Respected"
description: "Principles this convention implements."
category: explanation
subcategory: development
tags:
  - criticality
  - validation
  - checker-agents
  - fixer-agents
  - quality-assurance
created: 2025-12-27
when_to_use: "Use to trace this convention's principle rationale."
---

# Principles Implemented/Respected

This convention implements the following principles from [Core Principles Index](../../../principles/README.md):

## Explicit Over Implicit

**How**:

- Four clearly defined criticality levels with objective criteria
- Explicit decision matrix showing criticality × confidence combinations
- Standardized report format with clear section structure
- Explicit priority levels (P0-P4) with defined execution order

**Why**:

Removes ambiguity in severity assessment. Everyone interprets CRITICAL, HIGH, MEDIUM, LOW the same way.

## Automation Over Manual

**How**:

- Priority-based execution enables automated fix application
- HIGH confidence + CRITICAL/HIGH criticality → automatic fixing
- Clear criteria enable checker agents to categorize programmatically
- Progressive writing ensures automation survives context limits

**Why**:

Reduces manual decision-making for objective issues. Automation handles P0-P1 fixes reliably.

## Simplicity Over Complexity

**How**:

- Four levels (not five or seven) - sufficient granularity without overwhelm
- Section-based organization (not per-finding metadata) - human-readable
- Single decision tree for assessment - easy to apply
- Orthogonal dimensions (criticality vs confidence) - one concept per dimension

**Why**:

Simple system is easier to understand, apply consistently, and maintain long-term.

## Accessibility First

**How**:

- Emoji indicators (🟠🟡🟢) ALWAYS paired with text labels (CRITICAL/HIGH/MEDIUM/LOW)
- Color is supplementary - text labels provide primary identification
- Clear priority labels (P0-P4) supplement colors
- Text-based severity names work in all contexts (voice, text-only)
- Standardized format improves scannability

**Why**:

Ensures findings are accessible to all users regardless of visual ability or context. Unlike Mermaid diagrams (which must use accessible palette), emoji indicators can use standard emoji colors because they NEVER appear without text labels.

---
