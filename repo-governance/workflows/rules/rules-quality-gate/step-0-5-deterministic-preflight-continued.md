---
title: "Step 0.5: Deterministic Preflight — Command and Exit Handling"
description: The preflight command, the RHINO_AUDIT_NOW hash-reuse recommendation, exit-code handling, and the --skip/--exclude operator hatch.
when_to_use: Use when running the preflight command, debugging its exit code, or needing to bypass a category.
---

# Step 0.5: Deterministic Preflight — Command and Exit Handling

**Continued from** [Step 0.5: Deterministic Preflight — Overview](./step-0-5-deterministic-preflight.md).

**Command**:

```bash
rtk mkdir -p local-tmp/repo-governance-audit
rtk bash -lc './apps/rhino-cli/src/dist/rhino-cli-fsharp repo-governance audit -o json \
  --skip vendor-audit --skip governance-word-budget \
  > local-tmp/repo-governance-audit/repo-governance-audit__{uuid}__{timestamp}.json'
```

The binary must be built first via
`rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- build rhino-cli`; the prebuilt
path is `apps/rhino-cli/src/dist/rhino-cli-fsharp`.

> **Recommendation**: Pin `RHINO_AUDIT_NOW=<RFC3339>` per workflow run to enable the SHA-256 hash-reuse optimization (the `ran_at` field is derived from this env var; without it the timestamp defaults to `time.Now()` and the hash always changes). See [`apps/rhino-cli/README.md`](../../../../apps/rhino-cli/README.md#global-flags) for details.

- **Output**: `{preflight-report}` — JSON envelope at the captured path; schema `rhino-cli/repo-governance-audit/v1`
- **Exit handling**:
  - Exit 0 (clean): Retained domain categories pass; pass JSON path to checker.
  - Exit 1 (findings): Retained domain findings are present; pass the JSON path to the checker and
    count them in the domain result.
  - Exit 2 (invocation error): Terminate with `fail`. Re-run
    `rtk bash -lc './apps/rhino-cli/src/dist/rhino-cli-fsharp repo-governance audit -o text --skip vendor-audit --skip governance-word-budget'`;
    rebuild with
    `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- build rhino-cli` when needed.

The two lifecycle-owned skips are mandatory in this workflow, not an operator hatch. `--exclude`
may still narrow retained legacy paths when explicitly justified; never skip layer coherence or
traceability merely to obtain a pass.

**Success criteria**: Preflight completes; JSON file exists at expected path; JSON parses as valid `AuditEnvelope` with `schema` field set to `rhino-cli/repo-governance-audit/v1`.

**Depends on**: lifecycle delegation handoff. Runs again before every domain re-validation
iteration; delegated lifecycle predicates do not run again here.
