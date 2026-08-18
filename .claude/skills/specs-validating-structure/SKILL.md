---
name: specs-validating-structure
description: Validation methodology for specs/ folders — nine categories covering README/feature-file structural completeness, Gherkin format compliance, cross-folder consistency, C4 diagrams, cross-references, spec-to-implementation alignment, tree-shape compliance, and BDD/DDD/contracts adoption gaps. Used by specs-checker and specs-fixer.
---

# Validating Specs Structure

Methodology for validating explicitly-listed `specs/` folders (and their subfolders) for
structural completeness, content accuracy, internal consistency, and cross-folder coherence.

## Scope Rule

Validate **only** explicitly listed folders and their subfolders — never implicit discovery.
Cross-folder consistency (Category 4) runs only when 2+ folders are listed; it's skipped for a
single folder. Subfolders are always included automatically.

## The Nine Validation Categories

See [reference/01-validation-categories-1-4.md](reference/validation-categories-1-4.md) for
Structural Completeness (README coverage), Feature File Inventory Accuracy, Gherkin Format
Compliance, and Cross-Folder Consistency, and
[reference/02-validation-categories-5-9.md](reference/validation-categories-5-9.md) for C4
Diagram Consistency, Cross-Reference Integrity, Spec-to-Implementation Alignment, Spec Tree Shape
Compliance (deterministic via `rhino-cli specs validate-tree`), and Adoption Gaps (deterministic
via `rhino-cli specs validate-adoption`).

## Drift Detection, Execution Pattern, and Report Format

See [reference/03-drift-detection-and-reporting.md](reference/drift-detection-and-reporting.md)
for the four `nx run rhino-cli:validate:specs-*` deterministic targets, the six-step execution
pattern, and the full audit report template.

## Fixer Mechanics

See [reference/04-fixer-disposition.md](reference/fixer-disposition.md) for how `specs-fixer`
maps each of the nine categories to a fix disposition (auto-fixable / requires review / skip), and
[reference/05-fixer-execution-and-safety.md](reference/fixer-execution-and-safety.md) for its
execution pattern, fix report format, safety rules, and changed-file capture.

## What This Methodology Does NOT Cover

Test code or step definitions (`rhino-cli specs coverage`), governance docs (`repo-rules-checker`),
running tests (CI). This methodology is read-only — no file modification.

## Related

**Conventions**: [App README vs Specs Convention](../../../repo-governance/conventions/structure/app-readme-vs-specs.md),
[Specs Directory Structure Convention](../../../repo-governance/conventions/structure/specs-directory-structure.md).

**Agents**: `specs-checker` (implements this methodology), `specs-fixer`, `specs-maker`.
