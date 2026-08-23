# Propagation checklists under-cover the real changeset

One-line summary: a multi-repo propagation checklist enumerated by change-ID at authoring time
silently under-covers the changeset it is meant to mirror — derive the file list from the merged
source PR's actual diff instead, and stop asserting a sibling's pre-state.

> Surfaced 2026-07-21/22 during `bare-repo-governance-hardening` Phases 4 and 5 (four separate
> `learnings.md` entries, two repos).

## Problem / context

`bare-repo-governance-hardening` propagated one `ose-public` change into two sibling repos using a
checklist enumerated by change ID (C1-C7) at authoring time. Three independent failure modes showed
up, all with the same root:

- **Under-coverage.** The merged `ose-public` PR touched **22 files**; the propagation checklist
  named **8**. Sites that later PR-review cycles turned into real edit sites — a source note that
  began as "read-only, never edited" and became an edit site across two cycles;
  `trunk-based-development.md` and its SKILL mirror, discovered live by a sibling's own review
  cycle — appear in no checklist entry, so a reader following the list ships a contradiction.
  Confirmed live in both siblings, and worse in the second: one sibling carried **seven** links to a
  section the source repo had deleted, across four files, plus an eighth site (a workflow README
  index entry) that stated the rule in prose with no anchor at all, so no link-based sweep could
  have found it either.
- **Premises expire.** A step asserting "already verified absent in the sibling — confirm and move
  on, no deletion" was **false on contact in both siblings**: the brief had propagated sideways
  through an unrelated parity commit after the authoring-time survey. The step's own acceptance
  clause failed as written, and the only action satisfying it was the deletion the prose forbade.
- **A sibling can be _ahead_ of the source of truth.** One sibling's copy of a shared governance
  doc had already been independently hardened, so an acceptance grep asserting "exits 1 before this
  step" printed a hit and **exited 0 before any edit was made**. The same sibling was simultaneously
  ahead on structure and behind on correctness, and carried a whole section neither other repo has.

Across the two siblings, four premises measured once at authoring time scored **three false, one
intermittent**.

## Why now

Every propagation phase in this repo family runs this shape, and the parity loop between
`ose-public` and `ose-private` is a standing commitment, not a one-off. The next multi-repo plan
inherits all three failure modes verbatim unless the workflow that governs them changes. The
evidence is unusually good right now — two siblings, one changeset, per-premise verdicts recorded
while the work was live — and it decays as memory of which cycle touched what fades.

## Prior art / precedents

- **`plan-multi-repo-parity-planning` workflow** — the workflow that governs propagation phases and
  the natural home for the fix.
  [workflow](../../../repo-governance/workflows/plan/plan-multi-repo-parity-planning.md)
- **`plan-execution` workflow** — defines how phases and their acceptance criteria are executed;
  the propagation phases in question are ordinary phases under it.
  [plan-execution](../../../repo-governance/workflows/plan/plan-execution.md)
- **PR Review Quality Gate workflow** — the mechanism that _discovered_ every one of these gaps
  live, after the checklist had already been written and reviewed.
  [pr-review-quality-gate](../../../repo-governance/workflows/pr/pr-review-quality-gate.md)
- **Falsifiable acceptance evidence** — the "exits 1 before this step" clause above belongs to
  both failure classes.
- **Vendor-neutral analogue: cherry-pick by commit range, not by ticket** — the widely-practised
  release-engineering habit of backporting from the merge commit's diff rather than from a
  human-curated list of changes, for exactly this reason.

## Proposed direction (sketch)

- **Derive, don't enumerate.** A propagation phase computes its file list from the merged source
  PR's actual diff (`git show --stat <merge-sha>`, or `git diff --name-only <base>..<merge>`) minus
  an explicit, justified exclusion list — rather than from the plan's authoring-time change-ID
  table. The change-ID table stays as _rationale_, not as _scope_.
- **Assert the post state only.** A propagation acceptance criterion states what must be true after
  the edit. Any clause asserting a sibling's _pre_-state is an assumption about a repo the plan
  never read; if a pre-state reading is genuinely wanted, measure it at execution time and record
  it, never inherit the source repo's.
- **Every "verified absent" carries an if-present branch.** Never a bare do-nothing. Treat any
  premise measured at authoring time as **expired by default**, requiring live re-verification, not
  as fact awaiting contradiction.
- **Diff before mirroring.** "Copy the source's wording verbatim" is sound only for a file the
  source repo owns outright. For co-evolved documents, diff first and decide per site — the sibling
  may hold better content.

## Rough scope & non-goals

In scope: `plan-multi-repo-parity-planning`'s propagation-phase requirements (file-list derivation,
acceptance-criterion form, expired-premise handling, diff-before-mirror), and whatever mirror of
those requirements lives in the plan conventions.

Out of scope (for now): automating the derivation as a rhino-cli subcommand (worth considering, but
the rule has to exist before it can be enforced); changing the parity relationship between the
repos; retrofitting already-archived plans.

## Risks & open questions

- Deriving from the merged diff **over**-covers as easily as the change-ID table under-covers: a
  22-file diff includes plan-folder churn and generated artifacts that must not propagate. The
  exclusion list becomes the new place to get it wrong, and it needs a shape that makes each
  exclusion justify itself. (open)
- A source PR that lands as a squash merge has one diff; a source change that lands across several
  PRs has several. Which merge-sha(s) a propagation phase derives from is unresolved for the
  multi-PR case. (open)
- "Diff first, decide per site" is more work than "copy verbatim", and it re-introduces judgement
  where a checklist was trying to remove it. Where that trade lands — per document, per phase, or
  by declaring which files the source owns outright — needs deciding at promotion.

## What success looks like + promotion signal

Success: a propagation phase's file list is reproducible from a command against the source PR
rather than from a hand-curated table; no propagation acceptance criterion in a new plan asserts a
sibling's pre-state; every "verified absent" step in a new plan names what to do if the thing is
present. Observable check: re-run the derivation against this plan's own merged PR and confirm it
would have surfaced the sites the checklist missed.

Ready to promote once the exclusion-list shape is settled — that is the one open question that
changes the size of the work rather than just its wording.
