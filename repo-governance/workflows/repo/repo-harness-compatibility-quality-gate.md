---
name: repo-harness-compatibility-quality-gate
title: "repo-harness-compatibility-quality-gate"
goal: "Validate internal cross-vendor parity invariants and detect external drift between each supported coding-agent harness's current upstream conventions and the repository's platform-bindings catalog plus committed binding files, then fix any drift iteratively until zero findings achieved"
termination: "Zero findings on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)"
inputs:
  - name: scope
    type: string
    description: 'Subset of harnesses to validate for external drift (e.g., "all", or a harness identifier). Defaults to all supported harnesses.'
    required: false
    default: all
  - name: mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)"
    required: false
    default: strict
  - name: min-iterations
    type: number
    description: Minimum check-fix cycles before allowing zero-finding termination (prevents premature success)
    required: false
  - name: max-iterations
    type: number
    description: Maximum check-fix cycles to prevent infinite loops
    required: false
    default: 7
  - name: max-concurrency
    type: number
    description: "Background agents run concurrently — the N in the N+1 model (1 main thread + N background agents = N+1 total). Raise only when independent work, machine capacity, and budget headroom all allow; lower under budget, runner, or disk pressure. Never self-promoted beyond the declared value."
    required: false
    default: 3
outputs:
  - name: final-status
    type: enum
    values: [pass, partial, fail]
    description: Final validation status
  - name: iterations-completed
    type: number
    description: Number of check-fix cycles executed
  - name: final-report
    type: file
    pattern: generated-reports/harness-compat__*__*__audit.md
    description: Final audit report (4-part format with UUID chain)
---

# Repository Harness Compatibility Quality Gate Workflow

**Purpose**: Validate two complementary dimensions of binding-file health, then apply fixes
iteratively until zero findings:

1. **Internal cross-vendor parity** (deterministic, fast) — five invariants checking that
   `.claude/` ↔ `.opencode/` stay consistent: governance prose vendor-neutrality,
   root-instruction-surface vendor-neutrality, binding sync no-op, agent count parity, and
   translation-map coverage.
2. **External harness conformance** (web-research-backed, on-demand) — per-harness checks
   that the platform-bindings catalog (`docs/reference/platform-bindings.md`) and committed
   binding files still match each supported harness's current upstream configuration
   conventions.

**Distinction from the deterministic pre-push guard**: The `rhino-cli agents validate-bindings`
command (run automatically in the pre-push hook) checks internal byte-drift at the file level.
This workflow's Phase 0 checks behavioral-parity invariants at the semantic level; Phase 1
checks external convention drift via web research. All three guards are complementary: the
pre-push guard is fast and offline; this workflow is comprehensive and current.

**When to use**:

- After creating or modifying agents in `.claude/agents/`
- After modifying governance prose, `AGENTS.md`, or `CLAUDE.md`
- After modifying the binding-sync logic in `apps/rhino-cli/src/internal/agents/`
- After a supported harness publishes a breaking configuration change
- Periodically as a scheduled hygiene audit (recommended: before major releases)
- When adding support for a new harness (run after initial binding files are committed)

## Execution Mode

**Preferred Mode**: Agent Delegation — invoke `repo-harness-compatibility-checker` and
`repo-harness-compatibility-fixer` via the Agent tool with `subagent_type`
(see [Workflow Execution Modes Convention](../meta/execution-modes.md)).

**Fallback Mode**: Manual Orchestration — execute workflow logic directly using
Read/Write/Edit tools when Agent Delegation is unavailable.

The Agent tool runs delegated agents that persist file changes to the actual filesystem,
making it the preferred approach when these agents exist as defined delegated agent types.

**How to Execute**:

```
User: "Run repo harness compatibility quality gate workflow"
```

The orchestrator will:

1. Invoke `repo-harness-compatibility-checker` via the Agent tool (runs 5 deterministic
   parity invariants in Phase 0, then delegates per-harness web research to
   `web-researcher` in Phase 1, writes a combined drift audit report)
2. Invoke `repo-harness-compatibility-fixer` via the Agent tool (reads audit, applies fixes
   to parity drift, catalog rows, binding files, and specs as needed)
3. Iterate until zero findings achieved on two consecutive validations
4. Show git status with modified files
5. Wait for user commit approval

**Fallback (Manual Mode)**:

```
User: "Run repo harness compatibility quality gate workflow in manual mode"
```

