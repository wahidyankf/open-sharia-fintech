# Validation Categories 1-4: Structural, Inventory, Format, Cross-Folder

## Category 1: README Content Quality [LLM]

When `governance-readme-index` is delegated, do not check or infer README existence/index
membership. For READMEs that exist, retain semantic assessment of useful overview and contents.
Without delegation, the lifecycle command owns existence for each owner corpus's three required
entries (`README.md`, `architecture.md`, `behaviors/`), the `behaviors/README.md` index, all
domain subdirectories under `behaviors/<domain>/`, and `contracts/` when present.
Check semantic quality recursively. **HIGH**: README exists but is empty or lacks required
overview/contents information.

## Category 2: Feature File Inventory Accuracy [LLM]

When `specs-structure` is delegated, do not recount registered folders/files or infer numeric
mismatches. Retain narrative assessment that described domains and responsibilities are coherent.
Without delegation, use current structure/count commands rather than LLM counting.

## Category 3: Gherkin Format Compliance [LLM]

**CRITICAL**: feature file missing `Feature:` header. **HIGH**: missing user story block (As a / I
want / So that); Background step inconsistent within a folder. **MEDIUM**: filename not
kebab-case. **LOW**: scenario names not sentence case.

Repeated primary Given/When/Then cardinality belongs to `specs-gherkin-cardinality`; never
re-derive it when that exact ID is delegated.

## Category 4: Cross-Folder Consistency [LLM] — 2+ folders only

Contradiction detection: **CRITICAL** two folders define the same actor/entity with conflicting
attributes; **HIGH** shared domain with contradictory scenarios, or a folder references another
using a wrong/outdated path. Coherence: **HIGH** counterpart folders (e.g. `components/be` and
`components/web`) have mismatched domain coverage (excluding perspective-specific domains like
`layout/`); **MEDIUM** shared domain has >50% scenario-count variance, or actor names differ for
the same persona; **LOW** step wording inconsistency for the same concept. Blend: **HIGH** C4
diagrams show the same system boundary with contradictory containers/components; **MEDIUM** stale
cross-references between folders; **LOW** terminology drift for the same concept.
