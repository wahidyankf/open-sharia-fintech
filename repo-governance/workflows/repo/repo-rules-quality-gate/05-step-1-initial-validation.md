---
title: "Step 1: Initial Validation"
description: Runs the repository-wide consistency checker, its UUID chain tracking, and the graceful-degradation rule when the preflight report is unavailable.
when_to_use: Use when running the first checker pass of a repo-rules quality-gate iteration.
---

# Step 1: Initial Validation (Sequential)

Run repository-wide consistency check to identify all issues.

**Agent**: `repo-rules-checker`

- **Args**: `scope: all, EXECUTION_SCOPE: repo-rules, preflight-report: {step0_5.outputs.preflight-report}`
- **Output**: `{audit-report-1}` - Initial audit report in `generated-reports/` (4-part format: `repo-rules__{uuid-chain}__{timestamp}__audit.md`)

**UUID Chain Tracking**: Checker generates 6-char UUID and writes to `generated-reports/.execution-chain-repo-rules` before spawning any child agents. See [Temporary Files Convention](../../../development/infra/temporary-files/03-uuid-chain-generation.md#uuid-generation) for details.

**Note on preflight unavailability**: If the `preflight-report` argument is missing, the file does not exist, or the JSON fails schema validation, the AI checker falls back to full Steps 1-8 evaluation per its own Step 0.5 graceful-degradation rule (`.claude/agents/repo/repo-rules-checker.md`). This is NOT a workflow failure — the checker logs a `[WARN]` in the audit report and the workflow proceeds. Only an Exit 2 from rhino-cli itself (broken binary, missing dependency) terminates the workflow with `fail`.

**Success criteria**: Checker completes and generates audit report.

**On failure**: Terminate workflow with status `fail`.
