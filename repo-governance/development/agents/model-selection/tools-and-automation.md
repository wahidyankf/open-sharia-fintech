---
title: "Tools and Automation"
description: "Lists the gate and the agents that check model-tier compliance, and why the gate fails closed without a grade vocabulary."
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - development
  - standards
created: 2025-11-23
when_to_use: Use when looking for what validates an agent's model-tier declaration, or what the gate does without a registry.
---

# Tools and Automation

## The gate

`harness-claude` (`harness claude validate`) is the registered gate. Per agent it checks that the
declared `model` is in the grade vocabulary or a pinned `claude-*` ID, that the declared `effort`
matches the effort its grade declares, and that the body carries a **Model Selection Justification**
block whose first named grade is the one the frontmatter declares.

Whether the argument is a _good_ one is a judgement no validator can make. That it exists, and that
it argues for the grade actually declared, both are. The second check exists because a promotion
that edits frontmatter and leaves prose behind produces a file arguing against its own
configuration, and stale prose reads as a standing case for undoing the change. It compares only
backticked grade names, and only the first one in the block, so a later sentence contrasting with
another grade stays legal — which also means prose naming a grade without backticks is invisible to
it. The gate is a floor, not a substitute for reading.

Both the vocabulary and the effort pairing come from `repo-config.yml` — the `claude-code` entry's
`model-map:` and the top-level `model-grades:` block — never from the validator's own source. If
that registry supplies no vocabulary, the gate **fails closed** rather than passing every model:
a check that returns nothing because it was pointed at the wrong thing reads identically to a check
that returns nothing because the rule is being followed.

## The agents

The following agents enforce or assist with model selection:

- **agent-maker** -- applies these guidelines when creating new agents
- **rules-checker** -- judges whether a justification block's argument actually fits the agent's charter; the block's presence is already gated by `harness-claude`
- **rules-fixer** -- corrects model selection issues identified by the checker
