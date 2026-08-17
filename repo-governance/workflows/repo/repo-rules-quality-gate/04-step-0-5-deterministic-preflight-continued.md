---
title: "Step 0.5: Deterministic Preflight — Command and Exit Handling"
description: The preflight command, the RHINO_AUDIT_NOW hash-reuse recommendation, exit-code handling, and the --skip/--exclude operator hatch.
when_to_use: Use when running the preflight command, debugging its exit code, or needing to bypass a category.
---

# Step 0.5: Deterministic Preflight — Command and Exit Handling

**Continued from** [Step 0.5: Deterministic Preflight — Overview](./03-step-0-5-deterministic-preflight.md).

**Command**:

```bash
mkdir -p generated-reports
./apps/rhino-cli/dist/rhino-cli repo-governance audit -o json > generated-reports/repo-governance-audit__{uuid}__{timestamp}.json
```

The binary must be built first via `nx build rhino-cli`; the prebuilt path is `apps/rhino-cli/dist/rhino-cli`.

> **Recommendation**: Pin `RHINO_AUDIT_NOW=<RFC3339>` per workflow run to enable the SHA-256 hash-reuse optimization (the `ran_at` field is derived from this env var; without it the timestamp defaults to `time.Now()` and the hash always changes). See [`apps/rhino-cli/README.md`](../../../../apps/rhino-cli/README.md#global-flags) for details.

- **Output**: `{preflight-report}` — JSON envelope at the captured path; schema `rhino-cli/repo-governance-audit/v1`
- **Exit handling**:
  - Exit 0 (clean): All deterministic categories pass; pass JSON path to checker.
  - Exit 1 (findings): Deterministic findings present; pass JSON path to checker (the checker incorporates the deterministic findings verbatim into the final audit's "Deterministic Findings (rhino-cli preflight)" section).
  - Exit 2 (invocation error): Terminate workflow with `fail` status. **Debugging hint**: Re-run with `./apps/rhino-cli/dist/rhino-cli repo-governance audit -o text` for human-readable diagnostic. Common causes: missing binary (rebuild via `nx build rhino-cli`); broken category function (run the category on its own to isolate — `repo-governance layer-coherence validate`, `repo-governance traceability validate`, `repo-governance vendor validate`, or `governance word-budget validate`, which lives under the cross-cutting `governance` domain rather than `repo-governance`).

> **Operator hatch**: The orchestrator accepts `--skip <category>` (one of `layer-coherence`, `traceability-audit`, `vendor-audit`, `governance-word-budget`) to bypass a whole category, and `--exclude <glob>` to drop findings whose path matches a glob. The `vendor-audit` category is already scoped to `repo-governance/` plus `AGENTS.md` / `CLAUDE.md`, so build caches, app source, generated reports, and worktrees are never scanned; if a legacy governance subtree needs bypassing, prefer `--exclude <glob>` over `--skip vendor-audit` so the rest of the category still runs.

**Success criteria**: Preflight completes; JSON file exists at expected path; JSON parses as valid `AuditEnvelope` with `schema` field set to `rhino-cli/repo-governance-audit/v1`.

**Depends on**: None (first step in each iteration). Runs again before every re-validation iteration; if the JSON SHA-256 is unchanged from the prior iteration, the checker reuses the deterministic findings section unchanged and only re-evaluates AI-only categories.
