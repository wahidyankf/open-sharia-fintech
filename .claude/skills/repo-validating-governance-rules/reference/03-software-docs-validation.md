# Step 8: Software Documentation Validation

**Deterministic-gate annotation**: file naming (8.3), frontmatter shape and heading hierarchy
(8.4), and README index integrity (8.7) are enforced by the deterministic `rhino-cli md` gate
(`naming`, `frontmatter`, `heading-hierarchy`, `readme-index` validators) — not in the preflight
envelope. Re-evaluate only content accuracy, principle-alignment judgement, and cross-doc
terminology consistency.

**Scope**: `docs/explanation/software-engineering/` (~265 files, ~345k lines) — the authoritative
software design/coding-standards reference.

## 8.1 Governance Principle Alignment

Read each doc's frontmatter `principles:` field; check topic-appropriate citations (security docs
need explicit-over-implicit and automation-over-manual; architecture docs need
simplicity-over-complexity and explicit-over-implicit; development-practice docs need
automation-over-manual; testing docs need automation-over-manual and reproducibility).
**CRITICAL**: broken principle reference (file doesn't exist). **HIGH**: missing a critical
principle. **MEDIUM**: missing a recommended principle. **LOW**: enhancement suggestion only.

## 8.2 Cross-Reference Completeness

Build a bidirectional reference map between software docs and `repo-governance/`; validate targets
exist, links use `.md` extension, anchors resolve; check that a software-doc→governance reference
implies a reciprocal governance→software-doc listing (e.g. a Java doc referencing the governance FP
pattern doc should be listed in that doc's "Language Support"). **CRITICAL**: broken link (404).
**HIGH**: one-way reference when bidirectional expected. **MEDIUM**: missing internal
cross-reference within software docs. **LOW**: optional enhancement.

## 8.3 File Naming Convention Adherence

Plain kebab-case filenames (`idioms.md`, `spring-boot-rest-controller.md`); directory hierarchy
encodes category; `README.md` and `templates/` are the only exceptions; files live in the correct
directory for their topic. **CRITICAL**: file in wrong directory. **HIGH**: non-kebab-case
filename. **MEDIUM**: over-specified name when the directory already encodes the category. **LOW**:
minor naming variation still in kebab-case.

## 8.4 Document Structure Pattern Consistency

Validate against each language's own `README.md` index (not a fixed list — TypeScript/Python
typically need `idioms.md`/`best-practices.md`/`anti-patterns.md`; Java/Go/Elixir typically need
`coding-standards.md` and other `*-standards.md` files; every language needs `README.md`); every
framework doc (Spring Boot, Phoenix, React) needs a README with an architecture-integration
section. Frontmatter required fields: `title`, `description`, `category` ("software"),
`subcategory`, `tags` (non-empty), `principles` (recommended). Heading hierarchy: single H1, proper
nesting (never H2→H4 skip). **CRITICAL**: missing a core document per the language's own README
index. **HIGH**: invalid/missing required frontmatter field. **MEDIUM**: heading hierarchy
violation. **LOW**: missing optional frontmatter field.

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
corresponding docs; LTS coverage per language (Java: 17/21/25; Python: 3.11+; TypeScript: recent
majors; Go: supported versions; Elixir: recent releases). **CRITICAL**: README mentions a version
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