The orchestrator executes checker and fixer logic directly using Read/Write/Edit tools in
the main context — use this when agent delegation is unavailable.

## Research Delegation

The checker delegates **multi-page per-harness research** to `web-researcher` rather
than performing web lookups inline. This keeps the audit context lean and lets the checker
focus on diffing and reporting.

For each supported harness, the checker spawns a `web-researcher` sub-task that:

- Fetches current authoritative upstream documentation (official docs site, changelog,
  migration guides)
- Extracts the harness's current configuration conventions (frontmatter schema, file
  locations, model identifier format, permission schema, tool declarations)
- Returns a structured summary that the checker compares against the local catalog entry
  and committed binding files

The checker cites the upstream source URL and retrieval date in the audit report so reviewers
can verify research independently.

## Steps

### 1. Initial Validation (Sequential)

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
4. Agent count parity — compares `ls .claude/agents/*.md | wc -l` vs `ls .opencode/agents/*.md | wc -l`
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

### 2. Check for Findings (Sequential)

Analyze the audit report to determine if fixes are needed.

**Condition Check**: Count findings based on mode level in `{audit-report-1}`:

- **lax**: Count CRITICAL only
- **normal**: Count CRITICAL + HIGH
- **strict**: Count CRITICAL + HIGH + MEDIUM
- **ocd**: Count all levels (CRITICAL, HIGH, MEDIUM, LOW)

**Below-threshold findings**: Report in audit but do not block success.

**Decision**:

- If threshold-level findings > 0: Proceed to step 3 (reset `consecutive_zero_count` to 0)
- If threshold-level findings = 0: Initialize `consecutive_zero_count` to 1 (this check is
  the first zero), proceed to step 4 for confirmation re-check (consecutive pass requirement)

**Depends on**: Step 1 completion

### 3. Apply Fixes (Sequential, Conditional)

Apply validated fixes from the audit report based on mode level.

**Agent**: `repo-harness-compatibility-fixer`

- **Args**: `report: {audit-report-N}, approved: all, mode: {input.mode}, EXECUTION_SCOPE: harness-compat`
- **Output**: `{fix-report-N}` — Fix report with the same UUID chain as the source audit
- **Condition**: Threshold-level findings exist from step 2
- **Depends on**: Step 2 completion

**Auto-fixable scope** (fixer applies at HIGH confidence):

- **Parity Invariant 3**: binding sync drift — re-runs `npm run generate:bindings`
  and stages the changed `.opencode/agents/` files
- Catalog field updates where web-research evidence is unambiguous (e.g., a harness ships
  native `AGENTS.md` support and the catalog still marks it Tier 2)
- Tier reclassification (Tier 2 → Tier 1) backed by a dated, cited web source
- Stale verification dates in the catalog (bumps to current date when content unchanged)
- Mechanical binding file updates (frontmatter field additions/renames, file relocations
  within the dotdir, permission schema updates where the new schema is unambiguous)
- Spec updates in `specs/apps/rhino/` where a harness convention change alters rhino-cli
  behavior the specs document (Gherkin scenarios under `behavior/`, container/component
  descriptions, README claims) — the fixer edits the affected spec files to stay consistent
  with the catalog and binding changes

**Out-of-scope for automated fixing** (fixer flags and surfaces for human resolution):

- **Parity Invariants 1, 2** (governance prose, AGENTS.md/CLAUDE.md vendor-audit violations):
  rewriting load-bearing prose requires human judgment per the convention's Migration Guidance
- **Parity Invariant 4** (count mismatch): an orphan in `.opencode/` may need deletion OR a
  missing `.claude/` counterpart may need authoring — either choice has product implications
- **Parity Invariant 5** (color-map or tier-map gap): adding a new color/tier requires a
  decision about role mapping that a fixer cannot make mechanically
- Tier 1 → Tier 2 reclassification (requires authoring a new generated bridge and updating
  the pre-push guard corpus)
- Higher-precedence filename discoveries (AD3 implications require human judgment per the
  [Multi-Harness Binding Convention](../../conventions/structure/multi-harness-binding.md))
- New harness additions (full onboarding involves catalog row, binding directory decision,
  and rhino-cli implementation)
- rhino-cli **generator-logic** changes (a translation rule, not just regenerated data): only
  `apps/rhino-cli/` (Rust) is active and validated — surfaced as a human or `swe-rust-dev`
  agent authorship task

**On out-of-scope findings**: Surface with full context in the orchestrator's user-visible
status; do not loop further until the human resolves.

