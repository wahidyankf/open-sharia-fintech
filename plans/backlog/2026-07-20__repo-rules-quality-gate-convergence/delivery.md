# Delivery — Repo Rules Quality Gate Convergence

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase
> is not complete until its gate is green; do not start phase N+1 while any gate check fails.
>
> **Acceptance-clause forms used in this plan** — this plan is subject to the standards its sibling
> installs. Every clause below uses occurrence-unique counts
> (`command grep -ohE '…' file | sort -u | wc -l`) rather than `grep -c` alternation thresholds; `test -f`
> for existence rather than a count claim; no `grep -L`; no multi-file `grep -c`; and every fenced
> block indented to its list item's content column. Every stated pre-edit value was **measured on
> `main` at `a207b66e7` during authoring**.
>
> **Search-tool validity (DECISION 10 — binds every clause in this file)** — in this environment
> `grep` resolves to **ugrep**, which REJECTS ripgrep's `--glob`; with `2>/dev/null` appended, a hard
> failure is indistinguishable from a clean zero (measured: broken form 0 hits, POSIX `--include`
> form 543 hits, same pattern, same tree). Every sweep clause in this plan therefore uses
> `command grep … --include=…` or `/opt/homebrew/bin/rg` **by absolute path**, NEVER suppresses
> stderr, and — for any clause whose passing value is **zero** — runs a known-positive control probe
> first. Catalogue enumeration uses `find -print0`, never parsed `ls` output (hyperlink escapes eat
> leading characters and silently corrupt the diff).
>
> **Perishable evidence** — the corrective commits cited by this plan live on the unmerged branch
> `parallel-orchestration-shared-machine-governance`, not on `main`: the original twelve
> (`c23ae520b..c30ac344e`) plus the five from the PR-review session that produced BS-13/14/15
> (`e46235226`, `b61e29754`, `3ee6323b7`, `f5f819642`, `72af8ab83`). Steps that resolve a SHA MUST do
> so defensively (`git cat-file -t <sha>` first) and fall back to the inline evidence in
> [tech-docs.md](./tech-docs.md#blind-spot-class-registry--seed-content) when it no longer resolves.
> See README DECISION 8.

## Worktree

Worktree path: `worktrees/repo-rules-quality-gate-convergence/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree repo-rules-quality-gate-convergence
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before deleting
the worktree after the plan is archived and pushed.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Work happens in `worktrees/repo-rules-quality-gate-convergence/`; each phase group lands as a draft
PR against `main`; `[AI]` commits and pushes to the PR branch; the PR-Review Maker→Fixer Cycle (3
sequential CI-gated cycles) runs before the `[HUMAN]` merge. See the
[PR Review Quality Gate workflow](../../../repo-governance/workflows/pr/pr-review-quality-gate.md).

## Parallelization

Phases 2 and 3 are independent and may run concurrently; Phases 7 and 8 likewise. Phase 5B depends
on Phase 5 and is not parallelizable with it. Respect the repo's concurrency cap per
[Subagent Orchestration](../../../repo-governance/development/agents/subagent-orchestration.md).

---

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_

- [ ] [AI] Provision the worktree: `git worktree add worktrees/repo-rules-quality-gate-convergence origin/main`
      — acceptance: `test -d worktrees/repo-rules-quality-gate-convergence/.git || test -f worktrees/repo-rules-quality-gate-convergence/.git`
      succeeds
- [ ] [AI] Install dependencies in the root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized
- [ ] [AI] Converge the toolchain in the root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift
- [ ] [AI] Record the baseline commit SHA into `learnings.md` in exactly this literal format —
      `Baseline SHA: <full-40-char-sha>` — obtained via `git rev-parse HEAD`
      — acceptance: `command grep -ohE '^Baseline SHA: [0-9a-f]{40}$' plans/backlog/2026-07-20__repo-rules-quality-gate-convergence/learnings.md | sort -u | wc -l`
      returns exactly 1 (returns 0 before this step)
- [ ] [AI] Record the **pre-change `repo-rules-checker` validation-step inventory** into
      `learnings.md` as the list of every `### Step <n>` heading, obtained via
      `command grep -ohE '^### Step [0-9.]+[^\n]*' .claude/agents/repo-rules-checker.md | sort -u`
      — acceptance: the recorded inventory is non-empty; this is the AC-15 baseline
- [ ] [AI] **Resolve the evidence-branch availability question** (README DECISION 8): run
      `git cat-file -t c30ac344e` and record in `learnings.md` whether the twelve corrective SHAs
      still resolve in this worktree, and whether
      `git merge-base --is-ancestor c30ac344e origin/main` succeeds
      — acceptance: both results recorded; if the SHAs do not resolve, every later replay step uses
      the inline evidence path and this is noted in `learnings.md`
- [ ] [AI] Record the **candidate-set size** for the archived chain's governing document, to size
      DD-3 before building the validator: count documents linking to
      `repo-governance/development/workflow/trunk-based-development.md` via
      `command grep -orhE 'trunk-based-development\.md' --include='*.md' . | wc -l`
      — acceptance: an integer is recorded in `learnings.md`; DD-3's bounding claim becomes decidable
      on evidence rather than assumed
- [ ] [AI] **Establish the search-tool baseline** (DECISION 10) — record in `learnings.md` the
      output of all three forms against one known-positive pattern, so every later zero-asserting
      clause has a calibrated control:
      `grep -rn --glob '*.md' 'Trunk Based Development' . 2>/dev/null | wc -l`,
      `command grep -rn --include='*.md' 'Trunk Based Development' . | wc -l`, and
      `/opt/homebrew/bin/rg -c --glob '*.md' 'Trunk Based Development' . | wc -l`
      — acceptance: three integers recorded; the first is **0** and the second is **non-zero**,
      confirming the ugrep `--glob` trap is live in this worktree. If the first is non-zero, the
      environment differs from the authoring environment and this is recorded in `learnings.md`
      before any later sweep is trusted
- [ ] [AI] Establish the test baseline: `npx nx affected -t typecheck lint test:quick specs:coverage`
      — acceptance: baseline pass/fail counts recorded in `learnings.md`; every preexisting failure
      documented
- [ ] [AI] Resolve all preexisting failures before proceeding
      — acceptance: re-running the baseline command reports zero failures

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift
- [ ] [AI] `npx nx affected -t typecheck lint test:quick specs:coverage` reports zero failures
- [ ] [AI] `learnings.md` contains the Baseline SHA line, the step inventory, the evidence-branch
      availability record, the candidate-set size, the search-tool baseline, and the recorded test
      baseline — verified by reading the file
- [ ] [AI] The search-tool baseline confirms the ugrep `--glob` trap (broken form 0, POSIX
      `--include` form non-zero), or records the divergence explicitly

> **Pause Safety**: only the local toolchain was verified and the baseline recorded — no plan work
> exists yet. Safe to stop indefinitely. To resume: re-run
> `npx nx affected -t typecheck lint test:quick specs:coverage` and confirm it is still clean.

---

## Phase 1: Blind-Spot Class Registry

> _Suggested executor: `repo-rules-maker`_

- [ ] [AI] Create `repo-governance/development/quality/governance-sweep-blind-spots.md` containing
      the fifteen seed classes BS-1 through BS-15 from
      [tech-docs.md §Blind-Spot Class Registry](./tech-docs.md#blind-spot-class-registry--seed-content),
      each with its symptom, **inline evidence** (commit subject plus the proving file list), the
      missing sweep form, the catching sweep form, and its detection method; plus an
      "Appending a new class" section stating that any chain surfacing a new class appends it during
      Knowledge Capture
      — acceptance: `test -f repo-governance/development/quality/governance-sweep-blind-spots.md`
      succeeds (fails today — verified absent on `main` during authoring) **and**
      `command grep -ohE 'BS-1[0-5]|BS-[1-9]' repo-governance/development/quality/governance-sweep-blind-spots.md | sort -u | wc -l`
      returns 15
- [ ] [AI] Add the **classes compose** note to the registry (AC-19): entries are lenses, not a
      partition; BS-15 is simultaneously a BS-11 instance because a byte-budget trim replaced an
      inline enumeration with a pointer to an incomplete table; a reader continues matching after
      the first class matches
      — acceptance: `command grep -ohEi 'classes compose|not a partition|lens' repo-governance/development/quality/governance-sweep-blind-spots.md | sort -u | wc -l`
      returns at least 1 (the file does not exist today, so this returns 0 before Phase 1) **and**
      the BS-15 entry cross-references BS-11 — verified by reading it
- [ ] [AI] Ensure the BS-13, BS-14 and BS-15 entries each state **why no text search and no
      inbound-link sweep reaches them**, and each name completeness-diff as the catching form, with
      BS-15 recording that its ground truth is a set of git refs rather than a file on disk (AC-18,
      AC-21)
      — acceptance: `command grep -ohEi 'completeness-diff' repo-governance/development/quality/governance-sweep-blind-spots.md | sort -u | wc -l`
      returns at least 1, and the BS-15 entry names `git branch -r` as its ground-truth source —
      verified by reading it
- [ ] [AI] Re-derive the BS-13/BS-14/BS-15 inline evidence from the **current tree** rather than
      from their (perishable) SHAs — run
      `find .github/workflows -type f -print0 | tr '\0' '\n'`, then
      `command grep -c 'web-ui-build-deploy-prod' docs/reference/system-architecture/ci-cd.md .github/workflows/README.md`,
      then `git branch -r`, and confirm each entry's stated evidence matches what the tree reports
      — acceptance: each of the three entries' evidence is confirmed against live output, or the
      entry is amended to match the tree and the divergence is recorded in `learnings.md`; note the
      evidence describes the **pre-fix** state, so an entry whose defect has since been corrected
      records that explicitly rather than being deleted
- [ ] [AI] Ensure every entry's evidence is **self-contained** per DECISION 8 — each entry states its
      commit subject and proving file list inline, with the SHA marked as a best-effort pointer
      — acceptance: `command grep -ohE 'best-effort pointer' repo-governance/development/quality/governance-sweep-blind-spots.md | sort -u | wc -l`
      returns 1 (returns 0 today), and no entry cites a SHA as its only evidence — verified by
      reading each entry
- [ ] [AI] Verify each entry's inline evidence against git **defensively**: for each cited SHA run
      `git cat-file -t <sha>`; when it resolves, confirm `git show --name-only <sha>` lists the files
      the entry claims; when it does not resolve, mark the entry `[SHA unresolvable — inline evidence
authoritative]`
      — acceptance: every entry is either git-confirmed or explicitly marked; no entry is left
      claiming unverified provenance
- [ ] [AI] Add the **Sweep forms** summary table (DECISION 7) mapping each class to its missing form
      and catching form in one scannable table
      — acceptance: `command grep -ohE 'Sweep forms' repo-governance/development/quality/governance-sweep-blind-spots.md | sort -u | wc -l`
      returns 1 (returns 0 today)
- [ ] [AI] Register the new convention in `repo-governance/development/quality/README.md` and in
      `repo-governance/development/README.md` index tables
      — acceptance: **per file** (a union count across both files would return 1 whether one or both
      were updated — a non-discriminating clause), for each of
      `repo-governance/development/quality/README.md` and `repo-governance/development/README.md`:
      `test -f <file>` succeeds and
      `command grep -ohE 'governance-sweep-blind-spots' <file> | sort -u | wc -l` returns 1 — each returns 0
      today, verified on `main` during authoring
- [ ] [AI] Cross-link the registry from the sibling acceptance-clause registry created by
      [`plans/backlog/2026-07-20__plan-quality-gate-convergence/`](../2026-07-20__plan-quality-gate-convergence/README.md)
      **only if that plan has already landed** (DECISION 6 keeps the two registries separate but
      cross-linked)
      — acceptance: if
      `test -f repo-governance/development/quality/plan-acceptance-defect-classes.md` succeeds, then
      `command grep -ohE 'plan-acceptance-defect-classes' repo-governance/development/quality/governance-sweep-blind-spots.md | sort -u | wc -l`
      returns 1; otherwise the step is recorded as deferred in `learnings.md` with the reason
- [ ] [AI] Run the markdown validators over the new file:
      `npx markdownlint-cli2 "repo-governance/development/quality/governance-sweep-blind-spots.md"`
      and `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate`
      — acceptance: 0 markdownlint errors; all links valid

### Phase 1 Gate

> All checks below must pass before starting Phase 2 or Phase 3.

- [ ] [AI] `test -f repo-governance/development/quality/governance-sweep-blind-spots.md` succeeds
- [ ] [AI] All fifteen class IDs present — the `command grep -ohE … | sort -u | wc -l` clause above
      returns 15
- [ ] [AI] The classes-compose note is present and BS-15 cross-references BS-11
- [ ] [AI] BS-13, BS-14 and BS-15 each name completeness-diff as their catching form, and BS-15
      names `git branch -r` as its ground-truth source
- [ ] [AI] Every entry is git-confirmed or explicitly marked SHA-unresolvable
- [ ] [AI] Both index READMEs each return 1 for the registry reference
- [ ] [AI] `npx nx affected -t typecheck lint test:quick specs:coverage` reports zero failures

> **Pause Safety**: the registry is a standalone governance document with no consumer yet — nothing
> references it that would break. Safe to stop. To resume: re-run the fifteen-class count clause and
> confirm it returns 15.

---

## Phase 2: Deterministic Sweep-Completeness Validator (`rhino-cli`)

> _Suggested executor: `swe-rust-dev`_
>
> **Separability**: this phase implements README DECISION 1 option A. If the decision is revisited to
> option B or C, this phase is dropped wholesale and its detection rules move into the Phase 3 agent
> contracts; no other phase changes.
>
> **Byte-identity**: `apps/rhino-cli/**` and `specs/apps/rhino/behavior/rhino-cli/gherkin/**` are
> required to be byte-identical across `ose-public`, `ose-primer` and `ose-infra` per the
> [SDLC Gate Standard](../../../docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary).
> Every change in this phase propagates verbatim in Phases 7 and 8.

- [ ] [AI] Author the Gherkin behavior tree at
      `specs/apps/rhino/behavior/rhino-cli/gherkin/repo-governance/repo-governance-sweep-completeness.feature`
      covering never-touched computation and directory-scope detection, following the shape of the
      sibling `repo-governance-vendor-audit.feature` in the same directory
      — acceptance: `test -f specs/apps/rhino/behavior/rhino-cli/gherkin/repo-governance/repo-governance-sweep-completeness.feature`
      succeeds (file is new — directory verified to exist during authoring) and
      `npx nx run rhino-cli:specs:gherkin-cardinality-validation` exits 0

### TDD cycle 1 — never-touched candidate computation

- [ ] [AI] **RED**: add a failing unit test in
      `apps/rhino-cli/src/commands/governance_sweep_completeness.rs` asserting that, given a fixture
      candidate set and a fixture set of touched files, the pass reports exactly the candidates
      absent from the touched set
      — command: `npx nx run rhino-cli:test:unit`
      — acceptance: the test fails because the module does not exist yet (module verified absent
      during authoring)
      **Gherkin (binds) →** "The validator reports candidate files no corrective commit touched"

  ```gherkin
  Scenario: The validator reports candidate files no corrective commit touched
    Given a fixture repository state with a changed governing document and a set of corrective commits
    When the deterministic sweep-completeness pass runs against that range
    Then the pass reports every candidate file that links to the governing document and appears in no corrective commit
    And the pass reports zero never-touched candidates once every such file has been touched
  ```

- [ ] [AI] **GREEN**: implement the never-touched set computation in
      `apps/rhino-cli/src/commands/governance_sweep_completeness.rs`
      — command: `npx nx run rhino-cli:test:unit`
      — acceptance: the never-touched test passes; no other rhino-cli test breaks
- [ ] [AI] **REFACTOR**: extract the candidate-set derivation (inbound links, outbound links,
      declared blast radius per DD-3) into a named helper
      — command: `npx nx run rhino-cli:test:unit`
      — acceptance: all tests still pass; the computation body contains no inline link-parsing logic

### TDD cycle 2 — directory-scoped sweep detection

- [ ] [AI] **RED**: add a failing test asserting that a sweep report whose recorded command is rooted
      at a subdirectory, with a non-empty unjustified exclusion set, yields exactly one finding
      naming the excluded top-level paths
      — command: `npx nx run rhino-cli:test:unit`
      — acceptance: the test fails (detector absent)
      **Gherkin (binds) →** "A sweep report claiming repo-wide scope while excluding a subtree is flagged"

  ```gherkin
  Scenario: A sweep report claiming repo-wide scope while excluding a subtree is flagged
    Given a sweep report whose recorded command restricts the search to a single directory
    When the deterministic sweep-completeness pass evaluates the report
    Then the pass reports a finding stating the sweep is directory-scoped without an enumerated exclusion set
    And the finding names the excluded top-level paths it detected
    And a report whose exclusions are enumerated with justifications yields no finding
  ```

- [ ] [AI] **GREEN**: implement the directory-scope detector
      — command: `npx nx run rhino-cli:test:unit`
      — acceptance: the directory-scope test passes; no other test breaks
- [ ] [AI] **REFACTOR**: unify the finding-emission shape across both detectors so they render
      identically in the audit envelope
      — command: `npx nx run rhino-cli:test:unit`
      — acceptance: all tests still pass

### Wiring

- [ ] [AI] Register the subcommand in `apps/rhino-cli/src/cli.rs` and
      `apps/rhino-cli/src/commands.rs` as `repo-governance sweep-completeness validate`
      — acceptance: `command grep -ohE 'sweep-completeness|sweep_completeness' -r apps/rhino-cli/src | sort -u | wc -l`
      returns at least 2 (returns 0 today in both files, verified on `main` during authoring)
- [ ] [AI] Register `sweep-completeness` as the **fifth category** in the `repo-governance audit`
      orchestrator at `apps/rhino-cli/src/commands/governance_audit.rs`, alongside the existing
      `layer-coherence`, `traceability-audit`, `vendor-audit` and `instruction-size`
      — acceptance: `command grep -ohE 'sweep-completeness' apps/rhino-cli/src/commands/governance_audit.rs | sort -u | wc -l`
      returns 1 (returns 0 today) and
      `./apps/rhino-cli/dist/rhino-cli repo-governance audit -o json` emits a fifth entry in
      `result.categories[]`
- [ ] [AI] Confirm the JSON envelope still validates against schema
      `rhino-cli/repo-governance-audit/v1`, so the checker's Step 0.5 parser is unaffected
      — acceptance: the emitted JSON carries the unchanged `schema` field and parses; the checker's
      existing four-category skip table remains valid with one added row
- [ ] [AI] Run the validator against fixture sweep reports reproducing BS-12 and its corrected form
      — acceptance: the BS-12 fixture yields at least 1 finding and the corrected fixture yields 0 —
      falsifiable in both directions

### Phase 2 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] `npx nx run rhino-cli:test:unit` exits 0
- [ ] [AI] `npx nx run rhino-cli:specs:behavior:coverage` exits 0
- [ ] [AI] Validator yields ≥1 finding against the BS-12 fixture and 0 against its corrected form
- [ ] [AI] `repo-governance audit -o json` emits five categories and still validates against the
      unchanged schema
- [ ] [AI] `npx nx affected -t typecheck lint test:quick specs:coverage` reports zero failures

> **Pause Safety**: the validator is additive and its findings land in the preflight envelope, which
> Step 2 of the workflow already treats as visibility-only and never counts toward the mode
> threshold — so the gate's behavior is unchanged until Phase 5 consumes it. Safe to stop. To resume:
> `npx nx run rhino-cli:test:unit`.

---

## Phase 3: Sweep Methodology Contracts

> _Suggested executor: `agent-maker`_

- [ ] [AI] Add an **Inbound-Link Sweep (Primary)** section to `.claude/agents/repo-rules-checker.md`
      requiring the checker to derive its sweep set from documents linking to the changed governing
      document, its outbound links, and the declared blast radius (DD-3), with keyword phrasing
      search demoted to a secondary lens ranking within that set; link the registry
      — acceptance: `command grep -ohEi 'inbound link|inbound-link|secondary lens' .claude/agents/repo-rules-checker.md | sort -u | wc -l`
      returns at least 2 (returns 0 today, verified on `main`) **and**
      `command grep -ohE 'governance-sweep-blind-spots' .claude/agents/repo-rules-checker.md | sort -u | wc -l`
      returns 1 (returns 0 today)
- [ ] [AI] Add a **Sweep Transcript** requirement to `.claude/agents/repo-rules-checker.md`: every
      audit report records the verbatim sweep command and the exclusion set applied, or an explicit
      statement that no exclusions were applied; a report lacking the transcript is itself an
      incomplete-evidence finding
      — acceptance: `command grep -ohEi 'sweep transcript|verbatim sweep command' .claude/agents/repo-rules-checker.md | sort -u | wc -l`
      returns at least 1 (returns 0 today)
- [ ] [AI] Add the **enumerated-exclusion rule** (DECISION 3) to the same section: a directory-scoped
      sweep is permitted only when every exclusion is enumerated as a literal glob and justified
      — acceptance: `command grep -ohEi 'enumerated|directory-scoped' .claude/agents/repo-rules-checker.md | sort -u | wc -l`
      returns at least 1 (returns 0 today)
- [ ] [AI] Add a **Class-Wide Remediation** section to `.claude/agents/repo-rules-fixer.md`: a
      finding instantiating a registry class obliges the fixer to enumerate every instance of that
      class across the sweep set in one pass and list each site with its disposition in the fix report
      — acceptance: `command grep -ohEi 'class-wide|enumerate every instance|whole-class' .claude/agents/repo-rules-fixer.md | sort -u | wc -l`
      returns at least 2 (returns 0 today, verified on `main`)
- [ ] [AI] Add a **Self-Inflicted Drift Re-Check** section to `.claude/agents/repo-rules-fixer.md`
      (closes BS-11): after applying its commits, the fixer re-examines every document it changed for
      claims its own edits falsified, and lists each site with its disposition
      — acceptance: `command grep -ohEi 'self-inflicted|own change surface|falsified by' .claude/agents/repo-rules-fixer.md | sort -u | wc -l`
      returns at least 1 (returns 0 today)
- [ ] [AI] Add a BSCR reference to `.claude/agents/repo-rules-maker.md` so rule propagation starts
      from the inbound-link set rather than from the edited file (closes BS-2)
      — acceptance: `command grep -ohE 'governance-sweep-blind-spots' .claude/agents/repo-rules-maker.md | sort -u | wc -l`
      returns 1 (returns 0 today)
- [ ] [AI] Add the sweep methodology to
      `repo-governance/development/pattern/maker-checker-fixer.md` §Preventing Iteration Loops as a
      fifth safeguard, so the pattern convention (not just the agents) carries it
      — acceptance: `command grep -ohEi 'inbound link|inbound-link|sweep transcript' repo-governance/development/pattern/maker-checker-fixer.md | sort -u | wc -l`
      returns at least 1 (returns 0 today, verified on `main`)
- [ ] [AI] Verify no vendor-specific content entered any `repo-governance/` file edited in this phase
      per the [Governance Vendor-Independence Convention](../../../repo-governance/conventions/structure/governance-vendor-independence.md)
      — acceptance: `npx nx run rhino-cli:governance:vendor-audit-validation` exits 0

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] All seven surface-edit acceptance clauses above return their stated post-edit values
- [ ] [AI] `npx nx run rhino-cli:governance:vendor-audit-validation` exits 0
- [ ] [AI] `npx nx run rhino-cli:instruction-size:validation` exits 0 — no agent file exceeded its
      size budget
- [ ] [AI] `npx nx affected -t typecheck lint test:quick specs:coverage` reports zero failures

> **Pause Safety**: the sweep contracts are strictly additive — an agent that ignores them behaves
> exactly as before, and termination still uses today's double-zero rule until Phase 5. No surface is
> left half-migrated. Safe to stop. To resume: re-run the seven acceptance clauses above.

---

## Phase 4: Evidence Grounding and False-Alarm Guards

> _Suggested executor: `agent-maker`_
>
> This phase closes the observed false alarm, whose blast radius would have been three repositories.

- [ ] [AI] Add an **Evidence Grounding** section to `.claude/agents/repo-rules-checker.md` encoding
      DD-5 rule A: a claim about mechanical behavior is verified against the implementing workflow,
      hook or script file, never against another document restating it, and the audit cites the
      implementing file and line
      — acceptance: `command grep -ohEi 'implementing file|mechanism file|never against another document' .claude/agents/repo-rules-checker.md | sort -u | wc -l`
      returns at least 1 (returns 0 today, verified on `main`)
- [ ] [AI] Add the **Validator Invocation Parity** rule (DD-5 rule B) to the same section: a validator
      invocation cited as evidence must match the flags CI uses, or record a written justification
      for diverging; findings from an unjustified bare invocation are rejected as unverified
      — acceptance: `command grep -ohEi 'invocation parity|CI.s exact flags|same flags CI' .claude/agents/repo-rules-checker.md | sort -u | wc -l`
      returns at least 1 (returns 0 today)
- [ ] [AI] Document the concrete observed instance inline in the same section as a worked example:
      CI invokes `md mermaid validate` with
      `--exclude apps/rhino-cli/tests/fixtures --exclude plans/done`
      (`.github/workflows/main-ci.yml`), while the `package.json` lint-staged entry uses the bare
      form; the bare form flags the validator's own negative fixtures
      — acceptance: `command grep -ohE 'apps/rhino-cli/tests/fixtures' .claude/agents/repo-rules-checker.md | sort -u | wc -l`
      returns 1 (returns 0 today) — and the two invocations quoted in the agent match the two files
      verbatim, confirmed by reading both sources rather than trusting this plan's quotation of them
- [ ] [AI] Add the corresponding re-validation rule to `.claude/agents/repo-rules-fixer.md`: before
      acting on a finding sourced from a validator invocation, confirm the invocation carried CI's
      flags; otherwise mark the finding FALSE_POSITIVE rather than manufacturing a fix
      — acceptance: `command grep -ohEi 'invocation parity|CI.s exact flags|same flags CI' .claude/agents/repo-rules-fixer.md | sort -u | wc -l`
      returns at least 1 (returns 0 today)
- [ ] [AI] Add a guard note to the same fixer section: a finding inside `apps/rhino-cli/**` or
      `specs/apps/rhino/behavior/rhino-cli/gherkin/**` carries a three-repository blast radius per the
      byte-identity boundary and requires the parity check to pass before any edit
      — acceptance: `command grep -ohE 'byte-identical|byte-identity' .claude/agents/repo-rules-fixer.md | sort -u | wc -l`
      returns at least 1 (returns 0 today)

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [ ] [AI] All five acceptance clauses above return their stated post-edit values
- [ ] [AI] The quoted CI and lint-staged invocations in the agent match their source files verbatim —
      verified by reading `.github/workflows/main-ci.yml` and `package.json`, not by trusting this
      plan's transcription of them
- [ ] [AI] `npx nx run rhino-cli:instruction-size:validation` exits 0
- [ ] [AI] `npx nx affected -t typecheck lint test:quick specs:coverage` reports zero failures

> **Pause Safety**: evidence-grounding rules are additive constraints on how findings are justified;
> nothing about the loop's control flow has changed yet. Safe to stop. To resume: re-run the five
> clauses above.

---

## Phase 5: Adversarial Termination and Convergence Correction

> _Suggested executor: `repo-workflow-maker`_
>
> This is the phase that changes the gate's control flow. Everything before it is additive.

- [ ] [AI] Add `sweep-completeness` to the Step 0.5 category table in
      `repo-governance/workflows/repo/repo-rules-quality-gate.md`, documenting it as the fifth
      category of the `repo-governance audit` orchestrator
      — acceptance: `command grep -ohE 'sweep-completeness' repo-governance/workflows/repo/repo-rules-quality-gate.md | sort -u | wc -l`
      returns 1 (returns 0 today, verified on `main`)
- [ ] [AI] Add the matching row to the **deterministic skip set** table in
      `.claude/agents/repo-rules-checker.md` Step 0.5, so the checker knows the never-touched
      computation is already covered and must not AI-re-derive it
      — acceptance: `command grep -ohE 'sweep-completeness' .claude/agents/repo-rules-checker.md | sort -u | wc -l`
      returns 1 (returns 0 today)
- [ ] [AI] Insert the **Adversarial Round** as an explicit workflow step between the double-zero check
      and finalization: its agenda is the mechanical never-touched candidate set, it runs exactly
      once, and a non-zero result routes back to the fixer
      — acceptance: `command grep -ohEi 'adversarial' repo-governance/workflows/repo/repo-rules-quality-gate.md | sort -u | wc -l`
      returns at least 1 (returns 0 today, verified on `main`)
- [ ] [AI] Rewrite §Termination Criteria so `pass` requires: two consecutive zero threshold-level
      validations, **plus** a zero adversarial round, **plus** an empty never-touched candidate set —
      and so that an empty adversarial agenda is recorded explicitly with its derivation
      — acceptance: `command grep -ohEi 'never-touched|adversarial' repo-governance/workflows/repo/repo-rules-quality-gate.md | sort -u | wc -l`
      returns at least 2, and the Termination Criteria section names all three preconditions —
      verified by reading the section
- [ ] [AI] Update the `termination` frontmatter field in the same workflow to describe the
      adversarial rule
      — acceptance: the frontmatter `termination:` value names the adversarial round — verified by
      reading the frontmatter
- [ ] [AI] Correct the falsified convergence guidance (DD-7) in
      `repo-governance/development/pattern/maker-checker-fixer.md` §Preventing Iteration Loops:
      replace the 1-3 iteration claim and the escalate-after-5 rule with the phased budget
      (deterministic pass, bounded semantic budget, one adversarial round), citing the archived
      13-round chain as the falsifying evidence
      — acceptance: `command grep -ohE 'converge in 1-3 iterations' repo-governance/development/pattern/maker-checker-fixer.md | sort -u | wc -l`
      returns 0 after the edit (**returns 1 today** — phrase verified present on `main` during
      authoring) **and** `command grep -ohE 'after 5 iterations' repo-governance/development/pattern/maker-checker-fixer.md | sort -u | wc -l`
      returns 0 after the edit (**returns 1 today**) **and** the section states the phased budget
      instead — verified by reading it
- [ ] [AI] Reconcile the workflow's `max-iterations` frontmatter default (currently 7, escalation
      warning at 5) with the new phased budget, so the two surfaces do not contradict each other
      — acceptance: the workflow's frontmatter and the pattern convention describe the same budget
      shape — verified by reading both; any residual disagreement is itself a BS-2 instance and must
      be closed before the gate

