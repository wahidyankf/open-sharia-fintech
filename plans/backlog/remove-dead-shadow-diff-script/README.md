# Remove or Repurpose the Dead `shadow-diff.sh` Script

## Context

`apps/rhino-cli/scripts/shadow-diff.sh` was written during the prior Go→Rust rewrite
(`plans/done/2026-05-23__rhino-cli-rust-rewrite/`) to diff a Go binary against a Rust one, then was
repurposed during `rewrite-rhino-cli-to-fsharp` (Phase 2) to diff the Rust binary against the F#
port during the migration's wave-by-wave transition. It served that purpose well — several genuine
parity defects (a stale `target/gate` binary comparison, two Wave-D-only formatting bugs) were only
caught by treating its output as a first-class gate. Phase 9c deleted the Rust crate outright, which
means the script's Rust-side binary resolution (`apps/rhino-cli/target/{release,gate}/rhino-cli`,
`cargo build --profile gate`) now has nothing to resolve — the comparison is **permanently
unreachable**, not merely stale. The `rewrite-rhino-cli-to-fsharp` plan's own Phase 11a
rules-propagation sweep (R1) had to carve this file out by name as "not a hook, Nx target, or
workflow, and not invoked by any live automation today," and `tech-docs.md`'s File-Impact Analysis
deliberately marks it `[N]` with no `[D]` at any phase — a loose end the migration plan repeatedly
noted but never closed, because closing it was out of scope for every phase that touched it.

This item exists to close that loose end: either delete the script (its purpose is fully consumed)
or repurpose it into something with a live subject (e.g., a generic two-binary CLI differential
runner other future language migrations in this repo could reuse). No code change from this repo's
history depends on the file continuing to exist under its current name and content.

## Scope

**In scope**: `apps/rhino-cli/scripts/shadow-diff.sh`; any repo-wide reference to it (grep confirms
current references are limited to `docs/reference/sdlc-gate-standard.md`'s historical
dispatch-mechanism notes and this plan's own now-archived `learnings.md`, neither of which needs
further editing — they already describe it in the past tense).

**Out of scope**: designing a _new_ general-purpose differential-testing tool. If repurposing is
selected, it is repurposed only as far as making it generically two-binary-comparison-shaped; it is
not extended with new comparison surfaces beyond what it already covers (`md`, `governance`, `git`
namespaces).

## Business Rationale (condensed BRD)

**Why**: dead, unreachable tooling left in a scripts directory is a maintenance and comprehension
tax — a future contributor who finds `shadow-diff.sh` and does not know this history will either try
to run it (and get a confusing "no Rust binary" failure) or waste time deciding whether it is safe to
delete. Removing or clearly repurposing it prevents that friction.

**Affected roles**: any contributor working in `apps/rhino-cli/scripts/`.

**Success metric**: zero unreachable/dead scripts in `apps/rhino-cli/scripts/`; `grep -rn
'shadow-diff.sh'` outside `plans/done/**` returns either nothing (deleted) or only references to a
live, working tool (repurposed).

## Product Requirements (condensed PRD)

**User story**: As a contributor maintaining `rhino-cli`, I want every script in its `scripts/`
directory to have a live, working purpose, so that I never waste time investigating dead tooling.

**Acceptance criteria**:

```gherkin
Feature: shadow-diff.sh has no dead code path

  Scenario: The script is deleted
    Given no Rust binary has existed for rhino-cli since Phase 9c of rewrite-rhino-cli-to-fsharp
    When a maintainer decides deletion is the simpler outcome
    Then apps/rhino-cli/scripts/shadow-diff.sh no longer exists in either ose-public or ose-private
    And no repo-wide reference to it remains outside plans/done/**

  Scenario: The script is repurposed instead
    Given a maintainer decides a generic two-binary differential runner has future value
    When the script is rewritten
    Then it accepts two arbitrary binary paths and a namespace list as arguments
    And it carries no Rust-specific or F#-specific assumption in its resolution logic
    And running it against two identical binaries reports 0 differences
```

**Product scope**: in — the disposition decision (delete vs. repurpose) and its mechanical
execution in both `ose-public` and `ose-private`. Out — any new differential-testing feature beyond
generic two-binary comparison.

## Technical Approach

Two paths, either acceptable:

1. **Delete** (simpler, recommended default): `git rm apps/rhino-cli/scripts/shadow-diff.sh` in both
   repos, remove its `[N] Phase 2` row from any surviving file-impact reference (none live in
   `docs/` today — confirmed by grep), and confirm `rhino-bin.sh gate list` and `pr-quality-gate.yml`
   do not invoke it (they don't — Phase 11a's R1 already proved this).
