---
title: "Agent-Skill Separation — Duplication Patterns and Before/After Example"
description: "Lists common duplication patterns to avoid between agents and agent skills, and walks through a before/after simplification example."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when simplifying an agent that duplicates content already covered by one of its agent skills.
---

# Agent-Skill Separation — Duplication Patterns and Before/After Example

## Common Duplication Patterns to Avoid

Based on agent simplification audit findings:

| Pattern                                                                   | Instead Use                                   | Typical Reduction |
| ------------------------------------------------------------------------- | --------------------------------------------- | ----------------- |
| Content quality standards (active voice, headings, accessibility)         | `docs-applying-content-quality` Skill         | ~50-100 lines     |
| Diagram color palette (Blue #0173B2, Orange #DE8F05...)                   | `docs-creating-accessible-diagrams` Skill     | ~60-70 lines      |
| Report generation mechanics (UUID, progressive writing, filename pattern) | Temporary Files Convention                    | ~200 lines        |
| Validation methodology (source prioritization, confidence levels)         | `docs-validating-factual-accuracy` Skill      | ~150 lines        |
| Confidence assessment (HIGH/MEDIUM/FALSE_POSITIVE criteria)               | Fixer Confidence Levels Convention            | ~200 lines        |
| Criticality levels (CRITICAL/HIGH/MEDIUM/LOW definitions)                 | `repo-assessing-criticality-confidence` Skill | ~100 lines        |
| Mathematical notation rules (LaTeX delimiters, display math)              | Mathematical Notation Convention              | ~30 lines         |
| Maker-checker-fixer workflow (three-stage pattern)                        | `repo-applying-maker-checker-fixer` Skill     | ~50 lines         |

## Example: Before and After Simplification

**Before (docs-checker - 1,318 lines)**:

Agent contained full text of:

- Content quality standards (80 lines)
- Diagram color palette with all hex codes (60 lines)
- Report generation mechanics with UUID logic (200 lines)
- Factual validation methodology (150 lines)
- Criticality level definitions (100 lines)
- Mathematical notation validation rules (30 lines)
- Various validation examples (300+ lines)

**After (docs-checker - 515 lines, 60.9% reduction)**:

Agent contains:

- Task-specific validation workflow (what to check)
- Brief Skill references with context
- Links to Conventions for specifications
- Domain-specific examples (concise)
- All task-specific decision logic

**Result**: Agent remains fully functional, easier to maintain, zero knowledge loss (agent skills/Conventions provide depth).
