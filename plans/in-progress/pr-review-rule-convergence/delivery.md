# Delivery Checklist: PR Review Rule Convergence

## Delivery Mode

`worktree-to-pr` in `worktrees/ose-new-rules/` for the OSE-public policy delivery. OSE Primer uses one
worktree and a separate companion PR. The OSE-private companion uses one worktree but, under the
user's one-plan exception, commits and pushes directly to `origin/main` with no PR. The public PR
merges first, the private direct push follows immediately, and the OSE Primer companion follows.

## Worktree

| Repository  | Exact plan worktree                     | Delivery mode                          | Cleanup owner                   |
| ----------- | --------------------------------------- | -------------------------------------- | ------------------------------- |
| OSE Public  | `worktrees/ose-new-rules/`              | `worktree-to-pr`                       | `[AI]` after P5 archival merges |
| OSE Private | `worktrees/pr-review-rule-convergence/` | this-plan direct push to `origin/main` | `[AI]` after P4 verification    |
| OSE Primer  | `worktrees/pr-review-rule-convergence/` | `worktree-to-pr`                       | `[AI]` after P4P merge          |

Before work in any repository, run `git fetch origin`, compare `git rev-parse HEAD` with
`git rev-parse origin/main`, and read the full incoming diff after any integration. Provision only a
missing exact path with `git worktree add <exact-path> -b <branch> origin/main`; never use a foreign
or concurrent worktree.

## Delivery Boundaries

| Unit                | Repository  | Phases          | Branch                                          | Boundary | Delivery action                                                   |
| ------------------- | ----------- | --------------- | ----------------------------------------------- | -------- | ----------------------------------------------------------------- |
| Canonical policy    | OSE Public  | P1, P1R, P2, P3 | `governance/pr-review-rule-convergence-public`  | P3       | Draft PR, applicable review route, merge                          |
| Private propagation | OSE Private | P3, P4          | `governance/pr-review-rule-convergence-private` | P4       | Commit and direct push to `origin/main` under this-plan exception |
| Primer propagation  | OSE Primer  | P4P             | `governance/pr-review-rule-convergence-primer`  | P4P      | Draft PR, applicable review route, merge                          |
| Public closeout     | OSE Public  | P5              | `docs/pr-review-rule-convergence-closeout`      | P5       | Draft archival PR and merge                                       |

## Command Catalog

| ID  | Command                                                           | Use                                                 |
| --- | ----------------------------------------------------------------- | --------------------------------------------------- |
| C1  | `git status --short && git diff --check`                          | Safe ledger and diff baseline                       |
| C2  | `rg -n -i '<policy-pattern>' <target-paths>`                      | Canonical and live-plan reference inventory         |
| C3  | `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push` | Full local gate registry                            |
| C4  | `npm run generate:bindings && npm run validate:sync`              | Canonical-agent binding regeneration and validation |
| C5  | `npm run format:md:check && npm run lint:md`                      | Markdown validation                                 |
| C6  | `gh pr checks <pr-number>`                                        | PR final-head status at the required cadence        |
| C7  | `git worktree list && git status --short`                         | Exact worktree cleanup precondition                 |
| C8  | `git worktree remove <exact-plan-worktree>`                       | Direct cleanup of a verified plan worktree          |

## Legend

- `[AI]` — agent executes the task and records sanitized evidence.

Every checkbox in this plan is `[AI]`; no manual review, approval, check, or gate is required.

## Parallelization Model

Chosen N = 3 background slots. Public canonical wording serializes before generated bindings, the
immediate private companion, and the in-scope Primer companion; read-only reference discovery may run
independently. Cleanup is terminal.

