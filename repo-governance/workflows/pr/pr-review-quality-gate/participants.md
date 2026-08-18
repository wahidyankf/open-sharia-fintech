---
title: "PR-Review Quality Gate — Participants"
description: "Rosters the eleven pipeline agents — scout, nine discipline specialists, and the synthesis coordinator — plus the trivial-tier branch where the coordinator originates findings itself."
when_to_use: "Use when identifying which agent owns a given review discipline, or how the trivial-tier branch changes who originates findings."
---

# Participants

The retired single-maker `pr-review-maker` monolith is replaced by eleven agents — a stage-0
`pr-review-scout-maker` that classifies risk tier and assembles shared context ahead of the fan-out,
nine discipline-scoped specialists that fan out concurrently within each cycle, plus a mandatory
coordinator that consolidates their raw findings — feeding the unchanged `pr-review-fixer`. See the
[PR Reviewer-Discipline Convention](../../../development/quality/pr-review-disciplines.md) for each
specialist's full charter, owned scope, and routing rules.

**Trivial-tier branch**: when the scout classifies a cycle `trivial` (DD-7), `scout.specialists` is
the empty set — no specialist fans out. `pr-review-synthesis-maker` does not sit idle in this
branch; it performs one consolidated generalist pass itself in place of the fan-out and originates
findings directly, the single explicit carve-out to its otherwise-transform-only charter (see
[`pr-review-synthesis-maker.md`'s Charter](../../../../.claude/agents/pr-review/pr-review-synthesis-maker.md) and
[`pr-review-scout-maker.md`'s Trivial-Tier Handoff](../../../../.claude/skills/pr-review-scout-classification/reference/untrusted-input-and-output-contract.md#trivial-tier-handoff-dd-7)).

- **`pr-review-scout-maker`** — pipeline stage 0, runs once at the start of each cycle before the
  specialist fan-out. Owns risk-tier classification and specialist-set selection (D12) and
  shared-context assembly (D13), and reads the prior cycle's thread-resolution/dismissal state so the
  fan-out does not re-litigate a settled thread. Defined at `.claude/agents/pr-review/pr-review-scout-maker.md`.
- **Nine discipline specialists** — execution/sonnet-tier agents, one per discipline, run
  **concurrently** within a cycle's tier-selected fan-out. **Even under `full` tier, the fan-out is
  not unconditionally all nine**: the scout's Content-Type Applicability Filter (DD-10) skips
  `pr-review-types-maker` and `pr-review-integrity-maker` from a given cycle when their own declared
  artifact class (typed-language files; test/CI-workflow files, respectively) is verifiably absent
  from that cycle's current diff — see
  [`pr-review-scout-maker.md`'s Content-Type Applicability Filter](../../../../.claude/skills/pr-review-scout-classification/reference/risk-tier-and-specialist-selection.md#risk-tier-classification--specialist-set-selection-d12).
  Each fanned-out specialist reads the full PR context (diff + originating plan/issue) and emits raw,
  discipline-scoped findings; none posts to GitHub directly — every specialist's findings feed
  `pr-review-synthesis-maker`. Defined at `.claude/agents/pr-review-<discipline>-maker.md`:
  - `pr-review-architecture-maker` — new tradeoffs, module boundaries, reversibility, blast radius
  - `pr-review-logic-maker` — behavior vs. domain intent, Gherkin acceptance-criteria conformance
  - `pr-review-governance-maker` — mechanical conformance to documented `repo-governance/` conventions
  - `pr-review-security-maker` — secrets, injection, untrusted-input handling, unsafe git/FS operations
  - `pr-review-integrity-maker` — CI-gaming, weakened/skipped tests, missing regression tests
  - `pr-review-performance-maker` — performance regressions, hot-path/algorithmic-complexity concerns
  - `pr-review-docs-maker` — substantive documentation quality and completeness
  - `pr-review-instruction-maker` — instruction-decay against `AGENTS.md`/`CLAUDE.md`/`.claude/`
  - `pr-review-types-maker` — type-soundness: unsafe casts, `any`, `unsafe` blocks, `!` suppression
- **`pr-review-synthesis-maker`** — planning/opus-tier coordinator, the eleventh pipeline agent.
  Deduplicates, re-categorizes, reasonableness-filters, and tool-verifies the specialists' raw
  findings before posting exactly ONE consolidated, numeric-confidence, cited, line-anchored review
  via the GitHub Reviews API. Defined at `.claude/agents/pr-review/pr-review-synthesis-maker.md`.
- **`pr-review-fixer`** — execution/sonnet-tier agent, unchanged from the prior single-maker design.
  Lists unresolved review threads from the consolidated review, triages each, applies fixes, pushes,
  replies, and resolves threads. Defined at `.claude/agents/pr-review/pr-review-fixer.md`.

See [Pipeline Diagrams](./pipeline-diagrams.md) for the participants flowchart.
