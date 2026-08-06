# specs-checker Documents Phantom Nx Targets

One-line summary: `.claude/agents/specs-checker.md`'s "Drift Detection" section describes Nx targets
(`validate:specs-{adoption,tree,counts,links}`) that don't exist anywhere in `apps/rhino-cli/project.json`
or any other project's target list.

> Idea, added 2026-07-31.
> Relocated from beaver-nest/plans/ideas/specs-checker-phantom-nx-targets.md on 2026-08-06 by plan-ideas-grooming.

## Problem / context

Surfaced incidentally during the `baseerah-repo-reset` plan's Phase 3 Gate deleted-app-name sweep
(task #163) — unrelated to that sweep's actual scope, but a real doc/code drift bug worth tracking
separately rather than silently dropping. The agent file's Drift Detection section instructs whoever
reads it to run Nx targets that were either renamed, never implemented, or removed at some point
without the doc being updated to match.

**Data point:** none of `validate:specs-adoption`, `validate:specs-tree`, `validate:specs-counts`,
`validate:specs-links` appear in `apps/rhino-cli/project.json`'s target list (confirmed via the
Phase 3 Gate sweep agent's investigation).

## Why now

Not urgent, not blocking — `specs-checker` likely has other real validation paths that still work; this
is one section referencing dead commands. Worth fixing before someone follows the doc literally and
hits "no such target" confusion.

## Prior art / precedents

- **baseerah-repo-reset Phase 3 Gate** — where this was found, deliberately not fixed there since it's
  orthogonal to the app-name pruning sweep that task was scoped to.

## Proposed direction (sketch)

- Read `.claude/agents/specs-checker.md`'s Drift Detection section in full and cross-check each named
  command against `apps/rhino-cli`'s actual current target list / CLI subcommands
  (`cargo run ... -- specs --help` and equivalents).
- Either update the doc to the current real command names, or remove the section if the functionality
  it describes was genuinely retired rather than renamed.

## Rough scope & non-goals

In scope: `.claude/agents/specs-checker.md`'s Drift Detection section only (plus its regenerated
`.opencode/`/`.cursor` mirrors via `npm run generate:bindings` — no hand-editing the mirrors).

Out of scope: any other section of `specs-checker.md`; other agents' documentation accuracy (a
separate, much larger concern if it turns out to be systemic).

## Risks & open questions

- Is this an isolated stale section, or a symptom of `specs-checker.md` (and possibly sibling
  checker agents) not being kept in sync with `rhino-cli`'s CLI surface as it evolves? Worth a quick
  scan of the other checker agents' command references before concluding it's isolated. (open)

## What success looks like + promotion signal

Success: `specs-checker.md`'s Drift Detection section names only commands that actually exist and
resolve. Promote to a plan only if the open question above finds this is systemic across multiple
agent files rather than a single stale section.
