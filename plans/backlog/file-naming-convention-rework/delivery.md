# Delivery — File Naming Convention Rework (WS-B)

**Delivery Mode**: `worktree-to-pr` (mandatory). WS-B1 and WS-B2 are static prose and need a green
`pr-quality-gate.yml`; WS-B3 is executable and runs a CI-gated review cycle.

**Worktree**: `ose-public/worktrees/file-naming-rework/` on branch `worktree/file-naming-rework`, plus
an `ose-private` mirror provisioned at Phase 4. Phase 0 opens no PR.

**Delivery boundaries**: two. WS-B1 + WS-B2 ship together (one convention pair, one reader-facing
change). WS-B3 ships separately because it changes code.

**Executor legend**: `[AI]` — an agent performs it. `[HUMAN]` — requires a person.

## Phase 0: Baseline and Derivation

_Suggested executor:_ `repo-setup-manager`, then the orchestrator

- [ ] [AI] Provision the `ose-public` worktree and branch — acceptance: `git worktree list` shows it
      and `git status --short` is empty.
- [ ] [AI] Run `npm install` and `npm run doctor -- --fix` — acceptance: both exit 0.
- [ ] [AI] Derive the enforced exemption set from `naming.rs` **by reading the source**, and record it
      to `local-tmp/file-naming-rework/enforced-set.md` — acceptance: the file lists each exempt
      basename with the source line number.
- [ ] [AI] Derive the `md-naming` gate's `args.exempt` globs from `repo-config.yml` in **both**
      repositories — acceptance: both lists are recorded separately; any difference between the
      repositories is stated, not reconciled.
- [ ] [AI] Record the current word count of `file-naming.md` and `ordinal-filename-prefixes.md` in
      both repositories — acceptance: four figures, each with its distance from the 500-word FAIL
      threshold.
- [ ] [AI] Count the files each candidate WS-B2 range rule would rename, against the real tree in both
      repositories — acceptance: one count per candidate per repository, produced by command.
- [ ] [AI] Enumerate every surface restating either rule, per repository, with a per-file verdict —
      acceptance: the list names the rules-machinery agents, both skills, the quality-gate workflow
      shards, and `governance-word-budget-remediation.md`, or explicitly records each as not stating
      the rule.

### Phase 0 Gate

- [ ] [AI] `enforced-set.md` exists and every entry carries a source line number.
- [ ] [AI] The four word counts are recorded.
- [ ] [AI] The WS-B2 candidate rename counts exist for both repositories.
- [ ] [AI] The propagation enumeration has a verdict for every file it lists.

> **Pause Safety**: nothing is modified. Safe to stop. To resume: re-read `local-tmp/file-naming-rework/`.

## Phase 1: WS-B1 — Reconcile `file-naming.md`

_Suggested executor:_ `repo-rules-maker`, verified by the orchestrator

- [ ] [AI] Decide and record the `*__linkedin__*.md` disposition — acceptance: the decision is one of
      "stated repository-internal exception with its reason" or "rename the scheme", written down with
      the reason, before any prose is edited.
- [ ] [AI] Write the admission criterion (an externally-mandated fixed filename) into the convention —
      acceptance: the criterion appears, and every listed exemption is justified against it or marked
      as a repository-internal exception.
- [ ] [AI] Create the `file-naming/exemptions.md` child shard carrying the full list — acceptance: the
      parent stays under 500 words, the child is under 500, and the parent's Children section links it.
- [ ] [AI] Document `_index.md` explicitly against the "no underscores" clause — acceptance: the
      clause and the exemption are stated in the same place, so neither can be read without the other.
- [ ] [AI] Replace the "and similar locations" scope clause with an evaluable path expression —
      acceptance: `grep -cF 'and similar' file-naming.md` returns 0, and the new clause matches what
      the gate walks.
- [ ] [AI] Distinguish enforced from convention-only extensions — acceptance: the convention states
      that only `.md` is gated, and lists the others as convention-only.
- [ ] [AI] Run the reconciliation both directions — acceptance: every enforced exemption appears in the
      convention **and** every convention-stated exemption is enforced; both lists are printed and
      compared, not eyeballed.

### Phase 1 Gate

- [ ] [AI] `governance word-budget validate` exits 0 with no FAIL on either file.
- [ ] [AI] `governance readme-index validate` (gate args) exits 0 — the new shard is indexed.
- [ ] [AI] `rhino md links validate --exclude plans/done` exits 0.
- [ ] [AI] `repo-governance vendor validate` exits 0.
- [ ] [AI] The two-directional reconciliation is recorded and shows zero unmatched entries.

## Phase 2: WS-B2 — Repair the ordinal convention

_Suggested executor:_ `repo-rules-maker`, verified by the orchestrator

- [ ] [AI] Choose the range rule from the Phase 0 counts and record the choice with its rename count —
      acceptance: the chosen rule and the number of files it would affect in each repository are both
      written down.
- [ ] [AI] Move the range clause above the worked-cases table — acceptance: no table row depends on
      text below the table.
- [ ] [AI] Rewrite the `02-step-1-and-2-maker-and-checker.md` row so its verdict matches the chosen
      rule — acceptance: the row's Fails/Passes label and its arrow agree.
- [ ] [AI] Re-audit **every** row against the rule, not only the contradictory one — acceptance: each
      row carries an explicit verdict re-derived after the change, per Iron Rule 3.
