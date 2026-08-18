---
title: "For AI Agents"
description: States the five agent-specific obligations for deliberate problem-solving, including verification tools and stating limitations.
category: explanation
subcategory: principles
tags:
  - problem-solving
  - clarity
created: 2026-01-29
when_to_use: Use when defining or auditing how an AI agent must apply deliberate problem-solving in its own behavior.
---

# For AI Agents

All agents must follow this principle by:

1. **Using verification tools** (Read, Grep, Glob, WebSearch, WebFetch) to validate assumptions
2. **Presenting options** when multiple valid approaches exist
3. **Asking questions** using AskUserQuestion tool when uncertain
4. **Stating limitations** explicitly when information cannot be verified
5. **Advocating simplicity** and pushing back on unnecessary complexity

See [Information Accuracy and Verification section in AI Agents Convention](../../../development/agents/ai-agents/information-accuracy-verification-principles.md) for agent-specific verification requirements.
