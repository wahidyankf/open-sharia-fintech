---
title: "Plan-Specific Validation — Completeness Through Execution-Grade Clarity"
description: First half of the plan-checker validation catalog — completeness, technical accuracy, anti-hallucination, harness-neutrality, worktree specification, and execution-grade clarity.
when_to_use: Use when checking exactly what plan-checker validates for structural completeness, factual accuracy, or harness neutrality.
---

# Plan-Specific Validation — Completeness Through Execution-Grade Clarity

The plan-checker validates:

- **Completeness**: Every newly created formal plan contains `README.md`, `brd.md`, `prd.md`,
  `delivery.md`, `learnings.md`, and exactly one technical form: `tech-docs.md` or a mapped
  `tech-docs/`. Reader jobs and cohesion decide the technical shape; numeric thresholds do not.
  Apply this prospectively: archived plans and the existing Rhino plan receive no migration finding.
- **Comprehensive readability**: A junior engineer fresh from bootcamp with no professional,
  repository, or stack experience can trace evidence, goals, alternatives, decisions, design,
  delivery, proof, rollout, rollback, and learnings without chat history or author assistance.
- **Material decisions**: Each records the selected option and two viable alternatives (including
  status quo when viable), repository and applicable external prior art, evidence, constraints, trade-offs,
  rejection reasons, consequences, and revisit triggers. Evidence-backed disqualification is valid;
  fabricated alternatives are not. These are substantive product, architecture, implementation,
  delivery, rollout, testing, operational, or recovery choices—not wording, document layout,
  checker/fixer iterations, or other editorial history unless the delivered contract changed.
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
  body is plain markdown with no harness-specific syntax; (4) no generated skill copy is created
  manually—registry-declared bindings either read the canonical source directly or receive their
  mirror through the binding command; (5) governance doc changes
  live outside any "Platform Binding Examples" heading unless intentionally vendor-specific per
  [governance-vendor-independence.md](../../../conventions/structure/governance-vendor-independence.md).
  Reports CRITICAL if a plan skips this check when in scope. Skip entirely when plan touches only
  application code and tests.
- **Automatic Rules-Propagation Coverage**: Classify rule impact from the promised behavior and
  file-impact tree, not merely from paths named `repo-governance/`. For each affected repository,
  require a detailed repository-local `delivery.md` outcome invoking the canonical
  `rules-propagation` workflow in the rule-changing delivery unit. It must separately cover subject
  inventory, conflict/precedence and supersession, placement/eviction, canonical/config/
  enforcement/index edits, three-way enforcement disposition, generated bindings, verification
  and `rules-quality-gate`, manifest/final status, and sibling obligation. Missing propagation is
  **HIGH**; a generic checkbox or one repository's evidence standing in for another is **HIGH**.
- **Worktree Specification**: Plan contains a `## Worktree` section declaring the worktree path (`worktrees/<plan-identifier>/`) and provisioning command. See [Plans Organization Convention §Worktree Specification](../../../conventions/structure/plans/worktree-specification.md#worktree-specification).
- **Execution-Grade Clarity**: Every delivery outcome section has its acceptance-criterion label,
  Input, Outcome, and Proof; every independently verifiable action is a separate executor-tagged
  checkbox. A fresh bootcamp graduate can follow its prerequisites, exact paths/symbols, copyable
  commands, expected observations, failure handling, and evidence destinations. Code outcomes have
  separate detailed RED/GREEN/REFACTOR checkboxes. Exact paths and commands
  remain required where they materially remove ambiguity. Canonical Gherkin remains in PRD/spec
  files and is referenced, not copied. Packet, LOC, and file counts never create, erase, or force a
  delivery boundary. Validate natural cohesive seams, atomic consistency, every artifact required
  to build/verify/operate/roll back the unit, and an immediately production-deployable resulting
  `main` state. Incomplete behavior requires a temporary production-disabled flag, tests for both
  paths, and recorded rollout, rollback, and removal.

**Continued in** [Plan-Specific Validation — Operational Readiness and Knowledge Capture](./plan-specific-validation-operational-readiness.md) for the remaining checks (implementation readiness through knowledge capture).
