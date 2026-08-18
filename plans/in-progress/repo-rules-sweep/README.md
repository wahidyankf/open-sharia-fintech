# 🧹 Repo Rules Sweep

## Context

A standing sweep over the repository's **repo rules** — every normative surface, not one directory:
`repo-governance/`, `AGENTS.md`, `CLAUDE.md`, `.claude/` and its generated mirrors, `repo-config.yml`,
and the enforcement machinery in `apps/rhino-cli` (see
[glossary.md](../../../repo-governance/glossary.md)).

Rules here accreted through many separate plans. Some contradict each other, some describe a practice
the tree stopped following, and some are stated in six places that have drifted apart. This plan is
the container for correcting them one workstream at a time, so each correction gets a real delivery
unit, a real gate, and a real propagation sweep across the maker/checker/fixer triad.

**Structural rule**: a workstream is not executable until it is fully specified here. Phase 0 is
shared; each workstream adds phases before Knowledge Capture, which stays terminal with Archival.

## Workstreams

| ID | Workstream | Phases | Status |
| --- | --- | --- | --- |
| WS-A | Ordinal filename prefixes in governed trees | 1–4 | Specified |
| WS-B | File Naming Convention rework | — | **Declared, not executable** |

### WS-A — Ordinal filename prefixes

`repo-governance/` carries a numeric filename prefix on **2092 of 2494** markdown files across **176
numbered directories**; `ose-private` carries **1704 of 2131**, plus 217 under `.claude/`. That
numbering was never an ordering decision — it is residue from progressive-disclosure sharding under
the [Governance Word-Budget Convention](../../../repo-governance/conventions/structure/governance-word-budget.md).
`docs/` (0 of 211) and `specs/` (0 of 290) already navigate fine without it, because the annotated
`README.md` index carries navigation.

Three defects show the numbering has stopped paying for itself:

- **Insert pressure produced a letter escape.** `repo-governance/conventions/tutorials/swe-by-example/`
  holds 32 shards whose highest ordinal is 27, because inserts landed as `01b-`, `03b-`, `05b-`,
  `07b-`, `20b-`. Seven such files exist repo-wide.
- **Where order is genuinely semantic, the prefix contradicts it.**
  `repo-governance/workflows/infra/development-environment-setup/` runs
  `04-phase-1-system-package-manager.md` … `13-phase-11-repository-bootstrap.md` — two numbering
  systems in one basename, offset and drifting, with phase 5 skipped.
- **The governing convention already forbids the practice.**
  [File Naming Convention](../../../repo-governance/conventions/structure/file-naming.md) justifies
  itself as "no prefixes, abbreviations, or hierarchical encoding" while 84% of the tree it governs
  carries a prefix.

### WS-B — File Naming Convention rework

Declared because WS-A touches `file-naming.md` only enough to remove the contradiction it creates.
The broader rework — what that convention should say once prefixes are settled, and how it composes
with `workflow-naming.md`, `agent-naming.md`, and the report-filename standard — is a separate
workstream, **specified only after WS-A's Knowledge Capture records what is still wrong**.

## Scope

**Repositories**: `ose-public` and `ose-private`, both swept, in that order.

**Trees in scope**: `repo-governance/`, `.claude/` (with `.opencode/`, `.cursor/`, `.amazonq/`
regenerated), and `apps/rhino-cli` for the index tooling.

**Out of scope**: `plans/` (all 127 numbered files are immutable `done/` archives), `docs/` and
`specs/` (already unnumbered), `apps/` fixtures and content (public URL contract).

## The Rule (WS-A)

A filename carries a leading ordinal **only when the file is a real step in an ordered sequence and
the ordinal is that step's own number**. `01-init-with-repo-setup-manager.md` qualifies.
Everything else takes a plain kebab-case name — `common-syntax-errors.md` — and the parent index
carries the order. A basename never carries two numbering systems.

The rule is **prose only**: no gate, no `rhino-cli` detector, no audit category. `repo-rules-checker`
judges it as an AI-only category and `repo-rules-fixer` repairs it.

## Approach Summary

1. **Publish the rule and propagate it** through the `repo-rules-*` triad, their skills, and the
   `repo-rules-quality-gate` workflow.
2. **Make the index generator order-preserving** and add a rename-aware `rewrite-paths` mode.
3. **Sweep `ose-public`** — rename every non-qualifying file, rework continuation-shard boundaries
   into self-standing topics, re-split anything that busts the word budget on a topic seam.
4. **Sweep `ose-private`** the same way, with the tooling byte-identical.

## Documents

- [brd.md](./brd.md) — business goal, impact, success metrics, non-goals, risks.
- [prd.md](./prd.md) — personas, user stories, Gherkin acceptance criteria, product scope.
- [tech-docs.md](./tech-docs.md) — architecture, decisions, file-impact analysis, diagrams, rollback.
- [delivery.md](./delivery.md) — phased, tagged, gated delivery checklist.
- [learnings.md](./learnings.md) — running log drained by the Knowledge Capture phase.
