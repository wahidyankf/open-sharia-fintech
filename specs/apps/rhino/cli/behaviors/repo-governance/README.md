# rhino — cli/behaviors/repo-governance

Gherkin scenarios for rhino-cli repository governance audit commands.

Features in this domain:

- `repo-governance-audit.feature` — general governance audit
- `repo-governance-layer-coherence.feature` — governance layer coherence
- `repo-governance-traceability-audit.feature` — traceability audit
- `repo-governance-vendor-audit.feature` — vendor independence audit

> The frontmatter-dates audit, README-index audit, emoji audit, license audit, and
> instruction-size audits previously lived here but actually cover the `md`, `convention`, and
> `harness` command groups respectively — they moved to
> [`../md/`](../md/README.md), [`../convention/`](../convention/README.md), and
> [`../harness/`](../harness/README.md) during the Phase 1 rename/split step of the
> `enforce-identical-rhino-cli-gherkin` plan. The README-index audit later moved again, from
> `../md/` to [`../governance/`](../governance/README.md), and the instruction-size audit was
> renamed to the word-budget audit (still under `../harness/`) — both during the
> `optimize-governance-md` plan's Phase 1b.

See [Specs Directory Structure Convention](../../../../../../repo-governance/conventions/structure/specs-directory-structure.md)
for the canonical purpose of this folder.