### Phase 5 Gate

> All checks below must pass before starting Phase 5B.

- [ ] [AI] Adversarial round present in the workflow and ordered before finalization
- [ ] [AI] Termination criteria name all three preconditions (double zero, adversarial zero, empty
      never-touched set)
- [ ] [AI] **Control probe first** (DECISION 10 — both clauses below assert a ZERO, so the search
      tool must be proven working before its zero is trusted):
      `command grep -ohE 'Preventing Iteration Loops' repo-governance/development/pattern/maker-checker-fixer.md | sort -u | wc -l`
      returns at least 1
- [ ] [AI] `command grep -ohE 'converge in 1-3 iterations' repo-governance/development/pattern/maker-checker-fixer.md | sort -u | wc -l`
      returns 0 (returned 1 pre-edit, measured on `main` during authoring)
- [ ] [AI] `command grep -ohE 'after 5 iterations' repo-governance/development/pattern/maker-checker-fixer.md | sort -u | wc -l`
      returns 0 (returned 1 pre-edit)
- [ ] [AI] The workflow frontmatter and the pattern convention agree on the budget shape
- [ ] [AI] `npx nx run rhino-cli:naming:workflows-validation` exits 0
- [ ] [AI] `npx nx affected -t typecheck lint test:quick specs:coverage` reports zero failures

