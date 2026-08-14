# The Nine Validation Categories

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

## Category 5: C4 Diagram Consistency [LLM]

C4 diagrams live in `system-context/context.md`, `containers/container.md`,
`components/be/component-be.md`, `components/web/component-web.md`. **HIGH**: README lists
diagram files that don't exist; diagram references undefined actors/containers/components.
**MEDIUM**: diagram doesn't use the color-blind-friendly palette (Blue #0173B2, Orange #DE8F05,
Teal #029E73, Purple #CC78BC, Brown #CA9161, Gray #808080); actor names inconsistent across
context/container/component levels. **LOW**: no `classDef` styling.

## Category 6: Cross-Reference Integrity [LLM]

**CRITICAL**: markdown link to a non-existent file. **HIGH**: README "Related" section references
a missing file. **MEDIUM**: wrong relative path depth. Only links originating FROM listed folders
are checked; links pointing outside are checked for existence only, not target content.

## Category 7: Spec-to-Implementation Alignment [LLM]

**HIGH**: spec README references an implementation absent from `apps/`. **MEDIUM**: spec area has
no consuming implementation (acceptable for new areas). **LOW**: implementation exists but spec
area doesn't mention it.

## Category 8: Spec Tree Shape Compliance [Deterministic via rhino-cli]

Shell out to `rhino-cli specs validate-tree <app>`, parse JSONL. **HIGH**: top-level folder isn't
one of the five canonical folders; a flat-root artifact exists (`be/`, `web/`, `cli/`, `c4/`,
`contracts/` at app root); a BE/web/CLI feature file sits directly under
`behavior/<surface>/gherkin/` without a domain subdirectory (all surfaces require domain subdirs —
`behavior/<surface>/gherkin/<domain>/<feature>.feature`); a lib feature file sits directly under
`gherkin/` without a package subdirectory. **MEDIUM**: domain subdirectory not kebab-case. **LOW**:
domain subdirectory contains only one feature file named differently than the directory.

## Category 9: Adoption Gaps (BDD/DDD/Contracts) [Deterministic via rhino-cli]

Shell out to `rhino-cli specs validate-adoption <app>`, parse JSONL, per
[App README vs Specs Convention](../../../../repo-governance/conventions/structure/app-readme-vs-specs.md)
Standard 6:

| Surface profile | BDD required   | DDD expected                     | Contracts required       |
| --------------- | -------------- | -------------------------------- | ------------------------ |
| Full-stack      | HIGH if absent | MEDIUM if absent                 | HIGH if REST API exposed |
| Web-only        | HIGH if absent | MEDIUM if absent                 | NOT APPLICABLE           |
| CLI / Multi-CLI | HIGH if absent | LOW if adopted without rationale | NOT APPLICABLE           |

**HIGH**: full-stack/web-only app has no Gherkin specs at all; full-stack app exposes a REST API
but has no `containers/contracts/openapi.yaml`. **MEDIUM**: BDD present but no DDD adoption after
two rollout cycles; missing API contracts after one rollout cycle for a REST-exposing full-stack
app. **LOW**: CLI app has `components/cli/ddd/` without documented rationale.

Adoption-gap findings are always `[Adoption Gap]`-tagged and route to **Requires Review** in the
fixer (never auto-fix) — adoption decisions require explicit justification.
