# Business Requirements — rhino-cli Source-Drift Reconciliation

## Problem

`apps/rhino-cli` must be byte-identical across `ose-public`, `ose-primer`, and `ose-infra` (zero
carve-outs on `src/`, `Cargo.toml`, `Cargo.lock`, `project.json`, `LICENSE`, and the gherkin behavior
tree) per the codified
[rhino-cli Byte-Identity Boundary](../../../docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary)
`[Repo-grounded]`.
A tri-repo `diff` on 2026-07-17 proved the invariant is **currently broken**: four in-boundary
`src/` files have drifted (`docs/naming.rs`, `doctor/checker.rs`, `doctor/tools.rs`,
`repo_governance/instruction_size.rs`), plus `tests/doctor.rs` (adjacent, outside the strict list)
`[Repo-grounded: diff -rq apps/rhino-cli/src, 2026-07-17]`.
Example: `ose-public`'s `doctor/tools.rs` carries tool parsers (`parse_clang_format_version`,
OpenTofu version extraction) that `ose-primer` lacks — a union-surface gap, not a value difference
`[Repo-grounded]`.

## Business Impact

- **The identity guarantee is silently false today.** Any reader, agent, or gate that assumes
  "rhino-cli is identical across repos" is operating on a broken premise; a fix or feature landed in
  one repo's rhino-cli may not exist in another `[Judgment call]`.
- **It blocks clean rhino-cli feature work.** The upcoming `specs e2e-coverage` subcommand (the
  [e2e-scenario-coverage-gap-detector](../e2e-scenario-coverage-gap-detector/README.md)
  plan) must be added byte-identically to all three repos. Introducing it on top of already-drifted
  source risks compounding the divergence or masking it `[Repo-grounded: sibling plan explicitly
names this plan as its predecessor]`.
- **Drift grows silently.** There is no standing tri-repo `diff` gate catching per-file src drift
  today (only the `repo-config.yml` schema-parity gate), so drift accumulates until a manual audit
  (like this one) surfaces it `[Repo-grounded]`.

## Goals

- Reconcile the four drifted in-boundary `src/` files (and verify `tests/doctor.rs`) to a **single
  canonical union form** byte-identical across all three repos, with repo-inapplicable behavior
  **dormant, not absent** (driven by each repo's `repo-config.yml`).
- Re-establish and **verify** full rhino-cli byte-identity across all three repos (`src/` + manifest
  files + gherkin tree) via an explicit tri-repo `diff` that returns zero differences.
- Land the change with rhino-cli's own test suite green in every repo (no behavioral regression;
  dormant verbs stay dormant where inapplicable).

## Non-Goals

- Not adding new rhino-cli commands or behavior — this is a **reconciliation**, not a feature.
- Not building a standing automated tri-repo src-diff gate (candidate follow-up; this plan restores
  identity and can recommend the gate in Knowledge Capture, but does not implement it).
- Not touching `speccoverage/checker.rs` (already identical; owned by the multiline-scan plan).
- Not reconciling any files outside the rhino-cli byte-identity boundary.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears these hats, and these agents
consume the artifacts:

- **Toolchain-maintainer hat**: owns `apps/rhino-cli` and its byte-identity obligation across all
  three sibling repos `[Repo-grounded: docs/reference/sdlc-gate-standard.md]`.
- **Downstream plan author hat**: the e2e-coverage-detector and multiline-scan plans assume (or
  benefit from) an identical rhino-cli base `[Repo-grounded]`.
- **Reviewer / `pr-review-maker` / `pr-review-fixer`**: consume each repo's draft PR through the
  PR-Review Maker→Fixer Cycle before merge `[Repo-grounded: .claude/agents/pr-review-maker.md,
.claude/agents/pr-review-fixer.md]`.

## Business-Level Success Metrics

- **Observable**: the tri-repo boundary `diff` (`src/` + manifest files + gherkin tree) over all
  three repo pairs returns **zero** differences after reconciliation, where it currently reports
  five differing files `[Repo-grounded: tech-docs.md § Tri-repo verification command]`.
- **Observable**: rhino-cli's unit, integration, and `tests/` binary suites pass in each of the
  three repos after reconciliation, with no dormant verb becoming active in a repo where it is
  inapplicable `[Repo-grounded: prd.md acceptance scenario "No behavioral regression"]`.
- **Judgment call**: the reconciliation is durable — a follow-up automated tri-repo `diff` gate
  (proposed, not implemented, in this plan's Knowledge Capture) would find zero new drift against
  this plan's own changes if adopted immediately after landing `[Judgment call]`.

## Business Risks and Mitigations

| Risk                                                                                                                  | Likelihood | Mitigation                                                                                                                                                                                                                        |
| --------------------------------------------------------------------------------------------------------------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A "union" reconstruction accidentally drops behavior one repo actually applies                                        | Medium     | Phase 1 reads all three variants side-by-side before drafting the canonical form; Phase 2's RED step asserts the union surface is reachable before any GREEN write `[Repo-grounded: delivery.md Phase 1-2]`.                      |
| A partial tri-repo application (reconciled in one repo, not the others) re-introduces drift                           | Medium     | Phase 3's tri-repo `diff` gate blocks Phase 4 until all pairs report zero differences; `tech-docs.md`'s Rollback section requires all-three-or-none reverts to preserve the invariant `[Repo-grounded: tech-docs.md § Rollback]`. |
| A previously-dormant tool parser or check activates a false positive in a repo that never exercised it                | Low        | Phase 2's REFACTOR step runs the full local suite in every repo (not only the repo where drift originated) before Phase 3 verification `[Repo-grounded: delivery.md Phase 2]`.                                                    |
| Manual per-file classification (union-surface gap vs. hardcoded value) is judged inconsistently across the five files | Low        | Phase 1 requires a written per-file decision recorded in `learnings.md`, reviewable before Phase 2 begins `[Repo-grounded: delivery.md Phase 1]`.                                                                                 |

## Related

- [prd.md](./prd.md) — the testable acceptance scenarios that operationalize these goals.
- [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)
- [rhino-cli Byte-Identity Boundary](../../../docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary)
