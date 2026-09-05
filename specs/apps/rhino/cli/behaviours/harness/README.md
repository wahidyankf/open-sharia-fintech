# rhino — cli/behaviours/harness

Gherkin scenarios for rhino-cli agent-harness management commands.

Features in this domain:

- `agents-bindings.feature` — generate and validate every generated-tier harness binding
- `agents-skills-mirror.feature` — mirror `.claude/skills/` into `.agents/skills/` as real files, never symlinks
- `agents-detect-duplication.feature` — detect duplicate agent definitions
- `agents-sync.feature` — sync agent definitions across platform bindings
- `agents-validate-claude.feature` — validate Claude Code agent files
- `harness-audit.feature` — aggregate every harness validator into one pass/fail report
- `codex-binding.feature` — generate the Codex agent binding: standalone TOML files plus the delimited `.codex/config.toml` region
- `vendored-skill-preservation.feature` — the mirror emitter touches only what it generates, leaving declared vendored plugin directories byte-identical
- `harness-ownership.feature` — every tracked binding file carries exactly one declared ownership class: generated, vendored, or source
- `harness-sync-triage.feature` — divergence between canonical source and its generated mirrors is triaged by content, and a mirror edit is promoted only as a human-reviewed patch
- `harness-catalog.feature` — the Platform Binding Directories table is rendered from the harness registry, and a hand edit inside the generated region is rejected
- `governance-word-budget-pre-push.feature` — word-budget pre-push gate (`governance word-budget validate`)
- `governance-word-budget-rule.feature` — word-budget governance rule (`governance word-budget validate`)

> This directory was renamed from `gherkin/agents/` to `gherkin/harness/` (matching the `harness`
> CLI command group), and the remaining `governance-word-budget-*` files above were split in from
> `gherkin/repo-governance/` during the Phase 1 rename/split step of the
> `enforce-identical-rhino-cli-gherkin` plan. They were renamed from `repo-governance-*` once the
> byte-based `agents-md-size` validator was deleted, so every file name now matches the
> `governance word-budget validate` command it exercises. The remaining `agents-*` names are
> historical; renaming those is a separate concern. `agents-validate-naming.feature` was
> deleted along with the agent role-suffix rule and its validator — see
> [Withdrawn Rules](../../../../../../repo-governance/conventions/structure/file-naming.md#withdrawn-rules).
> Threshold behaviour now lives in `gherkin/governance/governance-word-budget.feature`; this
> directory retains only harness-specific governance and pre-push behaviour.

See [Specs Directory Structure Convention](../../../../../../repo-governance/conventions/structure/specs-directory-structure.md)
for the canonical purpose of this folder.
