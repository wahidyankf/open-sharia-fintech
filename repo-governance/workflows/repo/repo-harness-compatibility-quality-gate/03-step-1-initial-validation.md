---
title: "Step 1: Initial Validation"
description: Runs the combined check — five deterministic parity invariants (Phase 0) then per-harness external drift detection (Phase 1) — and writes the first audit report.
when_to_use: Use when running the first checker pass of a harness-compatibility quality-gate iteration.
---

# Step 1: Initial Validation (Sequential)

Run a combined check: five deterministic parity invariants (Phase 0) then per-harness
external drift detection (Phase 1).

**Agent**: `repo-harness-compatibility-checker`

- **Args**: `scope: {input.scope}, mode: {input.mode}, EXECUTION_SCOPE: harness-compat`
- **Output**: `{audit-report-1}` — Initial audit report in
  `generated-reports/harness-compat__{uuid-chain}__{timestamp}__audit.md`

**What the checker does**:

**Phase 0 — Deterministic parity invariants** (offline, Bash-based, runs first):

1. Governance prose vendor-neutrality — runs `rhino-cli repo-governance vendor validate repo-governance/`
2. Root instruction surface vendor-neutrality — runs vendor-audit on `AGENTS.md` and `CLAUDE.md`
3. Binding sync no-op — runs `npm run generate:bindings && git diff --quiet .opencode/ .amazonq/`
4. Agent count parity — compares `find .claude/agents -name '*.md' ! -name README.md | wc -l`
   against the same command over `.opencode/agents/` (`.claude/agents/` is nested into role
   subfolders, `.opencode/agents/` is flat, and the `.claude/agents/README.md` index is not an
   agent)
5. Translation-map coverage — checks all distinct `color:` and `model:` frontmatter values
   appear in the color-translation table and tier map

**Phase 1 — External harness drift** (web-research-backed):

For each harness listed in the platform-binding catalog:

1. Delegates research to `web-researcher` (fetches current upstream conventions)
2. Compares upstream conventions against the local catalog entry in
   `docs/reference/platform-bindings.md`
3. Compares upstream conventions against the committed binding files for that harness
4. Records any drift as a finding (CRITICAL / HIGH / MEDIUM / LOW)

**UUID Chain Tracking**: Checker generates a 6-char UUID and writes to
`generated-reports/.execution-chain-harness-compat` before spawning `web-researcher`
tasks. See the Temporary Files Convention for details.

**Success criteria**: Checker completes and generates audit report.

**On failure**: Terminate workflow with status `fail`.
