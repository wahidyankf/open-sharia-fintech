---
title: "Platform Binding Examples — Research Agent Note"
description: "Gives the special note for how research agents fit the color categorization system."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when handling a research agent's color assignment.
---

# Platform Binding Examples — Research Agent Note

**NOTE**: `web-researcher` is a research agent that carries the `researcher` role suffix and `color: green`. The `researcher` role maps to green because research is validation-adjacent.

**Why green (not blue)?**

1. **Primary role**: External web research and fact verification — gathering and validating external information
2. **Validation-adjacent**: The agent verifies claims, checks current facts, and returns cited findings — fundamentally a validation workflow
3. **Not content creation**: The agent does not create repository content, it verifies information for other agents
4. **Role and color agree**: The dedicated `researcher` role makes the green color consistent — there is no longer a `-maker`/green mismatch to reconcile

This pairing is intentionally documented here to prevent future confusion and maintain consistent governance.
