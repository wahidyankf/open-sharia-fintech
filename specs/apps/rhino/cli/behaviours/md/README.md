# rhino — cli/behaviours/md

Gherkin scenarios for rhino-cli documentation validation commands.

Features in this domain:

- `docs-validate-frontmatter.feature` — frontmatter validation
- `docs-validate-heading-hierarchy.feature` — heading hierarchy validation
- `docs-validate-links.feature` — link validation
- `docs-validate-mermaid.feature` — Mermaid diagram validation
- `docs-validate-naming.feature` — file naming convention validation
- `repo-governance-frontmatter-audit.feature` — frontmatter-dates audit (`md frontmatter-dates validate`)

> This directory was renamed from `gherkin/docs/` to `gherkin/md/` (matching the `md` CLI command
> group), and `repo-governance-frontmatter-audit.feature` above was split in from
> `gherkin/repo-governance/` (its content actually covers `md` commands, not `repo-governance`)
> during the Phase 1 rename/split step of the `enforce-identical-rhino-cli-gherkin` plan. Feature
> file names still say `docs-*`/`repo-governance-*` for historical reasons — renaming the files
> themselves is a separate, later concern. `repo-governance-readme-index-audit.feature` (README
> sibling-index audit) was removed here and superseded by
> `gherkin/governance/governance-readme-index.feature` during the `optimize-governance-md` plan's
> Phase 1b, since the underlying command moved from `md readme-index validate` to
> `governance readme-index validate`.

See [Specs Directory Structure Convention](../../../../../../repo-governance/conventions/structure/specs-directory-structure.md)
for the canonical purpose of this folder.