**Success criteria**: Fixer applies all in-scope fixes without errors; out-of-scope findings
are surfaced clearly.

**On failure**: Log errors, proceed to step 4 for verification.

### 4. Re-Validate (Sequential)

Re-run the harness compatibility check to confirm fixes resolved drift and no new drift was
introduced.

**Agent**: `repo-harness-compatibility-checker`

- **Args**: `scope: {input.scope}, mode: {input.mode}, EXECUTION_SCOPE: harness-compat`
- **Output**: `{audit-report-N+1}` — Verification audit report (continues the UUID chain
  from the prior iteration)

**Note on research reuse**: For harnesses where the upstream conventions did not change
between iterations (i.e., the fixer only made local file edits), the checker may reuse the
prior `web-researcher` research summary rather than re-fetching. The checker logs
whether research was reused or refreshed for each harness.

**Success criteria**: Checker completes validation.

**On failure**: Terminate workflow with status `fail`.

### 5. Iteration Control (Sequential)

Determine whether to continue fixing or terminate.

**Logic**:

- Count findings based on mode level in `{audit-report-N+1}` (same as step 2)
- Track `consecutive_zero_count` across iterations (resets to 0 when threshold-level
  findings > 0, increments when = 0)
- If `consecutive_zero_count >= 2` AND `iterations >= min-iterations` (or min not provided):
  Proceed to step 6 (Success — double-zero confirmed)
- If `consecutive_zero_count >= 2` AND `iterations < min-iterations`: Loop back to step 4
  (re-validate)
- If `consecutive_zero_count < 2` AND threshold-level findings = 0: Loop back to step 4
  (confirmation check — no fix needed, just re-verify)
- If threshold-level findings > 0 AND `max-iterations` provided AND
  `iterations >= max-iterations`: Proceed to step 6 (Partial)
- If threshold-level findings > 0 AND (`max-iterations` not provided OR
  `iterations < max-iterations`): Loop back to step 3
- At iteration 5: emit escalation warning if not converging

**Below-threshold findings**: Continue to be reported in audit but do not affect iteration
logic.

**Depends on**: Step 4 completion

### 6. Finalization (Sequential)

Report final status and summary.

**Output**: `{final-status}`, `{iterations-completed}`, `{final-report}`

**Status determination**:

- **Success** (`pass`): Zero threshold-level findings on two consecutive validations
- **Partial** (`partial`): Findings remain after max-iterations, or fixer flagged
  out-of-scope findings requiring human resolution
- **Failure** (`fail`): Technical errors during check or fix

**Depends on**: Reaching this step from step 2, 4, or 5

## Termination Criteria

**Success** (`pass`):

- `lax`: Zero CRITICAL findings on 2 consecutive checks (HIGH/MEDIUM/LOW may exist)
- `normal`: Zero CRITICAL/HIGH findings on 2 consecutive checks (MEDIUM/LOW may exist)
- `strict`: Zero CRITICAL/HIGH/MEDIUM findings on 2 consecutive checks (LOW may exist)
- `ocd`: Zero findings at all levels on 2 consecutive checks

**Partial** (`partial`):

- Threshold-level findings remain after max-iterations safety limit
- Fixer reported out-of-scope findings that require human resolution

**Failure** (`fail`):

- Technical errors during check or fix (e.g., `web-researcher` unreachable, binding
  file unreadable, `rhino-cli` build failure)

**Note**: Below-threshold findings are reported in the final audit but do not prevent
success status. Success requires two consecutive zero-finding validations (consecutive pass
requirement).

## Success Criteria (Gherkin)

