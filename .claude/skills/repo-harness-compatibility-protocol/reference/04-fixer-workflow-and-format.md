# Fixer Workflow and Fix Format

## Confidence Assessment (Re-validation Required)

Before applying any fix: (1) read the current state of the target file — the drift may already
be resolved; (2) check the checker's cited source confidence tag — `[Verified]` → proceed to
HIGH; `[Needs Verification]`/`[Unverified]` → downgrade to MEDIUM, skip for safety;
`[Outdated]` → treat as FALSE_POSITIVE; (3) assess fix confidence — HIGH (drift confirmed,
source `[Verified]`, mechanical update), MEDIUM (drift likely but target ambiguous — skip,
document), FALSE_POSITIVE (drift no longer exists, or source was `[Outdated]` — skip, record).

## Out-of-Scope (Require Human Judgment)

The fixer does NOT auto-remediate: Invariant 1/2 failures (rewriting governance/root-instruction
prose); Invariant 4 (count mismatch — either an orphan deletion or a missing-counterpart
authoring, a product decision); Invariant 5 (adding a color/tier mapping); a Tier 1→2
reclassification; higher-precedence filename discoveries (AD3 implications); new harness
additions (full onboarding); rhino-cli generator-logic changes (a translation rule, not just
regenerated data — surface for human or `swe-rust-dev`); evidence that conflicts across sources.
Surface these in the fix summary and exit non-zero so the orchestrator escalates.

## Fix Patterns

**Catalog row update**: use Edit with a narrow `old_string`/`new_string` targeting only the
affected row cell.

**Frontmatter field removal (D6)**: read the agent file first, Edit to remove the deprecated
field line, verify with Grep that it no longer appears.

**Post-edit sync (D4 Claude Code agent changes)**: after any edit to `.claude/agents/` files,
run `npm run generate:bindings` — this keeps `.opencode/agents/` aligned. Failure here is a
blocker; do not mark the fix complete until sync succeeds.

**Post-fix verification**: after every Edit, `grep -q "new-value" path/to/file.md || echo "WARNING: edit did not match — fix NOT applied to path/to/file.md"`.
If verification fails, log the fix as **FAILED (not applied)** and continue to the next finding.

**Spec updates (`specs/apps/rhino/`)**: when a harness convention change alters rhino-cli
behavior that specs document (Gherkin features, container descriptions, README claims), Edit the
affected spec files to stay consistent — update the changed scenario(s), keep Given-When-Then
structure intact, record each touched file in the fix summary.

## Process Summary

1. Initialize fix report (`repo-generating-validation-reports` skill).
2. Read the checker's audit report.
3. For each finding, in criticality × confidence priority order (P0 first): re-read the target
   file to verify drift still exists, check the source confidence tag, apply (HIGH confidence
   only) or skip with reason, verify the fix was applied, write the result progressively.
4. After all Invariant 3 fixes: confirm `npm run generate:bindings` is idempotent.
5. After all `.claude/agents/` edits: run `npm run generate:bindings`.
6. Re-run binding validation (`apps/rhino-cli/scripts/rhino-bin.sh agents validate-bindings`) —
   pass logs VALIDATED, fail surfaces failing files and exits non-zero.
7. Re-run vendor audit (`apps/rhino-cli/scripts/rhino-bin.sh repo-governance vendor validate repo-governance/`)
   — pass logs VALIDATED, fail surfaces violations and exits non-zero.
8. Capture changed files: `git diff --name-only HEAD`.
9. Write FALSE_POSITIVE carry-forward entries.
10. Recommend re-running `repo-harness-compatibility-checker` to verify.

**Focus on safety**: better to skip an uncertain fix than silently corrupt a binding file
multiple harnesses depend on.

## Fix Report Format

Write progressively to `generated-reports/harness-compat__{uuid-chain}__{YYYY-MM-DD--HH-MM}__fix.md`.
The UUID chain extends the checker's chain (append a new segment).

```markdown
## Fix: [Phase 0 Invariant N / D1 Root File / ...] — [Subject]

**Finding ref**: [Finding heading from audit report]
**Confidence**: [HIGH / MEDIUM / FALSE_POSITIVE]
**Status**: [Applied / Skipped — reason / Failed — reason]

**Before**:
[Value before fix]

**After**:
[Value after fix]

**Files changed**:

- [path/to/file.md]
```

## FALSE_POSITIVE Carry-Forward

Add an `## Accepted FALSE_POSITIVE Findings` section and append each skipped FALSE_POSITIVE to
`generated-reports/.known-false-positives.md`:

```bash
cat >> generated-reports/.known-false-positives.md << 'EOF'
## FALSE_POSITIVE: [dimension] | [harness or invariant] | [brief-description]

**Accepted**: [YYYY-MM-DD--HH-MM]
**Category**: Harness Compatibility
**Finding**: [Brief description matching checker's finding text]
**Reason**: [Why this was accepted as false positive]

---
EOF
```

## Mode Parameter Handling

See `repo-applying-maker-checker-fixer` skill: **lax** fixes CRITICAL only; **normal** fixes
CRITICAL+HIGH; **strict** (default) fixes CRITICAL+HIGH+MEDIUM; **ocd** fixes all levels.
