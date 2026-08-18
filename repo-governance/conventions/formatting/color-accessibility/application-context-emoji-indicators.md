---
title: "Application Contexts: Emoji Indicators with Text Labels"
description: "Defines when standard emoji colors are acceptable because text labels always accompany them."
when_to_use: "Use when adding emoji status indicators such as criticality or pass/fail markers to confirm the color choice is acceptable."
category: explanation
subcategory: conventions
tags:
  - accessibility
  - color-blindness
  - wcag
  - design
  - conventions
  - mermaid-diagrams
  - color-palette
created: 2025-12-04
---

# Application Contexts: Emoji Indicators with Text Labels

This section distinguishes between two different color usage contexts with different accessibility requirements.

## Context 1: Emoji Indicators with Text Labels

**Use Case**: Status indicators, criticality levels, validation findings that ALWAYS include text labels.

**Accessibility Approach**: Color is supplementary to text - standard emoji colors acceptable.

**Examples**:

- Criticality levels: CRITICAL, HIGH, MEDIUM, LOW
- Status markers: PASS: Success, FAIL: Error, Warning
- Validation results: [Verified] , [Error] , [Broken]

**Why standard emoji colors (red/green/yellow) are acceptable here**:

1. **Text labels are MANDATORY** - Color never appears without descriptive text
2. **Text provides primary identification** - Users can understand meaning from text alone
3. **Color is supplementary enhancement** - Adds visual scannability but not required for comprehension
4. **Screen readers announce text** - "CRITICAL" is read aloud, not just "red circle emoji"

**Critical Rule**: Emoji indicators MUST ALWAYS include text labels. Never use colored emojis alone without text context.

PASS: **Acceptable**: `CRITICAL Issues (Must Fix)` - Color + text
FAIL: **Not Acceptable**: `Issues` - Color without clear severity text
FAIL: **Not Acceptable**: Section marked only with - Color-only identification
