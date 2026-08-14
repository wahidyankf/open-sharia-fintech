---
title: "Criticality Levels Convention"
description: Universal criticality level system for categorizing validation findings across all checker and fixer agents
category: explanation
subcategory: development
tags:
  - criticality
  - validation
  - checker-agents
  - fixer-agents
  - quality-assurance
created: 2025-12-27
when_to_use: "Use when a checker or fixer agent needs to classify or report a validation finding."
---

# Criticality Levels Convention

This convention defines a universal CRITICAL/HIGH/MEDIUM/LOW criticality-level system, orthogonal to confidence levels, for categorizing validation findings across all checker and fixer agents.

## Documents

- [Overview](./criticality-levels/01-overview.md) — Overview of the criticality-level system. Use to orient to the criticality-level system.
- [Four Universal Criticality Levels: CRITICAL](./criticality-levels/02-four-universal-criticality-levels-critical.md) — The CRITICAL level definition and examples. Use when classifying a finding as CRITICAL.
- [Four Universal Criticality Levels: HIGH](./criticality-levels/03-four-universal-criticality-levels-high.md) — The HIGH level definition and examples. Use when classifying a finding as HIGH.
- [Four Universal Criticality Levels: MEDIUM](./criticality-levels/04-four-universal-criticality-levels-medium.md) — The MEDIUM level definition and examples. Use when classifying a finding as MEDIUM.
- [Four Universal Criticality Levels: LOW](./criticality-levels/05-four-universal-criticality-levels-low.md) — The LOW level definition and examples. Use when classifying a finding as LOW.
- [Decision Matrix: Priority Levels](./criticality-levels/06-criticality-confidence-decision-matrix-priority-levels.md) — The priority matrix and priority-level explanations. Use to map a criticality+confidence pair to a priority.
- [Decision Matrix: Execution Strategy for Fixers](./criticality-levels/07-criticality-confidence-decision-matrix-execution-strategy.md) — Fixer execution strategy per priority. Use for a fixer agent's execution-order rules.
- [Report Format: Header and Issue Sections](./criticality-levels/08-standardized-report-format-header-and-issue-sections.md) — The report header and issue-section template. Use when authoring a report header or issue section.
- [Report Format: Next CRITICAL Issue Example](./criticality-levels/09-standardized-report-format-next-critical-issue-example.md) — A worked example of a second issue entry. Use for a second-issue-entry report example.
- [Report Format: Dual-Label Pattern](./criticality-levels/10-standardized-report-format-dual-label-pattern.md) — The criticality + confidence dual-label pattern. Use when labeling a finding with both dimensions.
- [Examples: Repo-Governance through Documentation](./criticality-levels/11-domain-specific-examples-repo-governance-through-documentation.md) — Examples for repo-governance, ayokoding-www, ose-www, docs checkers. Use for a domain example in these checkers.
- [Examples: Plans through By-Example Tutorials](./criticality-levels/12-domain-specific-examples-plans-through-by-example-tutorials.md) — Examples for plans, README, workflows, by-example checkers. Use for a domain example in these checkers.
- [Implementation Guidelines for Checker Agents](./criticality-levels/13-implementation-guidelines-for-checker-agents.md) — Decision tree and writing pattern for checkers. Use when implementing a checker agent's logic.
- [Fixer Guidelines: Decision Logic and Execution Order](./criticality-levels/14-implementation-guidelines-for-fixer-agents-decision-logic-and-execution-order.md) — Criticality-aware decision logic and fix order. Use when implementing a fixer's fix-execution order.
- [Fixer Guidelines: Priority Function and Fix Report Format](./criticality-levels/15-implementation-guidelines-for-fixer-agents-priority-function-and-fix-report-format.md) — Priority-determination function and a fix-report example. Use for priority determination or a fix-report template.
- [Fix Report: P1-P4 Summary and Next Steps](./criticality-levels/16-fix-report-p1-p4-summary-and-next-steps.md) — P1-P4 fix summary, false positives, next steps. Use for the P1-P4 fix-report summary.
- [Principles Implemented/Respected](./criticality-levels/17-principles-implemented-respected.md) — Principles this convention implements. Use to trace this convention's principle rationale.
- [Conventions Implemented/Respected](./criticality-levels/18-conventions-implemented-respected.md) — Conventions this convention implements. Use to trace this convention's cross-references.
- [Migration Path](./criticality-levels/19-migration-path.md) — How agents migrate to the criticality-level system. Use when migrating an agent to this system.
- [Frequently Asked Questions](./criticality-levels/20-frequently-asked-questions.md) — FAQ about the criticality-level system. Use for a quick answer about this system.
- [Summary](./criticality-levels/21-summary.md) — Summary of the criticality-level convention. Use for a one-paragraph summary of this convention.
