# Tri-repo rhino-cli byte-identity drift gate

One-line summary: automatically diff the `apps/rhino-cli` byte-identity boundary across all three
repos so silent drift is caught the moment it lands, not by chance during unrelated work.

> Surfaced 2026-07-17 during rhino-cli-source-drift-reconciliation execution.

## Problem / context

`apps/rhino-cli` must be byte-identical across `ose-public`, `ose-primer`, and `ose-private`, but nothing
enforces it continuously — identity is only checked when someone runs a manual `diff -rq`. This plan
found **4 drifted files** entirely by accident while researching something unrelated; the drift had
been sitting there silently since it was introduced.

**Update 2026-08-05 (plan-ideas-grooming-workflow)**: the drift is worse than file-count-4 suggested.
Propagating a single naming-type token (`grooming`) required an independent, differently-shaped
`WORKFLOW_TYPES` fix in **every** repo's own `rhino-cli` fork, including `beaver-nest` — four
separate RED/GREEN cycles for what byte-identity implies should be one shared change. A `diff -rq`
between `ose-public`'s and `ose-primer`'s `apps/rhino-cli/src` trees showed dozens of files differ
and several exist only on one side — not a handful of drifted files but substantial, structural
divergence. This raises the open question below from "where does the gate run" to "is
reconciliation to true byte-identity still realistic, or should the claim itself be corrected to
describe independently-maintained forks with shared design intent instead." See
`plans/done/2026-08-05__plan-ideas-grooming-workflow/learnings.md` for the four-occurrence detail.

## Why now

Drift has already happened once and went undetected until a coincidental manual audit. Every rhino-cli
change across the three repos is another chance to reintroduce it, and there is no automatic backstop.

## Prior art / precedents

- **SDLC Gate Standard §rhino-cli byte-identity boundary** — codifies the exact `src/`/`Cargo.*`/Gherkin
  boundary this gate would diff. [sdlc-gate-standard](../../../docs/reference/sdlc-gate-standard.md)
- **Related Repositories reference** — documents the three repos (one private, two bare) across which
  byte-identity must hold, framing the run-location question. [related-repositories](../../../docs/reference/related-repositories.md)
- **plan-multi-repo-parity-planning workflow** — the parity process this standing gate would back up
  with continuous detection. [parity-planning](../../../repo-governance/workflows/plan/plan-multi-repo-parity-planning.md)

## Proposed direction (sketch)

- A standing gate (periodic or CI-triggered) that diffs the codified byte-identity boundary — `src/`,
  `Cargo.toml`, `Cargo.lock`, `project.json`, `LICENSE`, and the Gherkin behavior tree — across the
  three repos.
- Fail the moment any file in the boundary differs between repos.
- Report which files drifted, so the fix is a targeted reconcile rather than a full re-audit.

## Rough scope & non-goals

In scope: detecting drift over the already-codified byte-identity boundary.

Out of scope (for now): auto-reconciling drift (the gate only detects); whether `apps/rhino-cli/tests/`
should join the boundary (a separate open idea); any change to the boundary's own definition.

## Risks & open questions

- Where does the gate run, given `ose-private` is private and both siblings are bare repos — one repo's
  CI checking out the other two, or a scheduled job with cross-repo read access? (open)
- Cadence: per-PR (catches drift at introduction, but needs cross-repo checkout on every PR) vs.
  nightly (cheaper, but drift lives up to a day)? (open)
- Auth model for a public-repo CI job reading the private `ose-private`. (open)
- Given the 2026-08-05 finding of dozens of pre-existing drifted files (not a handful), is
  reconciling to true byte-identity still the right target, or should the AGENTS.md claim itself be
  corrected to describe independently-maintained forks instead of demanding a drift-detection gate
  over a boundary that has already substantially diverged? (open — may reshape this idea's proposed
  direction from "detect drift" to "measure drift size, then decide reconcile vs. correct-the-claim")

## What success looks like + promotion signal

Success: any byte-identity drift is flagged the moment it is introduced, not discovered by chance
weeks later. Ready to promote to a `backlog/` plan once the run-location and cross-repo auth questions
are answered well enough to design against — the diff mechanics themselves are straightforward.