| Node | Work                                                                  | blockedBy | blocks |
| ---- | --------------------------------------------------------------------- | --------- | ------ |
| P0   | Baseline and canonical-reference inventory                            | —         | P1     |
| P1   | Define the public workflow and merge algorithm                        | P0        | P1R    |
| P1R  | Retrofit all related live plans                                       | P1        | P2     |
| P2   | Propagate public instructions, maker guidance, and generated bindings | P1R       | P3     |
| P3   | Validate and merge the public canonical PR                            | P2        | P4     |
| P4   | Merge and reconcile the OSE-private companion                         | P3        | P4P    |
| P4P  | Deliver the OSE Primer companion and retrofit                         | P4        | P5     |
| P5   | Capture knowledge, archive, and remove exact plan worktrees           | P4P       | —      |

## Phase 0: Baseline and Inventory

Run C1 before this phase and C2 for every inventory task below. Store only paths, hashes, and
sanitized statuses in `plans/in-progress/pr-review-rule-convergence/learnings.md`.

- [x] [AI] [P0-001] Record the starting public branch, worktree status, and path-only file-touch
      ledger in the plan's `learnings.md` — acceptance: no pre-existing change is claimed.
  - Date: 2026-08-11
  - Status: passed
  - Files Changed: `plans/in-progress/pr-review-rule-convergence/learnings.md`, `delivery.md`
  - Evidence: `governance/pr-review-rule-convergence-public` began clean at `cb3c99f7e`, equal to
    `origin/main`; no foreign working-tree path was claimed.
- [x] [AI] [P0-002] Search for every canonical mention of fixed PR-review cycle counts, merge
      preconditions, executable/configuration routing, secret remediation, and public/private parity —
      acceptance: the impact tree is reconciled or amended with each discovered canonical path.
  - Date: 2026-08-11
  - Status: passed
  - Files Changed: `plans/in-progress/pr-review-rule-convergence/learnings.md`, `delivery.md`
  - Evidence: the canonical and agent consumer inventory is recorded in `learnings.md`; all future
    policy edits will reconcile against this list rather than a filename guess.
- [x] [AI] [P0-003] Inspect `.github/workflows/pr-quality-gate.yml` and record its workflow/check names
      without copying sensitive output — acceptance: later verification targets the exact workflow.
  - Date: 2026-08-11
  - Status: passed
  - Files Changed: `plans/in-progress/pr-review-rule-convergence/learnings.md`, `delivery.md`
  - Evidence: `pr-quality-gate` and its top-level job keys are recorded in `learnings.md` without CI
    payloads or secret-like output.
- [x] [AI] [P0-004] Inspect `plans/ideas/README.md` and existing two-pagers for an already-owned Low
      finding/non-convergence topic — acceptance: no duplicate idea is planned.
  - Date: 2026-08-11
  - Status: passed
  - Files Changed: `plans/in-progress/pr-review-rule-convergence/learnings.md`, `delivery.md`
  - Evidence: `pr-review-bot-identity` is adjacent but not a duplicate; a new idea is deferred until
    a concrete Low finding or slow-convergence cause exists.
- [x] [AI] [P0-005] Inventory portable governance, agent, skill, and related-rule files shared with
      OSE-private; record their public path and byte hash in a sanitized manifest — acceptance: every
      private-only operational exception is explicit.
  - Date: 2026-08-11
  - Status: passed
  - Files Changed: `plans/in-progress/pr-review-rule-convergence/learnings.md`, `delivery.md`
  - Evidence: the public manifest baseline covers the portable governance and agent paths; the
    concurrent private remediation worktree is excluded from this plan's comparison.

### Phase 0 Gate

- [x] [AI] [P0-006] Run C1 in `worktrees/ose-new-rules/` and reconcile its output with the
      `plans/in-progress/pr-review-rule-convergence/learnings.md` ledger — acceptance: no foreign change
      is modified.
  - Date: 2026-08-11
  - Status: passed
  - Files Changed: `plans/in-progress/pr-review-rule-convergence/delivery.md`
  - Evidence: `git diff --check` passed; the only modified paths are the two P0 ledger/checklist files.

