---
title: "Step 4: Re-validate"
description: Re-runs the deterministic preflight and the AI checker, reusing the deterministic findings section when the preflight JSON is unchanged.
when_to_use: Use when re-checking after a fix cycle in a repo-rules quality-gate iteration.
---

# Step 4: Re-validate (Sequential)

Re-run the deterministic preflight (Step 0.5) first, then invoke the AI checker. If the preflight JSON SHA-256 is unchanged from the prior iteration, the checker reuses the deterministic findings section unchanged and only re-evaluates AI-only categories.

**Preflight re-run**:

```bash
mkdir -p generated-reports
./apps/rhino-cli/dist/rhino-cli repo-governance audit -o json > generated-reports/repo-governance-audit__{uuid}__{timestamp}.json
```

The binary must be built first via `nx build rhino-cli`; the prebuilt path is `apps/rhino-cli/dist/rhino-cli`.

**Agent**: `repo-rules-checker`

- **Args**: `scope: all, preflight-report: {step4.preflight.outputs.preflight-report}`
- **Output**: `{audit-report-N}` - Verification audit report
- **Depends on**: Step 3 completion

**Note on preflight unavailability**: If the `preflight-report` argument is missing, the file does not exist, or the JSON fails schema validation, the AI checker falls back to full Steps 1-8 evaluation per its own Step 0.5 graceful-degradation rule (`.claude/agents/repo/repo-rules-checker.md`). This is NOT a workflow failure — the checker logs a `[WARN]` in the audit report and the workflow proceeds. Only an Exit 2 from rhino-cli itself (broken binary, missing dependency) terminates the workflow with `fail`.

**Success criteria**: Checker completes validation.

**On failure**: Terminate workflow with status `fail`.
