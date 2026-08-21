# Reconcile the live `apps/rhino-cli` byte-identity drift against `ose-private`

One-line summary: `apps/rhino-cli` byte-identity across `ose-public`/`ose-private` — a zero-carve-out
MUST boundary — is broken in at least two independently-measured places (a 17-file union from the
`optimize-cis` era and a one-line fixture string in `sync_validator.rs`), and both escaped the same
way: the fix landed in one repo after the sibling's PR had already merged, with nothing left to
propagate it automatically.

> **Scope note (2026-08-16)**: `ose-primer` left the parity set and carries no propagation
> obligation. The 2026-08-09 measurements below are preserved verbatim as evidence, but only the
> `ose-private` half of the drift is actionable; the `ose-primer`-only files are out of scope.
> Merged with `rhino-cli-sync-validator-wrong-model-drift.md` (itself demoted from a full `backlog/`
> plan on 2026-08-05 and relocated from `ose-private` on 2026-08-06) on 2026-08-21 by
> plan-ideas-grooming.
> Renamed from `rhino-cli-parity-propagation-optimize-cis.md` on 2026-08-21 by plan-ideas-grooming.

## Problem / context

`apps/rhino-cli` is governed by a byte-identity rule with **zero carve-outs** across the two sync-loop
repos: `src/`, `Cargo.toml`, `Cargo.lock`, `project.json`, `LICENSE`, and the shared Gherkin behavior
tree at `specs/apps/rhino/behavior/rhino-cli/gherkin/**` must all match byte for byte. Two separate
violations are live.

**Violation 1 — the `optimize-cis`-era union.** Measured on **2026-08-09** during cycle 7 of the
PR-Review Maker→Fixer Cycle on `ose-public` #162, by diffing `parity-manifest.sha256` (659 entries)
against both siblings' live `main` via the GitHub Contents API: 15 files diverge against `ose-primer`,
8 against `ose-private` (6 overlapping), for a **union of 17 distinct files** —
`src/application/doctor/tools.rs`, `src/application/parity.rs`, `src/commands/gate/run.rs`,
`src/commands/gate/validate.rs`, `src/commands/harness_generate_bindings.rs`,
`src/commands/md_validate_frontmatter_dates.rs`, `src/commands/repo_config_validate.rs`,
`tests/agents.rs`, `tests/cursor_binding.rs`, `tests/docs.rs`, `tests/gate_dispatch.rs`,
`tests/gate_format_verify_wrappers.rs`, `tests/gate_specs.rs`, `tests/specs_tree.rs`, and three files
under `specs/apps/rhino/behavior/rhino-cli/gherkin/` (`gate/gate-declaration.feature`,
`gate/gate-execution.feature`, `README.md`). The original PR-review finding (`AR5`) reproduced only
the `ose-primer` diff and reported 14 — two files diverge only against `ose-private` and were never
named, and a 17th was found during cycle-8 re-verification.

Root cause: cycle 6 fixed a `validate.rs` staleness finding in `ose-public` only (commit `891ef597a`),
then regenerated `ose-public`'s own `parity-manifest.sha256` to match (`18ae58897`) — silencing the
_local_ gate while leaving the _cross-repo_ contract violated. That landed after both siblings'
`optimize-cis` PRs had merged, so no live PR remained to carry the propagation.

**Violation 2 — the `sync_validator.rs` fixture string.** The test fixture exercising the
unrecognized-model code path embeds a placeholder that the two repos disagree on:
`zai-coding-plan/wrong` in `ose-private` versus `opencode-go/wrong` in `ose-public`. Neither
corresponds to a real supported model, so the functional risk is nil, but the invariant violation is
real and live. Surfaced by the Phase 6 Gate byte-identity re-check during
`rename-ose-infra-to-ose-private`, which also confirmed a previously-documented four-file
`spec-coverage` drift had self-resolved — this is a new finding that appeared in its place.

The two are one problem because the fix is one act: reproduce the manifest diff, classify each file,
and propagate. Doing them as separate plans means two passes over the same manifest, with the second
inheriting whatever the first left half-done.

## Why now

`AGENTS.md` §Related Repositories declares this boundary "with zero carve-outs," and
`plans/done/2026-08-09__optimize-cis/delivery.md`'s AC-15 asserts it holds — honestly recorded as
**not met, accepted-with-reason**, rather than silently re-ticked. That disclosure is not a fix, and
the drift grows every time either sibling's `rhino-cli` changes independently before it is closed.

The same Phase 6 Gate caught a more expensive symptom of the same weakness: the `is_naming_exempt` gap
in `docs/naming.rs` was discovered and fixed **three separate times** — once per repo — because no
earlier fix checked the siblings before declaring itself done. That is direct evidence that
byte-identity here rests on manual `diff` discipline alone. Reconciling now is cheap and gets
progressively more expensive as further drift accretes on top.

## Prior art / precedents

- [`optimize-cis`](../../done/2026-08-09__optimize-cis/README.md) — the plan whose Phase 10
  propagation this escaped from; its `delivery.md` AC-15 annotation carries the reproduction commands
  and full file list, and `baseline/pr-numbers.md` the PR ledger.
