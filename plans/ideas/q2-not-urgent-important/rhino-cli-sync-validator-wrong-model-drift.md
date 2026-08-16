# rhino-cli `sync_validator.rs` Wrong-Model Fixture Drift

One-line summary: a single-line test-fixture placeholder string in `sync_validator.rs` differs between
`ose-private` and `ose-public`, breaking the zero-carve-out `apps/rhino-cli` byte-identity rule.

> Demoted from a full `backlog/` plan to a two-pager on 2026-08-05. The full plan carried the standard
> five documents — `README.md`, `brd.md`, `prd.md`, `tech-docs.md`, and a `delivery.md` with a
> single-phase reconcile checklist and its Phase 1 Gate — all of which collapse into the sections below.
> Relocated from ose-private/plans/ideas/rhino-cli-sync-validator-wrong-model-drift.md on 2026-08-06 by plan-ideas-grooming.

## Problem / context

`apps/rhino-cli` is governed by a byte-identity rule with zero carve-outs across the two sync-loop
repos (`ose-public`, `ose-private`): `src/`, `Cargo.toml`, `Cargo.lock`, `project.json`,
`LICENSE`, and the shared Gherkin behavior tree at `specs/apps/rhino/behavior/rhino-cli/gherkin/**`
must all match byte for byte. A confirmed single-line drift currently violates that rule. In
`apps/rhino-cli/src/application/agents/sync_validator.rs`, the test fixture that exercises the
unrecognized-model code path embeds a placeholder model string, and the two repos disagree on its
value — `zai-coding-plan/wrong` in `ose-private` (line 676 as of this writing) versus
`opencode-go/wrong` in `ose-public`. Neither value corresponds to a real, supported model; both are
equally arbitrary fixtures, so the functional risk is nil, but the invariant violation is real and
live. The drift was surfaced by the Phase 6 Gate byte-identity re-check during
`plans/done/2026-07-29__rename-ose-infra-to-ose-private`, which also confirmed that the previously
documented four-file `spec-coverage` drift (`speccoverage/checker.rs`, `speccoverage/parser.rs`,
`tests/spec_coverage.rs`, `spec-coverage-validate.feature`) had resolved itself — this is a new,
unrelated finding that appeared in its place.

## Why now

The same Phase 6 Gate caught a second, more expensive symptom of the same underlying weakness: the
`is_naming_exempt` gap in `apps/rhino-cli/src/application/docs/naming.rs` (missing `CONTRIBUTING.md`
and `LICENSING-NOTICE.md` exemptions) was discovered and fixed **three separate times** — once in
`ose-private`, once in `ose-primer`, once in `ose-public` — because no earlier fix checked the sibling
repos' independent copies before declaring itself done. That incident is direct evidence that
byte-identity here rests on manual `diff` discipline alone. Reconciling this fixture string is cheap
now and gets progressively more expensive to untangle as further drift accretes on top of it, since
every additional divergence makes a full reconciliation pass harder to reason about.

## Prior art / precedents

