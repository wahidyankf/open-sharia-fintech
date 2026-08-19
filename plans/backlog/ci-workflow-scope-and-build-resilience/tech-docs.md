# Technical Documentation — CI Workflow Scope and Build Resilience

## WS-C1 — the path filter

### Current state

`.github/workflows/beavernest-app-test-local-deploy-stag.yml` declares:

```yaml
paths:
  - "apps/beavernest-app/**"
  - "apps/beavernest-app-e2e/**"
  - "apps/beavernest-be/**"
  - "infra/dev/beavernest-app/**"
  - "specs/apps/beavernest/**"
  - ".fvmrc"
  - "repo-config.yml"
```

The first five entries name trees the workflow builds. `.fvmrc` pins the Flutter version the app
compiles with — a genuine input. `repo-config.yml` is neither: it is the gate and harness registry,
and nothing the workflow runs reads it.

### Fix design

Remove `repo-config.yml` from the filter, and check every sibling workflow for the same entry — the
fix is the class, not the one file this plan happened to notice.

If some job in that workflow genuinely does read `repo-config.yml`, the correct fix is the inverse:
name that dependency explicitly in the job and keep the trigger. Establish which is true by reading
the workflow's steps before editing the filter — a filter narrowed on an assumption is a silent
coverage loss.

### Verification

Path-filter behaviour cannot be verified by reading YAML. Push a `repo-config.yml`-only commit to a
scratch branch and record which workflows start; push an `apps/beavernest-be/**` commit and record
the same. Both observations are the acceptance evidence.

## WS-C2 — unretried network fetches

### Site 1: `setup-playwright`

`.github/actions/setup-playwright/action.yml`'s cache-hit branch runs
`npx playwright install-deps`, which shells out to `apt-get update`. Observed: two consecutive runs
(`32231836567`, job `96013835006`) cancelled at their 35-minute `timeout-minutes` while still inside
this step, with repeated `Ign:` lines and 32 minutes of silence. The step was identifiable only from
the teardown line `Terminate orphan process: pid (4377) (npm exec playwright install-deps)`.

### Site 2: the contract-build image

`infra/dev/beavernest-app`'s Dockerfile line 18 runs `npx @redocly/cli bundle` followed by
`npx openapi-generator-cli generate`. The generator CLI downloads its JAR at build time. Observed
2026-08-19 on run `32270339593`: `Download failed, because of: ""` and
`AggregateError [ETIMEDOUT]` with four underlying errors, failing the layer and the job.

### Fix design

Three properties, applied at both sites:

1. **Retry with backoff.** Three attempts is the usual shape; the exact count matters less than that
   a single transient failure is not terminal.
2. **A step-level timeout smaller than the job's.** A stall must exhaust the step, not the job, or
   the failure surfaces as a bare cancellation with no named cause.
3. **A message naming the fetch.** The current failures name a `RUN` line and a process id.

For site 2, ask additionally whether the JAR belongs in the image at build time at all — a pinned,
cached artifact removes the fetch rather than making it survivable. That is the stronger fix and the
one to prefer if the version can be pinned.

## WS-C3 — the unnameable assertion

### Current shape

`DatabaseConfigurationTests.fs:30` iterates seven invalid inputs and asserts the whole list with a
single `Assert.True`. Three inputs are computed from the environment and compared against values
`isDisallowedDirectory` recomputes the same way, so a divergence between the two computations — a
different temp root, a different current directory under a coverage runner — fails the assertion
with no indication of which element diverged.

### Evidence the case is environment-dependent

`beavernest-be:test:unit` passed 104/104 and `beavernest-be:test:coverage` then failed 1/104 in the
same CI job, on the same binary, seconds apart. The same target passes locally with
`--skip-nx-cache`. Same code, two results: the difference is the environment the runner presents.

### Fix design

Convert the list assertion into a per-case theory so each input is its own test with its own name,
and make the message carry both the input and the value the implementation computed for it. The
diagnosis this plan could not complete then completes itself the next time it fails.
