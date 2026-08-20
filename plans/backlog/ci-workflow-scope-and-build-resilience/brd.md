# Business Requirements — CI Workflow Scope and Build Resilience

## The problem in one line

A pull request that changes no application code can be blocked by a full application pipeline
failing for a reason no one can read off the log.

## What actually happened

| Date       | Symptom                                                                 | Actual cause                                        |
| ---------- | ----------------------------------------------------------------------- | --------------------------------------------------- |
| 2026-08-19 | `Infra shell-test harness` fails on a governance-only PR                | `openapi-generator-cli` JAR download `ETIMEDOUT`    |
| Earlier    | Two consecutive E2E jobs cancelled at their 35-minute `timeout-minutes` | `apt-get update` stalled against an Ubuntu mirror   |
| Earlier    | `.NET quality gate` fails 1/104 after passing 104/104 in the same job   | Environment-dependent case, unidentifiable from log |

In all three the PR's diff contained no file the failing job builds. In all three the workflow ran
only because `repo-config.yml` appears in its `paths:` filter.

## Cost of doing nothing

**Every governance PR pays for a full application pipeline.** Container build, backend integration
suite, and browser E2E, on every push, for a change that cannot affect any of them. The cost is
runner minutes and, more expensively, wall-clock: a plan executing across a dozen pushes waits on
jobs whose result is a foregone conclusion.

**Transient upstream conditions become blocking.** A mirror stall or a slow artifact host reddens a
check. With no retry and no per-step budget, the failure mode is either a 35-minute burn or a
one-line timeout deep in a Docker layer. Neither says "the network was slow", so each occurrence
costs a fresh investigation.

**An unnameable assertion failure invites the wrong response.** When a 7-case assertion says only
`Expected: True, Actual: False`, the cheapest available action is to re-run it. That is how a real
environment-dependent defect gets reclassified as a flake and stops being investigated.

## Success criteria

1. A push that changes only governance surfaces starts no BeaverNest application workflow —
   demonstrated by naming the workflows a governance-only push actually starts, before and after.
2. Each of the two network fetches retries with backoff and carries a step-level budget smaller than
   the job's, so a stall surfaces as a named failure rather than a job-level cancellation.
3. `DatabaseConfigurationTests` names the failing input and its computed value in the assertion
   message, and a regression test pins that message.

## Non-goals

Removing `repo-config.yml` from Nx's global inputs — correct there for a different reason. Vendoring
the openapi-generator JAR, which is a candidate outcome of WS-C2, not a premise. Adding a merge
queue.