- **rhino-cli Byte-Identity Boundary** — the authoritative statement of the zero-carve-out rule this
  drift violates, including exactly which paths are in the boundary.
  [sdlc-gate-standard.md](https://github.com/wahidyankf/ose-private/blob/main/docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary)
- **`rename-ose-infra-to-ose-private` plan** — the Phase 6 Gate run that surfaced this drift and the
  adjacent three-times-fixed `naming.rs` incident; its `learnings.md` is the primary evidence.
  [learnings.md](https://github.com/wahidyankf/ose-private/blob/main/plans/done/2026-07-29__rename-ose-infra-to-ose-private/learnings.md)
- **Multi-repo parity planning workflow** — the existing, sanctioned procedure for coordinating a
  change that must land in more than one repo at once.
  [plan-multi-repo-parity-planning.md](https://github.com/wahidyankf/ose-private/blob/main/repo-governance/workflows/plan/plan-multi-repo-parity-planning.md)
- **The `nx affected` rhino-cli-detection gap** — the adjacent rhino-cli-in-`ose-public` finding from
  the same plan; distinct problem, same family. Promoted 2026-08-07 into `rhino-cli-optimization`,
  which was superseded and deleted 2026-08-08 by
  [optimize-cis](../../done/2026-08-09__optimize-cis/README.md) — **this specific concern is not carried
  forward into `optimize-cis`'s scope** (verified against its `brd.md`/`tech-docs.md` 2026-08-08; no
  `nx affected` detection-gap workstream present). It currently has no tracking home and should be
  re-filed as its own idea brief if still relevant at pickup, rather than assumed covered.

## Proposed direction (sketch)

Pick one canonical placeholder value and apply it identically everywhere. The earlier plan leaned
toward `opencode-go/wrong` (the `ose-public` value) on the grounds that `ose-public` is the
publicly-visible repo whose fixture strings external contributors are most likely to read — but this
was explicitly a suggestion, not a requirement, and whoever picks this up may choose the other value if
something found at pickup time argues for it (for example, a sibling test file already anchored on one
of them). Whatever is chosen must not encode any assumption about a real, currently-supported model.
The work itself is: re-verify the drift is still live in `ose-private`; find every reference to the
losing string in each repo; update them
together with the fixtures that depend on them, without deleting or weakening any test to route around
the change; then re-run the byte-identity `diff` and the local rhino-cli gates. Because `apps/rhino-cli`
sits inside the zero-carve-out byte-identity boundary, this change is not a single-repo edit — the
identical bytes must land in `ose-public` and `ose-private`, and the change is not done
until both agree.

## Rough scope & non-goals

In scope: aligning the wrong-model placeholder string in `sync_validator.rs` across the repos that hold
a losing value, and restoring full `apps/rhino-cli` byte-identity.

Out of scope, carried forward verbatim from the source plan:

- Building an automated cross-repo byte-identity CI gate — a larger, separate investment; track it as
  its own idea if pursued.
- The `ose-public`-specific `nx affected` rhino-cli-detection gap — previously slated for
  `rhino-cli-optimization` (superseded and deleted 2026-08-08); not carried by its successor
  [optimize-cis](../../done/2026-08-09__optimize-cis/README.md), so currently untracked pending re-filing.
- `ose-primer`'s copy — that repo is outside the parity set and is free to diverge.
- Any change to the wrong-model _behavior_. Only the fixture string identity moves.

## Risks & open questions

- Which value becomes canonical? (open — `opencode-go/wrong` is the standing recommendation, not a
  decision; re-evaluate at pickup.)
- Is the drift still present in `ose-private`? (open — must be re-verified before any edit, since the
  sibling `spec-coverage` drift already demonstrated that these findings can self-resolve between
  authoring and pickup.)
- Does anything outside `sync_validator.rs` reference the losing string, so that changing it in one
  place alone leaves a broken or inconsistent fixture? (open)
- Coordination risk: a three-repo edit that lands in only two repos recreates exactly the drift class
  this brief exists to close — the `naming.rs` incident is the worked example of that failure mode.
- Low-stakes-change risk: because nothing functional breaks while the drift persists, it can sit
  indefinitely and quietly normalize byte-identity violations as acceptable.

## What success looks like + promotion signal

Success is `apps/rhino-cli` reporting zero differences across the repos checked under a
`diff -rq -x target -x lcov.info -x dist -x cover.out` comparison, with the standard local gates
(`lint`, `typecheck`, `test:quick`) green in every repo touched and no test deleted or weakened along
the way.

Promotion signal: re-run the drift check. If `sync_validator.rs` still diverges, promote this to a
`backlog/` plan immediately — the problem is fully understood and the only open item is which of two
arbitrary strings wins, which a plan can settle in its first step. If the check comes back clean (as
the earlier `spec-coverage` drift did), close this idea instead and fold any remaining concern about
undetected rhino-cli drift into a dedicated automated-byte-identity-gate idea.
