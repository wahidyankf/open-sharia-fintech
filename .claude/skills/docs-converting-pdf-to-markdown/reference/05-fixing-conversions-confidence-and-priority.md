# Fixing PDF-to-Markdown Conversions: Confidence Assessment and Priority Order

Workflow for `pdf-to-md-fixer`: read `pdf-to-md-checker` audit reports, re-validate every finding
against both PDF (source of truth) and Markdown (target), and apply only HIGH_CONFIDENCE fixes.
Never trust a checker finding blindly — always re-verify it still exists before editing.

## Confidence Assessment

See `repo-assessing-criticality-confidence` Skill for the full matrix. **HIGH_CONFIDENCE** (apply
automatically): issue confirmed in current MD, fix is unambiguous (re-extract missing text, fix
invalid Mermaid syntax), no risk of introducing new errors. **MEDIUM_CONFIDENCE** (skip, flag for
review): fix approach uncertain, subjective Mermaid quality, OCR quality disputes.
**FALSE_POSITIVE** (skip, persist to skip list): issue doesn't exist on re-validation, text present
in different normalized form, table data actually correct.

**Confidence downgrade**: even a `HIGH_CONFIDENCE`-labeled finding downgrades to
`MEDIUM_CONFIDENCE` and skips auto-application when: the fix would mechanically alter >10
occurrences of the same structural pattern (wide-scope restructure — cascading-side-effect risk);
the fix would touch document regions outside the finding's `location_md` field (out-of-locus edit);
or another finding's expected fix touches the same span (conflicting concurrent finding). Record
the downgrade reason in the fix report under **Skipped (MEDIUM_CONFIDENCE)** as
`<finding-id>: downgraded — <reason>` — downgraded findings stay out of the `Applied
(HIGH_CONFIDENCE)` count so workflow orchestration can correctly detect stagnation.

## Priority Execution Order

P0: CRITICAL + HIGH_CONFIDENCE (missing sections, wrong text). P1: HIGH + HIGH_CONFIDENCE (missing
paragraphs, invalid Mermaid). P2: CRITICAL/HIGH + MEDIUM_CONFIDENCE (log, skip). P3: MEDIUM +
HIGH_CONFIDENCE (heading drift, missing placeholders). P4: LOW + HIGH_CONFIDENCE (whitespace, minor
punctuation).
