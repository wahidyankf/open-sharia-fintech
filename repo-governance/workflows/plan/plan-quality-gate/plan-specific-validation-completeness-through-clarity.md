---
title: "Plan-Specific Validation — Completeness Through Execution-Grade Clarity"
description: First half of the plan-checker validation catalog — completeness, technical accuracy, anti-hallucination, harness-neutrality, worktree specification, and execution-grade clarity.
when_to_use: Use when checking exactly what plan-checker validates for structural completeness, factual accuracy, or harness neutrality.
---

# Plan-Specific Validation — Completeness Through Execution-Grade Clarity

The plan-checker validates:

- **Completeness**: All five canonical documents present in multi-file plans — `README.md`, `brd.md`, `prd.md`, `tech-docs.md`, `delivery.md`. Required sections populated in each file per the [Content-Placement Rules](../../../conventions/structure/plans/content-placement-rules.md#content-placement-rules-brdmd-vs-prdmd). Single-file exception is allowed when the plan is trivially small (≤1000 lines) and a single `README.md` covers the nine mandatory sections: Context, Scope, Business Rationale (condensed BRD), Product Requirements (condensed PRD), Technical Approach, **Worktree**, Delivery Checklist, Quality Gates, Verification.
- **Technical Accuracy**: Commands, versions, tool names, API signatures verified via repo `Grep` first (free, fast, accurate); external claims verified via `web-researcher` per the lower plan-content delegation threshold
- **Anti-Hallucination Scan**: Every non-trivial factual claim carries an inline confidence label
  (`[Repo-grounded]` / `[Web-cited]` / `[Judgment call]` / `[Unverified]`); zero violations of
  Anti-Pattern Catalog AP-1 through AP-10; every cited file path / Nx target / agent / skill
  resolves on the current commit. See
  [Plan Anti-Hallucination Convention](../../../development/quality/plan-anti-hallucination.md).
- **Harness-Neutrality Scan** (conditional — applies when plan touches agents, skills, rules, or
  `repo-governance/` paths): Verifies (1) agent definitions follow
  [multi-harness-binding conventions](../../../conventions/structure/multi-harness-binding.md);
  (2) agent mirrors are generated via `rtk npm run generate:bindings`, not hand-written; (3) skill
  body is plain markdown with no harness-specific syntax; (4) no manual `.opencode/skill(s)` copy
  is created because OpenCode reads `.claude/skills/` natively, while the required
  `.agents/skills/` mirror is generated through the binding command; (5) governance doc changes
  live outside any "Platform Binding Examples" heading unless intentionally vendor-specific per
  [governance-vendor-independence.md](../../../conventions/structure/governance-vendor-independence.md).
  Reports CRITICAL if a plan skips this check when in scope. Skip entirely when plan touches only
  application code and tests.
- **Worktree Specification**: Plan contains a `## Worktree` section declaring the worktree path (`worktrees/<plan-identifier>/`) and provisioning command. See [Plans Organization Convention §Worktree Specification](../../../conventions/structure/plans/worktree-specification.md#worktree-specification).
- **Execution-Grade Clarity**: Every delivery checkbox names explicit file path(s), verbatim shell command(s), and a concrete acceptance criterion. See [Plans Organization Convention §Execution-Grade Clarity](../../../conventions/structure/plans/execution-grade-clarity.md#execution-grade-clarity-hard-rule).

**Continued in** [Plan-Specific Validation — Operational Readiness and Knowledge Capture](./plan-specific-validation-operational-readiness.md) for the remaining checks (implementation readiness through knowledge capture).
