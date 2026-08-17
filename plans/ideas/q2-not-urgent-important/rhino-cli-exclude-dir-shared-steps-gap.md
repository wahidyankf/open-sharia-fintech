# rhino-cli: thread `--exclude-dir` through the whole-app step scan

One-line summary: make `extract_all_step_texts` (rhino-cli's whole-app step-implementation scan)
respect the CLI's `--exclude-dir` flag, so both sides of a `--shared-steps` comparison exclude the
same directories consistently.

> Surfaced 2026-07-03 while fixing `crud-be-kotlin-ktor` spec-coverage; worked around per-project
> rather than fixed at the rhino-cli level.
> Relocated from a sibling repo's `plans/ideas/` on 2026-08-06 by plan-ideas-grooming.

## Problem / context

In rhino-cli's spec-coverage tooling the two scans disagree on directory exclusion:
`walk_feature_files` (the Gherkin side) honors the user-supplied `exclude_dirs`, but
`extract_all_step_texts` (the shared-steps whole-app step-implementation side) ignores
`--exclude-dir` entirely and filters only via a hardcoded `skip_dirs()` build-artifact list. The
asymmetry produced a real false report: once `crud-be-kotlin-ktor`'s `test-support/test-api.feature`
Gherkin scenario was excluded, its fully-working `test-support` step implementations in
`UnitTestSupportSteps.kt` / `IntegrationTestSupportSteps.kt` were flagged as **20 "orphan step
implementations"** — because `--exclude-dir test-support` only ever applied to the Gherkin-side scan.
(This was the tail of the same investigation that chased a phantom "59 missing step implementations"
gap; the coverage itself was fine — `14 specs, 92 scenarios, 344 steps — all covered`.) The immediate
symptom was patched by dropping `--exclude-dir test-support` from `crud-be-kotlin-ktor`'s
`specs:behavior:coverage` command specifically, but the underlying rhino-cli asymmetry is still open.

## Why now

The per-project workaround only holds because nothing else currently depends on the asymmetry — it is
a latent trap. Any future project that legitimately needs a shared-steps comparison with an excluded
directory will hit the same false-orphan report, and rhino-cli must stay byte-identical across all
three repos, so a real fix propagates once and protects every consumer.

## Prior art / precedents

- **ripgrep** — a recursive scanner that applies one consistent set of ignore/exclusion rules across
  every directory walk; this fix threads exclusions symmetrically the same way.
  [ripgrep](https://github.com/BurntSushi/ripgrep)
- **Cucumber step definitions** — rhino-cli's orphan-step-implementation report is the analogue of
  Cucumber matching Gherkin steps to step definitions; symmetric exclusion keeps both scans in
  agreement. [step-definitions](https://cucumber.io/docs/cucumber/step-definitions/)
- **Regression Test Mandate (repo-internal)** — the promoted plan must land a reproducing fixture test
  (fail-before / pass-after), exactly as the brief anticipates.
  [regression-test-mandate](../../../repo-governance/development/quality/regression-test-mandate.md)

## Proposed direction (sketch)

- Thread the user-supplied `exclude_dirs` through to `extract_all_step_texts`, so the whole-app
  step scan and the Gherkin scan exclude the same directories.
- Keep the hardcoded `skip_dirs()` build-artifact list as an always-on floor, additive to the
  user-supplied exclusions.
- Once fixed, restore `--exclude-dir test-support` to `crud-be-kotlin-ktor`'s coverage command so the
  per-project carve-out can be retired.

## Rough scope & non-goals

In scope: making both sides of a `--shared-steps` comparison honor `exclude_dirs` symmetrically, and
retiring the `crud-be-kotlin-ktor` per-project workaround.

Out of scope (for now): redesigning the coverage tool's directory-walk architecture beyond this
consistency fix; changing the hardcoded build-artifact `skip_dirs()` defaults; any change to the
Gherkin-side scan, which already behaves correctly.

## Risks & open questions

- Does any current project rely on the whole-app scan seeing directories that the Gherkin scan
  excludes? (open — needs an audit before making exclusion symmetric)
- Regression-test shape: the fix is code in `apps/rhino-cli`, so under the code-routing rule it lands
  as a full `backlog/` plan with a reproducing test (a fixture where an excluded dir must not produce
  orphan-step reports) failing before and passing after. (open — belongs in the promoted plan)

## What success looks like + promotion signal

Success: excluding a directory hides its steps from **both** the Gherkin and the step-implementation
scans, so no fully-implemented excluded-directory steps are ever reported as orphans, and
`crud-be-kotlin-ktor` can run its real `--exclude-dir test-support` command with clean coverage. Ready
to promote to a `backlog/` plan now — the fix location and behavior are well understood; promotion just
needs the reproducing-test design and the cross-repo byte-identity propagation folded into the plan.