> **Pause Safety**: the workflow is internally consistent — the validator from Phase 2 is consumed by
> termination, and no step references a mechanism that does not exist. Safe to stop. To resume:
> re-read §Termination Criteria.

---

## Phase 5B: Guard Placement, Search-Tool Validity, and Cycle Termination

> _Suggested executor: `agent-maker`, with `repo-workflow-maker` for the PR-workflow edits_
>
> This phase carries the three mechanisms added from the PR-review session — DECISIONs 9, 10, 12 and 13. It depends on Phase 5's termination rewrite because DD-12 mirrors DD-6's shape and the two
> must land describing the same rule.

### Guard placement (DECISION 9 / DD-9)

- [ ] [AI] Add a **Guard Placement** section to
      `repo-governance/development/pattern/maker-checker-fixer.md` stating the
      **enumeration-fails-open rule**: any safety property expressed as an enumeration fails open on
      the member nobody listed; prefer properties expressed by what they **protect** over what they
      **enumerate**; a guard is co-located with every rewrite that could violate the invariant, and
      an umbrella clause is documentation, never the mechanism (AC-22)
      — acceptance: `command grep -ohEi 'fails open|point of rewrite|what they protect' repo-governance/development/pattern/maker-checker-fixer.md | sort -u | wc -l`
      returns at least 2 (control probe: the same file returns at least 1 for
      `command grep -ohE 'Preventing Iteration Loops' … | sort -u | wc -l`; the target clause returns
      0 pre-edit, measured on `main` during authoring)
