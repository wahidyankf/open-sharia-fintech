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
`apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-commit`, which executes these
registry-declared `pre-commit`-surface gates in declaration order:

| Step | Action                                                                                         | Failure Mode                |
| ---- | ---------------------------------------------------------------------------------------------- | --------------------------- |
| 1    | Validate `.claude/` and `.opencode/` config (YAML, tools, model, skills, semantic equivalence) | Blocks commit               |
| 2    | Validate `docker-compose` files found in staged changes                                        | Blocks commit               |
| 3    | Run `nx affected run-pre-commit` (format checks, lightweight per-project hooks)                | Warn only — does not block  |
| 4    | Stage `ayokoding-www` content files (auto-generated link data)                                 | N/A (staging step)          |
| 5    | Run lint-staged (format all staged files by language)                                          | Blocks commit               |
| 6    | Sync app `package-lock.json` files                                                             | Blocks commit if sync fails |
| 7    | Validate docs file naming convention across staged files                                       | Blocks commit               |
| 8    | Validate markdown links in staged files                                                        | Blocks commit               |
| 9    | Lint all markdown files (`markdownlint-cli2`)                                                  | Blocks commit               |

**Lint-staged language formatters (step 5)**:

| Language / File Type                              | Formatter       |
| ------------------------------------------------- | --------------- |
| JavaScript, TypeScript, JSON, YAML, CSS, Markdown | Prettier        |
| Rust                                              | `rustfmt`       |
| F# / C#                                           | `dotnet format` |

## commit-msg

The commit-msg hook runs `commitlint` to enforce the [Conventional Commits](https://www.conventionalcommits.org/) format.

**Required format**: `<type>(<scope>): <description>`

Valid types: `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`,
`style`, `test`.

The scope is optional but recommended. The description must use imperative mood and must not end
with a period.
