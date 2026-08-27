---
title: "Git Hooks Standard — Pre-Commit and Commit-msg"
description: Pre-commit gate steps and the commit-msg format.
category: explanation
subcategory: development
tags: [ci-cd, git-hooks]
created: 2026-03-31
when_to_use: Use when debugging the pre-commit hook or commit format.
---

# Git Hooks Standard — Pre-Commit and Commit-msg

All developer machines run three Husky hooks. Hook logic is implemented via `rhino-cli` subcommands
to keep the raw hook files thin and testable.

## pre-commit

The pre-commit hook delegates entirely to
`rtk apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-commit`. `repo-config.yml:gates` is
the live inventory, including ordering, scope, blocking behavior, mutations, and restaging. Query
that registry instead of maintaining a second list here:

```bash
rtk apps/rhino-cli/scripts/rhino-bin.sh gate list --surface=pre-commit --format=text
```

Use `rtk apps/rhino-cli/scripts/rhino-bin.sh gate validate` to check that the hook and registry
remain conformant. Language formatter and file-selection details belong to the corresponding
registry entries and project targets, not this overview.

## commit-msg

The commit-msg hook runs `commitlint` to enforce the [Conventional Commits](https://www.conventionalcommits.org/) format.

**Required format**: `<type>(<scope>): <description>`

Valid types: `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`,
`style`, `test`.

The scope is optional but recommended. The description must use imperative mood and must not end
with a period.
