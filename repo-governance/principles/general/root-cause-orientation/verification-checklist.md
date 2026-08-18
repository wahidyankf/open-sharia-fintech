---
title: "Verification Checklist"
description: A pre-completion checklist for confirming a fix addressed the actual root cause with minimal, senior-engineer-approved scope.
category: explanation
subcategory: principles
tags:
  - principles
  - root-cause
  - minimal-impact
created: 2026-03-09
when_to_use: Use as a checklist immediately before declaring a task complete.
---

# Verification Checklist

Before declaring a task complete:

- [ ] The actual root cause has been identified, not just the symptom
- [ ] Every changed line traces directly to the problem being solved
- [ ] No unrelated code has been modified
- [ ] All edge cases related to the root cause are handled
- [ ] A senior engineer would approve the approach and the scope
- [ ] Preexisting errors encountered during this work have been fixed at root cause, not mentioned and deferred
