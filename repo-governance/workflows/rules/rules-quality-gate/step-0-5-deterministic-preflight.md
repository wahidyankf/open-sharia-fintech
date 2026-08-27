---
title: "Step 0.5: Deterministic Preflight — Overview"
description: What the rhino-cli repo-governance audit orchestrator does (four fixed-order categories), and why the step is numbered 0.5 instead of renumbering Steps 1-6.
when_to_use: Use when understanding what the deterministic preflight covers before invoking it.
---

# Step 0.5: Deterministic Preflight — Overview

Run the `rhino-cli repo-governance audit` orchestrator with `vendor-audit` and
`governance-word-budget` skipped. Those predicates belong to registry lifecycle gates and arrive
through exact `delegated-gate-ids` plus the lifecycle evidence ledger; missing/stale evidence is
`pending`, never a reason to rerun or AI-rederive them here. The retained preflight categories are
`layer-coherence` and `traceability-audit`, which are unique domain checks. The AI checker retains
paraphrased duplication, semantic contradictions, terminology alignment, and
principle-appropriateness judgement.

**Why Step 0.5 (and not Step 1, renumbering everything down)**: This step was inserted between the pre-existing Step 1 (Initial Validation) and the workflow start. Decimal numbering preserves the existing Step 1-6 references in the checker/fixer prompts that pre-date the preflight. The [Workflow Identifier Convention](../../meta/workflow-identifier.md) explicitly allows sub-step decimals for non-disruptive insertions.

This quality-gate-specific filtering follows the shared
[validation-ownership rule](../../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md).
Standalone `repo-rules-checker` behavior is unchanged.

**Continued in** [Step 0.5: Deterministic Preflight — Command and Exit Handling](./step-0-5-deterministic-preflight-continued.md).