- [ ] [AI] Add the **entry-path verification** rule to `.claude/agents/repo-rules-fixer.md`: guard
      coverage is established by enumerating every way an agent **enters** the file (finding type,
      step number, invocation mode) and tracing each path to the guard before any rewrite; a
      section's own claim to bind every recipe is NOT accepted as evidence of coverage (AC-23)
      — acceptance: `command grep -ohEi 'entry path|entry-path|before any rewrite' .claude/agents/repo-rules-fixer.md | sort -u | wc -l`
      returns at least 1 (returns 0 pre-edit, measured on `main` during authoring)
- [ ] [AI] Record the five-axis worked example inline in the same section — tag value, verb,
      delivery mode, confidence level, finding type — naming the decisive fifth axis: a recipe with
      no enforcement pointer is reachable by a finding type that never mentions the invariant
      — acceptance: `command grep -ohEi 'finding type' .claude/agents/repo-rules-fixer.md | sort -u | wc -l`
      returns at least 1, and the section lists all five axes — verified by reading it
- [ ] [AI] Cross-reference BS-12 and BS-15 from the new rule as its two registry instances
      — acceptance: `command grep -ohE 'BS-12|BS-15' repo-governance/development/pattern/maker-checker-fixer.md | sort -u | wc -l`
      returns 2

