---
title: "How It Applies — Workflow Documentation"
description: Requirements for documenting multi-step workflows.
category: explanation
subcategory: principles
tags:
  - principles
  - documentation
created: 2025-12-28
when_to_use: Use when documenting a deployment, validation, or content workflow.
---

# How It Applies — Workflow Documentation

**Context**: All multi-step processes (deployment, validation, content creation).

**Requirements**:

PASS: **Every workflow** is documented with:

- **Purpose**: What the workflow achieves
- **Steps**: Exact sequence of actions
- **Tools**: What tools or agents are involved
- **Inputs**: What information is required
- **Outputs**: What is produced
- **Error handling**: What to do when things fail

FAIL: **Anti-pattern**: "Just run these commands in order (which order? what do they do?)"

**Example**: See [Maker-Checker-Fixer Pattern](../../../development/pattern/maker-checker-fixer.md):

- Explains the three-stage pattern clearly
- Lists exact agents involved in each stage
- Describes inputs and outputs
- Provides execution examples

**Why this works**: Anyone can execute the workflow correctly without tribal knowledge or guessing.
