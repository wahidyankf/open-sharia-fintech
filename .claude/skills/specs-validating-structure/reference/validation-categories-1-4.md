# Validation Categories 1-4: Structural, Inventory, Format, Cross-Folder

## Category 1: Structural Completeness (README Coverage) [LLM]

Every directory within listed folders must have a `README.md`: the five top-level folders
(`product/`, `system-context/`, `containers/`, `components/`, `behavior/`), per-surface subfolders
(`components/be|web|cli/`, `behavior/<product>-<surface>/gherkin/`), all domain subdirectories
under `behavior/<product>-<surface>/gherkin/<domain>/` (required for every surface), DDD
subdirectories (`ddd/`, `ddd/ubiquitous-language/`), and `containers/contracts/` when present.
Check recursively. **CRITICAL**: missing README.md. **HIGH**: README exists but is empty or lacks
required sections (overview, contents listing).

## Category 2: Feature File Inventory Accuracy [LLM]

For each listed folder with gherkin specs: count actual `.feature` files recursively, count
`Scenario:`/`Scenario Outline:` lines per feature, list actual domain directories, compare against
README claims. **CRITICAL**: README claims N scenarios but actual count differs. **HIGH**: README
claims N feature files but actual count differs; README lists a domain with no corresponding
directory/feature. **MEDIUM**: domain directory exists but README doesn't mention it.

## Category 3: Gherkin Format Compliance [LLM]

**CRITICAL**: feature file missing `Feature:` header. **HIGH**: missing user story block (As a / I
want / So that); Background step inconsistent within a folder. **MEDIUM**: filename not
kebab-case. **LOW**: scenario names not sentence case.

## Category 4: Cross-Folder Consistency [LLM] — 2+ folders only

Contradiction detection: **CRITICAL** two folders define the same actor/entity with conflicting
attributes; **HIGH** shared domain with contradictory scenarios, or a folder references another
using a wrong/outdated path. Coherence: **HIGH** counterpart folders (e.g. `components/be` and
`components/web`) have mismatched domain coverage (excluding perspective-specific domains like
`layout/`); **MEDIUM** shared domain has >50% scenario-count variance, or actor names differ for
the same persona; **LOW** step wording inconsistency for the same concept. Blend: **HIGH** C4
diagrams show the same system boundary with contradictory containers/components; **MEDIUM** stale
cross-references between folders; **LOW** terminology drift for the same concept.
