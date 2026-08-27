---
title: "1. Initial Validation (Sequential)"
description: "Step 1: invokes docs-software-engineering-separation-checker to identify separation violations and write the initial audit report."
when_to_use: "Use when implementing or debugging the initial-validation step of the quality gate."
---

# 1. Initial Validation (Sequential)

## 0. Lifecycle Validation Filter

Apply [Lifecycle Validation Ownership](../../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md)
before composing checker prompts. Pass the resulting exact gate IDs as
`delegated-gate-ids` and `lifecycle-evidence`; delegated predicates cannot become findings or enter
the fix loop.

Run software engineering documentation separation check to identify violations.

**Agent**: `docs-software-engineering-separation-checker`

- **Args**: `scope: {input.scope}, delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {step0.outputs.lifecycle-evidence}`
- **Output**: `{audit-report-1}` - Initial audit report in `generated-reports/` (4-part format: `docs-swe-sep__{uuid-chain}__{timestamp}__audit.md`)

**Success criteria**: Checker completes and generates audit report.

**On failure**: Terminate workflow with status `fail`.
