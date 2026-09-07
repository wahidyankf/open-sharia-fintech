---
title: "Migration Path"
description: "How agents migrate to the criticality-level system."
category: explanation
subcategory: development
tags:
  - criticality
  - validation
  - checker-agents
  - fixer-agents
  - quality-assurance
created: 2025-12-27
when_to_use: "Use when migrating an agent to this system."
---

# Migration Path

Existing agents using different terminology should migrate to this convention.

## Phase 1: Documentation (Week 1)

1. Create this convention document
2. Update [Fixer Confidence Levels Convention](.././fixer-confidence-levels.md) with criticality integration
3. Update [Maker-Checker-Fixer Pattern Convention](../../pattern/maker-checker-fixer.md) with criticality flow
4. Update AGENTS.md with brief summary and link

## Phase 2: Pilot Agent (Week 2)

1. Update `rules-checker` to use CRITICAL/HIGH/MEDIUM/LOW sections
2. Test report generation with standardized format
3. Validate that `repo-workflow-fixer` correctly interprets new format
4. Identify any issues before broader rollout

## Phase 3: Checker Agent Families (Week 2-3)

**Severity-Based Family**:

- apps-ayokoding-www-general-checker
- apps-ayokoding-www-by-example-checker
- apps-ayokoding-www-in-the-field-checker
- apps-ose-www-content-checker
- repo-workflow-checker

**Dual-Label Family** (preserve existing labels + add criticality):

- docs-checker ([Verified]/[Error]/[Outdated] + CRITICAL/HIGH/MEDIUM/LOW)
- docs-tutorial-checker
- docs-software-engineering-separation-checker
- apps-ayokoding-www-facts-checker
- apps-ayokoding-www-link-checker
- docs-link-checker ([OK]/[BROKEN]/[REDIRECT] + CRITICAL/HIGH/MEDIUM/LOW)
- rules-checker

**Plan/Priority Family**:

- plan-checker
- plan-execution-checker
- readme-checker

## Phase 4: Fixer Agents (Week 3)

Update all fixer agents to use priority-based execution:

- repo-workflow-fixer (pilot)
- apps-ayokoding-www-general-fixer
- apps-ayokoding-www-by-example-fixer
- apps-ayokoding-www-facts-fixer
- apps-ayokoding-www-in-the-field-fixer
- apps-ayokoding-www-link-fixer
- docs-tutorial-fixer
- docs-software-engineering-separation-fixer
- apps-ose-www-content-fixer
- readme-fixer
- docs-fixer
- docs-fixer
- repo-workflow-fixer

## Phase 5: Validation (Week 4)

1. Run full repository audit with all checkers
2. Test all fixers on new report formats
3. Verify priority-based execution works correctly
4. Confirm backward compatibility with old reports

---
