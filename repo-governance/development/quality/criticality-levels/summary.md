---
title: "Summary"
description: "Summary of the criticality-level convention."
category: explanation
subcategory: development
tags:
  - criticality
  - validation
  - checker-agents
  - fixer-agents
  - quality-assurance
created: 2025-12-27
when_to_use: "Use for a one-paragraph summary of this convention."
---

# Summary

This convention establishes **universal criticality levels** (CRITICAL/HIGH/MEDIUM/LOW) for all checker agents, working orthogonally with existing **confidence levels** (HIGH/MEDIUM/FALSE_POSITIVE).

**Key Takeaways**:

1. **Four criticality levels** provide clear prioritization without overwhelming users
2. **Orthogonal with confidence** - criticality measures importance, confidence measures certainty
3. **Standardized reports** with emoji indicators and consistent section structure
4. **Priority-based execution** enables automated fixing for HIGH confidence + CRITICAL/HIGH criticality
5. **Dual labels preserved** for verification/status agents (both dimensions provide value)
6. **Progressive writing mandatory** for all checker agents (survives context compaction)
7. **Backward compatible** - fixers handle both old and new report formats

**For Checker Agents**: Categorize findings using the decision tree, generate standardized reports with criticality sections.

**For Fixer Agents**: Process findings in priority order (P0 → P1 → P2 → P3), auto-fix HIGH confidence, flag MEDIUM confidence for review.

**For Users**: Quickly identify what must be fixed (CRITICAL), what should be fixed (HIGH), and what's optional (MEDIUM/LOW).

---

**Convention Status**: Active

**Version**: 1.0