> **Pause Safety:** Discovery is complete and no policy file has changed. Resume with P1-001.

## Phase 1: Canonical Public Rules

For P1-001 through P1-007B, first run C2 against the named canonical file, edit only that file, then
run C5 before continuing. Each task changes documentation, not application code, so no TDD cycle is
applicable.

- [x] [AI] [P1-001] Update `repo-governance/workflows/pr/pr-review-quality-gate.md` frontmatter and
      input contract for behavior-based eligibility, default ceiling seven, and early clean M/H/C exit —
      acceptance: the workflow owns the algorithm rather than a copied variant. Evidence: frontmatter
      now defaults to seven and the workflow owns the route algorithm.
- [x] [AI] [P1-002] Add the scout classification record, fail-safe ambiguity behavior, code-finding
      filter, and sequential cycle transition rules in
      `repo-governance/workflows/pr/pr-review-quality-gate.md` — acceptance: every PR selects exactly one route.
      Evidence: classifier records eligible/noneligible and ambiguity selects eligible.
- [x] [AI] [P1-003] Add cycle-six-and-seven sanitized learning capture plus Low-finding disposition to
      `repo-governance/workflows/pr/pr-review-quality-gate.md` — acceptance: Lows are routed to
      deduplicated ideas and do not prolong the loop. Evidence: the loop and route-specific
      done-definition specify both capture points and Low disposition.
- [x] [AI] [P1-004] Add the seven-cycle non-convergence merge block for code Medium, High, and Critical
      findings in `repo-governance/workflows/pr/pr-review-quality-gate.md` — acceptance: a green CI run
      alone cannot merge that PR. Evidence: ceiling status is `blocked` and merge precondition (b)
      includes code-related MEDIUM findings.
- [x] [AI] [P1-004A] Add immediate reclassification of every still-open PR at its next review or merge
      action in `repo-governance/workflows/pr/pr-review-quality-gate.md` — acceptance: no legacy or
      per-PR opt-in route remains. Evidence: classifier scope includes every still-open PR at its next
      review or merge action.
- [x] [AI] [P1-005] Update `repo-governance/development/workflow/pr-merge-protocol.md` preconditions
      and terminal steps for eligible versus non-eligible PRs — acceptance: non-eligible PRs require the
      named workflow only, while universal secret handling remains explicit. Evidence: route-specific
      preconditions and the universal secret check are now canonical.
- [x] [AI] [P1-006] Update `repo-governance/development/quality/pr-review-disciplines.md` to limit
      specialist findings to eligible code behavior and retain Low-finding evidence requirements —
      acceptance: severity labels match the new workflow. Evidence: classifier-owned eligibility,
      code-related M/H/C blocking, and Low evidence/disposition are documented together.
- [x] [AI] [P1-007] Update `repo-governance/development/workflow/git-push-safety.md` and the canonical
      secrets rule with the standing full-rewrite and replacement-PR algorithm — acceptance: each names
      all affected reachable refs and never records a secret value. Evidence: the linked incident
      exception and authoritative procedure cover containment through replacement PR and provider purge.
- [x] [AI] [P1-007A] Update `repo-governance/development/workflow/ci-monitoring.md` so runner contention
      preserves the active goal and requires patient cadence-based investigation — acceptance: it forbids
      cancellation solely for a queued or stalled runner and retains the required-check gate. Evidence:
      the runner section explicitly preserves the active goal and checklist through the wait.
- [x] [AI] [P1-007B] Update `repo-governance/development/workflow/worktree-and-artifact-cleanup.md`,
      `repo-governance/conventions/structure/plans.md`, and
      `repo-governance/workflows/plan/plan-execution.md` for immediate exact-path cleanup — acceptance:
      self-created plan worktrees are removed automatically after their final delivery, while foreign
      worktrees are never touched. Evidence: all three canonical surfaces now require exact-path,
      self-created cleanup with pre-removal checks and no confirmation prompt.