- The cycle-6 PR-review thread `PRRT_kwDOQXc0486Xoj-t` (resolved, `ose-public` #162) — the fixer
  disclosed the propagation gap honestly at the time, but only in a review-thread reply, not in
  `delivery.md` or the PR body, which is what let it go unactioned.
- [`plan-multi-repo-parity-planning`](../../../repo-governance/workflows/plan/plan-multi-repo-parity-planning.md)
  — the sanctioned workflow for a change that must land in more than one repo at once; this follow-up
  should use it rather than an ad hoc cross-repo push.
- [rhino-cli-tools-superset-carveout](../q2-not-urgent-important/rhino-cli-tools-superset-carveout.md)
  — argues `doctor/tools.rs`, which is **in the 17-file union above**, carries a legitimate
  `ose-private`-only divergence. Reconciliation cannot simply converge that file without settling that
  brief first.
- [extend-byte-identity-to-claude-hooks](../q2-not-urgent-important/extend-byte-identity-to-claude-hooks.md)
  — the adjacent proposal to widen byte-identity checking to a tree that has none; the natural home
  for the "make this a standing check" question both source briefs raised.
- **rhino-cli Byte-Identity Boundary** —
  [sdlc-gate-standard.md](https://github.com/wahidyankf/ose-private/blob/main/docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary),
  the authoritative statement of the zero-carve-out rule and exactly which paths it covers.

## Proposed direction (sketch)

- **Step 0 — reproduce, and do not trust this brief's lists.** Re-run the manifest diff against
  `ose-private`'s current `main` and re-check `sync_validator.rs` specifically. Drift may have grown
  since 2026-08-09, and it may also have self-resolved — the `spec-coverage` case proves both
  directions happen.
- **Step 1 — classify each file, without a default winner.** For every diverging file, determine which
  side is authoritative: some are `optimize-cis`'s own work a sibling then diverged from post-merge;
  others may be the reverse. Naively copying `ose-public` over `ose-private` risks reverting a
  sibling-side fix that never made it upstream. For the fixture string specifically, pick one
  canonical placeholder — `opencode-go/wrong` is the standing recommendation on the grounds that
  `ose-public` is the publicly-readable repo, not a decision — and apply it identically everywhere,
  updating every reference to the losing string rather than only the one line.
- **Step 2 — propagate via `plan-multi-repo-parity-planning`**, landing in its own worktree/PR, with
  no test deleted or weakened to route around the change.
- **Step 3 — re-verify before closing.** `parity manifest validate` must exit 0 with an identical hash
  in both parity repos. Re-tick `optimize-cis`'s AC-15 checkbox and its terminal closing criterion
  only once that is independently confirmed, per that plan's own instruction not to silently re-tick.

## Rough scope & non-goals

In scope: reproducing and classifying the drift against `ose-private`, including the
`sync_validator.rs` fixture string; a propagation plan/PR for that repo; re-verification of
`parity manifest validate` across both parity repos with the standard local gates (`lint`,
`typecheck`, `test:quick`) green in each.

Out of scope (for now):

- Re-opening or amending the already-merged sibling PR (`ose-private` #30) — propagation lands as new
  commits/PRs, never history rewrites.
- The `ose-primer`-only files in the measured union, and `ose-primer`'s own copies generally — that
  repo is outside the parity set and free to diverge.
- Building an automated cross-repo byte-identity CI gate — a larger, separate investment.
- `beaver-nest` — deliberately outside the parity boundary. As of 2026-08-21 it carries no
  `rhino-cli` at all: its `apps/` holds only `bnest-app` and `bnest-e2e`, and the repo was rebuilt on
  Phoenix LiveView and Elixir.
- Any change to the wrong-model _behaviour_, or any further `apps/rhino-cli` feature work beyond what
  closes this drift.
- The `ose-public`-specific `nx affected` rhino-cli-detection gap — previously slated for
  `rhino-cli-optimization` (superseded and deleted 2026-08-08) and verified **not** carried by
  `optimize-cis`; currently untracked and needing its own brief if still relevant at pickup.

## Risks & open questions

- **Are the lists still current?** Neither the 17-file union nor the fixture divergence has been
  re-measured since authoring, and independent `rhino-cli` work in either repo may have grown or
  closed them. This is Step 0 and it gates everything else. (open)
- **For each file, which repo's version is correct?** No default winner is safe. (open)
- **What happens to `doctor/tools.rs`?** It is in the union _and_ the subject of a brief arguing its
  divergence is legitimate. Converging it may be the wrong move; the two briefs have to be read
  together. (open)
- **Does anything outside `sync_validator.rs` reference the losing string?** Changing it in one place
  alone would leave an inconsistent fixture. (open)
- **Should this become a standing cross-repo parity-drift monitor** rather than a one-time
  propagation, given this is not the first time a `rhino-cli`-touching PR merged in one repo before
  its sibling caught up? (open — a follow-on, not this brief's scope)
- Coordination risk: an edit that lands in only one of the two repos recreates exactly the drift class
  this brief exists to close — the `naming.rs` three-times-fixed incident is the worked example.
- Normalization risk: because nothing functional breaks while the drift persists, it can sit
  indefinitely and quietly make byte-identity violations feel acceptable.

## What success looks like + promotion signal

Success: `apps/rhino-cli/scripts/rhino-bin.sh parity manifest validate` exits 0 with an identical
manifest hash in `ose-public` and `ose-private`, a `diff -rq -x target -x lcov.info -x dist -x cover.out`
across the boundary reports zero differences, the standard local gates are green in every repo
touched with no test deleted or weakened, and `optimize-cis`'s AC-15 checkbox is legitimately
re-ticked with the re-verification evidence recorded.

Promotion signal: Step 0's re-reproduction. Once the current, verified file list is in hand, promote
directly to a `plan-multi-repo-parity-planning`-shaped `backlog/` plan — the propagation mechanics are
well understood, so this is not a design question and the brief should not sit long. If the re-check
comes back clean in both places (as the earlier `spec-coverage` drift did), close it instead and fold
the residual concern into the standing-monitor idea.
