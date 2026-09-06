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
block. Only the block's presence is checked: whether its argument is a good one is a judgement no
validator can make, but its absence is not — an agent nobody argued a grade for is how the grade
stops meaning anything.

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
