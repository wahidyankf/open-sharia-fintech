---
title: "Git Identity From Global Config Convention"
description: Prohibits per-repo [user] overrides in .git/config; git author identity must come exclusively from the global git config
category: explanation
subcategory: development
tags:
  - git
  - identity
  - commits
  - security
  - reproducibility
created: 2026-05-19
when_to_use: Use when a `.git/config` may contain a per-repo `[user]` override, or when managing git author identity.
---

# Git Identity From Global Config Convention

Git commit authorship must come exclusively from the developer's global git configuration
(`~/.gitconfig` or `~/.config/git/config`). No subrepo in this monorepo may contain a
`[user]` block in its `.git/config`.

## Contents

- [Principles and Conventions Implemented](./git-identity-from-global-config/principles-and-conventions-implemented.md) — Why this rule exists.
- [Standards](./git-identity-from-global-config/standards.md) — The three standards: no `[user]` section, global-config-only resolution, behavioural enforcement.
- [Examples](./git-identity-from-global-config/examples.md) — PASS and FAIL configuration examples.
- [Remediation and Sibling Repos](./git-identity-from-global-config/remediation-and-sibling-repos.md) — How to remove an existing override and verify sibling repos.

## Related Documentation

- [`AGENTS.md` — Git Identity Guardrail](../../../AGENTS.md) — Policy-level guardrail forbidding
  AI agents from setting or modifying git identity.
- [`.husky/pre-commit`](../../../.husky/pre-commit) — Husky hook for commit-time automation.
- [Code Quality Convention](../quality/code.md) — Git hooks and pre-commit automation.
- [Commit Message Convention](../workflow/commit-messages.md) — Conventional Commits format.
- [Reproducible Environments Convention](../workflow/reproducible-environments.md) — Deterministic
  development environments across machines.
- [No Machine-Specific Information in Commits](../quality/no-machine-specific-commits.md) —
  Related constraint preventing machine-specific paths and credentials from entering git history.

## Background

At one point a `[user]` block was added to a subrepo's `.git/config`, setting the local
`user.name` and `user.email` to values different from the developer's global identity.
Because git resolves local config before global config, every subsequent commit in that
repository was attributed to the override identity — not the developer's real identity.
The problem went undetected across several days and hundreds of commits before anyone
noticed. History had to be rewritten to correct the attribution.

This incident illustrates a structural risk: the override mechanism is silent, requires no
confirmation, and persists until explicitly removed. The only reliable defense is a
pre-commit guard that prevents commits entirely when an override is present.