## Phase 1R: Retrofit Related Live Plans

For each P1R task, run C2 against the named plan folder, edit only `edit`-classified forward-facing
documents, then run C5 for that folder. Do not change a completed-plan document or an append-only
execution record merely to retrofit a historical instruction.

- [x] [AI] [P1R-001] Create an exact, path-level retrofit manifest from a deterministic search of
      `plans/backlog/` and `plans/in-progress/` for retired PR-cycle, merge, secret-remediation,
      public/private-parity, and runner-contention language — acceptance: every candidate is classified
      `edit`, `current`, or `historical-record-exempt` with a reason.
- [x] [AI] [P1R-002] Retrofit every `edit`-classified document in
      `ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness` — acceptance: its README
      and delivery instructions route future PRs through the new classifier and cycle ceiling.
- [x] [AI] [P1R-003] Retrofit every `edit`-classified document in
      `ayokoding-learning-path-07-course-authoring-low-level-systems` — acceptance: remaining workflow,
      merge, and learning instructions no longer mandate a retired fixed cycle.
- [x] [AI] [P1R-004] Retrofit every `edit`-classified document in
      `ayokoding-learning-path-08-course-authoring-security-and-ops` — acceptance: its secret response
      and PR delivery rules agree with the canonical incident and routing policy.
- [x] [AI] [P1R-005] Retrofit every `edit`-classified document in
      `ayokoding-learning-path-09-course-authoring-interview-technique` — acceptance: requirements,
      delivery, and learnings references remain mutually consistent.
- [x] [AI] [P1R-006] Retrofit every `edit`-classified document in
      `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own` — acceptance: its future PR
      instructions refer to the canonical routing workflow instead of a copied count.
- [x] [AI] [P1R-007] Retrofit every `edit`-classified document in
      `ayokoding-learning-path-11-course-authoring-capstones` — acceptance: its BRD, PRD, README, and
      delivery references agree with the bounded review policy.
- [x] [AI] [P1R-008] Retrofit every `edit`-classified document in
      `ayokoding-learning-path-12-careers-se-manifests` — acceptance: its future delivery path is
      plan-origin independent.
- [x] [AI] [P1R-009] Retrofit every `edit`-classified document in
      `ayokoding-learning-path-13-careers-ai-manifest` — acceptance: the specialist loop is conditional
      on behavior-changing content, not on plan existence.
- [x] [AI] [P1R-010] Retrofit every `edit`-classified document in
      `ayokoding-learning-path-14-skills-accounting-foundations` — acceptance: its planned PR boundary
      references the same exit, Low-finding, and non-convergence rules.
- [x] [AI] [P1R-011] Retrofit every `edit`-classified document in
      `ayokoding-learning-path-15-skills-accounting-enterprise-reporting` — acceptance: no old merge
      precondition remains in its active delivery language.
- [x] [AI] [P1R-012] Retrofit every `edit`-classified document in
      `ayokoding-learning-path-16-skills-accounting-sharia-extension` — acceptance: its delivery text
      delegates to the canonical policy where appropriate.
- [x] [AI] [P1R-013] Retrofit every `edit`-classified document in
      `ayokoding-learning-path-17-skills-erp-foundations` — acceptance: all matching future-facing plan
      documents are updated while its curriculum content remains untouched.
- [x] [AI] [P1R-014] Retrofit every `edit`-classified document in
      `ayokoding-learning-path-18-skills-erp-enterprise-depth` — acceptance: all matching future-facing
      plan documents are updated while its curriculum content remains untouched.
- [x] [AI] [P1R-015] Retrofit remaining unchecked delivery instructions in
      `repository-onboarding-readme-refresh` — acceptance: future work uses the new policy and its
      append-only execution records preserve historical evidence unchanged.
- [x] [AI] [P1R-016] Re-run the deterministic live-plan search and manually review every remaining
      match — acceptance: no forward-facing backlog or active-plan instruction retains the retired rule;
      every retained historical-record match has an explicit exemption reason. Evidence: `learnings.md`
      records the four historical/exempt categories and the zero forward-facing retained result.