- [ ] [AI] Re-run each repository's published non-vacuity command — acceptance: `ose-public`'s claim of
      non-vacuity and `ose-private`'s claim of vacuity each still hold, or the claim is restated.

### Phase 2 Gate

- [ ] [AI] No worked-case row's verdict contradicts the rule stated above it.
- [ ] [AI] Both repositories' non-vacuity commands run without error and match their copy's claim.
- [ ] [AI] `governance word-budget validate` and `readme-index validate` exit 0.

## Phase 3: Propagation

_Suggested executor:_ `repo-rules-fixer`

- [ ] [AI] Apply the reconciled rules to every surface from the Phase 0 enumeration — acceptance: each
      enumerated file has a recorded disposition (edited, or verified as not stating the rule).
- [ ] [AI] Run `npm run generate:bindings` and `npm run validate:sync` — acceptance: both exit 0 and
      no mirror was hand-edited.

### Phase 3 Gate

- [ ] [AI] Every Phase 0 enumeration entry has a disposition.
- [ ] [AI] `npm run validate:sync` and `harness bindings validate` exit 0.
- [ ] [HUMAN] Open the WS-B1+B2 PR; merge once `pr-quality-gate.yml` is green.

> **Pause Safety**: the prose half is shippable on its own. Safe to stop after the merge.

## Phase 4: `ose-private` Parity (prose)

- [ ] [AI] Re-derive `ose-private`'s own facts by command before editing — acceptance: its exemption
      list, word counts, and non-vacuity result are produced there, never copied from `ose-public`.
- [ ] [AI] Provision `ose-private/worktrees/file-naming-rework/` — acceptance: `git worktree list`
      shows it and the tree is clean.
- [ ] [AI] Apply WS-B1, WS-B2, and the propagation there — acceptance: the same gates exit 0 in
      `ose-private`.

### Phase 4 Gate

- [ ] [AI] `word-budget`, `readme-index`, `md links`, `vendor validate`, `validate:sync` all exit 0 in
      `ose-private`.
- [ ] [AI] Both repositories state the same rule; every per-repository figure was re-derived there.
- [ ] [HUMAN] Open the `ose-private` PR; merge once green.

## Phase 5: WS-B3 — Collision verdict and emitter refusal

_Suggested executor:_ `repo-rules-maker` for the verdict, `swe-rust-dev` for the emitter

- [ ] [AI] State the collision verdict in `ordinal-filename-prefixes.md` — acceptance: the convention
      says whether the ordinal is kept, why, and what to do instead; the 40 `ose-private` instances are
      covered by the wording.
- [ ] [AI] Add the emitter scenarios from `prd.md` to `specs/apps/rhino/` — acceptance:
      `specs structure validate` exits 0.
- [ ] [AI] RED: a unit test where a split would emit two basenames equal after ordinal-stripping —
      acceptance: fails today by writing both files.
- [ ] [AI] GREEN: refuse before writing, with both candidate names in the message — acceptance: the
      RED test passes and no file is written on the failure path.
- [ ] [AI] Add a near-miss test — stems differing by one character — that must still be allowed —
      acceptance: passes, proving the check is not over-broad.
- [ ] [AI] Regenerate and stage the parity checksum manifest — acceptance: `parity manifest validate`
      exits 0.
- [ ] [AI] Apply WS-B3 to `ose-private` byte-identically — acceptance: `parity manifest validate` exits
      0 in both repositories.

### Phase 5 Gate

- [ ] [AI] `npx nx run rhino-cli:test`, `:test:integration`, and `:lint` exit 0 in both repositories.
- [ ] [AI] The collision refusal fires on a collision and does not fire on a near miss. Both asserted.
- [ ] [AI] `parity manifest validate` exits 0 in both repositories.
- [ ] [HUMAN] Open the WS-B3 PRs; merge once green.

## Phase 6: Knowledge Capture

- [ ] [AI] Triage every `learnings.md` entry through the
      [Knowledge Capture](../../../repo-governance/development/quality/knowledge-capture.md) routing
      matrix — acceptance: every entry reaches a terminal state, or the file carries the explicit
      `No generalizable learnings — <reason>` escape.
- [ ] [AI] Run both safety gates on every surviving entry — acceptance: each records a verdict.
- [ ] [AI] File the corrective rename of the 40 collision files as its own follow-up — acceptance: a
      `plans/backlog/` folder exists, or the verdict explicitly says no rename is needed.

### Phase 6 Gate

- [ ] [AI] `learnings.md` has no untriaged entry.
- [ ] [AI] The 40-file rename has a terminal disposition.

## Phase 7: Archival

- [ ] [AI] Move the plan to `plans/done/<YYYY-MM-DD>__file-naming-convention-rework/` — acceptance: the
      folder exists only under `done/`.
- [ ] [AI] Update `plans/README.md`, `plans/backlog/README.md`, and `plans/done/README.md` —
      acceptance: `governance readme-index validate` exits 0.
- [ ] [AI] Remove both worktrees non-force and prune — acceptance: `git worktree list` shows no plan
      worktree in either repository.
- [ ] [AI] Delete `local-tmp/file-naming-rework/` in both repositories — acceptance: neither path
      exists.

### Phase 7 Gate

- [ ] [AI] All PRs show `MERGED`.
- [ ] [AI] Both root checkouts are level with `origin/main`.
