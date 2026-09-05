---
title: "Summary of Anti-Patterns"
description: "Summarizes all eleven anti-patterns in one table for quick reference."
category: explanation
subcategory: development
tags:
  - ai-agents
  - anti-patterns
  - development
  - best-practices
created: 2025-11-23
when_to_use: Use when you need a quick-reference list of every anti-pattern instead of reading each section.
---

# Summary of Anti-Patterns

| Anti-Pattern                   | Problem                                       | Solution                                                |
| ------------------------------ | --------------------------------------------- | ------------------------------------------------------- |
| **God Agent**                  | Too many responsibilities                     | Decompose into focused agents                           |
| **Excessive Tool Permissions** | Requesting unused tools                       | Request only necessary tools                            |
| **Vague Descriptions**         | Unclear purpose                               | Clear, actionable descriptions                          |
| **Hardcoded Paths**            | Breaks in different environments              | Use relative paths                                      |
| **No Error Handling Guidance** | Unclear error behaviour                       | Document error handling                                 |
| **Missing Tool Usage Docs**    | Unclear how tools are used                    | Document tool usage                                     |
| **Wrong Model Selection**      | Cost/performance mismatch                     | Match model to task complexity                          |
| **No Testing**                 | Production issues                             | Test edge cases before deployment                       |
| **Generic Names**              | Hard to discover and categorize               | Use descriptive, categorized names                      |
| **Enumeration-Based Guards**   | Denylist guard fails open on any unnamed axis | Hoist an invariant to entry, stated by what it protects |
| **Presupposing Verification**  | Prompt asserts its own conclusion             | State a hypothesis; license the negative finding        |
