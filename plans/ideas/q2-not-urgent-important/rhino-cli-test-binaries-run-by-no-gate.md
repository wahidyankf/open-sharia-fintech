# 20 of rhino-cli's 27 integration test binaries are executed by no gate

One-line summary: `apps/rhino-cli/project.json`'s `test:unit` target names a seven-binary
allowlist, and the `test:integration` target that would pick up the rest is referenced by no
workflow for this project, so 20 test binaries under `apps/rhino-cli/tests/` never run on any
surface.

> Surfaced 2026-08-18 during PR #227's cycle-2 review as finding C2-F2, enumerated
> programmatically, verified pre-existing, and recorded rather than fixed in that PR.

## Problem / context

`test:unit` runs `cargo test --lib` plus exactly seven named binaries — `repo_governance`,
`env_contract`, `repo_config_data_driven`, `fsharp_tool_invocation`, `gate_specs`,
`gate_dispatch`, `docs`. `test:quick` (the pre-push gate) composes `test:unit`, so it inherits that
allowlist; `test:coverage` is `--lib` only. `test:integration` (`cargo test --tests`) would sweep
every binary, but the only two `test:integration` call sites in `.github/workflows/` are
`_reusable-app-test-local-deploy-stag.yml` and `_reusable-www-test-local-deploy.yml`, both
parameterized on a web/app project name, and no caller ever passes `rhino-cli`.

The 20 unexecuted binaries: `agents.rs`, `cargo_target_share.rs`, `cli_smoke.rs`, `contracts.rs`,
`convention.rs`, `cursor_binding.rs`, `ddd.rs`, `doctor.rs`, `env.rs`, `env_validate_integration.rs`,
`gate_format_verify_wrappers.rs`, `git_hooks.rs`, `golden_master.rs`, `governance.rs`,
`mermaid_golden_corpus.rs`, `repo_config_validate.rs`, `spec_coverage.rs`, `specs_tree.rs`,
`stdio_blocking_wiring.rs`, `test_coverage.rs`.

The orphaning predates PR #227: that PR's only `project.json` delta is deleting the two withdrawn
`naming:*` Nx targets, and the `test:unit` allowlist and `test:integration` target are untouched
across its whole range.

## Why now

Not urgent — the underlying logic of most of these binaries does get real coverage from the `--lib`
unit tests, so the gap is mostly in the cucumber/BDD layer rather than in the logic itself. It stays
open because a regression guard that runs nowhere reads as coverage while providing none: a future
PR can delete the guarded behaviour and see a fully green pre-push.

A trap worth recording for whoever picks this up: the `rewrite-paths` Gherkin steps live in
`tests/governance.rs`, which is **not** the allowlisted `tests/repo_governance.rs`. Two
near-identical names, one gated and one not.

## Prior art / precedents

- **`specs-checker-phantom-nx-targets`** — [specs-checker-phantom-nx-targets](./specs-checker-phantom-nx-targets.md)
  is the same failure shape one layer up: a declared target that does not do what its name implies.
- **`behavior-coverage-json-report-wiring`** — [behavior-coverage-json-report-wiring](./behavior-coverage-json-report-wiring.md)
  covers the adjacent question of what the coverage reporting actually measures.
- **SDLC Gate Standard** — [sdlc-gate-standard.md](../../../docs/reference/sdlc-gate-standard.md)
  is where any decision about which tier these binaries belong on has to land.

## Proposed direction (sketch)

Decide per binary which surface it belongs on rather than wiring all 20 wholesale: cheap
deterministic ones join the `test:unit` allowlist (with matching `inputs` entries); expensive ones
(`stdio_blocking_wiring.rs` alone carries ~6000 fixture files and a deliberate 300 ms sleep) belong
on a heavier CI-only tier that some workflow actually invokes for `rhino-cli`. Any binary that
stays ungated gets its module doc annotated as manual-only, with the command to run it.

Since `apps/rhino-cli` is byte-identical across `ose-public` and `ose-private`, the same wiring must
land on both sides or the parity manifest diverges.

## Rough scope & non-goals

In scope: `apps/rhino-cli/project.json` target definitions, any workflow that needs to start calling
a heavier rhino-cli test tier, and module-doc annotations on whatever stays ungated.

Out of scope: rewriting the tests themselves, and the separate Git Fixture Isolation defects some of
these binaries carry — those are their own findings and must be fixed before an unisolated fixture
is wired into a parallel pre-push fanout.

## Risks & open questions

- Wiring 20 binaries in wholesale risks turning a green pre-push red for reasons unrelated to any
  one change — the per-binary triage is the work, not the config edit.
- Open: whether `rhino-cli` should gain a heavy CI-only test job at all, or whether the answer is a
  smaller allowlist plus explicit manual-only annotations.

## What success looks like + promotion signal

Success: every binary under `apps/rhino-cli/tests/` is either executed by a named surface or
annotated in its own module doc as manual-only with the command to run it, with no third state.
Ready to promote once the per-binary surface assignment is drafted — that triage is the gate, not
the `project.json` edit.
