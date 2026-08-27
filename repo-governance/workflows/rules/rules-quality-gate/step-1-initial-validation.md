---
title: "Step 1: Initial Validation"
description: Runs the repository-wide consistency checker, its UUID chain tracking, and the graceful-degradation rule when the preflight report is unavailable.
when_to_use: Use when running the first checker pass of a repo-rules quality-gate iteration.
---

# Step 1: Initial Validation (Sequential)

Run repository-wide consistency check to identify all issues.

**Agent**: `repo-rules-checker`

- **Args**: `scope: all, EXECUTION_SCOPE: repo-rules,
preflight-report: {step0_5.outputs.preflight-report},
delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {step0.outputs.lifecycle-evidence}`
- **Output**: `{audit-report-1}` - Initial audit report in `generated-reports/` (4-part format: `repo-rules__{uuid-chain}__{timestamp}__audit.md`)

**UUID Chain Tracking**: Checker generates 6-char UUID and writes to `generated-reports/.execution-chain-repo-rules` before spawning any child agents. See [Temporary Files Convention](../../../development/infra/temporary-files/uuid-chain-generation.md#uuid-generation) for details.

**No lifecycle fallback**: missing/stale delegated evidence sets `lifecycle-status: pending`.
The checker does not run or imitate vendor, word-budget, or any other exact delegated predicate.
If the retained domain preflight is unavailable, report a technical domain failure; do not replace
layer-coherence or traceability with an AI approximation.

**Success criteria**: Checker completes and generates audit report.

**On failure**: Terminate workflow with status `fail`.
