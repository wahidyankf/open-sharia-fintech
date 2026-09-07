---
description: What this workflow places, what it refuses to place, and where its authority to rewrite existing rules begins and ends.
when_to_use: Use when checking whether a stated rule is in scope for propagation, or whether the workflow may touch a given surface.
---

# Purpose and Scope

**Purpose**: Take one or more rules that have already been decided and write them into the
repository so they bind — on the narrowest surface that reaches their audience, contradicting no
existing rule, retaining no duplicate without a recorded keep rationale, and carrying a recorded
enforcement disposition.

## In Scope

Every surface the [Repo Rules — Scope Boundaries](../../../glossary/repo-rules-scope.md) table
names, plus anything the [Membership Test](../../../glossary/repo-rules-membership-test.md) admits:
governance prose, the canonical instruction surface and its binding shims, agent and skill
definitions, the machine-readable declarations, the enforcement wiring, and the language style
guides.

## Out of Scope

- **Deciding the rule.** The workflow places a rule; it does not invent one. An unfalsifiable
  input is normalized or rejected at Step 0, never guessed at.
- **The wide sweep.** Tidying is subject-scoped. Repository-wide duplication, contradiction, and
  traceability findings belong to [rules-grooming](../rules-grooming.md), the corpus-state-triggered
  sweep, which hands each reduction back to this workflow to write. This workflow never invokes
  [rules-quality-gate](../rules-quality-gate.md) — see
  [Step 8](./step-8-verification.md), which explains why that edge stays absent. Where a
  repository-wide concern is suspected mid-run, invoke `rules-checker` directly and treat what it
  finds as new input rather than this run's blocker.
- **Enforcement implementation.** The workflow declares and arms a gate; it does not write the
  validator behind one. That is application work under its own specs.
- **The sibling repository.** One run touches one repository. The sibling obligation is recorded,
  not executed — see Step 9.

## Authority

Within its delivery, the workflow may rewrite, merge, relocate, and delete existing rules. The PR
diff is the review surface, and no separate approval gate precedes a deletion.

Two limits bound that authority. It may never raise a word-budget threshold to fit a rule, and it
may never resolve a higher-layer conflict by editing the higher-layer rule — that escalates to a
human under Step 3.

## Related Documents

- [Execution Mode](./execution-mode.md) — how the run is driven.
- [Safety Features](./safety-features.md) — the guards on the authority described above.
