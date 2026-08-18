# Drift Detection, Execution Pattern, and Report Format

## Drift Detection

Before completing validation of any listed `specs/apps/<app-family>/` folder, run the four
allowlist-driven `rhino-cli specs validate-*` Nx targets via
`nx run rhino-cli:validate:specs-{adoption,tree,counts,links}`. Each accepts a `--apps <csv>` flag
for explicit scoping; absent any flag, it defaults to the `AppsWithDDD` allowlist (`organiclever`,
`ose`).

| Target                    | What it checks                                                        | Finding level |
| ------------------------- | --------------------------------------------------------------------- | ------------- |
| `validate:specs-adoption` | BDD/DDD/Contracts adoption gaps per surface profile                   | HIGH          |
| `validate:specs-tree`     | Five-folder canonical layout — no flat-root artifacts                 | HIGH          |
| `validate:specs-counts`   | Required subfolders contain ≥1 spec file (HIGH missing, MEDIUM empty) | HIGH/MEDIUM   |
| `validate:specs-links`    | Markdown link integrity within the spec tree                          | HIGH          |

Route-level drift (endpoints, contracts) is not currently implemented — the placeholder command
files were removed in the BDD+DDD tooling gap-fill plan; re-introduction needs a new dedicated
plan, not a stub.

## Execution Pattern

1. **Initialize**: generate UUID, create the report file in `generated-reports/`.
2. **Run deterministic checks**: shell out to the four `nx run rhino-cli:validate:specs-*` targets
   for each listed app (or the `AppsWithDDD` allowlist when no folder is listed); parse non-zero
   exit codes and printed findings into report entries.
3. **Validate per folder**: for each listed folder, run LLM Categories 1-7 on it and its
   subfolders.
4. **Cross-validate**: if 2+ folders are listed, run Category 4 across them.
5. **Progressive write**: update the audit report after each category completes per folder.
6. **Summarize**: write finding counts by criticality level.

## Report Format

```markdown
# Specs Validation Audit Report

**Folders validated**:

- `specs/apps/organiclever/components/be`
- `specs/apps/organiclever/components/web`

**Timestamp**: YYYY-MM-DD--HH-MM UTC+7
**UUID Chain**: {uuid}

## Summary

| Criticality | Count |
| ----------- | ----- |
| CRITICAL    | N     |
| HIGH        | N     |
| MEDIUM      | N     |
| LOW         | N     |

## Findings by Folder

### specs/apps/organiclever/components/be

#### [CRITICAL] {Category} — {Brief description}

**File**: `path/to/file`
**Line**: N
**Evidence**: What was found
**Expected**: What should be there
**Confidence**: HIGH | MEDIUM

## Cross-Folder Findings

#### [HIGH] Cross-Folder Consistency — {Brief description}

**Folders**: `specs/apps/organiclever/components/be`, `specs/apps/organiclever/components/web`
**Evidence**: What contradicts or does not blend
**Expected**: What consistency looks like
**Confidence**: HIGH | MEDIUM

## Validator Findings

#### [HIGH] Allowlist gate — validate:specs-counts missing folder

**App**: `wahidyankf`
**Command**: `nx run rhino-cli:validate:specs-counts`
**Evidence**: `specs/apps/wahidyankf/containers: HIGH: missing required folder: containers`
**Expected**: Add the canonical `containers/` folder with at least one spec .md file
**Confidence**: HIGH
```
