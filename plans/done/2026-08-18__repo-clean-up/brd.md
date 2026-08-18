# 🧭 Business Requirements: Repository Clean-Up

## Business Goal

Stop paying to maintain code that does nothing, and convert a nominal quality control into a real
one.

Two Rust binaries, their spec trees, registry entries, Nx wiring, licensing rows, and documentation
are maintained on every toolchain bump, dependency audit, and lint sweep. They produce no executed
behaviour. Meanwhile the content trees they were meant to protect are checked by nothing.

## Why This Matters

**A rule nobody can follow is worse than no rule.** The governance doc tells contributors to run
`nx run ayokoding-www:links:check`. That target does not exist. A contributor who tries it learns the
governance surface cannot be trusted — the same failure mode the `optimize-gov` pass spent its whole
scope correcting.

**Dormant code is not free.** Each CLI carries a `Cargo.toml`, `deny.toml`, `rust-toolchain.toml`,
`project.json`, spec tree, and `repo-config.yml` registration. Every polyglot toolchain change and
dependency audit touches them. That cost buys nothing.

**The coverage gap is the real finding.** The `md-links` gate excludes both content trees. Everyone
assumes the per-domain CLIs cover them; the CLIs never run. This is the same vacuous-gate shape as the
filed `markdownlint` zero-file defect: the board is green because nothing looked.

## Success Criteria

- No reference to `ayokoding-cli` or `ose-cli` survives outside `plans/done/**`, which is historical
  record.
- The `md-links` gate runs with no content exclusions and passes.
- The gate demonstrably fails when a content link is deliberately broken — proving coverage is real,
  not nominal.
- No documented command in `repo-governance/**` or `docs/**` names a target that does not exist.

## Non-Goals

- Reducing CI time. Neither CLI runs, so removing them saves no wall-clock.
- Auditing `crane-cli`. Deliberately deferred rather than assumed.
- Broad content link remediation beyond the single broken link the change reveals.

## Risks

- **The CLIs are invoked somewhere the audit missed.** Mitigated by a falsifiable pre-deletion check
  that must return zero across the whole tree, not just the places already inspected.
- **Dropping the exclusions surfaces more than measured.** The count was taken on this branch and may
  drift; the delivery re-measures before and after rather than trusting the figure recorded here.
- **Someone runs the binaries locally by habit.** They are not installed products; the replacement is
  a single documented `rhino-cli` command.
