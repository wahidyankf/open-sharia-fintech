# Sync `ose-primer` Governance Parity

## Context

[`optimize-governance-md`](../../done/2026-08-15__optimize-governance-md/README.md) introduced a
500-word ceiling on governance Markdown
across `ose-public` **and** `ose-private`: two new rhino-cli gates
(`governance-word-budget`, `governance-readme-completeness`), a rename-in-place of the
already-live `md-readme-index` gate to `governance-readme-index`, and the `md-frontmatter` gate's
`description` field flipped from WARN to FAIL for governance docs. It did this identically in both
repos, including a byte-for-byte sync of the `apps/rhino-cli` boundary into `ose-private`.

**`ose-primer` was deliberately left out of that plan's scope.** Per
[Related Repositories §Sync cadence across repos](../../../docs/reference/related-repositories.md#sync-cadence-across-repos)
`[Repo-grounded]`: `ose-private` is kept in real-time sync because it backs live operations, while
`ose-primer` — the reusable polyglot starter — is kept on a **delayed** sync, batching updates to
conserve review cost for a repo that does not need every governance change the moment it lands.
`optimize-governance-md`'s own README records this as an "Accepted divergence," explicitly requiring
"A follow-up plan must close it." **This is that follow-up plan.**

### What is actually out of sync (verified live, 2026-08-15)

[Repo-grounded, read directly against `/Users/wkf/ose-projects/ose-primer` — a normal (non-bare)
checkout on `main`, clean working tree, HEAD `4161f0507`]

**1. The rhino-cli boundary has drifted.** `ose-primer`'s `apps/rhino-cli` still carries the
pre-`optimize-governance-md` module and command names — `instruction_size.rs`,
`harness_validate_instruction_size.rs`, `convention_validate_instruction_size.rs`,
`readme_index_audit.rs`, `md_validate_readme_index.rs` — where `ose-public` now has
`word_budget.rs`, `readme_index.rs`, `governance_validate_word_budget.rs`,
`governance_validate_readme_index.rs`, `governance_generate_readme_index.rs`. Neither
`governance word-budget validate` nor `governance readme-index validate` exists as a command in
`ose-primer` today. `apps/rhino-cli/parity-manifest.sha256` pins **659** files in `ose-primer`
versus **651** in `ose-public` (both counts drift as either plan lands further commits — re-verify
live, do not trust these numbers past this plan's Phase 0).

**2. `repo-governance/` content has not been split.** [Repo-grounded, `wc -w` census] Of 186
Markdown files under `ose-primer/repo-governance/`, **158** exceed 500 words. Combined with
`.claude/agents/` (67 files, 58 over) and `.claude/skills/` (41 files, 32 over), plus the
generated mirrors `.cursor/` (66 files, 55 over), `.opencode/` (81 files, 67 over), and
`.amazonq/` (1 file, 0 over), the full covered surface is **444 files, 372 over the 500-word
ceiling** — including `AGENTS.md` (3,109 words) and `CLAUDE.md` (756 words). Root `README.md`
(877 words) is already under the 900-word README ceiling — no action needed there. Reachability
is close to solved already: only **1** directory under `repo-governance/` lacks a `README.md`.
Retrieval is not: **0** of 186 `repo-governance/**/*.md` files carry `when_to_use`; 22 are
missing `description`.

**3. The two new gates are not registered at all.** `ose-primer/repo-config.yml` has no
`governance-word-budget` or `governance-readme-completeness` entry. It still carries the
now-replaced `instruction-size:` top-level config block (lines 200–243) and the `instruction-size`
gate id (byte-budget, superseded by the word cap in `ose-public`/`ose-private`), and its
`md-readme-index` gate is still under the pre-rename id. Its `md-frontmatter` gate **already**
registers a `ci: { scope: all-file-type }` surface — the exact precondition that broke `ose-private`
PR10's CI the moment the byte-identical `frontmatter.rs` (which hardcodes FAIL severity for
governance docs, no WARN/FAIL toggle in the Rust source) landed ahead of the content splits that
make that severity survivable. This plan applies the same mitigation `ose-private`'s Phase 10
discovered, proactively, in Phase 1 rather than waiting to hit it in CI.

## What This Plan Changes

Three changes, mirroring `optimize-governance-md`'s own three-part shape, applied to `ose-primer`
only:

1. **rhino-cli boundary sync** — copy `apps/rhino-cli`'s `src/`, `tests/`, `Cargo.toml`,
   `Cargo.lock`, `project.json`, `LICENSE`, and the Gherkin behavior tree byte-for-byte from
   `ose-public` into `ose-primer`, re-establishing the
   [rhino-cli Byte-Identity Boundary](../../../docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary).
   Register the two new gates **dark-launched** (unarmed) at the same time, exactly matching
   `ose-public`'s Phase 1 / `ose-private`'s Phase 10 registration state.
2. **Content parity** — split every `repo-governance/`, `.claude/agents/`, `.claude/skills/` file
   over 500 words into an index parent plus capped children; add `when_to_use` frontmatter;
   backfill missing `description`; regenerate the `.cursor/`/`.opencode/`/`.amazonq/` mirrors via
   `npm run generate:bindings`; rewrite `AGENTS.md`/`CLAUDE.md` as directive indexes under the
   same ceiling.
3. **Arm the gates** — flip `governance-word-budget` and `governance-readme-completeness` from
   dark-launched to enforced (`pre-push` + `ci`), and re-register `md-frontmatter`'s `ci` surface
   now that the content backing it is compliant.

## Decisions and Rationale

| Decision           | Choice                                                                                                                                                         | Why                                                                                                                                                                                                                                 |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Scope              | `ose-primer` only; no edits to `ose-public` or `ose-private`                                                                                                   | User-scoped; those two repos are already done                                                                                                                                                                                       |
| Mechanism          | Copy `ose-public`'s already-proven gate implementation and content-split pattern; do not reimplement or redesign                                               | The pattern is proven across two repos already; a third bespoke implementation would just be a third place for the boundary to drift                                                                                                |
| md-frontmatter gap | Proactively drop the `ci` surface at sync time (Phase 1), re-add it once content is split (Phase 4)                                                            | `[Judgment call]` — applying `ose-private`'s Phase 10 discovered mitigation up front avoids repeating a CI break that is already fully understood                                                                                   |
| Phase granularity  | 6 phases (0–5): baseline, rhino-cli sync, `repo-governance/`+root-files split, `.claude/`+mirrors split, arm, knowledge capture                                | `[Judgment call]` — `ose-primer`'s governance surface (444 files) is under half `ose-public`'s pre-split size (658 in the source-only count); one phase per tree is proportionate rather than the parent plan's per-subtree fan-out |
| `.codex/` scope    | Kept in the covered-surface/trigger declarations even though currently 0 `.md` files                                                                           | `[Judgment call]` — matches `ose-public`'s boundary declaration; a future file added there stays covered without a repo-config.yml edit                                                                                             |
| Delivery mode      | `worktree-to-pr` (mandatory in `ose-public`/`ose-primer` — `main` is branch-protected in both)                                                                 | [Repo-grounded, `AGENTS.md` §Git Workflow, both repos]                                                                                                                                                                              |
| Review cycle       | Full PR-Review Maker→Fixer Cycle on Phase 1 (rhino-cli) and Phase 4 (gate arming); `pr-quality-gate.yml`-only on Phases 2, 3, 5 (markdown/config-content only) | Mirrors exactly how `optimize-governance-md` classified its own executable vs. markdown-only phases                                                                                                                                 |

## Top Risks

### The `md-frontmatter` premature-FAIL gap is a known, already-hit failure mode

[Repo-grounded — `ose-private` PR10, `optimize-governance-md/delivery.md` Phase 10 "Discovered
gap" note] The exact same byte-for-byte copy mechanism this plan uses already broke CI once,
because the copied Rust source hardcodes FAIL severity with no config toggle, while the target
repo's `repo-config.yml` already registers a full-tree `ci` scan for `md-frontmatter`. This plan's
Phase 1 applies the known mitigation proactively (see `tech-docs.md` §2) instead of discovering it
live a second time.

### Content-split judgment work is not mechanical

Splitting 158 `repo-governance/` files, 58 agent files, and 32 skill files into index parent +
capped children requires the same content judgment `optimize-governance-md` exercised by hand
across two repos — this is not a scripted transform. `ose-primer`'s content is not
byte-identical to `ose-public`'s (it is a _starter_, not the product), so the split cannot be a
blind copy of `ose-public`'s post-split shape; each file's own content decides its own split
boundary.

### `ose-primer`'s AGENTS.md/CLAUDE.md are not byte-identical to `ose-public`'s

Both repos' `AGENTS.md`/`CLAUDE.md` are platform-binding shims with repo-specific content (see
`ose-primer/CLAUDE.md`'s own "Platform Binding Examples" section). Rewriting `ose-primer`'s
`AGENTS.md` (3,109 → ≤500 words) as a directive index must preserve `ose-primer`'s own directives,
not copy `ose-public`'s post-split `AGENTS.md` verbatim.

## Repos and Delivery

| Repo         | Worktree                                  | Plan docs         | PRs                                              |
| ------------ | ----------------------------------------- | ----------------- | ------------------------------------------------ |
| `ose-public` | `worktrees/sync-primer-governance-parity` | **Authoritative** | 1 (PR5, markdown-only — plan-doc lifecycle only) |
| `ose-primer` | `worktrees/sync-primer-governance-parity` | none (uses this)  | 4 (PR1–PR4; 2 executable, 2 markdown-only)       |

**Delivery mode**: `worktree-to-pr` in **both** repos — `main` is branch-protected in each,
including `ose-public`, where the historical plan-docs-only direct-push carve-out is
[retired](../../../repo-governance/workflows/plan/plan-planning/07-plan-docs-only-carve-out.md#the-plan-docs-only-carve-out-superseded--retired-in-two-of-three-repos).
Phases 2 and 3 are `ose-primer` markdown/doc-only static work — they merge on a green
`.github/workflows/pr-quality-gate.yml` run with no PR review cycle. Phases 1 and 4 (`ose-primer`)
carry changed executable behaviour (rhino-cli source, `repo-config.yml` gate enforcement) and run
the full PR-Review Maker→Fixer Cycle. Phase 5 is the sole `ose-public` PR: it lands this plan's own
accumulated doc-lifecycle changes (delivery ticks, `learnings.md`, `evidence/`) plus the archival
move, as markdown-only static work.

All product-surface delivery (rhino-cli boundary sync, `repo-governance/`/`.claude/` content
splits, gate arming) happens inside the `ose-primer` worktree — **no `ose-public` product-surface
file changes** as part of this plan; `ose-public`'s own worktree is used exclusively for this
plan's own doc-lifecycle bookkeeping and final archival.

## Open Questions (judgment calls made without blocking — see report)

- Phase granularity (one phase per tree rather than the parent plan's per-subtree fan-out) —
  revisit if `repo-governance/`'s actual split work proves too large for one PR's review budget.
- Whether `.codex/` (0 md files today) needs any live content action, or is purely a forward-looking
  scope declaration — currently the latter.
- Exact final wording of `ose-primer`'s post-split `AGENTS.md`/`CLAUDE.md` directive index —
  deferred to Phase 2 content-authoring judgment, not resolved at plan-authoring time.

## Documents

- [brd.md](./brd.md) — business goal and impact
- [prd.md](./prd.md) — requirements and Gherkin acceptance criteria
- [tech-docs.md](./tech-docs.md) — gate registration mechanics, split pattern, file-impact analysis
- [delivery.md](./delivery.md) — phased delivery checklist
- [learnings.md](./learnings.md) — running learnings log (empty until execution begins)