- [x] [AI] [P1R-017] Repair links exposed by the Phase 1 gate in the source agent and live idea
      documents, then regenerate bindings — acceptance: no public document references retired workflow
      anchors. Evidence: source and idea anchors are updated; generated mirrors were regenerated.

### Phase 1 Gate

- [x] [AI] [P1-008] Run C3 and C5 from `worktrees/ose-new-rules/` plus
      `apps/rhino-cli/scripts/rhino-bin.sh md mermaid validate`,
      `apps/rhino-cli/scripts/rhino-bin.sh md heading-hierarchy validate`, and
      `apps/rhino-cli/scripts/rhino-bin.sh md links validate --exclude plans/done` — acceptance: every
      changed public canonical and retrofitted plan document passes. Evidence: all listed commands exit
      0 after the P1R-017 anchor repair.

> **Pause Safety:** The canonical public algorithm and every related live plan are coherent but not yet propagated to entry points. Resume with P2-001.

## Phase 2: Manual and Generated Propagation

For P2-001 through P2-004, run C2 against the named canonical path before editing it. Run C4 after
the `.claude/agents/repo-rules-maker.md` edit; do not hand-edit generated mirrors.

- [x] [AI] [P2-001] Update `AGENTS.md` with the plan-independent eligible/non-eligible routing,
      cycle ceiling, convergence, secret, parity, and runner-contention rules — acceptance: all interactive
      roots receive the same decision rule. Evidence: delivery and review-agent entries use the classifier.
- [x] [AI] [P2-002] Update Plans Organization so plan execution does not create a different review
      path from ad-hoc work — acceptance: planned and unplanned PRs point to one canonical workflow.
      Evidence: Delivery Mode now delegates to the canonical classifier.
- [x] [AI] [P2-003] Update Related Repositories with public-first, immediate private governance
      reconciliation, this plan's OSE Primer companion, runner contention, and direct cleanup — acceptance:
      it states the bounded skew and all three delivery paths honestly. Evidence: portable propagation,
      runner, and self-created-cleanup rules are explicit.
- [x] [AI] [P2-004] Update `.claude/agents/repo-rules-maker.md` to require manual canonical propagation,
      generated-binding regeneration, patient runner-contention guidance, and portable public/private
      byte-identity verification — acceptance: the maker cannot update one rule surface in isolation or
      silently omit a parity-manifest exception. Evidence: the maker now specifies manifest verification,
      generated regeneration, contention patience, and exact-path cleanup.
- [x] [AI] [P2-005] Run `npm run generate:bindings` — acceptance: generated harness mirrors are changed
      only by the generator and remain in the same delivery diff as their `.claude/` source. Evidence:
      generator completed after all source-agent changes.
- [x] [AI] [P2-006] Run `npm run validate:sync` — acceptance: canonical and generated bindings agree.
      Evidence: 97/97 harness synchronization checks passed.

### Phase 2 Gate

- [x] [AI] [P2-007] Run C3, C4, and C5 from `worktrees/ose-new-rules/` — acceptance: public entry
      points, canonical rules, and generated files are all clean. Evidence: pre-push registry, binding
      generator/sync, markdown format/lint, and `git diff --check` all passed.

> **Pause Safety:** Public policy and all local bindings are ready for a draft PR. Resume with P3-001.

## Phase 3: Public Delivery

Use `git add -- <ledger-paths>`, `git commit -m 'docs(governance): converge PR review rules'`, and
`git push -u origin governance/pr-review-rule-convergence-public` for P3-003. Use
`gh pr create --draft --base main --head governance/pr-review-rule-convergence-public` for P3-004,
C6 for its status, and `gh pr merge <public-pr> --merge --delete-branch` only after P3-005 passes.

