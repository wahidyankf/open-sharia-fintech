---
title: "Target-State Husky Hooks — SDLC Gate Registry Enforcement"
description: The post-rewire hook shims for each repo, showing that no check list survives in shell
category: explanation
subcategory: plans
tags:
  - ci-cd
  - git-hooks
  - parity
created: 2026-08-02
---

# Target-State Husky Hooks

Three shims per repo, twelve files. Each replaces a hand-maintained hook with a single
`gate run --surface=<name>` invocation.

| Hook         | Files                  | Replaces                                                       |
| ------------ | ---------------------- | -------------------------------------------------------------- |
| `commit-msg` | `commit-msg-<repo>.sh` | A one-line `commitlint` call                                   |
| `pre-commit` | `pre-commit-<repo>.sh` | Four hand-ordered steps plus an inline lockfile loop           |
| `pre-push`   | `pre-push-<repo>.sh`   | Seven repo-wide commands plus a hand-written path-gating block |

Copy each to `.husky/<hook>` in its repo, dropping the `.sh` extension. The extension exists only so
these files are covered by `shellcheck --severity=warning` while they live in the plan folder — they
pass it today, which is a cheap check that the shipped hooks will too.

## The whole point: they are identical across all four repos

Open any two and diff them. They are byte-identical, because **every per-repo difference now lives in
`repo-config.yml`** rather than in shell. That is the structural claim this plan makes, made
inspectable: if these twelve files are not four identical triples, something is still hand-wired that
should be declared.

```sh
# Should print nothing.
for h in commit-msg pre-commit pre-push; do
  for r in ose-primer ose-private beaver-nest; do
    diff "$h-ose-public.sh" "$h-$r.sh"
  done
done
```

## What disappears from `pre-push`

The current `pre-push` carries a hand-written block that computes an upstream range and greps the
changed file list against six regexes to decide which governance validators to run:

```sh
RANGE=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1 && echo '@{u}..HEAD' || echo "")
if [ -n "$RANGE" ]; then
  CHANGED=$(git diff --name-only "$RANGE" 2>/dev/null || echo "")
  if echo "$CHANGED" | grep -qE '^(\.claude/agents/|\.opencode/agents/)'; then
    ...
```

Every one of those triggers becomes a `trigger:` list on a `scope: path-gated` gate, and `gate run`
computes the changed set itself. This is the single largest source of surface drift the audit found,
because a maintainer adding a validator had to remember to add a matching regex here — in four repos.

## What deliberately does not change

`pre-commit` still delegates per-file work to `npx lint-staged`. `gate run --surface=pre-commit` does
not reimplement file-type dispatch; it invokes `lint-staged`, whose block is itself generated from the
registry. That preserves `lint-staged`'s stash-and-restore behaviour, which a bespoke dispatcher would
have to re-earn — see [tech-docs §2.2.2](../tech-docs.md#222-lint-staged-is-generated-not-replaced).

## Related

- [repo-configs/](../repo-configs/README.md) — where every check these shims run is declared
- [package-json/](../package-json/README.md) — the generated `lint-staged` block `pre-commit` delegates to
