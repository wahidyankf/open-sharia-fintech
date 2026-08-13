# rhino — behavior/rhino-cli/gherkin/harness

Gherkin scenarios for rhino-cli agent-harness management commands.

Features in this domain:

- `agents-bindings.feature` — emit and validate the Amazon Q Developer binding bridge
- `agents-detect-duplication.feature` — detect duplicate agent definitions
- `agents-sync.feature` — sync agent definitions across platform bindings
- `agents-validate-claude.feature` — validate Claude Code agent files
- `agents-validate-naming.feature` — validate agent naming conventions
- `repo-governance-agents-md-size.feature` — AGENTS.md word-budget audit (`governance word-budget validate`)
- `repo-governance-instruction-size-governance.feature` — word-budget governance rule (`governance word-budget validate`)
- `repo-governance-instruction-size-pre-push.feature` — word-budget pre-push gate, dark-launched until Phase 9 (`governance word-budget validate`)
- `repo-governance-instruction-size.feature` — word-budget threshold audit (`governance word-budget validate`)

> This directory was renamed from `gherkin/agents/` to `gherkin/harness/` (matching the `harness`
> CLI command group), and the four `repo-governance-*` files above were split in from
> `gherkin/repo-governance/` (their content actually covers `governance word-budget validate`,
> not `repo-governance`) during the Phase 1 rename/split step of the
> `enforce-identical-rhino-cli-gherkin` plan. Feature file names still say
> `agents-*`/`repo-governance-*` for historical reasons — renaming the files themselves is a
> separate, later concern. The `optimize-governance-md` plan's Phase 1b renamed the underlying
> command from `harness instruction-size validate` to `governance word-budget validate` (word-count
> metric, moved to the `governance` command group) without renaming these files again.

See [Specs Directory Structure Convention](../../../../../../../repo-governance/conventions/structure/specs-directory-structure.md)
for the canonical purpose of this folder.
