---
title: "Agent Naming Convention — Applies To and Enforcement"
description: Which directories this convention governs and the audit command repo-rules-checker runs to enforce it.
when_to_use: Use when you need to know which agent directories this convention governs, or how conformance is audited.
category: explanation
subcategory: conventions
tags:
  - agents
  - naming
  - conventions
created: 2026-04-17
---

# Applies To and Enforcement

## Applies To

This convention applies to both:

- **`.claude/agents/*.md`** — Source of truth. All agent definitions authored here.
- **`.opencode/agents/*.md`** — Generated mirror. Produced by the sync pipeline from `.claude/agents/`.

Filenames MUST be identical pair-for-pair between the two directories. Every `.claude/agents/<name>.md` has exactly one corresponding `.opencode/agents/<name>.md`, and vice versa. Any asymmetry (orphan file in either tree, rename in one tree but not the other) is a governance violation.

## Enforcement

`repo-rules-checker` MUST run the following audit command as part of every governance pass:

```bash
find .claude/agents -name '*.md' ! -name README.md \
  | sed 's|.*/||; s|\.md$||' \
  | grep -vE -- '-(maker|checker|fixer|dev|deployer|manager|tester|researcher)$' \
  | grep -v '^README$'
```

Any non-empty output is a governance violation. Every line printed is an agent filename whose suffix does not match the Role Vocabulary; each such file MUST be renamed to a compliant name before the checker can pass. The same command SHOULD be run against `.opencode/agents/*.md` to detect mirror drift.
