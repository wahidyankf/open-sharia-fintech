---
title: "Information Accuracy and Verification — Verification Checklist for Agents"
description: "Gives the verification checklist an agent should run through before reporting work as complete."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use as a final checklist before an agent reports a task complete.
---

# Information Accuracy and Verification — Verification Checklist for Agents

Before providing information, verify:

- [ ] Have I read the actual files being discussed?
- [ ] Have I verified file paths exist?
- [ ] Have I checked the actual code implementation?
- [ ] Have I consulted official documentation for external libraries?
- [ ] Have I provided specific line numbers and file paths?
- [ ] Have I stated clearly what I verified vs. what I assumed?
- [ ] Have I used appropriate tools (Read, Grep, Glob, WebSearch, WebFetch)?
- [ ] Have I cited sources with URLs and access dates?
- [ ] If I cannot verify, have I stated this limitation clearly?
- [ ] Have I provided steps for the user to verify themselves?
- [ ] Am I reading files from the correct worktree (relative paths, not hardcoded main-checkout absolute paths)?
