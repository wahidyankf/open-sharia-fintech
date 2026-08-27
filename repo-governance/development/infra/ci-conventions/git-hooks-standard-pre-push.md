---
title: "Git Hooks Standard — Pre-Push"
description: The registry-driven pre-push hook and its live gate set.
category: explanation
subcategory: development
tags: [ci-cd, git-hooks]
created: 2026-03-31
when_to_use: Use when debugging or speeding up the pre-push hook.
---

# Git Hooks Standard — Pre-Push

## pre-push

The pre-push hook delegates entirely to
`apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`, which executes every
registry-declared `pre-push`-surface gate in declaration order, failing fast. It is **not** a
fixed `typecheck`/`lint`/`test:quick`/`specs:coverage` invocation — `specs:coverage` was renamed
to `specs:behavior:coverage` and, per DD-7, coverage validation was lifted out of the local
pre-push chain entirely so pre-push stays fast (it runs on CI instead; see
[Nx Target Standards](../nx-targets.md)). Discover the live, current gate set rather than trusting
a hardcoded list:

```bash
apps/rhino-cli/scripts/rhino-bin.sh gate list --surface=pre-push --format=text
```

See [Git Hook Lifecycle](../../workflow/git-hook-lifecycle.md) for the shared discovery/conformance
workflow (`gate list`, `gate validate`) across all three Husky surfaces.

If the pre-push hook times out, warm the Nx cache first — see
[`.claude/hooks/warm-cache-before-push.sh`](../../../../.claude/hooks/warm-cache-before-push.sh),
which derives its warm-target list from the same `gate list --surface=pre-push` registry
projection rather than a hardcoded target list — then push again; cached results make the second
run fast.

Registry entries carry their own scope and triggers, so a missed trigger is a declared
`not-applicable` result rather than an implicit pass. PR CI evaluates the `ci` projection against
the PR's actual changed paths and records evidence for that exact repository, head, and base. It
does not run every pre-push predicate unconditionally, and evidence from an earlier head is stale.
