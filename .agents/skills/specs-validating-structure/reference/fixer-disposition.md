# Fixer Mechanics: Fix Disposition by Category

Maps `specs-checker`'s nine categories (see
[validation-categories-1-4.md](validation-categories-1-4.md) and
[validation-categories-5-9.md](validation-categories-5-9.md)) to `specs-fixer`'s fix
disposition.

## Fix Disposition by Category

**Fixable automatically (HIGH confidence)**: Category 1 missing README (generate from directory
contents using the standard template, for all five canonical folders and per-surface subfolders);
Category 2 README scenario/feature counts and domain listings (recount from actual `.feature`
files); Category 3 feature file naming (kebab-case via `git mv`); Category 5 C4 color palette
(replace non-standard colors with the accessible palette) and C4 README file listings; Category 6
broken cross-references (fix relative paths from actual file locations); Category 8 directory
structure violations (move feature files to correct nesting via `git mv`, per
[Specs Directory Structure Convention](../../../../repo-governance/conventions/structure/specs-directory-structure.md));
allowlist-gate findings from `nx run rhino-cli:validate:specs-counts`/`-links` (create missing
folder + `README.md` + placeholder spec; repair or remove a broken link).

**Requires Review (MEDIUM confidence)**: Category 1 missing user-story blocks (template
generatable, content needs human review); Category 4 cross-folder coverage gaps, contradictions
(needs domain decision), actor-name inconsistency (may cascade to implementations); Category 3
Background step inconsistency (may change test behavior); Category 9 adoption gaps — always
flagged and documented, **never auto-fixed**, adoption is a team decision; Category 8 tree-shape
migrations at the subtree level — flagged and documented, **never auto-fixed**, migration is a
plan-level operation requiring an atomic commit across rhino-cli path constants, Nx cache inputs,
and step definitions; drift-detection re-introduction (routes/endpoints/contracts) — flags only,
requires a new dedicated plan.

**Skip (FALSE_POSITIVE or unfixable)**: implementation alignment (Category 7 — out of scope, that
is a developer agent's job); step wording consistency (subjective); scenario count variance across
perspectives (legitimate).
