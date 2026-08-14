---
title: "Background"
description: The incident that motivated the Git Identity From Global Config Convention — a silent per-repo identity override that went undetected for days.
category: explanation
subcategory: development
tags:
  - git
  - identity
  - commits
  - security
  - reproducibility
created: 2026-05-19
when_to_use: Use when explaining why a per-repo `[user]` override is treated as a structural risk rather than a one-off mistake.
---

# Background

At one point a `[user]` block was added to a subrepo's `.git/config`, setting the local
`user.name` and `user.email` to values different from the developer's global identity.
Because git resolves local config before global config, every subsequent commit in that
repository was attributed to the override identity — not the developer's real identity.
The problem went undetected across several days and hundreds of commits before anyone
noticed. History had to be rewritten to correct the attribution.

This incident illustrates a structural risk: the override mechanism is silent, requires no
confirmation, and persists until explicitly removed. The only reliable defense is a
pre-commit guard that prevents commits entirely when an override is present.
