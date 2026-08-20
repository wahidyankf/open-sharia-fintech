# Delivery Checklist — Harness Mirror and Test-Isolation Defects

> Delivery mode: `worktree-to-pr`. One worktree, one PR per repository. WS-H1 and WS-H2 touch the
> `rhino-cli` parity boundary, so `ose-public` and `ose-private` merge as a pair.

## Phase 0: Setup

- [ ] [AI] Create one worktree for this plan; confirm the working location is the worktree, not the
      primary checkout — acceptance: `git rev-parse --show-toplevel` ends in the plan slug.
- [ ] [AI] Sync the branch with the latest `origin/main` before implementing.
- [ ] [AI] Run `npm install` **inside the worktree** — a worktree that only runs Rust targets looks
      healthy until the first TypeScript-touching `nx affected` run.
- [ ] [AI] Create `learnings.md` with `## Baseline`, `## PR`, and per-phase headings.
- [ ] [AI] Record the three baselines this plan is measured against, verbatim, into `learnings.md`:
      the `opencode agent list` repository-agent count; the `md links validate` repo-wide broken
      count with registered exclusions; the dangling-anchor count under `.claude/skills` with
      `SKILL_TREE_MARKERS` disabled — acceptance: three numbers with their commands.
- [ ] [AI] Establish the green baseline: `npx nx run rhino-cli:test:quick` exits 0.

### Phase 0 Gate

- [ ] [AI] `nx run rhino-cli:test:quick` exits 0.
- [ ] [AI] `npm run generate:bindings` leaves a clean diff.
- [ ] [AI] `learnings.md` carries all three baseline numbers with their commands.

> Phase 0 opens no PR. The earliest PR is Phase 1.

## Phase 1: WS-H2 — explicit roots (do this first)

> Ordered first: any later phase that adds tests to the same binary would otherwise inherit the
> flake this phase removes.

- [ ] [AI] RED: restore the two `run(...)` generate smoke tests removed during
      `update-harness-support` Phase 5 — acceptance: `cargo test --release` shows
      `harness_unknown_name_is_error` failing under the default parallel runner and passing under
      `--test-threads=1`. A RED that reproduces only in one mode must state both.
- [ ] [AI] GREEN: give the generate command an explicit repository-root parameter; the binary's
      entry point passes the discovered root, tests pass a fixture path.
- [ ] [AI] REFACTOR: audit every sibling command for the same ambient-root read; fix the class, not
      only the site the failing test named.
- [ ] [AI] Add the Gherkin from `prd.md` US-2 to the appropriate feature file, checking first which
      cucumber runner owns that directory and whether a tag filter is needed.

### Phase 1 Gate

- [ ] [AI] `cargo test --release` passes three consecutive times under the default runner.
- [ ] [AI] `git grep -n "current_dir" apps/rhino-cli/src/commands/` names no path that a test drives.
- [ ] [AI] `nx run rhino-cli:specs:behavior:coverage` exits 0.
- [ ] [AI] Regenerate `apps/rhino-cli/parity-manifest.sha256` after staging every changed boundary
      file — the boundary includes `.feature` files, not only `.rs`.

## Phase 2: WS-H1 — a globbed binding directory holds only agents

- [ ] [AI] RED: add a failing test asserting no tracked file under a globbed agent directory lacks
      agent frontmatter — acceptance: fails naming `.opencode/agents/README.md` before the fix.
- [ ] [AI] GREEN: declare per harness in `repo-config.yml` whether its agent directory is globbed by
      the vendor tool, and implement the check in `harness bindings validate`.
- [ ] [AI] Decide and record where the index moves; re-run
      `rhino-cli governance readme-index validate` — acceptance: exits 0 with the index relocated,
      not with the requirement weakened.
- [ ] [AI] Regenerate the bindings and confirm idempotence across two runs.
- [ ] [AI] Add the US-1 Gherkin.

### Phase 2 Gate

- [ ] [AI] `harness bindings validate` exits 0, and exits 1 naming a probe `.md` planted in a globbed
      directory — falsifiable both ways, with the probe removed afterwards.
- [ ] [AI] `governance readme-index validate` exits 0.
- [ ] [AI] `npm run validate:sync` exits 0.
- [ ] [HUMAN] `opencode agent list` names no agent called `README` — paste the count.

## Phase 3: WS-H3 — repair the 47 dangling anchors

- [ ] [AI] Regenerate the finding list with `SKILL_TREE_MARKERS` disabled; write one row per anchor
      (file, anchor, intended target, verdict) into `learnings.md` before editing anything.
- [ ] [AI] Repair each anchor: repoint to the split-pattern child that now carries the heading, or
      remove the reference and state what replaced it.
- [ ] [AI] Re-measure with the exemption disabled — acceptance: 0 dangling anchors.
- [ ] [AI] Restore the exemption and confirm the repo-wide count is no greater than the baseline.

### Phase 3 Gate

- [ ] [AI] Every anchor in the list has a recorded verdict; the count is 0.
- [ ] [AI] `md links validate` with registered exclusions is no worse than baseline.
- [ ] [AI] `nx affected -t typecheck,lint,test:quick` exits 0.

## Phase 4: Knowledge Capture

- [ ] [AI] Apply the litmus test, the sensitivity gate, and the repo-relevance gate to every
      `learnings.md` entry; route each survivor to exactly one durable home.
- [ ] [AI] Record the terminal state of every entry, or the explicit
      `No generalizable learnings — <reason>` escape.

## Terminal Review and Paired Merge

- [ ] [AI] Mark the PR ready for review.
- [ ] [AI] Replay the `apps/rhino-cli/**` and `specs/apps/rhino/**` changes into `ose-private` on one
      branch, open exactly one PR there, regenerate that repository's parity manifest.
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle to a clean result on both PRs.
- [ ] [AI] Poll CI every 2 minutes on both PRs; never `gh run watch`.
- [ ] [AI] Confirm no unresolved review thread via the GraphQL `reviewThreads` query — a PR can read
      BLOCKED with every check green.
- [ ] [AI] Merge both PRs in the same session; fast-forward local `main` in both repositories.

## Plan Archival

- [ ] [AI] Verify every checklist item is ticked and every gate passes.
- [ ] [AI] Remove the worktree; `git mv` this folder to `plans/done/<date>__<slug>`.
- [ ] [AI] Update `plans/backlog/README.md` and `plans/done/README.md`.