### Search-tool validity (DECISION 10 / DD-11)

- [ ] [AI] Add a **Search-Tool Validity** section to `.claude/agents/repo-rules-checker.md`
      requiring, for any sweep whose conclusion is "nothing found": the verbatim command recorded,
      stderr NOT suppressed, an invocation form the tool accepts (POSIX `--include`, or
      `/opt/homebrew/bin/rg` by absolute path), and a known-positive control probe returning
      non-zero before the zero is trusted (AC-24)
      — acceptance: `command grep -ohEi 'control probe|known-positive|stderr' .claude/agents/repo-rules-checker.md | sort -u | wc -l`
      returns at least 2 (returns 0 pre-edit, measured on `main` during authoring)
- [ ] [AI] Document the measured trap inline as the worked example: `grep` resolves to ugrep, which
      rejects ripgrep's `--glob`; the broken form returned **0** where POSIX `--include` returned
      **543** on the same pattern and tree; and `ls` output carries hyperlink escapes that corrupt
      catalogue diffs, so enumeration uses `find -print0`
      — acceptance: `command grep -ohE 'ugrep|find -print0' .claude/agents/repo-rules-checker.md | sort -u | wc -l`
      returns 2 (returns 0 pre-edit)
- [ ] [AI] Add the mirrored rule to `.claude/agents/repo-rules-fixer.md`: a finding whose evidence is
      a zero-result sweep without a passing control probe is marked `FALSE_POSITIVE` pending
      re-verification rather than acted on
      — acceptance: `command grep -ohEi 'control probe' .claude/agents/repo-rules-fixer.md | sort -u | wc -l`
      returns at least 1 (returns 0 pre-edit)

