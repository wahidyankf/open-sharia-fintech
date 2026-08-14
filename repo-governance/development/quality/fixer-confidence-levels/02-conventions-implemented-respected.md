---
title: "Conventions Implemented/Respected"
description: "Conventions this convention implements."
category: explanation
subcategory: development
tags:
  - fixer-agents
  - confidence-levels
  - validation
  - automation
  - quality-assurance
created: 2025-12-14
when_to_use: "Use to trace this convention's cross-references."
---

# Conventions Implemented/Respected

**REQUIRED SECTION**: All development practice documents MUST include this section to ensure traceability from practices to documentation standards.

This practice implements/respects the following conventions:

- **[Criticality Levels Convention](.././criticality-levels.md)**: Confidence levels work orthogonally with criticality levels to determine fix priority. Criticality measures importance/urgency, confidence measures certainty/fixability.

- **[Repository Validation Methodology Convention](.././repository-validation.md)**: Fixer agents use the same standard validation patterns (frontmatter extraction, field checks, link validation) for re-validation that checker agents use for initial detection.

- **[Temporary Files Convention](../../infra/temporary-files.md)**: Fix reports are written to generated-reports/ directory using pattern {agent-family}**{timestamp}**fix.md, following the same storage and naming conventions as audit reports.

- **[Timestamp Format Convention](../../../conventions/formatting/timestamp.md)**: Fix report filenames use UTC+7 timestamps in format YYYY-MM-DD--HH-MM (hyphen-separated for filesystem compatibility).
