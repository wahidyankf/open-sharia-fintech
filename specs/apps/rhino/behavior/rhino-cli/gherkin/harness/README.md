# rhino — behavior/rhino-cli/gherkin/harness

Gherkin scenarios for rhino-cli agent-harness management commands.

Features in this domain:

- `agents-bindings.feature` — emit and validate the Amazon Q Developer binding bridge
- `agents-detect-duplication.feature` — detect duplicate agent definitions
- `agents-sync.feature` — sync agent definitions across platform bindings
- `agents-validate-claude.feature` — validate Claude Code agent files
- `governance-word-budget-agents-md.feature` — AGENTS.md word-budget audit (`governance word-budget validate`)
- `governance-word-budget-pre-push.feature` — word-budget pre-push gate (`governance word-budget validate`)
- `governance-word-budget-rule.feature` — word-budget governance rule (`governance word-budget validate`)
- `governance-word-budget-thresholds.feature` — word-budget threshold audit (`governance word-budget validate`)

> This directory was renamed from `gherkin/agents/` to `gherkin/harness/` (matching the `harness`
> CLI command group), and the four `governance-word-budget-*` files above were split in from
> `gherkin/repo-governance/` during the Phase 1 rename/split step of the
> `enforce-identical-rhino-cli-gherkin` plan. They were renamed from `repo-governance-*` once the
> byte-based `agents-md-size` validator was deleted, so every file name now matches the
> `governance word-budget validate` command it exercises. The remaining `agents-*` names are
> historical; renaming those is a separate concern. `agents-validate-naming.feature` was
> deleted along with the agent role-suffix rule and its validator — see
> [Withdrawn Rules](../../../../../../../repo-governance/conventions/structure/file-naming.md#withdrawn-rules). Consolidating these four into
> `gherkin/governance/` alongside `governance-word-budget.feature` requires moving their step
> definitions between cucumber runners and is likewise deferred.

See [Specs Directory Structure Convention](../../../../../../../repo-governance/conventions/structure/specs-directory-structure.md)
for the canonical purpose of this folder.