```gherkin
Scenario: Phase 0 parity invariants pass before external drift check
  Given the five deterministic parity invariants are configured
  When repo-harness-compatibility-checker runs Phase 0
  Then it invokes rhino-cli vendor-audit for governance prose and root instruction surfaces
  And it verifies the binding sync no-op, agent count parity, and translation-map coverage
  And only after all five invariants pass does it proceed to Phase 1 web research

Scenario: Phase 0 binding sync drift is auto-fixed
  Given Phase 0 detects Invariant 3 drift (sync produced changes in .opencode/)
  When repo-harness-compatibility-fixer processes the finding
  Then it re-runs npm run generate:bindings
  And stages the updated .opencode/agents/ files
  And verifies the second sync run produces no further changes

Scenario: Checker delegates web research and produces a cited drift audit
  Given the workflow runs with scope "all"
  When repo-harness-compatibility-checker completes Phase 1
  Then it delegates multi-page upstream research to web-researcher for each harness
  And it diffs the fetched data against docs/reference/platform-bindings.md and committed binding files
  And it writes a drift audit to generated-reports/ citing the web sources for each finding
  And each finding identifies the affected harness, the stale field, and the upstream source URL

Scenario: Fixer updates catalog entries for unambiguous in-scope drift
  Given the audit contains a HIGH-confidence finding that a harness now reads AGENTS.md natively
  And the current catalog marks that harness as Tier 2
  When repo-harness-compatibility-fixer is invoked
  Then it updates the harness row in docs/reference/platform-bindings.md to Tier 1
  And it records the web citation and verification date in the catalog entry
  And it writes a fix report using the same UUID chain as the audit

Scenario: Fixer updates rhino specs when a harness change alters documented CLI behavior
  Given the audit contains a HIGH-confidence finding that a harness changed a convention rhino-cli emits
  And specs/apps/rhino/ documents the old behavior in a Gherkin scenario
  When repo-harness-compatibility-fixer applies the catalog and binding updates
  Then it edits the affected specs/apps/rhino/ files to match the new behavior
  And it preserves the Given-When-Then scenario structure
  And it records each touched spec file in the fix report

Scenario: rhino-cli generator-logic change is surfaced for human resolution
  Given the audit contains a finding that requires changing a binding translation rule
  When repo-harness-compatibility-fixer encounters it
  Then it flags the change as out-of-scope code authorship for apps/rhino-cli/ (Rust)
  And the workflow surfaces it for human or swe-rust-dev agent resolution

Scenario: Out-of-scope findings escalate to human without looping
  Given the audit contains a finding that a harness introduced a new higher-precedence filename
  When repo-harness-compatibility-fixer encounters this finding
  Then it flags it as out-of-scope with a human-action annotation
  And the workflow terminates with status "partial" rather than looping further
  And the user-visible output surfaces the finding with full context

Scenario: Double-zero confirmation prevents premature success
  Given the first validation pass returns zero drift findings
  When the workflow reaches iteration control
  Then it increments consecutive_zero_count to 1 and loops to re-validate
  And only after a second consecutive zero-finding validation does it terminate with "pass"

Scenario: Scheduled execution stays within bounded iteration budget
  Given max-iterations is set to 7 (default)
  When drift findings persist through all 7 iterations
  Then the workflow terminates with status "partial"
  And the final audit report lists all remaining drift findings
  And an escalation warning was emitted at iteration 5
```

## Example Usage

### Standard Invocation (Strict Mode — Default)

```
User: "Run repo harness compatibility quality gate workflow"
```

The orchestrator invokes specialized agents:

- `repo-harness-compatibility-checker` runs Phase 0 (5 parity invariants) then Phase 1
  (fetches current upstream conventions for all supported harnesses and diffs against the
  catalog and committed binding files)
- `repo-harness-compatibility-fixer` applies in-scope parity fixes (CRITICAL/HIGH/MEDIUM)
  and catalog updates
- Iterates until zero findings achieved on two consecutive checks
- Reports LOW-severity drift without fixing it

### Single Harness Scope

```
User: "Run repo harness compatibility quality gate workflow with scope=codex-cli"
```

Scopes Phase 1 to a single harness — Phase 0 always runs in full regardless of scope.

### With Iteration Bounds

```
User: "Run repo harness compatibility quality gate workflow in strict mode with min-iterations=2 and max-iterations=5"
```

Requires at least 2 check-fix cycles and caps at 5 iterations.

## Iteration Example

Typical execution flow when the only outstanding issue is parity sync drift:

```
Step 1: Initial validation (Phase 0)
  Invariant 3 → 1 finding (sync drift)

Step 3: Apply fixes
  Fixer runs npm run generate:bindings → agents regenerated
  Stages .opencode/agents/<changed>.md

Step 4: Re-validate
  Iteration 2 → 0 findings (consecutive_zero: 1)

Step 5: Iteration control → loop to re-validate

Step 4: Re-validate
  Iteration 3 → 0 findings (consecutive_zero: 2 — double-zero confirmed)

Result: SUCCESS (3 iterations)
```

Typical flow when out-of-scope findings are present:

```
Iteration 1:
  Check → 1 finding (new higher-precedence filename for a harness)
  Fix   → Flags as out-of-scope: human action required
Result: PARTIAL after 1 iteration; user must resolve before re-running.
```

