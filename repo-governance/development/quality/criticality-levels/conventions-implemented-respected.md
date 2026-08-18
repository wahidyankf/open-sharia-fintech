---
title: "Conventions Implemented/Respected"
description: "Conventions this convention implements."
category: explanation
subcategory: development
tags:
  - criticality
  - validation
  - checker-agents
  - fixer-agents
  - quality-assurance
created: 2025-12-27
when_to_use: "Use to trace this convention's cross-references."
---

# Conventions Implemented/Respected

This convention builds upon and references:

## [Fixer Confidence Levels Convention](.././fixer-confidence-levels.md)

**Relationship**: Criticality works orthogonally with confidence levels.

- Criticality (CRITICAL/HIGH/MEDIUM/LOW) measures importance/urgency
- Confidence (HIGH/MEDIUM/FALSE_POSITIVE) measures certainty/fixability
- Combined in decision matrix to determine priority (P0-P4)

## [Maker-Checker-Fixer Pattern Convention](../../pattern/maker-checker-fixer.md)

**Relationship**: Criticality enhances Stage 2 (Checker) and Stage 3 (Fixer).

- Stage 2: Checkers categorize findings by criticality
- Stage 3: Fixers use criticality + confidence to determine priority
- Priority-based execution aligns with pattern's quality gates

## [Repository Validation Methodology Convention](.././repository-validation.md)

**Relationship**: Validation checks produce findings that need criticality assessment.

- Validation patterns detect issues
- Criticality system categorizes detected issues
- Standardized report format presents categorized findings

## [Temporary Files Convention](../../infra/temporary-files.md)

**Relationship**: Checker reports using criticality system are temporary files.

- All checker agents write to `generated-reports/`
- Filename pattern: `{agent-family}__{uuid-chain}__{timestamp}__audit.md`
- Progressive writing requirement ensures reports survive context compaction

## [Content Quality Principles Convention](../../../conventions/writing/quality.md)

**Relationship**: Content quality violations are categorized by criticality.

- WCAG A violations: CRITICAL
- WCAG AA violations: HIGH
- Heading hierarchy errors: HIGH
- Style inconsistencies: MEDIUM

## [Color Accessibility Convention](../../../conventions/formatting/color-accessibility.md)

**Relationship**: Criticality emoji indicators use standard emoji colors WITH text labels.

**Why emoji indicators can use red/green/yellow (unlike Mermaid diagrams)**:

- CRITICAL - Red emoji ALWAYS paired with "CRITICAL" text label
- HIGH - Orange emoji ALWAYS paired with "HIGH" text label
- MEDIUM - Yellow emoji ALWAYS paired with "MEDIUM" text label
- LOW - Green emoji ALWAYS paired with "LOW" text label

**Key Distinction**: Emoji indicators NEVER rely on color alone - text labels provide primary identification. This differs from Mermaid diagrams, which must use the verified accessible palette (Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC, Brown #CA9161) to ensure color-blind users can distinguish elements visually.

See [Color Accessibility Convention](../../../conventions/formatting/color-accessibility.md) for complete details on when standard emoji colors are acceptable (always with text) versus when accessible palette is required (Mermaid diagrams).

## [AI Agents Convention](../../agents/ai-agents.md)

**Relationship**: All checker and fixer agents must follow this convention.

- Checker agents: Generate reports with criticality sections
- Fixer agents: Use criticality + confidence for priority execution
- Progressive writing: Required for all checkers per AI Agents Convention

---
