# `nx affected` lets one worktree's dirty WIP block another push entirely

One-line summary: `nx affected -t test:quick` includes **uncommitted working-directory changes**, so
a concurrent plan's unrelated, mid-edit uncommitted test file selected 25 projects and failed —
blocking an entirely unrelated, docs-only push until a `--no-verify` exception was granted; confirmed
by reproducing the same 25-project selection with **zero committed diff** in the tree.

> Surfaced 2026-07-30 while pushing the `ayokoding-www-ai-benchmark-merged-chart` plan docs to
> `origin/main`. Routed as its own brief per Knowledge Capture routing (CI/tooling-homed, not a
> plan-docs fix) — filed directly rather than fixed inline, per explicit user instruction during
> that session ("put 3 to ideas").

## Problem / context

The pre-push hook run `npx nx affected -t test:quick --parallel=$N` reported:

```text
NX   Affected criteria defaulted to --base=origin/main --head=HEAD
NX   Running target test:quick for 25 projects and 11 tasks they depend on:
- ayokoding-www
- ayokoding-www-fe-e2e
- organiclever-contracts
... (22 more)
```

for a commit whose entire diff was 11 files under `plans/in-progress/ayokoding-www-ai-benchmark-merged-chart/`
— a path `.nxignore` already excludes (`.nxignore` line 3: `plans/`). That run then failed:

```text
FAIL  unit-fe  test/unit/fe-steps/course-rehome-redirects.steps.tsx (30 tests | 2 failed)
  × Given the thirty-seven shipped topics ... expected 53 to be 37
  × And every named prerequisite resolves to another course ... unresolved: 9 pairs
```

`course-rehome-redirects.steps.tsx` and its paired `.feature` file are **uncommitted, mid-edit** work
belonging to a concurrent sibling plan (`ayokoding-learning-path-04-course-authoring`), sitting
directly in the primary checkout's working tree (not inside that plan's own
`worktrees/ayokoding-course-*` worktrees) — modified but not committed at the time of this push.
Nothing in the plan-docs commit touched `apps/ayokoding-www` at all.

**This blocked a push that could not possibly have caused the failure.** The only path forward that
didn't touch the sibling's uncommitted files or wait indefinitely was an explicit,
user-authorized `git push --no-verify` — a one-time, hand-approved exception, not a repeatable fix.

**Confirmed after the push landed**: with `origin/main` fast-forwarded to the exact plan-docs commit
(so `--base=origin/main --head=HEAD` is a zero-commit diff), re-running `nx show projects --affected`
with no explicit flags reproduced the **identical 25-project list** — while the tree still had the
sibling's two files dirty. Zero committed diff, same 25 projects selected: this isolates the cause to
`nx affected`'s inclusion of uncommitted working-directory changes, not `.nxignore` failing to cover
`plans/`.

## Why now

The repo's own concurrency model (`repo-governance/development/agents/agent-workflow-orchestration.md`
"Same-machine assumption") explicitly expects multiple agents/plans to run concurrently against the
same shared working tree, and the `worktree-to-pr` delivery mode exists specifically so one plan's
in-flight work doesn't block another's. This incident shows a gap in that isolation: a plan's
uncommitted WIP — sitting in the **primary** checkout rather than its own worktree — was able to fail
an unrelated push's pre-push gate. Whether that gap is "WIP that shouldn't be in the primary tree at
all" or "`nx affected` scoping too broadly" (or both) is exactly what promotion needs to resolve.

## Prior art / precedents

- **`.nxignore`** (repo root) already lists `plans/`, `docs/`, `*.md` as ignored — confirmed not the
  culprit here (the reproduction isolated the cause to uncommitted working-directory state, not a
  `.nxignore` gap), but worth re-checking once a fix is scoped, in case a second contributing factor
  exists.
  [`.nxignore`](../../../.nxignore)