2. **Repurpose**: parameterize the script's binary-resolution logic (currently hardcoded to
   `RUST_BIN`/`FSHARP_BIN` env vars and Rust-only tiered resolution) into two positional arguments,
   drop the Rust-specific `cargo build --profile gate` fallback, and keep its namespace-diffing core
   (`md`, `governance`, `git`) as a reusable comparison harness for a future CLI rewrite in this
   repo, if one is ever undertaken.

No existing mechanism already does this — this is genuinely either a deletion or a net-new
generalization, not a duplicate of anything live today.

## Worktree

Worktree path: `worktrees/remove-dead-shadow-diff-script/` — to be provisioned at execution start
per [Worktree Specification](../../../.claude/skills/plan-creating-project-plans/reference/worktree-specification.md).
Not yet provisioned; this is a backlog-stage plan.

## Delivery Mode: worktree-to-pr

Mandatory default in `ose-public` (branch-protected `main`); used identically in `ose-private` for
consistency.

## Parallelization Model

Resolve the single disposition first, then deliver one repository at a time so both repositories
apply the same decision without concurrent drift. The private unit follows the verified public unit.

### Delivery Boundaries

| Boundary                   | Phase and natural cohesive seam                                                                                              | Exact resulting `main` state and flag disposition                                                                                                                                                                                                                                                       |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Public script disposition  | Phase 1's `ose-public` deletion or complete generic repurpose, including references and verification required by that choice | `ose-public/main` contains no dead resolver path and passes its gates, so it is immediately production-deployable. A feature flag is not applicable: this is a complete developer-tool disposition with no incomplete user-reachable behavior; rollback is a PR revert. Integrate promptly after proof. |
| Private script disposition | Phase 2's identical `ose-private` disposition and repository-local verification                                              | `ose-private/main` independently contains the same complete, working disposition and is immediately production-deployable. The same no-flag rationale and PR-revert rollback apply. Integrate promptly rather than batching it with unrelated work.                                                     |

Each boundary keeps the chosen script change or deletion, affected references, tests, verification,
and rollback evidence together. LOC and file counts never create or alter these boundaries.

## Delivery Checklist

Executor legend: `[AI]` = autonomous agent action, `[HUMAN]` = requires human judgment or approval.

### Phase 1: Decide and deliver `ose-public`

- [ ] [HUMAN] Decide delete vs. repurpose (default: delete, given no identified future consumer).
- [ ] [AI] Execute the decision in `ose-public` (delete the file, or repurpose per Technical
      Approach) on a fresh worktree.
- [ ] [AI] `grep -rn 'shadow-diff.sh'` outside `plans/done/**` in `ose-public` returns either nothing
      or only references to the repurposed, working tool.
- [ ] [AI] If repurposed: prove it works by diffing two identical binaries (0 differences reported)
      and two intentionally different binaries (differences reported, non-zero exit).

### Phase 1 Gate

- [ ] [AI] Full `nx affected -t test:quick` clean in `ose-public`.
- [ ] [AI] `rhino-cli:specs:behavior:coverage` unaffected (this script is not itself a spec subject).

> **Pause Safety**: `ose-public/main` contains a complete, verified, production-deployable script
> disposition. Safe to stop before beginning the dependent private mirror.

### Phase 2: Deliver `ose-private`

- [ ] [AI] Apply the verified public decision identically in `ose-private` on its fresh worktree.
- [ ] [AI] `grep -rn 'shadow-diff.sh'` outside `plans/done/**` in `ose-private` returns either nothing
      or only references to the repurposed, working tool.
- [ ] [AI] If repurposed: repeat the identical- and different-binary proof in `ose-private`.

### Phase 2 Gate

- [ ] [AI] Full `nx affected -t test:quick` clean in `ose-private`.
- [ ] [AI] `rhino-cli:specs:behavior:coverage` unaffected (this script is not itself a spec subject).

> **Pause Safety**: both repositories contain the same complete disposition, each independently
> verified and production-deployable. Safe to stop and proceed to plan finalization.

## Quality Gates

Standard repo-wide local gates: `rtk nx affected -t typecheck,lint,test:quick`. No new Nx target is
introduced by this plan.

## Verification

`grep -rln 'shadow-diff.sh' apps/ docs/ .github/ .husky/` in both repos returns nothing (deleted) or
only the repurposed script's own file and its (updated) callers.
