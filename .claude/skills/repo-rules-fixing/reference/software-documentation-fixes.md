# Software Documentation Fixes

Scope: `docs/explanation/software-engineering/` — roughly 265 files, ~345k lines. Every
sub-pattern below follows the same shape: Pattern (what triggers it) → Re-validation (what to
re-check before fixing) → Confidence Assessment → Fix Application → Tool.

## 8.1 Principle Alignment

**Pattern**: a language/style guide page states a principle contradicting the repo's cross-cutting
software-engineering principles index. **Re-validation**: re-read the principles index for the
current canonical wording. **Confidence**: HIGH only when the contradiction is a direct textual
conflict. **Fix**: align the page's wording to the index; **Tool**: Edit.

## 8.2 Cross-Reference

**Pattern**: a page references another doc by a stale title/path. **Re-validation**: confirm the
current path via Glob. **Confidence**: HIGH (mechanical). **Fix**: update the link; **Tool**: Edit
or the Python multi-line pattern if the reference spans a paragraph.

## 8.3 File Naming

**Pattern**: a file's name violates the kebab-case/naming convention. **Re-validation**: confirm
via `find` that no other file already claims the correct name. **Confidence**: HIGH. **Fix**:
`git mv old-name.md new-name.md`, then `find`/`sed` to update every referencing link across the
repo. **Tool**: `git mv` + Grep-driven sed sweep + post-fix verification per file.

## 8.4 Structure Pattern

**Pattern**: a page doesn't follow the standard section template for its doc type. **Fix**: copy
the template structure, stub missing sections with `[TODO]` markers rather than inventing content.
**Confidence**: MEDIUM (structural correctness is judged, not just matched).

## 8.5 Template (cross-language adaptation)

**Pattern**: one language's style guide has a section another language's guide is missing, and the
content is language-agnostic in spirit. **Fix**: adapt the template to the target language's
idiom, never copy verbatim. **Confidence**: MEDIUM — requires language judgment.

## 8.6 Diagram/Mermaid

**Pattern**: a Mermaid diagram uses colors failing WCAG AA contrast. **Fix**: apply the repo's
accessible `classDef` color palette:

```
classDef default fill:#fff,stroke:#333,color:#000
classDef highlight fill:#e6f2ff,stroke:#0059b3,color:#003366
```

**Confidence**: HIGH (mechanical palette swap) unless the diagram's semantic grouping is unclear.

## 8.7 README Index

**Pattern**: a directory's `README.md` index is missing an entry for a file that exists, or lists
one that was deleted. **Fix**: sync the index against `Glob` results for that directory.
**Confidence**: HIGH.

## 8.8 Version Documentation

**Pattern**: a page is missing an LTS/version-support stub. **Fix**: add the standard stub with
full YAML frontmatter (`version`, `lts_until`, `status`). **Confidence**: MEDIUM — verify the
actual LTS date before writing it.

## Re-Validation Strategy

For every sub-pattern: re-read the target file's current state before fixing (docs drift fast),
and re-check any file the fix's `find`/`sed` sweep touched — not just the originally-cited file.

## Execution Order

**P0** — File Naming (8.3, since renames affect every other pattern's paths) → **P1** — Principle
Alignment (8.1) and Cross-Reference (8.2) → **P2** — Structure (8.4) and Template (8.5) → **P3** —
Diagram (8.6) → **P4** — README Index (8.7) and Version Documentation (8.8).

## Tool Selection

Single-line/single-reference fixes: `sed` + grep-verify. Multi-line/structural fixes: the Python
pattern from reference module 01. Renames: `git mv`, never plain `mv` (preserves history).
