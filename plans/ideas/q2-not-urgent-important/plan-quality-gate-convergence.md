# Plan quality gate — faster convergence without quality loss

One-line summary: make the plan-quality-gate maker-checker-fixer loop reach its first zero in far
fewer iterations, catching every defect it catches today, by running disjoint lenses in parallel
instead of one lens repeatedly.

> De-promoted 2026-07-21 from a full backlog plan (full detail preserved in git history).

## Problem / context

The plan-quality-gate workflow's stated convergence target is **3-5 iterations**. On 2026-07-20 a
real chain against the `parallel-orchestration-shared-machine-governance` plan took **17 iterations**
to reach its first zero — more than triple the target — surviving on disk as 16 audit reports before
the confirming zero plus a terminal 17th, and 2 fix reports. It was not a low-quality chain: the
checker found real defects every single iteration. The cost came from structural failure modes, not
carelessness. Roughly **5 of the 17 iterations** were consumed by fix-site defect injection (nearly
every fix introduced a new defect at the very site it repaired — mistyped backticks, six-space
indents that reparse a fence as an indented block, grep-on-absent-file claims). The `grep -c`
line-counting defect class recurred at fresh sites across **three consecutive iterations (9, 10, 11)**
because each fix addressed instances, not the class, closing only when one pass finally enumerated
**46+ sites**. And once the change-surface defects were exhausted, the checker began mining a
**1000+ line, 178-checkbox** document for pre-existing latent defects — unbounded by construction,
with no principled stopping point. The double-zero termination rule assumes a stationary finding
distribution; the distribution was not stationary.

## Why now

The research base explains why sequential rounds could never converge: one lens iterating over its
own prior output violates reviewer independence (capture-recapture), and Perspective-Based Reading
shows only genuinely different lenses find non-overlapping defects. Adding rounds adds observations
of the same shape; adding lenses adds shapes. A structurally identical sibling gate
(`repo-rules-quality-gate-convergence`) hit the same wall in the same week, so the fix is a shared
substrate worth building once rather than a one-off tweak.

## Prior art / precedents

- **Fagan inspection** — the classic formal software-inspection process showing structured review
  finds defects that sequential re-reading misses.
  [fagan inspection](https://en.wikipedia.org/wiki/Fagan_inspection)
- **plan-quality-gate workflow** — the maker-checker-fixer loop whose 3-5-iteration target this idea
  aims to actually hit. [plan-quality-gate](../../../repo-governance/workflows/plan/plan-quality-gate.md)
- **Maker-Checker-Fixer pattern** — the three-stage substrate the parallel-lens redesign builds on.
  [pattern](../../../repo-governance/development/pattern/maker-checker-fixer.md)
- **Sibling repo-rules-quality-gate-convergence idea** — the structurally-identical gate sharing the
  same convergence substrate. [sibling idea](./repo-rules-quality-gate-convergence.md)

## Proposed direction (sketch)

- A **Defect-Class Registry** of catalogued acceptance-clause traps (grep semantics, CommonMark
  structure), each with a runnable proof, so a trap is paid for once repo-wide instead of
  rediscovered per plan.
- A **deterministic pre-flight validator** (`rhino-cli plan validate-acceptance`) that catches
  mechanically-detectable classes before the expensive semantic lens runs.
- **Symmetric empirical verification**, transcript-enforced: a fix claiming "verified" must carry the
  literal command output, removing the fix-site injection round.
- **Class-level remediation** with mechanized closure via a registry-replay count-diff.
- **Parallel operationally-disjoint lenses** per round (each declaring the artifact set it reads;
  a subset declaration is rejected as a relabel) and **saturation-based termination** — stop when the
  new-class discovery curve flattens across disjoint lenses, never on a round count.
- Shared idempotent substrate with the sibling plan; propagation of the rhino-cli pieces to `ose-private`.

## Rough scope & non-goals

In scope: the workflow's step model / termination criteria, the new registry, the deterministic
validator plus Gherkin tree, the four plan-\* agents and the plan-authoring skill, binding
regeneration, and propagation to `ose-private`.

Out of scope (for now): editing the audited plan itself (it is evidence, not a target); the
PR-review quality gate (the sibling plan owns it); any relaxation of a check, threshold, or
criticality level (explicitly forbidden — reducing findings is a failure, not a success); retroactive
sweeps of in-progress plans; and μSE-style mutation testing of the detectors (recorded as an
escalation path with no citable prose-linter precedent, not executed).

## Risks & open questions

- The in-surface/latent split converts required-fix into reported-and-owned — the mitigation (route
  every latent finding to an unconditional mechanism, never a follow-up ticket that evaporates) is
  designed but unproven in practice.
- Parallel lenses could degenerate into relabels of one procedure — the disjointness check is the
  guard, but its real-world discriminating power is untested.
- The underpinning research citations entered via a 2026-07-20 research brief and were not re-fetched
  from primary sources; several remain `[Web-cited]` and one is `[Needs Verification]` (paywalled).
  Re-verification is a hard precondition before any gate text depends on them.

## What success looks like + promotion signal

Success (observable, not fabricated): replaying the archived chain's actual defect sites through the
new deterministic pass flags them and reports zero against the corrected forms; termination criteria
name the flattened discovery curve rather than a round count; the plan-checker step inventory does
not shrink; and verified fix claims carry re-executable transcripts. No specific iteration-count
reduction is claimed — one archived chain is one data point, and the next few chains are the
measurement. Ready to re-promote once the research re-verification step has a home and the
shared-substrate sequencing with the sibling plan is confirmed executable.
