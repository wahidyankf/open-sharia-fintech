# Repo rules quality gate — bounded, measurable sweep convergence

One-line summary: make the repo-rules governance sweep reach a trustworthy zero in far fewer rounds
by adding mechanisms that reach the blind spots text search structurally cannot, so a "converged"
verdict actually means the text is consistent.

> De-promoted 2026-07-21 from a full backlog plan (full detail preserved in git history).

## Problem / context

The repo-rules-quality-gate workflow's stated convergence expectation is **1-3 iterations, escalate
after 5**. On 2026-07-20 a real governance change (inverting the plan merge default from `[HUMAN]` to
`[AI]` and hardening merge preconditions) required **14 sequential checker rounds in its first
session**, 13 of which found genuine survivors, landing as **12 corrective commits touching 46 files**.
Every round surfaced a **new blind-spot class** the prior round's sweep had structurally missed — 15
classes in total. Three of them (BS-13/14/15) were **unreachable by any text search, however
well-phrased**: a workflow trigger described without naming the swept term, an artifact present on
disk but in no catalogue, and a safety rule scoped to an enumeration whose ground truth is a live git
ref (`git branch -r` showed **11** environment branches; the table the rule pointed at covered **8**).
Two compounding failure modes made it worse. A broken search command was indistinguishable from a
clean result — `grep` resolves to ugrep here, which rejects ripgrep's `--glob`, so one measured query
returned **0 hits (false)** where the POSIX form returned **543**. And enumeration-based guards failed
open **four consecutive times**: each of four successive fixes was correct on the axis it named and
wide open on an axis nobody had named. The loop terminates when the operator gets tired, not when the
text is actually consistent.

## Why now

The same research base that explains the sibling plan applies here: one lens iterating can only
discover the one class its own shape lets it see, so 15 classes cost roughly 15 rounds. The central
new finding — **enumeration-based guards fail open on the member nobody listed** — generalizes
directly into a first-class mechanism, and it composes with the two-repo byte-identity constraint on
`apps/rhino-cli`, meaning every fix landed here also has to land cleanly in
`ose-private`. Building this alongside the sibling `plan-quality-gate-convergence` plan shares the
substrate cost.

## Prior art / precedents

- **Fagan inspection** — the classic formal review process establishing that structured
  defect-finding beats ad-hoc iteration.
  [fagan inspection](https://en.wikipedia.org/wiki/Fagan_inspection)
- **repo-rules-quality-gate workflow** — the sweep whose 1-3-round convergence expectation this
  idea makes trustworthy.
  [repo-rules-quality-gate](../../../repo-governance/workflows/repo/repo-rules-quality-gate.md)
- **Maker-Checker-Fixer pattern** — the three-stage substrate the disjoint-lens redesign extends.
  [pattern](../../../repo-governance/development/pattern/maker-checker-fixer.md)
- **Sibling plan-quality-gate-convergence idea** — the structurally-identical gate this shares a
  parallel-disjoint-lenses substrate with. [sibling idea](./plan-quality-gate-convergence.md)

## Proposed direction (sketch)

- A **Blind-Spot Class Registry** of the 15 observed classes, each with inline evidence (the SHAs are
  branch-local and perish on squash-merge, so evidence is embedded, not referenced), the sweep form
  that misses it and the form that catches it, and explicit that classes compose rather than partition.
- A **deterministic sweep-completeness validator** computing the never-touched-candidate set and
  flagging directory-scoped sweeps with unenumerated exclusions.
- **Inbound-link-target sweep** promoted to primary (stable key), keyword search demoted to secondary.
- A **completeness-diff contract** — enumerate ground truth (filesystem, git refs, a roster) and diff
  it against the document claiming to describe it — reaching the three text-invisible classes.
- A **guard-placement contract** (guard at the point of rewrite, verified by enumerating entry paths,
  not section self-descriptions) and a **search-tool validity contract** (a zero counts only with a
  verbatim command, unsuppressed stderr, and a known-positive control probe).
- Shared **parallel disjoint lenses** and **saturation-based termination** with the sibling plan;
  cross-repo propagation to `ose-private`.

## Rough scope & non-goals

In scope: the workflow's step model / termination criteria, the new registry, the deterministic
validator plus Gherkin tree, the three repo-rules-\* agents, the two in-scope PR-review-gate
termination gaps, binding regeneration, and propagation to `ose-private`.

Out of scope (for now): the governance change that supplied the evidence (evidence, not a target);
the sibling gates (`repo-harness-compatibility`, `repo-workflow`) with no evidence chain mined; the
third PR-cycle gap (`pr-review-synthesis-maker` cannot post `REQUEST_CHANGES` — an auth/tooling
change, filed as a follow-up); and any relaxation of a check, threshold, or criticality level
(forbidden).

## Risks & open questions

- Completeness-diff has no bounded ground truth — "everything the doc should mention" is open-ended;
  each contract instance must name its ground-truth source explicitly or be a finding.
- The never-touched set could be enormous and unusable — it is scoped to candidate files, but the
  practical size is unmeasured.
- Provenance and adversarial-round judgment are still performed by the same fatigued checker the plan
  is about — bounded by safe failure direction, but not fully closed.
- Same unverified-research-brief caveat as the sibling plan blocks any gate text depending on the
  cited findings until primary sources are re-fetched.

## What success looks like + promotion signal

Success (observable, not fabricated): replaying the archived chain's intermediate states through the
deterministic pass flags `.github/`/`specs/`/root candidates as never-touched at the point the chain
claimed repo-wide completion, and reports zero against the corrected state; the completeness-diff
contract reproduces all three text-invisible classes and reports zero against the fix; every "found
nothing" report carries its control probe; and no check is removed. No specific round-count reduction
is claimed — one chain is one data point. Ready to re-promote once the shared-substrate sequencing
with the sibling plan is confirmed and the research re-verification path is settled.
