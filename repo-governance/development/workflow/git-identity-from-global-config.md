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
---

# Git Identity From Global Config Convention

Git commit authorship must come exclusively from the developer's global git configuration
(`~/.gitconfig` or `~/.config/git/config`). No subrepo in this monorepo may contain a
`[user]` block in its `.git/config`.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**:
  Global git config is a deliberate, visible identity declaration that applies consistently
  across all projects. A per-repo override is an implicit, local mutation that silently
  overrides the developer's stated identity without any warning at commit time.

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: Commits
  attributed to an unintended identity are a symptom of a per-repo override existing in
  `.git/config`. Removing the override at the root eliminates the class of problem entirely,
  rather than rewriting history after the fact.

- **[Reproducibility First](../../principles/software-engineering/reproducibility.md)**:
  A developer's identity must resolve consistently regardless of which subrepo they are
  working in. Implicit per-repo overrides break that consistency.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**:
  A pre-commit hook enforces the rule automatically on every commit attempt, removing any
  dependency on manual audit of `.git/config` files.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Code Quality Convention](../quality/code.md)**: Identity enforcement is implemented as a
  Husky pre-commit hook, consistent with the automated quality gate pattern used across the
  repository.

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

## Standards

### Standard 1: No `[user]` Section in Any Sibling Repo `.git/config`

The `[user]` section MUST NOT appear in `.git/config` for any repository in the
ecosystem (`ose-public`, `ose-private`, `ose-primer`).

**Violation:**

```ini
# ose-public/.git/config  ← PROHIBITED
[user]
    name  = Some Name
    email = some@email.example
```

**Compliant state:** the `[user]` section is absent from `.git/config` entirely. Git falls
through to the developer's global `~/.gitconfig`.

This rule is **identity-agnostic**: any `[user]` value is a violation, regardless of
whether the identity it encodes happens to match the developer's real identity. The
mechanism itself is disallowed, not just incorrect values.

### Standard 2: Identity Comes From Global Git Config Only

The authoritative source for `user.name` and `user.email` in all subrepos is, in resolution
order:

1. `~/.gitconfig` — the standard per-user global config.
2. `~/.config/git/config` — the XDG-compliant alternative location.
3. System-level `/etc/gitconfig` — for shared CI environments only.

Developers who need a different identity per repository (e.g., work vs. personal projects)
MUST use `includeIf` directives in their global `~/.gitconfig` rather than editing any
subrepo's `.git/config`.

**Per-directory identity via `includeIf` (compliant approach):**

```ini
# ~/.gitconfig

[user]
    name  = Your Name
    email = personal@example.com

[includeIf "gitdir:/path/to/work-projects/"]
    path = ~/.gitconfig-work
```

```ini
# ~/.gitconfig-work

[user]
    name  = Your Name
    email = work@company.example
```

Git applies `~/.gitconfig-work` automatically for any repository whose `.git/` directory
is under `/path/to/work-projects/`. No per-repo `.git/config` edit is required.

**One-off override via environment variables (compliant approach for isolated commits):**

```bash
GIT_AUTHOR_NAME="Your Name" GIT_AUTHOR_EMAIL="other@example.com" \
  GIT_COMMITTER_NAME="Your Name" GIT_COMMITTER_EMAIL="other@example.com" \
  git commit -m "chore: one-off commit under alternate identity"
```

Environment variables override config for a single invocation without touching any
`.git/config` file.

### Standard 3: Enforcement Is a Behavioral Guardrail, Not a Pre-Commit Script

