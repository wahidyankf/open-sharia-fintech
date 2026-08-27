---
title: "Step 4: Re-validate"
description: Re-runs the deterministic preflight and the AI checker, reusing the deterministic findings section when the preflight JSON is unchanged.
when_to_use: Use when re-checking after a fix cycle in a repo-rules quality-gate iteration.
---

# Step 4: Re-validate (Sequential)

Re-run the retained domain preflight (Step 0.5), then invoke the AI checker. If its JSON SHA-256
is unchanged, reuse the retained findings section and re-evaluate AI-only domain categories.

**Preflight re-run**:

```bash
rtk mkdir -p generated-reports
rtk ./apps/rhino-cli/dist/rhino-cli repo-governance audit -o json \
  --skip vendor-audit --skip governance-word-budget \
  > generated-reports/repo-governance-audit__{uuid}__{timestamp}.json
```

The binary must be built first via `rtk nx build rhino-cli`; the prebuilt path is
`apps/rhino-cli/dist/rhino-cli`.

**Agent**: `repo-rules-checker`

- **Args**: `scope: all, preflight-report: {step4.preflight.outputs.preflight-report},
delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {step3.outputs.updated-lifecycle-evidence || step0.outputs.lifecycle-evidence}`
- **Output**: `{audit-report-N}` - Verification audit report
- **Depends on**: Step 2 completion, after Step 3 when fixes were required

Re-validation reruns retained domain predicates only. Relevant edits invalidate delegated evidence,
so lifecycle status becomes `pending` until its owner supplies exact current evidence. Missing
retained preflight output is a technical domain failure, not an AI fallback.

**Success criteria**: Checker completes validation.

**On failure**: Terminate workflow with status `fail`.
