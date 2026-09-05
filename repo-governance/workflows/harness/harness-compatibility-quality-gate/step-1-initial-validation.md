---
title: "Step 1: Initial Validation"
description: Filters lifecycle-owned parity, runs retained semantic parity and external drift detection, and writes the first audit report.
when_to_use: Use when running the first checker pass of a harness-compatibility quality-gate iteration.
---

# Step 1: Initial Validation (Sequential)

Run the unowned parity checks (Phase 0), then per-harness external drift detection (Phase 1).
Lifecycle-owned predicates are delegated under the shared
[validation-ownership rule](../../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md).

**Agent**: `harness-compatibility-checker`

- **Args**: `scope: {input.scope}, mode: {input.mode}, EXECUTION_SCOPE: harness-compat,
delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {step0.outputs.lifecycle-evidence}`
- **Output**: `{audit-report-1}` — Initial audit report in
  `local-tmp/harness-compat/harness-compat__{uuid-chain}__{timestamp}__audit.md`

**What the checker does**:

**Phase 0 — Local semantic parity** (offline, runs first):

1. Use only exact registry IDs in `delegated-gate-ids`. Record their evidence without rerunning
   vendor-independence, binding sync/ownership, catalog, or duplication predicates.
2. Mark missing, stale, or mismatched delegated evidence `pending`; never replace it with an AI
   approximation or a local lifecycle-gate run.
3. Run genuinely unregistered semantic parity, including translation-map intent and hand-authored
   config parity. Do not duplicate a predicate merely because it is inexpensive.

**Phase 1 — External harness drift** (web-research-backed):

For each harness listed in the platform-binding catalog:

1. Delegates research to `web-researcher` (fetches current upstream conventions)
2. Compares upstream conventions against the local catalog entry in
   `docs/reference/platform-bindings.md`
3. Compares upstream conventions against the committed binding files for that harness
4. Records any drift as a finding (CRITICAL / HIGH / MEDIUM / LOW)

**UUID Chain Tracking**: Checker generates a 6-char UUID and writes to
`local-tmp/.execution-chain-harness-compat` before spawning `web-researcher`
tasks. See the Temporary Files Convention for details.

**Success criteria**: Checker completes, generates the domain audit, and returns the lifecycle
ledger separately.

**On failure**: Terminate workflow with status `fail`.