### Completeness-diff contract (DECISION 11 / DD-10)

- [ ] [AI] Add a **Completeness-Diff** section to `.claude/agents/repo-rules-checker.md`: for any
      document describing an enumerable ground truth, enumerate the ground truth from its
      authoritative source and diff the document against it; the report NAMES the source; an unnamed
      source is itself an incomplete-evidence finding
      — acceptance: `command grep -ohEi 'completeness-diff|ground truth' .claude/agents/repo-rules-checker.md | sort -u | wc -l`
      returns at least 2 (returns 0 pre-edit, measured on `main` during authoring)
- [ ] [AI] Add the **not-a-file-on-disk rider** to the same section, with the three evidenced
      ground-truth sources tabulated: workflow `on:` blocks (BS-13),
      `find .github/workflows -type f -print0` (BS-14), and `git branch -r` (BS-15)
      — acceptance: `command grep -ohE 'git branch -r' .claude/agents/repo-rules-checker.md | sort -u | wc -l`
      returns 1 (returns 0 pre-edit) and all three sources are tabulated — verified by reading

### Review-cycle termination (DECISIONs 12 and 13 / DD-12, DD-13)

- [ ] [AI] Rewrite the cycle-termination rule in
      `repo-governance/workflows/pr/pr-review-quality-gate.md`: a cycle producing any **new**
      blocking finding extends the loop; termination requires a cycle producing **no new** finding;
      the fixed default count becomes a floor, not a ceiling (AC-25)
      — acceptance: `command grep -ohEi 'no new finding|evidence-based|extends the loop' repo-governance/workflows/pr/pr-review-quality-gate.md | sort -u | wc -l`
      returns at least 1 (returns 0 pre-edit, measured on `main` during authoring)
- [ ] [AI] Add the **negative-finding licence** requirement to the same file: every cycle's
      verification prompt must explicitly permit refuting the requester's hypothesis, citing the
      observed case where a reviewer told "assume the previous fix introduced a defect" reported the
      hypothesis wrong and found a real defect elsewhere
      — acceptance: `command grep -ohEi 'refut|negative finding' repo-governance/workflows/pr/pr-review-quality-gate.md | sort -u | wc -l`
      returns at least 1 (returns 0 pre-edit)
- [ ] [AI] Replace the thread-state merge precondition in the same file with a **committed-fix**
      precondition (gap D1): every finding's fix is verified present in the pushed diff; the count of
      unresolved threads is NOT accepted as evidence that findings were fixed (AC-26)
      — acceptance: `command grep -ohEi 'committed and pushed|pushed diff|unresolved threads' repo-governance/workflows/pr/pr-review-quality-gate.md | sort -u | wc -l`
      returns at least 1 (returns 0 pre-edit)
- [ ] [AI] Add the **review-state caveat** for gap D2 (which is NOT fixed here — see DECISION 13):
      `pr-review-maker` posts as `COMMENT` because `gh` authenticates as the PR author and GitHub
      rejects `REQUEST_CHANGES` on one's own PR, so merge preconditions gate on **finding text**,
      never on GitHub's review state
      — acceptance: `command grep -ohEi 'REQUEST_CHANGES|review state' repo-governance/workflows/pr/pr-review-quality-gate.md | sort -u | wc -l`
      returns at least 1 (returns 0 pre-edit)
- [ ] [AI] Verify no vendor-specific content entered any `repo-governance/` file edited in this phase
      — acceptance: `npx nx run rhino-cli:governance:vendor-audit-validation` exits 0

### Phase 5B Gate

> All checks below must pass before starting Phase 6.

- [ ] [AI] Every acceptance clause in this phase returns its stated post-edit value, and every
      zero-asserting clause ran its control probe first
- [ ] [AI] The enumeration-fails-open rule is present in `maker-checker-fixer.md` and cross-links
      BS-12 and BS-15
- [ ] [AI] Guard coverage for the entry-path rule is itself verified by entry-path enumeration —
      enumerate every finding type that routes a fixer into `.claude/agents/repo-rules-fixer.md` and
      confirm each reaches the guard before any rewrite; a single bypassing path fails this gate
- [ ] [AI] `repo-governance/workflows/pr/pr-review-quality-gate.md` describes evidence-based
      termination, the negative-finding licence, the committed-fix precondition, and the D2 caveat
- [ ] [AI] `npx nx run rhino-cli:governance:vendor-audit-validation` exits 0
- [ ] [AI] `npx nx run rhino-cli:instruction-size:validation` exits 0
- [ ] [AI] `npx nx affected -t typecheck lint test:quick specs:coverage` reports zero failures