- [ ] [AI] [P3-001] Create a sanitized OSE-private companion diff and governed-path equivalence manifest
      in its own repository/worktree — acceptance: no private facts are copied into OSE-public.
- [ ] [AI] [P3-002] Prepare the OSE-private worktree diff and verify its intended post-public base,
      secret-safety status, and public/private byte-identity manifest — acceptance: it is ready for the
      one-plan direct push without a PR or PR-quality wait.
- [ ] [AI] [P3-002A] Record the narrow user-authorized OSE-private direct-push exception in sanitized
      delivery evidence — acceptance: it names this plan only, never a reusable bypass.
- [ ] [AI] [P3-003] Commit and push the public policy branch using a Conventional Commit — acceptance:
      the explicit file-touch ledger matches the staged paths.
- [ ] [AI] [P3-004] Open a draft public PR and verify the `pr-quality-gate` workflow's final-head run —
      acceptance: every required job in that workflow is green.
- [ ] [AI] [P3-004A] If the public workflow is queued or stalled, investigate shared runner contention
      and continue polling at the documented cadence — acceptance: the active goal remains active and no
      run is cancelled merely to escape a queue.
- [ ] [AI] [P3-005] Classify this policy PR under the new behavior-based rule and perform only the
      applicable review route — acceptance: the route and evidence are recorded without circular guessing.
- [ ] [AI] [P3-006] Merge the public PR after its selected route and named workflow pass — acceptance:
      public canonical content is on `main`.

### Phase 3 Gate

- [ ] [AI] [P3-007] Run `git fetch origin && git rev-parse origin/main` in OSE Public and
      `git rev-parse HEAD` in the private worktree; record the revisions and manifest digest in the
      sanitized reconciliation record — acceptance: P4 can execute without rediscovery.

> **Pause Safety:** Public is canonical and private is prepared. Resume immediately with P4-001.

## Phase 4: OSE-Private Reconciliation

Use `git add -- <private-ledger-paths>`, `git commit -m 'docs(governance): converge PR review rules'`,
and `git push origin HEAD:main` only for this plan's exact private worktree after P4-001 succeeds.

- [ ] [AI] [P4-001] Reconfirm the private companion still matches the final public governed-path
      manifest byte-for-byte — acceptance: any public merge-time edit is propagated before private merge.
- [ ] [AI] [P4-002] Commit the OSE-private worktree and push its verified change directly to
      `origin/main` immediately after public merge — acceptance: post-public base, secret-safety, and
      manifest checks passed; no PR or quality-check result is required.
- [ ] [AI] [P4-003] Record public/private revisions, manifest outcome, and temporary-skew closure using
      safe identifiers only — acceptance: governed paths are on-par after the companion merge.
- [ ] [AI] [P4-005] Run C7 in `worktrees/pr-review-rule-convergence/` for OSE-private, then run C8
      against that exact path — acceptance: only this plan's clean private worktree is removed immediately.

### Phase 4 Gate

- [ ] [AI] [P4-004] Run `shasum -a 256 <manifest-paths>` in the public and private repository roots and
      compare the sanitized manifest — acceptance: zero unintended divergence; the ready OSE Primer
      companion is explicitly in scope.

> **Pause Safety:** Public/private parity is restored. Resume with P4P-001.

## Phase 4P: OSE Primer Companion and Retrofit

Use C1 and C2 in the OSE Primer worktree before edits, C4 after canonical agent edits, C3 and C5
before push, `git push -u origin governance/pr-review-rule-convergence-primer`,
`gh pr create --draft --base main --head governance/pr-review-rule-convergence-primer`, C6, and
`gh pr merge <primer-pr> --merge --delete-branch` after the selected review route passes.

- [ ] [AI] [P4P-001] Provision or enter the plan's single OSE Primer worktree and record its separate
      file-touch ledger — acceptance: no OSE-public or OSE-private working tree is modified from Primer.
