---
title: "Step 4: Re-Validate"
description: Re-runs the harness compatibility check to confirm fixes resolved drift and no new drift was introduced, reusing research where conventions were unchanged.
when_to_use: Use when re-checking after a fix cycle in a harness-compatibility quality-gate iteration.
---

# Step 4: Re-Validate (Sequential)

Re-run the harness compatibility check to confirm fixes resolved drift and no new drift was
introduced.

**Agent**: `harness-compatibility-checker`

- **Args**: `scope: {input.scope}, mode: {input.mode}, EXECUTION_SCOPE: harness-compat,
delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {step3.outputs.updated-lifecycle-evidence || step0.outputs.lifecycle-evidence}`
- **Output**: `{audit-report-N+1}` — Verification audit report (continues the UUID chain
  from the prior iteration)

**Note on research reuse**: For harnesses where the upstream conventions did not change
between iterations (i.e., the fixer only made local file edits), the checker may reuse the
prior `web-researcher` research summary rather than re-fetching. The checker logs
whether research was reused or refreshed for each harness.

Re-validation never reruns delegated lifecycle predicates. A relevant edit invalidates their
evidence and changes `lifecycle-status` to `pending`; the domain recheck still runs its unowned
semantic parity and external-drift dimensions.

**Success criteria**: Checker completes validation.

**On failure**: Terminate workflow with status `fail`.
