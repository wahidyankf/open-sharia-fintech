---
title: "Why"
description: Benefits of explicit configuration and problems with implicit configuration.
category: explanation
subcategory: principles
tags:
  - principles
  - explicit-configuration
  - transparency
  - clarity
created: 2025-12-15
when_to_use: Use when justifying why code or config should be made explicit.
---

# Why

## Benefits of Explicit Configuration

1. **Understandability**: Anyone can read the code/config and understand what happens
2. **Maintainability**: Changes don't break hidden assumptions
3. **Security**: No accidental permissions or unexpected behavior
4. **Debuggability**: Problems are easier to trace and fix
5. **Onboarding**: New team members can understand systems faster

## Problems with Implicit Configuration

1. **Hidden Behavior**: "Magic" that works until it doesn't
2. **Insider Knowledge**: Requires tribal knowledge to understand
3. **Debugging Nightmares**: Hard to trace where behavior comes from
4. **Accidental Breaking**: Changing defaults breaks everything
5. **Security Risks**: Unintended permissions or access