## Safety Features

**Infinite Loop Prevention**:

- `max-iterations` defaults to 7 — override with a higher value for more attempts
- Workflow terminates with `partial` if the limit is reached
- Tracks iteration count for observability
- Escalation warning at iteration 5 if not converging

**Research Quality Safeguards**:

- Checker cites source URL and retrieval date for every upstream fact in the audit report
- Fixer re-validates each finding before applying (prevents acting on stale research)
- Out-of-scope findings are surfaced to the human rather than silently skipped

**False Positive Protection**:

- Fixer re-validates each finding before applying
- Progressive writing ensures audit history survives across iterations
- Checker logs whether research was reused or refreshed per harness

**Error Recovery**:

- Continues to verification even if some fixes fail
- Reports which fixes succeeded and which were flagged for human resolution
- Generates final report regardless of status

## Related Workflows

- [Repository Rules Validation](./repo-rules-quality-gate.md) — validates internal
  consistency across principles, conventions, development practices, agent definitions, and
  skill packages; complementary to this workflow (internal governance vs. binding correctness)

## Notes

- **Phase 0 always runs**: The five deterministic parity invariants run in every execution
  regardless of `scope`, before any web research begins.
- **On-demand for Phase 1**: Phase 1 (external drift) does not run automatically on every
  push — schedule it periodically or trigger it when upstream harness changes are announced.
- **Pre-push guard is separate**: `rhino-cli agents validate-bindings` (the pre-push parity
  guard) checks internal byte-level consistency deterministically and runs automatically.
- **Idempotent**: Safe to run multiple times without breaking working state.
- **Observable**: Generates audit reports for every iteration in `generated-reports/`.
- **Bounded**: `max-iterations` prevents runaway execution.

## Principles Implemented/Respected

- PASS: **Explicit Over Implicit**: All steps, conditions, and termination criteria are
  explicit; the distinction between Phase 0 (deterministic parity) and Phase 1 (web-backed
  external drift) is stated directly
- PASS: **Automation Over Manual**: Fully automated validation and fixing without human
  intervention (except for out-of-scope findings)
- PASS: **Simplicity Over Complexity**: Clear linear flow with loop control
- PASS: **Accessibility First**: Generates human-readable audit reports
- PASS: **Progressive Disclosure**: Can run with different mode levels
- PASS: **No Time Estimates**: Focus on quality outcomes, not duration
- PASS: **Root Cause Orientation**: Tracks upstream harness changes as the root cause of
  external drift; tracks binding-sync gaps as root cause of parity drift

## Conventions Implemented/Respected

- **[Multi-Harness Binding Convention](../../conventions/structure/multi-harness-binding.md)**:
  this workflow is the enforcement arm of that convention's two-tier binding model and
  no-shadowing rule; it keeps both internal parity and the platform-binding catalog true to
  current upstream conventions
- **[Workflow Naming Convention](../../conventions/structure/workflow-naming.md)**: filename
  `repo-harness-compatibility-quality-gate` follows the `<scope>(-<qualifier>)*-<type>` rule
  (scope `repo`, qualifier `harness-compatibility`, type `quality-gate`)
- **[File Naming Convention](../../conventions/structure/file-naming.md)**: workflow file
  uses plain kebab-case in the correct subdirectory (`repo-governance/workflows/repo/`)
- **[Linking Convention](../../conventions/formatting/linking.md)**: all cross-references
  use GitHub-compatible markdown with `.md` extensions and relative paths
- **[Content Quality Principles](../../conventions/writing/quality.md)**: active voice,
  proper heading hierarchy, single H1
- **[Governance Vendor-Independence Convention](../../conventions/structure/governance-vendor-independence.md)**:
  harness product names confined to non-load-bearing examples; load-bearing prose uses
  vendor-neutral terms ("each supported harness", "the platform-binding catalog")
- **[Web Research Delegation Convention](../../conventions/writing/web-research-delegation.md)**:
  per-harness upstream research delegated to `web-researcher`

## Agents

- [repo-harness-compatibility-checker](../../../.claude/agents/repo-harness-compatibility-checker.md) — validates parity invariants (Phase 0) and detects external harness drift (Phase 1)
- [repo-harness-compatibility-fixer](../../../.claude/agents/repo-harness-compatibility-fixer.md) — applies validated parity and harness-compatibility fixes
