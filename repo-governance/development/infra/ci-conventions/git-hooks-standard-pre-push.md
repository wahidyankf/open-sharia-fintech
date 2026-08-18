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

The registry set includes path-gated entries (e.g. `governance-word-budget` and
`governance-readme-completeness` fire only when a governance surface such as `repo-governance/`,
`.claude/`, or `repo-config.yml` changed) that carry their own trigger lists and are skipped when
their triggers miss, so no-op pushes pay near-zero cost. The CI quality-gate workflow runs the
equivalent checks unconditionally on every PR against `main` to catch drift from hand-edited files
that bypassed the local hook.
