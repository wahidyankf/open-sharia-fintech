---
title: "Phase 0 — Pre-flight, and Phase 1 — Ripeness / Completeness Gate"
description: Resolving the two-pager, identifier, and push target, then gating the brief's eight sections for completeness before any plan is authored.
when_to_use: Use when starting the promotion procedure, or checking whether a two-pager is ripe enough to promote.
---

# Phase 0 — Pre-flight, and Phase 1 — Ripeness / Completeness Gate

## 0. Pre-flight (Sequential)

**Actions**:

- Resolve the `two-pager` input to a concrete `plans/ideas/<slug>.md` path. Accept either a bare
  slug or a path; reject the folder `README.md` and any non-existent path.
- Resolve `plan-identifier` — default to `<slug>` so the idea keeps its name. Confirm no
  `plans/backlog/<identifier>/` already exists (a name clash aborts here).
- Resolve `push-target` (default `origin main`).
- Confirm the working tree is clean per the repo's git-ops method (a bare sibling uses the
  [bare-repo git-ops method](../../../development/workflow/bare-repo-landing-method.md); never
  `git rev-parse --is-bare-repository`, in any topology, to answer whether a repository is bare).

**Output**: Resolved brief path, identifier, and push target.

**On failure**: If the brief does not exist or the backlog folder already exists, abort and report.

## 1. Ripeness / Completeness Gate (Sequential, Hard Gate)

Read the two-pager and verify **each** section holds a real answer, applying the convention's rule
that promotion is a **completeness gate, not a perfection gate** — a section may hold honest open
questions, but it may not be a stub, a placeholder, or a `TODO`:

1. Title + one-line summary — a real abstract, not a restated title.
2. Problem / context — a concrete specific example, not an abstract pain point.
3. Why now — a stated urgency/dependency/opportunity.
4. **Prior art / precedents** — at least two named precedents (tool/pattern/standard/prior plan),
   each with a resolving link. Zero prior art on a substantial idea is a smell.
5. Proposed direction (sketch) — core elements a reader immediately grasps.
6. Rough scope & non-goals — in-scope bullets **and** an explicit out-of-scope list.
7. Risks & open questions — named unknowns; **zero open questions is a smell** (over-specified or
   under-thought).
8. What success looks like + promotion signal — an observable/cited/labeled success condition (never
   a fabricated metric).

**If any section is a stub** → the brief is **not ripe**. Write a `readiness-report` to
`local-tmp/plan-idea-promotion-planning/` naming exactly which sections fail and why, tell the user the brief needs
enriching first (the legitimate **"not promoted yet"** state, distinct from "rejected"), set
`final-status=not-ripe`, and **terminate without creating any plan**. Do not silently promote a thin
brief.

**Output**: Ripe → proceed. Not ripe → `readiness-report` written, workflow ends.