`ose-public` previously enforced Standard 1 with an automated `scripts/git-identity-check.sh`
pre-commit guard. That script has been **removed** — see
[Reproducible Environments Convention §Git Identity Guardrail](./reproducible-environments.md#git-identity-guardrail)
for the removal rationale: it over-restricted human developers who legitimately maintain
per-repository identities via `includeIf`.

Enforcement today is the **Git Identity Guardrail** documented in
[Reproducible Environments Convention §Git Identity Guardrail](./reproducible-environments.md#git-identity-guardrail)
and in `AGENTS.md`: no AI agent may set or modify git identity at any scope
(`git config --local/--global/--system user.*`, or a direct `.git/config` `[user]`-block edit).
This is a behavioral rule enforced by agent instruction-following, not a Husky hook — human
developers remain free to use `includeIf` for legitimate multi-identity workflows, which is
exactly what the removed script could not distinguish from a violation.

For the current, registry-backed shape of the three Husky hook shims themselves (which no
longer include an identity-check step), see
[Git Hook Lifecycle](./git-hook-lifecycle.md).

## Examples

### PASS: Correctly configured global identity

```ini
# ~/.gitconfig — developer's global config
[user]
    name  = Developer Name
    email = developer@example.com
```

```ini
# ose-public/.git/config — no [user] section present
[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
[remote "origin"]
    url = git@github.com:org/ose-public.git
    fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
    remote = origin
    merge = refs/heads/main
```

`git log --format="%an <%ae>"` outputs the global identity. No `[user]` override exists for any
hook or agent to catch — there is nothing to detect.

### FAIL: Per-repo override present

```ini
# ose-public/.git/config — VIOLATION: [user] section present
[core]
    repositoryformatversion = 0
[user]
    name  = Test
    email = t@test.com
```

Manual detection (no automated hook currently catches this for human developers — see
Standard 3 above):

```bash
git config --local --list | grep "^user\."
# user.name=Test
# user.email=t@test.com
```

An AI agent encountering this state MUST NOT modify it under any of the forbidden actions in
[Reproducible Environments Convention §Git Identity Guardrail](./reproducible-environments.md#git-identity-guardrail)
— removal is a human-only fix, applied via the commands in Remediation below.

### PASS: Per-directory identity via `includeIf` (multi-identity workflow)

```ini
# ~/.gitconfig
[user]
    name  = Developer Name
    email = developer@personal.example

[includeIf "gitdir:~/work/"]
    path = ~/.gitconfig-work
```

```ini
# ~/.gitconfig-work
[user]
    name  = Developer Name
    email = developer@work.example
```

Commits inside `~/work/` use the work identity; commits outside use the personal identity.
Neither subrepo's `.git/config` contains a `[user]` section, so this remains fully compliant
with Standard 1.

## Remediation

If manual verification (or the AI agent Git Identity Guardrail's own read-before-commit check)
finds an existing override:

```bash
# Remove name override (if present)
git config --local --unset user.name

# Remove email override (if present)
git config --local --unset user.email

# Remove the section entirely if it is now empty
git config --local --remove-section user 2>/dev/null || true
```

Verify the section is gone:

```bash
git config --local --list | grep "^user\."
# Should produce no output
```

Then retry the commit. The global `~/.gitconfig` takes effect immediately.

## Sibling Repos

The automated `scripts/git-identity-check.sh` guard was removed in `ose-public`, not merely
never propagated to siblings — so there is no script-based mechanism left to propagate. The
behavioral Git Identity Guardrail (Standard 3 above) is a shared `AGENTS.md` guardrail and
applies identically wherever each sibling's own `AGENTS.md` copy is loaded. Human developers in
any of the three repos should periodically verify that no `[user]` section exists in that repo's
`.git/config`:

```bash
git -C /path/to/ose-private config --local --list | grep "^user\." || echo "clean"
git -C /path/to/ose-primer config --local --list | grep "^user\." || echo "clean"
```

## Related Documentation

- [`AGENTS.md` — Git Identity Guardrail](../../../AGENTS.md) — Policy-level guardrail forbidding
  AI agents from setting or modifying git identity (replaced the former shell guard script)
- [`.husky/pre-commit`](../../../.husky/pre-commit) — Husky hook for commit-time automation
- [Code Quality Convention](../quality/code.md) — Git hooks and pre-commit automation
- [Commit Message Convention](./commit-messages.md) — Conventional Commits format
- [Reproducible Environments Convention](./reproducible-environments.md) — Deterministic
  development environments across machines
- [No Machine-Specific Information in Commits](../quality/no-machine-specific-commits.md) —
  Related constraint preventing machine-specific paths and credentials from entering git history
