---
title: "1. Parallel Validation (Parallel)"
description: "Step 1: runs docs-checker, docs-tutorial-checker, and docs-link-checker concurrently, each writing an independent audit report."
when_to_use: "Use when implementing or debugging the parallel-validation step of the quality gate."
---

# 1. Parallel Validation (Parallel)

## 0. Lifecycle Validation Filter

Apply [Lifecycle Validation Ownership](../../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md)
before composing checker prompts. Pass the resulting exact gate IDs as
`delegated-gate-ids` and `lifecycle-evidence`; delegated predicates cannot become findings or enter
the fix loop.

Run all documentation validators concurrently to identify all issues across different quality dimensions.

**Agent 1a**: `docs-checker`

- **Args**: `scope: {input.scope}, EXECUTION_SCOPE: docs,
delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {step0.outputs.lifecycle-evidence}`
- **Output**: `{docs-report-N}` - Factual accuracy, technical correctness, contradictions

**Agent 1b**: `docs-tutorial-checker`

- **Args**: `scope: {input.scope}, EXECUTION_SCOPE: docs,
delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {step0.outputs.lifecycle-evidence}`
- **Output**: `{tutorial-report-N}` - Pedagogical structure, narrative flow, visual completeness

**Agent 1c**: `docs-link-checker`

- **Args**: `scope: {input.scope}, EXECUTION_SCOPE: docs,
delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {step0.outputs.lifecycle-evidence}`
- **Output**: `{links-report-N}` - Internal/external link validation, cache management

**Success criteria**: All three checkers complete and generate audit reports.

**On failure**: Terminate workflow with status `fail`.

**Notes**:

- All checkers run in parallel (up to max-concurrency) for efficiency
- Each generates independent audit report in `local-tmp/<agent-family>/`
- UUID chain scope = "docs" (execution-chain-docs)
- Tutorial-checker gracefully handles non-tutorial files
- Reports use progressive writing to survive context compaction