> **Pause Safety**: all three new contracts are additive text; the PR-review workflow's new
> termination rule is strictly more conservative than the count it replaces (it can only extend a
> loop, never shorten one), so stopping here leaves every gate at least as strict as before. Safe to
> stop. To resume: re-run the acceptance clauses in this phase.

---

## Phase 6: Historical Replay, Bindings, and the ose-public PR

- [ ] [AI] Build replay fixtures reproducing the archived chain's blind-spot states — at minimum the
      round-11 state (`.github/`, `specs/` and root files untouched while the sweep claimed repo-wide
      scope) and the post-final state (all touched)
      — acceptance: two fixture states exist; if the evidence SHAs no longer resolve (Phase 0
      record), fixtures are constructed from the inline evidence in the registry instead, and this is
      noted in `learnings.md`
- [ ] [AI] Run the Phase 2 validator against both replay fixtures
      — acceptance: the round-11 fixture yields a non-zero never-touched count naming `.github/` and
      `specs/` candidates, and the post-final fixture yields **zero** — falsifiable in both
      directions
- [ ] [AI] **Replay the completeness-diff contract against the three BS-13/14/15 pre-fix states**
      (AC-20, AC-21): reconstruct the `.github/workflows/README.md` trigger row omitting
      `push: branches: [main]`, the catalogues missing `web-ui-build-deploy-prod.yml` and
      `apps-web-ui-storybook-deployer`, and the `AGENTS.md` enumeration covering 8 of the 11 branches
      — acceptance: the contract reports a finding for each of the three pre-fix states and **zero**
      against the corrected states; the BS-15 replay enumerates `git branch -r` rather than the
      on-disk table, and a run that enumerates only on-disk artifacts is confirmed to MISS it —
      falsifiable in both directions
- [ ] [AI] Verify the AC-15 no-check-removed invariant: re-derive the `repo-rules-checker` step
      inventory via `command grep -ohE '^### Step [0-9.]+[^\n]*' .claude/agents/repo-rules-checker.md | sort -u`
      and compare against the Phase 0 baseline recorded in `learnings.md`
      — acceptance: every Phase 0 baseline step is still present and the post-change count is greater
      than or equal to the baseline count
- [ ] [AI] Regenerate the secondary harness bindings: `npm run generate:bindings`
      — acceptance: exits 0; `.opencode/` and `.amazonq/` reflect the `.claude/` changes; no
      `.opencode/` or `.amazonq/` file was hand-edited at any point in this plan
- [ ] [AI] Validate binding sync: `npx nx run rhino-cli:naming:harness-validation` and the repo's
      harness sync validation
      — acceptance: both exit 0 with no drift reported

### Local Quality Gates (Before Push)

- [ ] [AI] `npx nx affected -t typecheck` — exits 0
- [ ] [AI] `npx nx affected -t lint` — exits 0
- [ ] [AI] `npx nx affected -t test:quick` — exits 0
- [ ] [AI] `npx nx affected -t specs:coverage` — exits 0
- [ ] [AI] Fix ALL failures, including preexisting issues not caused by these changes
- [ ] [AI] Re-run every failing check to confirm resolution — zero failures before pushing

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows the root cause orientation principle — proactively fix preexisting errors encountered
> during work. Commit preexisting fixes separately with appropriate conventional commit messages.

### Commit Guidelines

- [ ] [AI] Commit thematically — the registry, the validator, the sweep contracts, the evidence
      guards, and the workflow termination are five distinct concerns and get separate commits
- [ ] [AI] Follow Conventional Commits: `<type>(<scope>): <description>`
- [ ] [AI] Preexisting fixes get their own commits, separate from plan work
- [ ] [AI] Do NOT bundle unrelated changes into a single commit

### Push and CI

- [ ] [AI] Commit and push to `origin <pr-branch>`
- [ ] [AI] Open a draft PR against `main` with the plan folder linked in the description
- [ ] [AI] Monitor ALL GitHub Actions workflows triggered by the push — poll every 2 minutes with a
      single `gh run view --json status,conclusion` per wakeup; never tight-loop; never use
      `gh run watch`
- [ ] [AI] Fix any CI failure immediately and push a follow-up commit; repeat until ALL checks pass

### PR-Review Maker→Fixer Cycle

- [ ] [AI] Cycle 1: `pr-review-maker` review, then `pr-review-fixer` remediation
      — acceptance: every inline comment answered; CI green before Cycle 2 starts
- [ ] [AI] Cycle 2: `pr-review-maker` review, then `pr-review-fixer` remediation
      — acceptance: every inline comment answered; CI green before Cycle 3 starts
- [ ] [AI] Cycle 3: `pr-review-maker` review, then `pr-review-fixer` remediation
      — acceptance: every inline comment answered; CI green
- [ ] [HUMAN] Merge the PR to `main`
      — the human merges on their own schedule once all three cycles are complete and CI is green;
      observable resume signal for the agent: `gh pr view <n> --json state` reports `MERGED`

### Phase 6 Gate

> All checks below must pass before starting Phase 7 or Phase 8.

- [ ] [AI] Round-11 replay fixture yields a non-zero never-touched count; post-final fixture yields 0
- [ ] [AI] AC-15 inventory comparison passes — no validation step was removed
- [ ] [AI] `npm run generate:bindings` exits 0 and sync validation reports no drift
- [ ] [AI] All three PR-review cycles complete with CI green
- [ ] [HUMAN] PR merged — `gh pr view <n> --json state` reports `MERGED`

> **Pause Safety**: `ose-public` carries the complete, self-consistent change set and CI is green on
> `main`. The two sibling repos are simply not yet updated, which is a normal steady state for this
> repo. Safe to stop indefinitely. To resume: `git -C <repo> log --oneline -1 origin/main`.

---

## Phase 7: Propagate to `ose-primer`

- [ ] [AI] Provision a worktree in `ose-primer` and sync it with `origin/main`
      — acceptance: the worktree exists and is at `origin/main`
