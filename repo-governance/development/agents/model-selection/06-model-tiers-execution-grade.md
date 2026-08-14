---
title: "Model Tiers — Execution-Grade"
description: "Defines the execution-grade tier: agents that declare sonnet for structured, execution-heavy work."
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - development
  - standards
created: 2025-11-23
when_to_use: Use when deciding whether a new agent should declare the execution-grade (sonnet) model tier.
---

# Model Tiers — Execution-Grade

**When to use**: Rule-based validation, applying validated fixes from audit reports, template-driven output, and structured pattern-following tasks.

**Cognitive profile**: Strong pattern recognition, reliable rule application, structured output generation, systematic validation against defined criteria.

**Task characteristics**:

- Validating content against a defined checklist or ruleset
- Applying fixes identified by a prior audit (checker output drives fixer input)
- Generating output from templates with variable substitution
- Following a documented procedure step-by-step
- Tasks where correctness means conforming to explicit rules, not inventing solutions

**Agent examples**:

- **All checkers** -- validate content against conventions using defined rulesets and produce structured audit reports (docs-checker, docs-tutorial-checker, docs-software-engineering-separation-checker, readme-checker, specs-checker, repo-rules-checker, repo-workflow-checker, plan-checker, plan-execution-checker, swe-code-checker, swe-ui-checker, ci-checker, apps-\*-checker)
- **Most fixers** -- apply corrections from checker audit reports following documented fix procedures (docs-fixer, docs-tutorial-fixer, docs-software-engineering-separation-fixer, readme-fixer, specs-fixer, repo-rules-fixer, repo-workflow-fixer, plan-fixer, swe-ui-fixer, ci-fixer, apps-\*-fixer)
- **social-linkedin-post-maker** -- generates social media posts following a defined template and tone guidelines
- **Structured makers** -- makers with tight, well-defined skills that pin down most decisions, making them rule-following rather than open-ended creation (docs-maker, readme-maker, agent-maker, specs-maker, repo-workflow-maker, apps-ose-www-content-maker, apps-ayokoding-www-by-example-maker, apps-ayokoding-www-general-maker, apps-ayokoding-www-in-the-field-maker, repo-rules-maker)
- **swe-e2e-dev** -- writes Playwright E2E tests following a dedicated skill with defined patterns (locators, fixtures, waits); lower stakes than production code written by language developer agents

**Frontmatter**: Specify `model: sonnet` explicitly.

```yaml
---
name: docs-checker
description: Expert documentation validator...
tools: [Read, Glob, Grep, Write, Bash]
model: sonnet
color: green
---
```
