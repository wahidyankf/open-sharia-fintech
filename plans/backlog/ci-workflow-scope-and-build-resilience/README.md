# 🧯 CI Workflow Scope and Build Resilience

## Context

Three CI findings surfaced while executing the `update-harness-support` plan (archived under
[`plans/done/`](../../done/README.md)). That plan changed governance surfaces and `apps/rhino-cli`;
it touched no application code and no workflow file. It nevertheless spent CI budget on a full
BeaverNest backend-plus-frontend run on **every** push, and was blocked twice by failures with no
connection to its diff.

None was fixed inline — all three are `.github/` or `apps/beavernest-be/` changes, which the
[Code-Routing Downstream Rule](../../../repo-governance/development/quality/knowledge-capture/the-code-routing-downstream-rule.md)
routes to a separate plan.

The shared shape: **CI reports a failure whose cause is outside the diff, and offers no way to tell
that from the log.** One workstream narrows what runs; one makes network fetches survivable; one
makes an assertion say which case failed.

## Workstreams

| ID    | Workstream                                                            | Status    |
| ----- | --------------------------------------------------------------------- | --------- |
| WS-C1 | `repo-config.yml` drags a full app pipeline on governance-only edits  | Specified |
| WS-C2 | CI builds fetch from the network with no retry and no per-step budget | Specified |
| WS-C3 | A 7-case assertion fails without naming which case                    | Specified |

### WS-C1 — one shared file, one whole pipeline

`.github/workflows/beavernest-app-test-local-deploy-stag.yml` triggers on
`pull_request.paths` including `repo-config.yml`. That file is the repository's gate and harness
registry: nearly every governance plan edits it. It is also the **only** entry in that filter a
governance PR ever matches, so the match is always a false positive — a full container build, backend
integration suite, and browser E2E run, none of which can be affected by a gate-registry edit.

The same coupling exists at the Nx layer, where `repo-config.yml` and `AGENTS.md` are global inputs,
so `nx affected` pulls in every project. That is defensible for a correctness-first task graph. A
GitHub `paths:` filter is not the same instrument and does not need the same conservatism.

### WS-C2 — two network fetches with no retry, both observed failing

Both were observed on one branch, weeks apart in symptom and identical in shape:

1. `./.github/actions/setup-playwright`'s cache-hit branch shells out to `apt-get update` against
   `azure.archive.ubuntu.com`. A mirror stall consumed the whole 35-minute job budget across two
   consecutive runs; the visible symptom was a bare cancellation. The step was identifiable only from
   the teardown line `Terminate orphan process: pid (4377) (npm exec playwright install-deps)`.
2. `infra/dev/beavernest-app`'s contract-build image runs `npx openapi-generator-cli generate`, which
   downloads its generator JAR **during `docker build`**. On 2026-08-19 that download failed with
   `AggregateError [ETIMEDOUT]` and `Download failed, because of: ""`, failing the job.

Neither fetch retries. Neither has a budget smaller than the job's. Both turn a transient upstream
condition into a red check on an unrelated PR.

### WS-C3 — the assertion that will not say what failed

`apps/beavernest-be/tests/unit/Tests/DatabaseConfigurationTests.fs:30` asserts that configuration
refuses seven invalid inputs, three of which are computed from the environment
(`Path.GetPathRoot(Path.GetTempPath())`, the user profile folder, the current directory) and compared
against values the implementation recomputes the same way. When it failed in CI, the log said
`Assert.True() Failure, Expected: True, Actual: False` and nothing more.

`test:unit` passed 104/104 seconds earlier in the same job on the same binary; `test:coverage` then
failed 1/104. That is the signature of an environment-dependent case — and the assertion is written
so that it cannot say which one.

## Scope

**Repository**: `ose-public`. None of the three files is inside the `rhino-cli` parity boundary, so
there is no paired-merge obligation.

**Trees in scope**: `.github/workflows/`, `.github/actions/setup-playwright/`,
`infra/dev/beavernest-app/`, and `apps/beavernest-be/tests/unit/`.

**Out of scope**: the Nx global-input treatment of `repo-config.yml`, which is correct for a task
graph; adding a merge queue; the container runtime itself.

## Approach Summary

WS-C1 is a workflow-filter change verified by observing which workflows a governance-only push
starts. WS-C2 is a build-and-action change whose acceptance is a deliberately failed fetch. WS-C3 is
an ordinary TDD change in F# with companion Gherkin.

WS-C3 is independent. WS-C1 should land first: it reduces how often WS-C2's fragility is exercised
by PRs that had no business running those jobs.

## Documents

- [brd.md](./brd.md) — the cost of a red check with no cause in the diff.
- [prd.md](./prd.md) — user stories and Gherkin acceptance criteria.
- [tech-docs.md](./tech-docs.md) — evidence and fix design per workstream.
- [delivery.md](./delivery.md) — the phase-by-phase execution checklist.
