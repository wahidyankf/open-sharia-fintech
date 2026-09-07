---
description: PASS and FAIL examples of git identity configuration — a clean global identity, a per-repo override violation, and a compliant multi-identity includeIf setup.
when_to_use: Use when verifying whether a specific `.git/config` and `~/.gitconfig` combination passes or fails this convention.
---

# Examples

## PASS: Correctly configured global identity

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

## FAIL: Per-repo override present

```ini
# ose-public/.git/config — VIOLATION: [user] section present
[core]
    repositoryformatversion = 0
[user]
    name  = Test
    email = t@test.com
```

Manual detection (no automated hook currently catches this for human developers — see
[Standard 3](./standards.md#standard-3-enforcement-is-a-behavioural-guardrail-not-a-pre-commit-script)):

```bash
git config --local --list | grep "^user\."
# user.name=Test
# user.email=t@test.com
```

An AI agent encountering this state MUST NOT modify it under any of the forbidden actions in
[Reproducible Environments Convention §Git Identity Guardrail](../reproducible-environments/git-identity-guardrail.md#git-identity-guardrail)
— removal is a human-only fix, applied via the commands in
[Remediation](./remediation-and-sibling-repos.md#remediation).

## PASS: Per-directory identity via `includeIf` (multi-identity workflow)

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
