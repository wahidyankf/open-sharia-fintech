---
description: "Principles and conventions this pattern implements."
when_to_use: "Use to trace a rule back to its principle."
---

# Principles and Conventions

## Principles Implemented/Respected

**REQUIRED SECTION**: All development practice documents MUST include this section to ensure traceability from practices back to foundational values.

This practice respects the following core principles:

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: Checker agents automatically validate content against conventions. Fixer agents apply validated fixes without manual intervention. Human effort focuses on content creation and subjective improvements, not mechanical validation.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Three clear stages (make, check, fix) instead of complex, multi-phase workflows. Each agent has single, well-defined responsibility. Separation of concerns keeps the workflow simple and predictable.

## Conventions Implemented/Respected

**REQUIRED SECTION**: All development practice documents MUST include this section to ensure traceability from practices to documentation standards.

This practice implements/respects the following conventions:

- **[Criticality Levels Convention](../../quality/criticality-levels.md)**: Checker agents categorize findings by criticality (CRITICAL/HIGH/MEDIUM/LOW) to indicate importance/urgency. Fixer agents combine criticality with confidence to determine fix priority (P0-P4).

- **[Fixer Confidence Levels Convention](../../quality/fixer-confidence-levels.md)**: Fixer agents assess confidence (HIGH/MEDIUM/FALSE_POSITIVE) for each finding. Only HIGH confidence fixes applied automatically. Criticality and confidence work orthogonally to determine priority.

- **[Temporary Files Convention](../../infra/temporary-files.md)**: All checker agents MUST write validation/audit reports to the `local-tmp/<agent-family>/` directory using pattern `{agent-family}__{uuid-chain}__{YYYY-MM-DD--HH-MM}__{type}.md`. Fixer agents write fix reports to same directory with `__fix.md` suffix. Progressive writing requirement ensures audit history survives context compaction.

- **[Timestamp Format Convention](../../../conventions/formatting/timestamp.md)**: Report filenames use UTC+7 timestamps in format `YYYY-MM-DD--HH-MM` (hyphen-separated for filesystem compatibility).

- **[Content Quality Principles](../../../conventions/writing/quality.md)**: Checker agents validate content against quality standards (active voice, heading hierarchy, alt text, WCAG compliance). Fixer agents apply quality improvements when findings have HIGH confidence.
