---
title: "Git Identity Guardrail"
description: No AI agent sets or modifies git identity at any scope; the human per-repository includeIf pattern and the CI service-account exemption.
category: explanation
subcategory: development
tags:
  - development
  - reproducibility
  - volta
  - docker
  - environment
  - dependencies
created: 2025-12-28
when_to_use: Use when an agent is about to run any git config user.* command, or when setting up per-repository git identity as a human.
---

# Git Identity Guardrail

No AI agent sets or modifies git identity at any scope. This behavioural guardrail replaces the
former `scripts/git-identity-check.sh` pre-commit script, which was removed because it
over-restricted human developers who legitimately maintain per-repository identities via
`includeIf`.

## Forbidden agent actions

All of the following are forbidden for AI agents:

- `git config --local user.name` / `git config --local user.email`
- `git config user.name` / `git config user.email` (bare form writes local scope by default)
- `git config --global user.*` (any identity key at global scope)
- `git config --system user.*` (any identity key at system scope)
- Direct edits to the `.git/config` `[user]` block

## Human rule

Developers set identity in `~/.gitconfig` (global default). For per-repository overrides, use
`includeIf`:

```gitconfig
[includeIf "gitdir:/path/to/repo/"]
  path = ~/.gitconfig-work
```

This keeps repository-specific identity local to the developer's machine without any script
intervention.

## CI exemption

CI service-account identity is configured in workflow YAML (e.g. setting `user.name` to
`github-actions[bot]` before a format-commit-back step). This is not an agent action and is the
one legitimate exemption. It is a CI platform concern, owned by the workflow YAML, not by any AI
agent.
