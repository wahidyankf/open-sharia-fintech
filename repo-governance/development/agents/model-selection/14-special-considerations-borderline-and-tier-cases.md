---
title: "Special Considerations — Borderline Cases and Tier Assignments"
description: "Covers borderline tier cases and why link checkers, the social media maker, structured makers, the E2E test developer, and the file manager sit at their assigned tiers."
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - development
  - standards
created: 2025-11-23
when_to_use: Use when an agent's task profile does not cleanly match one model tier, or when checking why a specific existing agent was assigned its tier.
---

# Special Considerations — Borderline Cases and Tier Assignments

## Borderline Cases

Some agents straddle tier boundaries. When uncertain:

1. **Analyze the core loop** -- what does the agent do repeatedly? If the core loop is rule application, use execution-grade even if setup requires some reasoning.
2. **Consider the failure mode** -- if the agent picks a wrong approach, how bad is the outcome? Higher-stakes failures justify a higher tier.
3. **Start lower, promote if needed** -- begin with execution-grade; promote to planning-grade only if quality issues emerge in practice.

## Link Checkers as Fast-Tier

Link checker agents (docs-link-checker, apps-ayokoding-www-link-checker) use the fast tier despite being categorized as checkers (green). This is because their validation is purely mechanical (HTTP status code checking), not rule-based reasoning. The checker color reflects their role in the maker-checker-fixer workflow, while the model reflects their cognitive requirements.

## Social Media Maker as Execution-Grade

The social-linkedin-post-maker uses execution-grade despite being a "maker" agent. This is because LinkedIn post generation follows a rigid template and tone guide, making it a structured pattern-following task rather than creative content creation.

## Structured Makers as Execution-Grade

Several maker agents use execution-grade because their output is structured by tight skills with well-defined rubrics (docs-maker, readme-maker, agent-maker, specs-maker, repo-workflow-maker, apps-ose-www-content-maker, apps-ayokoding-www-by-example-maker, apps-ayokoding-www-general-maker, apps-ayokoding-www-in-the-field-maker, repo-rules-maker). Each has an execution-grade checker and execution-grade fixer in its maker-checker-fixer trio, and the skill pins down most decisions. Contrast with planning-grade makers (plan-maker, docs-tutorial-maker, swe-ui-maker) where the creative work is open-ended, pedagogically demanding, or multi-concern.

## E2E Test Developer as Execution-Grade

The swe-e2e-dev uses execution-grade despite the other 12 language developer agents being planning-grade. Playwright E2E tests are pattern-driven (locators, fixtures, waits) with a dedicated skill, and test code regressions surface fast in CI. Production application code written by the language developers has higher stakes and unforgiving idioms, justifying their continued planning-grade tier.

## File Manager as Fast-Tier

The docs-file-manager uses the fast tier despite being categorized as a fixer (yellow). This is because its operations are deterministic file manipulation (`git mv`, `git rm`, find-and-replace link updates) with no judgment calls. The `agent-developing-agents` skill cites it as the canonical fast-tier example.
