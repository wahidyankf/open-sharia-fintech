# Delivery Checklist — Database Internals Course Ruff Configuration

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can perform a physical or credential-bound action. This plan has no
> `[HUMAN]` step.

## Delivery Boundaries

| Phase | Delivery unit | Worktree and PR |
| --- | --- | --- |
| 0 | Baseline only | No PR; evidence rides the Phase 1 PR. |
| 1–3 | Configuration, Knowledge Capture, and archival | One worktree, one branch, one PR. |

## Parallelization Model

`Phase 0 → Phase 1 → Phase 2 → Phase 3`; every node is dependent because the selected formatter
value must come from the baseline before configuration and verification can occur.

## Worktree

Use `worktrees/ayokoding-database-internals-ruff-config/` on a branch of the same name. Delivery mode
is `worktree-to-pr`; Phase 1 opens the sole draft PR after its configuration commit.

## Phase 0: Baseline

- [ ] [AI] Confirm `apps/ayokoding-www/content/en/learn/courses/database-internals-and-storage-engines/ruff.toml` is absent with `test ! -f <path>` — acceptance: exits 0 and no file is changed.
- [ ] [AI] Run `find apps/ayokoding-www/content/en/learn/courses/database-internals-and-storage-engines/{learning,drilling} -name '*.py' -print0 | xargs -0 awk 'length > max { max = length } END { print max }'` and record the measured value in `learnings.md` — acceptance: one reproducible baseline exists.

### Phase 0 Gate

- [ ] [AI] Confirm the baseline is recorded in `learnings.md` — acceptance: the measured line length and command are present.
- [ ] [AI] Confirm no branch is pushed and no PR is opened — acceptance: `git ls-remote --heads origin "$(git branch --show-current)"` prints no ref and `gh pr list --head "$(git branch --show-current)" --json number --jq 'length'` returns `0`.

> **Pause Safety**: a reproducible baseline exists; implementation has not started.

## Phase 1: Scoped Configuration

- [ ] [AI] Add `apps/ayokoding-www/content/en/learn/courses/database-internals-and-storage-engines/ruff.toml` with the baseline-derived line length and rationale — acceptance: `ruff format --check apps/ayokoding-www/content/en/learn/courses/database-internals-and-storage-engines` exits 0 without source rewrites.
- [ ] [AI] Inspect `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/'` — acceptance: it prints no path, proving the manifest ownership invariant.
- [ ] [AI] Run `npx nx affected -t lint,test:quick` — acceptance: both affected targets exit 0.
- [ ] [AI] Commit the configuration with `fix(ayokoding-www): add database internals ruff config` — acceptance: `git show --name-only --format=HEAD` contains only the scoped configuration and this plan's evidence.
- [ ] [AI] Open exactly one draft PR from the declared worktree branch — acceptance: the PR contains this delivery unit only.

### Phase 1 Gate

- [ ] [AI] Confirm the formatter check is green — acceptance: the Phase 1 `ruff format --check` command exits 0.
- [ ] [AI] Confirm affected quality targets are green — acceptance: `npx nx affected -t lint,test:quick` exits 0.
- [ ] [AI] Confirm PR CI is green — acceptance: `gh pr checks <PR>` has no pending or failing check.

> **Pause Safety**: the scoped configuration is committed, reviewed through its delivery PR, and safe
> to resume at Knowledge Capture.

## Phase 2: Knowledge Capture

- [ ] [AI] Triage every `learnings.md` entry to a durable home or explicitly record `none` — acceptance: every entry has one terminal route and both safety gates are applied.

### Phase 2 Gate

- [ ] [AI] Confirm Knowledge Capture is terminal and no unresolved learning remains — acceptance: `learnings.md` has no untriaged entry.

> **Pause Safety**: implementation and learning triage are complete; archival is the sole remaining
> action.

## Phase 3: Archival and Integration

- [ ] [AI] Move the plan with `git mv plans/in-progress/ayokoding-database-internals-ruff-config plans/done/YYYY-MM-DD__ayokoding-database-internals-ruff-config` — acceptance: the full plan folder is under `plans/done/`.
- [ ] [AI] Update `plans/in-progress/README.md`, `plans/done/README.md`, and `plans/backlog/README.md` for the archival move — acceptance: no plan index links to the former location.
- [ ] [AI] Complete the three-cycle PR-Review Maker→Fixer Cycle — acceptance: all three consolidated reviews are posted and every review thread is resolved.
- [ ] [AI] Merge under hardened preconditions — acceptance: the PR reports state `MERGED` and its merge commit is recorded.
- [ ] [AI] Verify the deployed static course remains reachable — acceptance: a production request to its course URL returns a successful response.

### Phase 3 Gate

- [ ] [AI] Confirm archival is complete — acceptance: the plan folder is under `plans/done/`.
- [ ] [AI] Confirm review and CI are complete — acceptance: all review threads are resolved and `gh pr checks <PR>` has no pending or failing check.
- [ ] [AI] Confirm merge and deployment are complete — acceptance: the PR is merged and the production course request succeeds.

> **Pause Safety**: terminal only after the merged PR and deployment verification.