- [ ] [AI] [P4P-002] Build an applicable-policy manifest from final public canonical files, naming each
      documented Primer-specific path or wording exception — acceptance: every routing, convergence, and
      secret-response rule has a Primer disposition.
- [ ] [AI] [P4P-003] Propagate the applicable PR-review workflow, merge protocol, plan convention,
      CI-monitoring, root instructions, and repo-rules-maker guidance in OSE Primer — acceptance: its
      canonical sources implement the same policy semantics.
- [ ] [AI] [P4P-004] Regenerate OSE Primer bindings from `.claude/` and run its binding-sync validation
      — acceptance: no generated mirror is hand-edited or omitted from the companion diff.
- [ ] [AI] [P4P-005] Search OSE Primer's `plans/backlog/` and `plans/in-progress/`, classify every
      retired-rule match, and retrofit each forward-facing plan document — acceptance: its live plans no
      longer encode the retired fixed-cycle rule; historical execution records stay historical.
- [ ] [AI] [P4P-006] Run applicable OSE Primer Markdown, policy-manifest, and quality-gate checks —
      acceptance: changed canonical, generated, and plan files pass without a bypass.
- [ ] [AI] [P4P-007] Commit, push, open a draft OSE Primer companion PR, apply its classifier-selected
      review route, and verify its final-head `pr-quality-gate` run — acceptance: the PR is ready to merge
      under the new plan-independent policy.
- [ ] [AI] [P4P-007A] If the OSE Primer workflow is queued or stalled, investigate contention and
      continue patient monitoring — acceptance: runner availability never cancels the active goal.
- [ ] [AI] [P4P-008] Merge the passing OSE Primer companion and record public/private/Primer revision
      reconciliation using safe identifiers only — acceptance: this plan's three-repository policy change
      is complete.
- [ ] [AI] [P4P-010] Run C7 in the OSE Primer `worktrees/pr-review-rule-convergence/`, then run C8
      against that exact path — acceptance: only this plan's clean OSE Primer worktree is removed immediately.

### Phase 4P Gate

- [ ] [AI] [P4P-009] Run `git fetch origin && git rev-parse origin/main` and C2 against OSE Primer
      `plans/backlog/ plans/in-progress/` — acceptance: all in-scope Primer changes landed and every
      exception is documented.

> **Pause Safety:** The three-repository policy rollout is complete. Resume with P5-001.

## Phase 5: Knowledge, Archive, and Cleanup

Use `git mv plans/in-progress/pr-review-rule-convergence
plans/done/2026-08-11__pr-review-rule-convergence`, update the two plan indexes, run C3 and C5, then
create and merge the `docs/pr-review-rule-convergence-closeout` archival PR before P5-004.

- [ ] [AI] [P5-001] Triage every `learnings.md` item: move reusable items into an existing/new
      `plans/ideas/` two-pager, or record the explicit none outcome — acceptance: no untriaged learning
      remains.
- [ ] [AI] [P5-002] Move the completed plan to `plans/done/YYYY-MM-DD__pr-review-rule-convergence/`
      and update plan indexes — acceptance: archival is included in the public delivery boundary.
- [ ] [AI] [P5-003] Reconcile `git status --short` with the full file-touch ledger — acceptance:
      no foreign file is staged or committed.
- [ ] [AI] [P5-004] Run C7 in `worktrees/ose-new-rules/`, verify its public delivery units and archival
      PR are complete, then run C8 against `worktrees/ose-new-rules/` — acceptance: only this plan's clean
      public worktree is removed immediately; no root checkout, broad path, glob, or foreign worktree is targeted.

### Phase 5 Gate

- [ ] [AI] [P5-005] Confirm all delivery nodes P0–P5 have evidence, planned indexes are current, and
      only repository root checkouts remain — acceptance: the plan has a safe terminal state.

> **Pause Safety:** The implementation is archived, all exact plan worktrees are removed, and root checkouts remain for final synchronization.
