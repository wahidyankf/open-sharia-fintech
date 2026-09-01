# rhino — cli/behaviors/governance

Gherkin scenarios for rhino-cli's `governance` subcommand family — the word-count size gate and
the README sibling-index gate introduced by the
`plans/done/2026-08-15__optimize-governance-md` plan.

Features in this domain:

- `governance-word-budget.feature` — the word-based per-file size gate and the resolved-tree
  check that replaces the byte-based `harness instruction-size validate` gate
  (`governance word-budget validate`)
- `governance-readme-index.feature` — the README sibling-index gate, a rename-and-extend of the
  already-armed `md readme-index validate` command (`governance readme-index validate`)

See [Specs Directory Structure Convention](../../../../../../repo-governance/conventions/structure/specs-directory-structure.md)
for the canonical purpose of this folder.
