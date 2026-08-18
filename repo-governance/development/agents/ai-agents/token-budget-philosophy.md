---
title: "Token Budget Philosophy"
description: "Explains the unlimited-budget mindset for agent context usage and how compaction handles scale."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when deciding how verbose an agent's instructions or a single execution can be.
---

# Token Budget Philosophy

**CRITICAL GUIDELINE**: When invoking agents (from the platform binding directory or secondary directories) and workflows (`repo-governance/workflows/`), **do NOT think about token budget constraints**.

## Why Unlimited Budget Mindset

- **Reliable compaction mechanism**: The AI coding agent handles context management through proven compaction
- **Quality is king**: Execution thoroughness matters more than token efficiency
- **No artificial constraints**: Agents should complete their work properly, not cut corners to save tokens
- **Workflow orchestration**: Multi-step workflows naturally require more tokens - this is expected and acceptable

## What This Means in Practice

When working with agents:

- PASS: **Do**: Let agents complete comprehensive validations, generate detailed reports, iterate until quality gates pass
- PASS: **Do**: Use multi-step workflows (check-fix iterations) without worrying about token usage
- PASS: **Do**: Focus on correct, thorough execution
- FAIL: **Don't**: Skip steps to save tokens
- FAIL: **Don't**: Reduce validation scope due to token concerns
- FAIL: **Don't**: Avoid iteration loops because of token budget fears

## Compaction Handles Scale

- Large repository audits → Compaction preserves key findings
- Multi-iteration workflows → Compaction maintains essential state
- Comprehensive reports → Written to files, conversation can be compacted
- Long validation runs → Progressive writing ensures nothing is lost

**Bottom line**: Trust the compaction mechanism. Execute quality work. Token budget is effectively unlimited for agent and workflow operations.
