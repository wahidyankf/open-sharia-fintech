# Step 8 (8.5-8.8): Software Docs Templates, Diagrams, README Index, Version Docs, Report Format

## 8.5 Template Completeness

Each language needs a `templates/` subdirectory with plain-kebab-case files; when documentation
describes a pattern (e.g. "Service Layer Pattern"), a corresponding template should exist.
**CRITICAL**: `templates/` missing entirely. **HIGH**: core template missing (REST controller,
entity, repository). **MEDIUM**: a specifically-referenced template is absent. **LOW**: enhancement
suggestion for a common pattern.

## 8.6 Diagram Consistency

Extract Mermaid blocks; verify `classDef` declarations use the WCAG AA palette (Blue #0173B2,
Orange #DE8F05, Green #029E73, Purple #CC78BC, Brown #CA9161); check for missing alt-text
description near the diagram. **CRITICAL**: WCAG AA contrast violation (<4.5:1). **HIGH**: missing
color definitions (defaults used). **MEDIUM**: non-standard palette. **LOW**: missing alt-text
description.

## 8.7 README Index Accuracy

Parse each subdirectory README's file listing, compare against actual directory contents (excluding
README.md/templates/); find orphaned files (exist, unlisted) and ghost references (listed, absent);
check listed descriptions match actual content. **CRITICAL**: README lists non-existent files.
**HIGH**: files exist but aren't listed (discoverability). **MEDIUM**: description mismatch. **LOW**:
README could be more comprehensive.

## 8.8 Version Documentation Consistency

Pattern: `release-<version>.md` inside the language directory. Check README version mentions have
corresponding docs; LTS coverage per language (TypeScript: recent majors; .NET/F#: current LTS;
Rust: recent stable editions) — read the language's own README for the set it claims, never a
fixed list. **CRITICAL**: README mentions a version
with no corresponding doc. **HIGH**: missing LTS version doc. **MEDIUM**: missing non-LTS recent
version. **LOW**: could document additional versions.

## Performance Strategy (~265 files, ~345k lines)

Cache governance files (principles list, naming rules, principle→topic mappings) once; group reads
by directory using Glob; write every finding progressively (no buffering — this is the step most
likely to be interrupted by compaction); use regex for filename checks and Grep for cross-reference
extraction, deep-parsing only when validation requires it. Estimated duration: ~35-40s for all
eight sub-checks.

## Report Format (shared across 8.1-8.8)

```markdown
### Finding: [Principle Alignment / Cross-Reference / File Naming / Structure Pattern /

Templates / Diagram Accessibility / README Index / Version Documentation]

**Category**: [sub-check name]
**File**: [path]
**Criticality**: [CRITICAL/HIGH/MEDIUM/LOW]

**Issue**: [description]
**Evidence**: [what was found vs. expected]
**Recommendation**: [specific fix]
```

## Step 8 Summary

After all eight sub-checks, write a summary with files/lines analyzed and a per-category finding
count (Principle Alignment, Cross-References, File Naming, Structure Patterns, Templates,
Diagrams, README Indices, Version Docs — each as CRITICAL/HIGH/MEDIUM/LOW counts) plus a total.
