# Fixer Fix Patterns and Process Summary

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
