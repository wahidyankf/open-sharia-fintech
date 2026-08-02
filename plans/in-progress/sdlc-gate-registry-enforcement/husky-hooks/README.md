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

Twenty-four files: the twelve hooks as they will be, and — in [`current/`](./current/) — the twelve
they replace, captured verbatim. Both sides are complete files, so the replacement is reviewable in
full rather than described.

A husky v9 hook is a plain script with no framework preamble, so each `.sh` here **is** the entire
file, not an excerpt. That is worth stating because the after-state is only 13 lines and could
otherwise read as a fragment.

| Hook         | After (lines) | Before (lines, `ose-public`) | Replaces                                                       |
| ------------ | ------------- | ---------------------------- | -------------------------------------------------------------- |
| `commit-msg` | 9             | 1                            | A one-line `commitlint` call                                   |
| `pre-commit` | 13            | 29                           | Four hand-ordered steps plus an inline lockfile loop           |
| `pre-push`   | 13            | 39                           | Seven repo-wide commands plus a hand-written path-gating block |

Copy each top-level `.sh` to `.husky/<hook>` in its repo, dropping the `.sh` extension. The extension
exists only so these files are covered by `shellcheck --severity=warning` while they live in the plan
folder — both the before and after sets pass it today, which is a cheap check that the shipped hooks
will too.

## What `current/` is for

`[Repo-grounded]` Captured 2026-08-02 from each repo's live `.husky/`. Two uses:

1. **Phase 0 reconciliation.** Before overwriting, diff `current/<hook>-<repo>.sh` against the live
   file. A non-empty diff means someone else changed that hook after 2026-08-02 — reconcile it rather
   than overwriting, exactly as [`repo-configs/`](../repo-configs/README.md) requires for the
   registry.
2. **Evidence for the central claim.** The plan asserts the four repos' hooks have silently diverged.
   `current/` is that assertion made checkable rather than asserted.

### Measured divergence before the plan

`[Repo-grounded]` Each cell is `diff` against `ose-public`'s copy of the same hook:

| Hook         | `ose-primer`       | `ose-private`       | `beaver-nest`      |
| ------------ | ------------------ | ------------------- | ------------------ |
| `commit-msg` | identical          | identical           | identical          |
| `pre-commit` | identical          | 27 lines differ     | identical          |
| `pre-push`   | **4 lines differ** | **56 lines differ** | **2 lines differ** |

`pre-push` is the drift surface: it differs in **all three** downstream repos, and nothing detects
that today. `ose-private`'s larger delta is partly legitimate (it carries an `iac-lint` pair the
others lack) and partly drift — the plan does not assume which, it moves every one of those lines
into `repo-config.yml` where the difference becomes declared data instead of divergent shell.

Reproduce:

```sh
cd current
for h in commit-msg pre-commit pre-push; do
  for r in ose-primer ose-private beaver-nest; do
    diff -q "$h-ose-public.sh" "$h-$r.sh" >/dev/null \
      && echo "$h/$r: identical" || echo "$h/$r: differs"
  done
done
```

## The whole point: they are identical across all four repos

Open any two and diff them. They are byte-identical, because **every per-repo difference now lives in
`repo-config.yml`** rather than in shell. That is the structural claim this plan makes, made
inspectable: if these twelve files are not four identical triples, something is still hand-wired that
should be declared.

```sh
# Run from this folder. Should print nothing.
for h in commit-msg pre-commit pre-push; do
  for r in ose-primer ose-private beaver-nest; do
    diff "$h-ose-public.sh" "$h-$r.sh"
  done
done
```

Run the same loop inside [`current/`](./current/) and it prints plenty — that contrast is the whole
argument for the change.

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

That excerpt is elided for readability only — the block in full, with all six regexes, is in
[`current/pre-push-ose-public.sh`](./current/pre-push-ose-public.sh), and the three downstream repos'
copies sit beside it.

Every one of those triggers becomes a `trigger:` list on a `scope: path-gated` gate, and `gate run`
computes the changed set itself. This is the single largest source of surface drift the audit found,
because a maintainer adding a validator had to remember to add a matching regex here — in four repos.
The divergence table above is what that costs: `pre-push` differs in all three downstream repos.

## What deliberately does not change

`pre-commit` still delegates per-file work to `npx lint-staged`. `gate run --surface=pre-commit` does
not reimplement file-type dispatch; it invokes `lint-staged`, whose block is itself generated from the
registry. That preserves `lint-staged`'s stash-and-restore behaviour, which a bespoke dispatcher would
have to re-earn — see [tech-docs §2.2.2](../tech-docs.md#222-lint-staged-is-generated-not-replaced).

## Related

- [repo-configs/](../repo-configs/README.md) — where every check these shims run is declared
- [package-json/](../package-json/README.md) — the generated `lint-staged` block `pre-commit` delegates to
