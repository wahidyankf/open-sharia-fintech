# Plan archival-in-PR has no multi-repo provision

One-line summary: `plan-execution.md` §8's Archival-in-PR rule assumes one plan → one repo → one
delivering PR, and a plan whose delivery spans multiple repositories has no PR that is both
"delivering" (last to merge) and "folder-holding" (in the repo that owns the plan folder) — §8
should gain an explicit provision for that shape.

> Surfaced 2026-07-21 during bare-repo-governance-hardening execution (see DD-11 in its
> `tech-docs.md`).

## Problem / context

`bare-repo-governance-hardening`'s delivery spans **three PRs across three repositories** — the
`ose-public` PR (Phase 3), the `ose-primer` PR (Phase 4), and the `ose-private` PR (Phase 5, the
third and last to merge). The plan folder itself is tracked in `ose-public` only; neither sibling
repo receives a mirrored folder. `plan-execution.md` §8's Archival-in-PR rule requires the archival
`git mv` land "inside the delivering PR itself... not as a separate commit landed on `main` after
merge," with no carve-out for this shape. This plan has no single PR that is both the delivering
(last-to-merge) PR and the folder-holding PR: `ose-public`'s PR holds the folder but merges first,
before Phases 4 and 5 even begin; `ose-private`'s PR merges last but holds no plan folder to move. §8
silently assumes one plan → one repo → one delivering PR — this plan is a live, structural
counterexample, not a case of careless authoring.

## Why now

`plan-multi-repo-parity-planning` already exists as a dedicated workflow for multi-repo plan
delivery, which is evidence multi-repo plans are a first-class, recurring shape here, not a one-off.
Any future plan choosing the same shape as `bare-repo-governance-hardening` — one folder, several
repos, sequential per-repo PRs — hits the identical gap and has to re-argue the same structural case
from scratch, as this plan did in its DD-11. `plan-planning.md`'s own text (its Plan-Docs-Only
Carve-Out section, added 2026-07-20, before this plan reached its archival phase) already names and
disclaims "DD-11 of any individual plan" as a non-precedent — direct evidence the maintainer had
already anticipated this exact situation arriving.

## Prior art / precedents

- **`plan-execution.md` §8, "Archival-in-PR"** — the rule with the gap; states the delivering-PR
  requirement with no multi-repo carve-out.
  [plan-execution.md §8](../../../repo-governance/workflows/plan/plan-execution/finalization-pre-archival-gates.md#8-finalization-and-archival-sequential)
- **`plan-multi-repo-parity-planning` workflow** — the repo's existing multi-repo plan-shape
  precedent, whose declared output is "one plan folder path per target repo"; DD-10 of
  `bare-repo-governance-hardening` deliberately diverges from it, which is what exposes the
  archival gap in the first place.
  [plan-multi-repo-parity-planning](../../../repo-governance/workflows/plan/plan-multi-repo-parity-planning.md)
- **The Plan-Docs-Only Carve-Out** — the existing partial mitigation this plan leans on for its
  archival push; its own text already names and disclaims "DD-11 of any individual plan" as a
  non-precedent.
  [plan-planning.md §The Plan-Docs-Only Carve-Out](../../../repo-governance/workflows/plan/plan-planning/plan-docs-only-carve-out.md#the-plan-docs-only-carve-out-superseded--retired-in-ose-public)
- **"Archival-in-PR" route-specific done-definition item 5** — the mirrored rule in the PR-review workflow, which
  gestures at a "three-repo nuance" for invocations that do not carry a plan folder but never
  defines one for a plan that does.
  [pr-review-quality-gate.md §Route-Specific Done-Definition](../../../repo-governance/workflows/pr/pr-review-quality-gate/route-specific-done-definition.md#route-specific-done-definition)

## Proposed direction (sketch)

- **Option A — explicit multi-repo carve-out in §8**: name the plan-folder-owning repo's own
  delivering PR as the archival-in-PR target regardless of whether other repos' PRs merge later, so
  a plan like this one archives inside its `ose-public` PR even though `ose-private`'s PR merges
  after.
- **Option B — permit a dedicated archival-only PR**: let §8 allow a small, review-cycle-gated PR
  in the folder-owning repo, opened after the last sibling PR merges, whose sole content is the
  `git mv` plus README updates — keeps the move inside a reviewed PR without redefining "delivering
  PR."
- **Option C — align §8 with the Plan-Docs-Only Carve-Out**: fold multi-repo archival explicitly
  into the existing plan-docs-only direct-push permission, formalizing what this plan currently
  argues case-by-case in its DD-11.

The maintainer's current standing preference — plan-document lifecycle work runs on local `main`
via the Plan-Docs-Only Carve-Out — pulls toward Option C. That is recorded here honestly as a
leaning, not a decision; promotion should weigh all three.

## Rough scope & non-goals

In scope: `plan-execution.md` §8's Archival-in-PR wording, and its mirror in
`pr-review-quality-gate.md`'s Done-Definition item 4.

Out of scope (for now): re-opening `bare-repo-governance-hardening`'s DD-10 decision to keep one
plan folder rather than mirroring one per repo (a separate, already-settled question for that plan);
any change to the Plan-Docs-Only Carve-Out's general scope beyond archival specifically.

## Risks & open questions

- Option A risks becoming technically satisfiable but practically stale: the "delivering PR" would
  no longer be the PR whose merge triggers archival's usual timing, so the review-cycle discipline
  could drift out of sync with when the folder actually becomes movable.
- Option B adds a fourth PR to an already three-PR plan shape for the sole purpose of one `git mv` —
  the promotion pass should weigh that proportionality against Option C's lighter footprint.
- Whether "multi-repo" should be defined structurally (the plan-folder repo differs from the
  last-merging PR's repo, as here) or declaratively (a plan explicitly opts in) is unresolved — the
  wrong definition either overfires on ordinary single-repo plans or underfires on a different
  multi-repo shape this plan never exercised.

## What success looks like + promotion signal

Success (observable, not fabricated): `plan-execution.md` §8 states an explicit rule for a plan
whose delivery spans repositories the plan folder does not solely live in, and a future plan of
that shape can cite the rule directly instead of authoring its own DD-N justification. Ready to
promote once `bare-repo-governance-hardening` has actually archived under its DD-11 reasoning
(a second real data point beyond this one) and, if a second multi-repo plan of this shape exists by
then, it confirms the chosen option generalizes.
