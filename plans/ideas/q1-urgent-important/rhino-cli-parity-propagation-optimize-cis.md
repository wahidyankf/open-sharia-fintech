# Propagate the optimize-cis-era `apps/rhino-cli` byte-identity drift to `ose-private`

One-line summary: `apps/rhino-cli` byte-identity parity across `ose-public`/`ose-private`
— a zero-carve-out MUST boundary — is currently broken, and the sibling
`optimize-cis` PR is already merged, so nothing propagates it automatically.

> **Scope note (2026-08-16)**: `ose-primer` left the parity set and carries no propagation
> obligation. The 2026-08-09 measurements below are preserved verbatim as evidence, but only the
> `ose-private` half of the drift is actionable; the `ose-primer`-only files are out of scope.

## Problem / context

Measured on **2026-08-09** during cycle 7 of the PR-Review Maker→Fixer Cycle on `ose-public` #162
(the `optimize-cis` plan's own PR), by diffing `apps/rhino-cli/parity-manifest.sha256` (659 entries)
against both siblings' live `main` via the GitHub Contents API:

- Against `ose-primer`: 15 files diverge.
- Against `ose-private`: 8 files diverge, 6 of which overlap with the `ose-primer` set.
- **Union across both siblings: 17 distinct files.** The original PR-review finding (`AR5`,
  `pr-review-architecture-maker`) reproduced only the `ose-primer` diff and reported 14 (later
  corrected to 15) — it did not separately audit `ose-private`, so 2 files
  (`apps/rhino-cli/src/commands/harness_generate_bindings.rs`,
  `apps/rhino-cli/tests/gate_format_verify_wrappers.rs`) diverge only against `ose-private` and were
  never named in the finding, and a 17th file
  (`specs/apps/rhino/behavior/rhino-cli/gherkin/README.md`, diverging against both siblings) was
  independently found during the cycle-8 PR-review re-verification.

Full 17-file union (`apps/rhino-cli/` root implied unless noted):

- `src/application/doctor/tools.rs`
- `src/application/parity.rs`
- `src/commands/gate/run.rs`
- `src/commands/gate/validate.rs`
- `src/commands/harness_generate_bindings.rs`
- `src/commands/md_validate_frontmatter_dates.rs`
- `src/commands/repo_config_validate.rs`
- `tests/agents.rs`
- `tests/cursor_binding.rs`
- `tests/docs.rs`
- `tests/gate_dispatch.rs`
- `tests/gate_format_verify_wrappers.rs`
- `tests/gate_specs.rs`
- `tests/specs_tree.rs`
- `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-declaration.feature`
- `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature`
- `specs/apps/rhino/behavior/rhino-cli/gherkin/README.md`

Root cause: cycle 6 of the same PR-review cycle fixed a `validate.rs` staleness finding in
`ose-public` only (commit `891ef597a`), then regenerated `ose-public`'s own
`parity-manifest.sha256` to match (`18ae58897`) — silencing the _local_ `parity manifest validate`
gate while leaving the _cross-repo_ contract violated. That fix landed after both siblings'
`optimize-cis` PRs (`ose-primer` #31, `ose-private` #30) had already merged, so there was no live PR
in either sibling to carry the propagation.

## Why now

`AGENTS.md` §Related Repositories declares this boundary "with zero carve-outs," and `plans/done/
2026-08-09__optimize-cis/delivery.md`'s AC-15 acceptance criterion asserts it holds. As of this
writing that criterion is honestly recorded as **not met**, accepted-with-reason, rather than
silently re-ticked (see `delivery.md`'s Phase 10 Gate AC-15 annotation and its 4th §Delivery
Boundaries item). That disclosure is not a fix — the underlying drift is real and grows every time
either sibling's `rhino-cli` changes independently before this is closed.

## Prior art / precedents

- `plans/done/2026-08-09__optimize-cis/` — the plan whose Phase 10 propagation work this gap
  escaped from; see `delivery.md`'s AC-15 annotation for the reproduction commands and full file
  list, and `baseline/pr-numbers.md` for the PR ledger.
- The cycle-6 PR-review thread `PRRT_kwDOQXc0486Xoj-t` (resolved, `ose-public` #162) — the fixer who
  landed `891ef597a` disclosed the propagation gap honestly at the time, but only in a review-thread
  reply, not in `delivery.md` or the PR body — which is what let it go unactioned once both sibling
  PRs merged.
- [`plan-multi-repo-parity-planning`](../../../repo-governance/workflows/plan/plan-multi-repo-parity-planning.md) —
  the standard workflow for a plan whose objective touches `apps/rhino-cli`; this follow-up should
  use it rather than an ad hoc cross-repo push.

## Proposed direction (sketch)

- **Step 0 — reproduce.** Re-run the manifest diff against both siblings' current `main` (drift may
  have grown since 2026-08-09) before assuming the 17-file list above is still exhaustive or still
  accurate file-by-file.
- **Step 1 — classify each file.** For each of the 17 files, determine which side is authoritative:
  some are plainly this `optimize-cis` PR's own Phase 2-9 work that Phase 10 propagated and a
  sibling then diverged from post-merge; others may be the reverse. Do not assume `ose-public` wins
  by default.
- **Step 2 — propagate via `plan-multi-repo-parity-planning`.** Author the propagation for
  `ose-private` per that workflow, landing in its own worktree/PR.
- **Step 3 — re-verify.** `parity manifest validate` must exit 0 with an identical hash in both
  parity repos before this is closed. Re-tick `optimize-cis`'s AC-15 checkbox and its terminal closing
  criterion only once that is independently confirmed, per the plan's own instruction not to
  silently re-tick.

## Rough scope & non-goals

**In scope**: reproducing and classifying the drift against `ose-private`; a propagation plan/PR for
that repo; re-verification of `parity manifest validate` across both parity repos.

**Out of scope**:

- Re-opening or amending the already-merged sibling PR (`ose-private` #30) —
  propagation lands as new commits/PRs, not history rewrites.
- The `ose-primer`-only files in the measured union — that repo is outside the parity set.
- Any further `apps/rhino-cli` feature work beyond what closes this specific drift.
- `beaver-nest` — it is deliberately outside the 3-repo parity boundary (it carries a fork, not a
  byte-identical copy).

## Risks & open questions

- Is the 17-file list still current, or has independent `rhino-cli` work in either sibling grown it
  further since 2026-08-09? **(open — re-check at Step 0)**
- For each file, which repo's version is actually correct? Naively copying `ose-public`'s version
  over both siblings risks reverting a sibling-side fix that never made it back upstream. **(open)**
- Should this become a standing CI check (e.g. a scheduled cross-repo parity-drift monitor) rather
  than a one-time propagation, given this is not the first time a `rhino-cli`-touching PR has merged
  in one repo before its siblings caught up? **(open — possible follow-on idea)**

## What success looks like + promotion signal

Success: `apps/rhino-cli/scripts/rhino-bin.sh parity manifest validate` (or the cross-repo
equivalent) exits 0 with an identical manifest hash in `ose-public` and
`ose-private`, and `optimize-cis`'s AC-15 checkbox is legitimately re-ticked with the re-verification
evidence recorded.

**Promotion signal**: Step 0's re-reproduction. Once the current, verified file list is in hand,
promote directly to a `plan-multi-repo-parity-planning`-shaped `backlog/` plan — the propagation
mechanics are already well-understood (this is not a design question), so this two-pager should not
sit long before promotion.
