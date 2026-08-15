# Business Requirements: Sync `ose-primer` Governance Parity

## Business Goal

Close the deliberate, plan-recorded deferral from `optimize-governance-md`: bring `ose-primer`'s
`apps/rhino-cli` boundary and governance-Markdown surface to the same word-budget-enforced,
reachability-guaranteed state that `ose-public` and `ose-private` already have, so all three
sibling repos in the
[rhino-cli byte-identity family](../../../docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary)
share one enforcement posture instead of two.

## Business Rationale

`ose-primer` is the reusable polyglot starter maintainers and downstream adopters clone to bootstrap
new products from OSE's own practices [Repo-grounded, `docs/reference/related-repositories.md`].
Every day it carries an un-split, unenforced governance tree is a day a fresh clone starts from the
same over-grown, hard-to-navigate state `optimize-governance-md` fixed in the other two repos —
median governance file well over the 500-word ceiling, no `when_to_use` retrieval signal anywhere,
and a rhino-cli boundary that has already begun to name-drift from its two siblings. The
[sync-cadence policy](../../../docs/reference/related-repositories.md#sync-cadence-across-repos)
explicitly permits batching this work rather than landing it in real time — this plan is that batch,
filed at the close of `optimize-governance-md` rather than left open indefinitely.

## Business Impact

**Pain point**: a maintainer or agent working in a freshly-cloned `ose-primer` today inherits the
same problems `optimize-governance-md`'s own `README.md` §Context documented for `ose-public`
before that plan started — 372 of 444 covered governance files over budget, zero retrieval
signal, and a rhino-cli that no longer matches its two siblings' command surface
(`governance word-budget validate` / `governance readme-index validate` do not exist there today).

**Expected benefit**: once this plan lands, all three repos in the rhino-cli family enforce the
identical ceiling, the identical two new gate ids, and the identical `md-frontmatter` FAIL
severity for governance docs — closing the "Accepted divergence" `optimize-governance-md`
explicitly flagged as needing a follow-up.

## Affected Roles

Solo-maintainer repo — no sign-off ceremonies. The "roles" below are hats the maintainer wears and
agents that consume the changed surfaces:

- **Repo maintainer** — reviews and merges the two executable PRs (rhino-cli sync, gate arming).
- **`ose-primer` downstream adopters** — anyone bootstrapping a new product from this starter
  inherits whichever governance shape is live at clone time; this plan is what keeps that shape
  current with `ose-public`'s.
- **AI agents operating in `ose-primer`** — `plan-maker`, `plan-checker`, `repo-rules-checker`, and
  every governance-consuming agent read `repo-governance/**` and `.claude/**`; the same reachability
  and retrieval benefits `optimize-governance-md`'s `brd.md` documented for `ose-public` apply here.

## Business-Level Success Metrics

[Repo-grounded, measured 2026-08-15 against `/Users/wkf/ose-projects/ose-primer`, HEAD `4161f0507`
— re-verify live in Phase 0, these numbers drift]

| Metric                                                                                                           | Before this plan                      | Target after this plan            |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------- | --------------------------------- |
| Governance files over the 500-word ceiling (full covered surface)                                                | 372 / 444                             | 0                                 |
| `repo-governance/**/*.md` with `when_to_use` frontmatter                                                         | 0 / 186                               | 186 / 186                         |
| `repo-governance/**/*.md` with `description` frontmatter                                                         | 164 / 186                             | 186 / 186                         |
| `repo-governance/` directories missing a `README.md`                                                             | 1                                     | 0                                 |
| rhino-cli commands matching `ose-public` (`governance word-budget validate`, `governance readme-index validate`) | 0 of 2 present                        | 2 of 2 present                    |
| `apps/rhino-cli` boundary diff against `ose-public`                                                              | non-empty (module/command name drift) | empty across all 7 boundary paths |
| `governance-word-budget` / `governance-readme-completeness` gate ids registered                                  | 0                                     | 2 (armed)                         |

The word-count figures above are [Repo-grounded, `wc -w` census] reproduced in `README.md`
§Context; re-derive live in Phase 0 rather than trusting this table past that point — both
`ose-public` and `ose-primer` continue landing commits after this plan is authored.

## Business-Scope Non-Goals

- **No changes to `ose-public` or `ose-private`** — both are already done; this plan touches only
  `ose-primer`.
- **No redesign of the word-budget or readme-index mechanism** — the gate logic, thresholds
  (400 warn / 500 fail), and split pattern (index parent + sibling directory) are inherited
  verbatim from `optimize-governance-md`'s already-shipped, already-reviewed design. This plan is a
  parity sync, not a design revision.
- **No change to `ose-primer`'s product-specific content** (`apps/`, `libs/`, `docs/`, `specs/`,
  `plans/`) beyond what the governance-word-budget gate's own scope already touches
  (`AGENTS.md`, `CLAUDE.md`, root `README.md` if it were over budget — it is not, at 877 words).

## Business Risks and Mitigations

### Risk: content-split judgment work stalls behind a scripted expectation

`ose-primer`'s content is not byte-identical to `ose-public`'s (starter vs. product), so this is
authored content work, not a mechanical copy, for `repo-governance/`, `.claude/agents/`, and
`.claude/skills/`. **Mitigation**: the delivery checklist budgets full phases for this
(Phases 2–3), matching the effort class `optimize-governance-md` itself budgeted per subtree, not
a single "just copy it" step.

### Risk: repeating the `md-frontmatter` CI break `ose-private`'s PR10 already hit

**Mitigation**: Phase 1 applies the already-discovered mitigation proactively (drop the `ci`
surface at sync time, re-add once content is split) instead of waiting to rediscover it in CI —
see `tech-docs.md` §2.

### Risk: `ose-primer`'s parity-manifest drift compounds if this plan itself stalls

Every commit either repo lands after this plan is authored but before it executes changes the
"651 vs 659" baseline this plan's README cites. **Mitigation**: Phase 0 re-derives the live
baseline rather than trusting authoring-time numbers; the delivery checklist's acceptance criteria
are phrased as "boundary diff is empty," not as fixed file counts.
