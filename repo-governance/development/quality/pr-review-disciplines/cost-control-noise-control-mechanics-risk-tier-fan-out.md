---
title: "Cost/Noise Control: Risk-Tier Fan-Out (D12)"
description: "The trivial/lite/full risk-tier specialist fan-out."
category: explanation
subcategory: development
tags:
  - pr-review
  - governance
  - agents
  - quality-gates
  - boundary-rules
created: 2026-07-23
when_to_use: "Use when determining which specialists run on a PR."
---

# Cost-Control and Noise-Control Mechanics: Risk-Tier Fan-Out (D12)

## Cost-Control & Noise-Control Mechanics

The Cloudflare production AI-code-review system this repo's fan-out/coordinator shape is modeled
on carries a set of cost- and noise-control mechanics beyond the discipline split itself. They are
folded into this convention because an unbounded nine-specialist fan-out on every PR would cost
far more than a single reviewer without a matching gain in review quality.

### Risk-tier fan-out (D12)

The primary cost lever is **diff-size tiering**, not model choice. Risk-tier classification is
performed by [`pr-review-scout-maker`](../../../../.claude/agents/pr-review/pr-review-scout-maker.md), not by
`pr-review-synthesis-maker` directly — the scout classifies each PR into one of three tiers by line
count, file count, and whether it touches a security-sensitive path, and the specialist set fans out
accordingly:

- **Trivial** (≤10 changed lines AND ≤20 files, no security-sensitive path) → coordinator-only: the
  coordinator runs one consolidated generalist pass itself, with no specialist fan-out.
- **Lite** (≤100 lines AND ≤20 files) → a reduced specialist set of the four highest-yield lenses
  for this repo (governance, logic, security, integrity) plus the coordinator.
- **Full** (>100 lines OR >20 files OR touches a security-sensitive path — secrets/`.env`, git
  identity, CI/workflow, `pr-merge-protocol`) → all nine specialists plus the coordinator, minus the
  Content-Type Applicability Filter (DD-10).

**Security-sensitive paths force `full` regardless of size** — this repo's no-secrets iron rule and
git-identity guardrail make that non-negotiable. The tier is computed once per PR, re-evaluated each
cycle (since the fixer's commits change the diff), and recorded in the consolidated review header so
the tier decision is auditable.

**Content-type applicability filter (DD-10)**: within `full` tier, `pr-review-scout-maker` may skip
`pr-review-types-maker` (no typed source in the diff) or `pr-review-integrity-maker` (no test/CI
files in the diff) — the only two disciplines whose own charter is gated on a specific artifact class
rather than being applicable to any changed content. The other seven specialists are never skipped by
file type; see
[`pr-review-scout-maker.md`'s own filter definition](../../../../.claude/skills/pr-review-scout-classification/reference/risk-tier-and-specialist-selection.md#risk-tier-classification--specialist-set-selection-d12)
for the full rule and its fresh-per-cycle re-evaluation requirement.