- **Same-machine assumption / DAG-first orchestration** — the standing convention that concurrent
  agents/plans share disk, git objects, and worktrees safely; this is the convention this incident
  stress-tested and found a gap in.
  [agent-workflow-orchestration](../../../repo-governance/development/agents/agent-workflow-orchestration.md)
- **CI Blocker Resolution practice** — root-cause the blocker rather than bypass it; the `--no-verify`
  taken here was an explicit, one-time, user-approved exception specifically because the standing
  practice reserves bypass for exactly this kind of provably-unrelated, hand-approved case.
  [ci-blocker-resolution](../../../repo-governance/development/quality/ci-blocker-resolution.md)
- **`ci-setup-rust-toolchain-retry` two-pager** — a structurally similar prior incident (a markdown-only
  changeset gated by an unrelated, non-deterministic CI failure); same class of "unrelated failure
  blocks an innocent push," different layer (CI infra vs. local pre-push + Nx affected).
  [ci-setup-rust-toolchain-retry](./ci-setup-rust-toolchain-retry.md)

## Proposed direction (sketch)

Two independent angles, likely both needed:

- **Nx-affected angle**: the pre-push hook's `nx affected -t test:quick` should reflect what a push
  actually changes (the committed diff against the merge-base), not the pusher's incidental
  working-directory dirt from unrelated concurrent work. At promotion, evaluate pinning the hook's
  invocation to a committed-only diff (e.g. an explicit `--files` list from `git diff --name-only
<merge-base>..HEAD`, or whichever documented Nx flag excludes working-directory state) so a clean
  commit's push is judged on its own diff.
- **Worktree-hygiene angle**: whatever process modified `course-rehome-redirects.steps.tsx` in the
  primary checkout instead of inside the sibling plan's own `worktrees/ayokoding-course-*` directory
  should not have been able to leave WIP there — reinforcing (or tooling-enforcing) the
  one-worktree-per-independent-unit rule this repo already documents.

## Rough scope & non-goals

In scope: scoping the pre-push hook's `nx affected` invocation to the actual committed diff being
pushed, rather than the pusher's ambient working-directory state; a decision on whether
primary-checkout WIP from a worktree-based plan is itself the bug to fix (vs. `nx affected` scoping
alone, vs. both).

Out of scope: any change to the pre-push hook's actual test/lint/validator set; touching the specific
sibling plan's in-progress content-authoring work (that plan owns its own timeline); building new
tooling to auto-detect or auto-clean stray primary-tree WIP (a heavier fix than this brief's scope).

## Risks & open questions

- **Which exact Nx mechanism/flag governs this.** Confirmed _that_ uncommitted changes are included
  when no explicit `--head`/`--files` is passed to the pre-push hook's invocation; not yet confirmed
  _which_ documented Nx option (or absence of one) is the cleanest lever to pin the hook to a
  committed-only diff without breaking `nx affected`'s normal local-dev ergonomics (where including
  dirty state is often exactly what a developer wants). (open)
- Whether scoping the pre-push hook to a committed-only diff could mask a **real** case where locally
  uncommitted changes should legitimately gate the push (e.g. a developer who forgot to commit a
  source file their own change depends on) — the fix needs to distinguish "my own WIP" from "someone
  else's stray WIP in a shared tree" if it's going to be safe to adopt. (open)
- Whether the stray sibling-plan WIP in the primary tree is itself a one-off (a slip) or a recurring
  pattern — if recurring, the worktree-hygiene angle is the higher-leverage fix of the two. (open)

## What success looks like + promotion signal

Success: a docs-only (or otherwise `.nxignore`d-only) commit reliably resolves to zero affected
projects under `nx affected`, and/or concurrent plans' uncommitted WIP can no longer surface in the
primary checkout in a way that blocks unrelated pushes. Ready to promote once the root-cause
reproduction above is done and points at a concrete, scoped fix (Nx config, hook change, or worktree
tooling) rather than a hypothesis.
