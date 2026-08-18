---
title: "For AI Agents"
description: Five agent-specific obligations for simplicity, including avoiding premature abstraction.
category: explanation
subcategory: principles
tags:
  - principles
  - simplicity
  - over-engineering
created: 2025-12-15
when_to_use: Use when auditing agent behavior against this principle.
---

# For AI Agents

All agents must follow this principle by:

1. **Only implementing what was requested** - no speculative features
2. **Avoiding premature abstractions** - inline first, extract when needed
3. **Trusting type systems and frameworks** - no defensive code for guaranteed scenarios
4. **Applying the senior engineer test** - questioning complexity proactively
5. **Preferring boring solutions** - battle-tested patterns over clever code

See the "Principles Implemented/Respected" section in [AI Agents Convention](../../../development/agents/ai-agents/principles-implemented-respected.md#principles-implementedrespected) for how agents apply this principle.