- [ ] [AI] Port surfaces 1-6, 10 and 12 from the
      [Surface Inventory](./tech-docs.md#surface-inventory) as byte-identical text where the repos do
      not legitimately diverge
      — acceptance: `test -f repo-governance/development/quality/governance-sweep-blind-spots.md`
      succeeds in `ose-primer` and its fifteen-class count clause returns 15
- [ ] [AI] Port `apps/rhino-cli` and the rhino Gherkin tree **byte-identically** per the
      [SDLC Gate Standard](../../../docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary)
      — acceptance: `diff -r` between the two repos' `apps/rhino-cli` reports no differences, and
      `diff -r` between their `specs/apps/rhino/behavior/rhino-cli/gherkin` reports no differences
- [ ] [AI] Regenerate bindings: `npm run generate:bindings`
      — acceptance: exits 0 with no drift
- [ ] [AI] Run local quality gates, then commit and push to `origin <pr-branch>`; open a draft PR
- [ ] [AI] Run the three PR-review cycles with CI green between each
- [ ] [HUMAN] Merge the `ose-primer` PR — resume signal: `gh pr view <n> --json state` reports `MERGED`

### Phase 7 Gate

- [ ] [AI] `diff -r` on `apps/rhino-cli` between `ose-public` and `ose-primer` reports no differences
- [ ] [AI] `diff -r` on the rhino Gherkin tree between the two repos reports no differences
- [ ] [AI] `ose-primer` CI green on `main`
- [ ] [HUMAN] PR merged

> **Pause Safety**: `ose-primer` matches `ose-public`; `ose-infra` remains on the prior state, which
> is independently coherent. Safe to stop. To resume: re-run the `diff -r` byte-identity check.

---

## Phase 8: Propagate to `ose-infra`

- [ ] [AI] Provision a worktree in `ose-infra` and sync it with `origin/main`
      — acceptance: the worktree exists and is at `origin/main`
- [ ] [AI] Port surfaces 1-6, 10 and 12, applying the repo-relevance gate — no infra-private content
      flows outward, and no `ose-public` content that is meaningless in `ose-infra` is force-fitted
      — acceptance: `test -f repo-governance/development/quality/governance-sweep-blind-spots.md`
      succeeds in `ose-infra` and its fifteen-class count clause returns 15
- [ ] [AI] Port `apps/rhino-cli` and the rhino Gherkin tree byte-identically
      — acceptance: `diff -r` between `ose-public` and `ose-infra` reports no differences for both
      paths
- [ ] [AI] Regenerate bindings: `npm run generate:bindings` — acceptance: exits 0 with no drift
- [ ] [AI] Run local quality gates, then commit and push to `origin <pr-branch>`; open a draft PR
- [ ] [AI] Run the three PR-review cycles with CI green between each
- [ ] [HUMAN] Merge the `ose-infra` PR — resume signal: `gh pr view <n> --json state` reports `MERGED`

### Phase 8 Gate

- [ ] [AI] `diff -r` on `apps/rhino-cli` across all three repos reports no differences
- [ ] [AI] `diff -r` on the rhino Gherkin tree across all three repos reports no differences
- [ ] [AI] `ose-infra` CI green on `main`
- [ ] [HUMAN] PR merged

> **Pause Safety**: all three repos are converged. Safe to stop. To resume: re-run the tri-repo
> byte-identity check.

---

## Phase 9: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason
      — acceptance: every entry has either a route or a discard reason
- [ ] [AI] **Append any newly discovered blind-spot class to the registry** — this plan's own
      execution is expected to surface at least one, exactly as its authoring surfaced the perishable
      -evidence problem (DECISION 8)
      — acceptance: either a new BS-N entry exists in
      `repo-governance/development/quality/governance-sweep-blind-spots.md`, or `learnings.md`
      records the explicit reason none was found
- [ ] [AI] **File the sibling-gate adoption follow-up** (DECISION 5) as a
      `plans/backlog/YYYY-MM-DD__<slug>/` plan covering
      `repo-harness-compatibility-quality-gate` and the `repo-workflow` gate
      — acceptance: the backlog folder exists and its README names both gates; the path is recorded
      in `learnings.md`
- [ ] [AI] **File the gap-D2 follow-up** (DECISION 13) as a `plans/backlog/YYYY-MM-DD__<slug>/` plan:
      `pr-review-maker` cannot post `REQUEST_CHANGES` because `gh` authenticates as the PR author and
      GitHub rejects self-review state changes, so reviews post as `COMMENT` with a blocking banner
      and any gate reading GitHub's review **state** sees the PR as unblocked; the fix is a
      token/identity change, deliberately out of this plan's scope
      — acceptance: the backlog folder exists, its README states the limitation, the observed
      consequence, and the candidate fixes (separate bot token, or a state-independent precondition);
      the path is recorded in `learnings.md`
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret,
      credential, token, or private hostname to a `<placeholder>` token, or discard if unsanitizable
      — acceptance: `learnings.md` contains no raw secret
- [ ] [AI] Apply the **repo-relevance gate** — infra-private content stays in `ose-infra` only and is
      never cross-routed into `ose-public`/`ose-primer`
      — acceptance: no infra-private content appears in this repo's routed output
- [ ] [AI] Route each surviving learning to exactly one durable home; code-homed learnings
      (`apps/`, `libs/`, tests) are ALWAYS filed as a separate `plans/backlog/<slug>/` plan and NEVER
      landed inline
      — acceptance: every entry records its terminal routing state
- [ ] [AI] If no generalizable learning surfaced, record the explicit escape in `learnings.md`:
      `No generalizable learnings — <one-line reason>`
      — acceptance: `learnings.md` is never silently empty

### Phase 9 Gate

> All checks below must pass before Plan Archival.

- [ ] [AI] Every `learnings.md` entry is in a terminal state, or the explicit "none" escape is present
- [ ] [AI] No code-homed learning landed inline in this plan's own commits or PRs
- [ ] [AI] Any newly discovered blind-spot class is appended to the registry in all three repos
- [ ] [AI] The DECISION 5 follow-up backlog plan exists on disk
- [ ] [AI] The DECISION 13 gap-D2 follow-up backlog plan exists on disk and its path is recorded in
      `learnings.md`

> **Pause Safety**: `learnings.md` is fully triaged; no future process depends on querying it later.
> Safe to stop. To resume: re-read `learnings.md` and confirm every entry is terminal.

---

## Plan Archival

- [ ] [AI] Verify ALL delivery checklist items are ticked
- [ ] [AI] Verify the Knowledge Capture phase is complete — every `learnings.md` entry reached a
      terminal state or the explicit "none" escape is recorded; both safety gates were applied
- [ ] [AI] Verify ALL quality gates pass (local + CI) in all three repos
- [ ] [AI] Verify the thirteen decisions in [README.md](./README.md) were reviewed and their outcomes
      recorded in the plan documents
- [ ] [AI] Rename and move:
      `git mv plans/in-progress/repo-rules-quality-gate-convergence/ plans/done/YYYY-MM-DD__repo-rules-quality-gate-convergence/`
      using the completion date, not the creation date
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with completion date
- [ ] [AI] Update any other READMEs referencing this plan
- [ ] [AI] Commit the archival: `chore(plans): move repo-rules-quality-gate-convergence to done`

### Not Applicable

- **Manual UI verification (Playwright MCP)** — not applicable: this plan adds and changes no web UI.
- **Manual API verification (curl)** — not applicable: this plan adds and changes no HTTP endpoint.
- **Rule-15 three-tester retest** — not applicable: no web UI feature change.
- **Rule-16 API exploratory retest** — not applicable: no REST or GraphQL endpoint change.
- **UI-design-funnel** — not applicable; exemption recorded in
  [tech-docs.md §UI-Design-Funnel Exemption](./tech-docs.md#ui-design-funnel-exemption).
