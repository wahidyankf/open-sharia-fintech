# 🧹 Repository Clean-Up

## Context

Three retirements CI cannot see, plus the coverage gap the first was hiding.

`apps/ayokoding-cli` and `apps/ose-cli` are two ~330-line Rust binaries that each check internal
Markdown links in one content tree. Neither is executed by anything.

They are not Hugo leftovers: both began as Go tools and were ported to Rust by the two
`2026-05-25__*-cli-rust-migration` plans. Only link-checking survived, and
`rhino-cli md links validate` now does that repository-wide.

Dormancy is measured, not assumed:

|                          | `ayokoding-cli`        | `ose-cli`                                               |
| ------------------------ | ---------------------- | ------------------------------------------------------- |
| Nx target invoking it    | none exists            | `ose-www:links:check`                                   |
| Is that target executed? | —                      | no: absent from `test:quick`, every gate, CI, and hooks |
| Remaining tie            | `implicitDependencies` | `implicitDependencies` + the dead target                |

`repo-governance/development/quality/code/14-ayokoding-www-link-validation.md` tells readers to run
`nx run ayokoding-www:links:check`. No such target exists. The documented workflow cannot be
followed.

A real coverage gap sits underneath. `md-links` excludes `apps/ayokoding-www/content` and
`apps/ose-www/content` — exactly the trees these CLIs were meant to cover. Since the CLIs never run,
those trees are checked by nothing. Deletion does not create that gap; it makes it permanent unless
the exclusions are dropped.

Cost of dropping them, measured on this branch: **exactly one broken link** —
`chart-of-accounts-and-data-modeling/overview.md:10` → `../sql-essentials/overview.md`, which does
not exist. All 47 other files referencing that course use `../sql-essentials/learning/overview.md`.
`apps/ose-www/content` produced zero. Already fixed; see [tech-docs.md](./tech-docs.md).

## Scope

### In scope

- Delete `apps/ayokoding-cli/` and `apps/ose-cli/` with their spec trees and registry entries.
- Delete `libs/rust-commons/` and its spec tree. Those two CLIs are its only consumers, so the
  deletion orphans it.
- Delete `apps/beavernest-app-web/` — one `LICENSE` file left behind when the React frontend was
  replaced by the Flutter `beavernest-app`. Not an Nx project, in no registry.
- Remove the dead `ose-www:links:check` target and both `implicitDependencies`.
- Correct every surface that documents the CLIs or the phantom `links:check` chain.
- Drop the two `md-links` content exclusions and fix the one broken link they reveal, so the content
  trees gain real coverage rather than silently losing their nominal owner.
- Retire the superseded `simplify-ayokoding-ose-cli` two-pager.

### Out of scope

- `crane-cli` and `libs/fsharp-crane-core` — the former holds a live `ProjectReference` to the
  latter, so neither is an orphan.
- `apps/rhino-cli/**`. Its four mentions of deleted paths are all `#[cfg(test)]` tempdir fixtures or
  `//!` comments; editing them opens a four-repo parity obligation for no functional gain.
- The filed `markdownlint` zero-file gate defect, which has its own two-pager.
- Content rewriting beyond the single broken link. The 23 courses with no root `overview.md` break
  no link today; filed as a `plans/ideas/` two-pager.

## Resolved Decisions

- **Deletion over simplification.** The `simplify-ayokoding-ose-cli` idea proposed folding these
  into `rhino-cli`. There is nothing to fold: their only capability already exists there.
- **The CLI Gherkin trees are deleted, not salvaged.** `md links validate` already carries its own
  spec coverage for the same behaviour at repository scope; folding the per-domain scenarios in
  would duplicate it.
- **`14-ayokoding-www-link-validation.md` is deleted, not rewritten.** Nothing survives the phantom
  chain, and `md links validate` is already documented in the gate registry and the SDLC gate
  standard; a thin pointer would be one more surface to keep true. Files `15`–`18` renumber to
  `14`–`17`, since every other split directory in `repo-governance/` is contiguous.
- **One delivery unit, one PR, one worktree.** Retirement, the `md-links` arming, knowledge
  capture, and archival all land in the same PR — `main` is branch-protected, so a post-merge
  archival step would require a second PR.
- **This plan declares `worktree/repo-clean-up`,** so that worktree now resolves to a real plan
  identifier and the exemption previously recorded for the branch is no longer needed.

## Approach Summary

The audit is complete, so the work is mechanical: prove non-invocation with a falsifiable check,
delete, correct the documenting surfaces, then close the coverage gap and prove the gate now bites.

## Plan Documents

- [brd.md](./brd.md) — why this is worth doing and what success means
- [prd.md](./prd.md) — the behaviour a contributor should observe afterwards
- [tech-docs.md](./tech-docs.md) — the exact deletion surface and the coverage change
- [delivery.md](./delivery.md) — the execution checklist
- [learnings.md](./learnings.md) — observations captured during execution

## Definition of Done

No reference to either CLI survives outside `plans/done/**`; `md-links` runs with no content
exclusions and passes; and a deliberately broken content link fails the gate.
