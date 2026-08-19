# Delivery Checklist — CI Workflow Scope and Build Resilience

> Delivery mode: `worktree-to-pr`. One worktree, one PR. No file here is inside the `rhino-cli`
> parity boundary, so there is no paired `ose-private` merge.

## Phase 0: Setup

- [ ] [AI] Create one worktree; confirm the working location is the worktree, not the primary
      checkout.
- [ ] [AI] Sync with the latest `origin/main`; run `npm install` inside the worktree.
- [ ] [AI] Create `learnings.md` with `## Baseline`, `## PR`, and per-phase headings.
- [ ] [AI] Record the baseline: push a `repo-config.yml`-only commit to a scratch branch and list
      every workflow it starts — acceptance: the list is recorded verbatim and includes the
      BeaverNest application workflow. This is the before-state AC-1 is measured against.
- [ ] [AI] Establish the green baseline for `beavernest-be:test:unit`.

### Phase 0 Gate

- [ ] [AI] The before-state workflow list exists in `learnings.md`.
- [ ] [AI] `nx run beavernest-be:test:unit` exits 0 locally.

> Phase 0 opens no PR.

## Phase 1: WS-C1 — narrow the path filter

- [ ] [AI] Read every job in `beavernest-app-test-local-deploy-stag.yml` and record whether any step
      reads `repo-config.yml` — acceptance: a written verdict per job, not an assumption.
- [ ] [AI] Sweep every workflow under `.github/workflows/` for a `repo-config.yml` path entry and
      record one verdict per occurrence — fix the class, not the one file.
- [ ] [AI] Remove the entries whose verdict is "does not read it"; for any that does, name the
      dependency in the job instead and keep the trigger.
- [ ] [AI] Verify on real pushes, both directions: a `repo-config.yml`-only commit and an
      `apps/beavernest-be/**` commit, each recorded with the workflows it started.

### Phase 1 Gate

- [ ] [AI] The governance-only push starts no BeaverNest application workflow (AC-1).
- [ ] [AI] The application push still starts it (AC-2) — the pair, or the filter is merely disabled.
- [ ] [AI] Every swept occurrence carries a recorded verdict.

## Phase 2: WS-C2 — make the fetches survivable

- [ ] [AI] Determine whether the openapi-generator JAR can be pinned and cached rather than fetched
      at build time — acceptance: a written decision with the version, or a stated reason it cannot.
- [ ] [AI] Add retry-with-backoff and a step-level timeout to `setup-playwright`'s cache-hit branch.
- [ ] [AI] Apply the same to the contract-build fetch, or remove the fetch per the decision above.
- [ ] [AI] Prove each guard fires: force a fetch failure (an unroutable host, a blocked resolver)
      and record that the step fails within its own budget, naming the fetch — acceptance: the
      failure message names the fetch, and the job's own timeout is not reached.
- [ ] [AI] Restore the forced-failure conditions and confirm both steps pass again.

### Phase 2 Gate

- [ ] [AI] Both guards proved falsifiable both ways, with the probe removed afterwards.
- [ ] [AI] A normal run of both steps is unchanged in duration beyond the retry wrapper.

## Phase 3: WS-C3 — name the failing case

- [ ] [AI] RED: add a per-case test for each of the seven invalid inputs — acceptance: with the
      implementation temporarily accepting one case, exactly one named test fails and its message
      carries the input and the computed value.
- [ ] [AI] GREEN: replace the single list assertion with the per-case theory; keep the coverage
      identical, case for case.
- [ ] [AI] Add the US-3 Gherkin to the BeaverNest spec tree.
- [ ] [AI] Run `beavernest-be:test:coverage` — the target whose environment differed — not only
      `test:unit`.

### Phase 3 Gate

- [ ] [AI] `nx run beavernest-be:test:unit` and `test:coverage` both exit 0.
- [ ] [AI] The seven cases appear as seven named results.
- [ ] [AI] `nx affected -t typecheck,lint,test:quick` exits 0.

## Phase 4: Knowledge Capture

- [ ] [AI] Apply the litmus test, the sensitivity gate, and the repo-relevance gate to every
      `learnings.md` entry; route each survivor to exactly one durable home.
- [ ] [AI] Record the terminal state of every entry, or the explicit
      `No generalizable learnings — <reason>` escape.

## Terminal Review and Merge

- [ ] [AI] Mark the PR ready for review.
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle to a clean result.
- [ ] [AI] Poll CI every 2 minutes; never `gh run watch`.
- [ ] [AI] Confirm no unresolved review thread via the GraphQL `reviewThreads` query.
- [ ] [AI] Merge; fast-forward local `main`.

## Plan Archival

- [ ] [AI] Verify every checklist item is ticked and every gate passes.
- [ ] [AI] Remove the worktree; `git mv` this folder to `plans/done/<date>__<slug>`.
- [ ] [AI] Update `plans/backlog/README.md` and `plans/done/README.md`.
