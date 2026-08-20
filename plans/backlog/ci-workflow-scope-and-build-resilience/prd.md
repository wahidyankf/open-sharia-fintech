# Product Requirements — CI Workflow Scope and Build Resilience

## User Stories

### US-1 — A governance-only push starts no application pipeline

**As a** developer landing a governance change
**I want** CI to run only the checks my change can affect
**So that** my PR is not gated on a pipeline that cannot observe my diff.

```gherkin
Feature: Workflow path filters match what a workflow actually builds

  Scenario: A gate-registry edit does not start the BeaverNest application pipeline
    Given a pull request whose only changed file is "repo-config.yml"
    When GitHub evaluates the workflow path filters
    Then the BeaverNest application workflow is not triggered

  Scenario: An application change still starts it
    Given a pull request that changes a file under "apps/beavernest-be"
    When GitHub evaluates the workflow path filters
    Then the BeaverNest application workflow is triggered
```

### US-2 — A slow network is a named failure, not a burnt job

**As a** developer reading a red check
**I want** a stalled download to fail fast with its own message
**So that** I can tell an upstream condition from a defect in my change.

```gherkin
Feature: Network fetches in CI retry and are bounded

  Scenario: A transient fetch failure is retried
    Given a network fetch inside a CI build step
    When the first attempt fails with a timeout
    Then the step retries with backoff before failing the job

  Scenario: A persistent stall fails the step, not the job budget
    Given a network fetch that never completes
    When the step's own timeout elapses
    Then the step fails naming the fetch
    And the failure occurs before the job's timeout is reached
```

### US-3 — A multi-case assertion names the case that failed

**As a** developer diagnosing a CI-only failure
**I want** the assertion to report which input failed and what it computed
**So that** an environment-dependent case is diagnosable from the log alone.

```gherkin
Feature: Configuration rejection is asserted case by case

  Scenario Outline: Each invalid directory value is rejected on its own
    Given a database configuration whose directory is <case>
    When the configuration is validated
    Then it is refused
    And a failure message names <case> and the value computed for it

    Examples:
      | case              |
      | empty             |
      | filesystem root   |
      | home directory    |
      | repository root   |
      | nonpositive timeout |
```

## Acceptance Criteria

| ID   | Criterion                                            | Pre-change                             | Post-change                             |
| ---- | ---------------------------------------------------- | -------------------------------------- | --------------------------------------- |
| AC-1 | Workflows started by a `repo-config.yml`-only push   | includes the BeaverNest app pipeline   | excludes it                             |
| AC-2 | Workflows started by an `apps/beavernest-be/**` push | includes it                            | still includes it                       |
| AC-3 | A forced fetch failure in `setup-playwright`         | job cancelled at 35 minutes, no reason | step fails within its own budget, named |
| AC-4 | A forced fetch failure in the contract-build image   | opaque Docker layer error              | retried, then a named step failure      |
| AC-5 | A deliberately failing configuration case            | `Expected: True, Actual: False`        | message names the case and its value    |

AC-1 and AC-2 are a matched pair: a filter change that satisfies AC-1 by disabling the workflow
fails AC-2. Both must be demonstrated on real pushes, not reasoned about from the YAML.

## Out of Scope

The Nx global-input treatment of `repo-config.yml`. Merge-queue adoption. Replacing the
openapi-generator toolchain.
