# rhino — cli/behaviors/convention

Gherkin scenarios for rhino-cli repository-convention audit commands.

Features in this domain:

- `repo-governance-emoji-audit.feature` — emoji usage audit (`convention emoji validate`)
- `repo-governance-license-audit.feature` — license audit (`convention license validate`)

> Feature file names still say `repo-governance-*` for historical reasons — these two files were
> split out of `gherkin/repo-governance/` (their content actually covers the `convention` command
> group, not `repo-governance`) during the Phase 1 rename/split step of the
> `enforce-identical-rhino-cli-gherkin` plan. Renaming the files themselves is a separate,
> later concern.

See [Specs Directory Structure Convention](../../../../../../repo-governance/conventions/structure/specs-directory-structure.md)
for the canonical purpose of this folder.
