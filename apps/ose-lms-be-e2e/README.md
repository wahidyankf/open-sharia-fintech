# ose-lms-be-e2e

End-to-end tests for [`ose-lms-be`](../ose-lms-be/README.md), the OSE LMS backend. They drive the
service the way a real client does: start the built jar as its own process, send real HTTP, and
assert on what comes back.

## What it proves

Four scenarios from the owner corpus at `specs/apps/ose/lms-be/behaviours/`:

| Scenario                                           | Feature                   |
| -------------------------------------------------- | ------------------------- |
| Health endpoint returns a healthy status           | `health/health.feature`   |
| Hello endpoint returns the greeting                | `hello/hello.feature`     |
| Actuator health endpoint reports the service is up | `health/actuator.feature` |
| Actuator exposes no endpoint other than health     | `health/actuator.feature` |

The three port-resolution scenarios in `config/port-resolution.feature` are tagged `@e2e-exempt`
and deliberately excluded here. They assert how the port is chosen _before_ the process binds one,
which a black-box HTTP client cannot observe. They are proven in the Unit adapter instead, which
carries no exemption at all — so every scenario in the corpus is proven somewhere.

## Running

```bash
# the full suite; builds the jar first through the Nx dependency
npm exec nx -- run ose-lms-be-e2e:test:e2e

# static checks only, no service started
npm exec nx -- run ose-lms-be-e2e:test:quick
```

## How the service is started

`steps/backend-process.ts` spawns the Gradle-built jar from `../ose-lms-be/build/libs/` and waits
for `/api/v1/health` to answer before any scenario runs, then stops it on teardown. The jar is
built by the `ose-lms-be:build` target, which `test:e2e` declares in `dependsOn`, so the suite
never runs against a stale artifact.

Tests bind port **8403**, not the service's default 8303. The `ose-be-e2e` sibling reuses its
service's normal port, but doing that here would make the suite fight two things this plan needs
running on 8303: a developer's `nx run ose-lms-be:dev` session, and the exploratory-testing step
in the same delivery unit. Set `LMS_API_BASE_URL` to point the suite elsewhere.

## Retries

`retries` is `0` on CI as well as locally, which differs from the `ose-be-e2e` sibling's `2`. The
repository's flaky-test rule requires fixing a flaky test at its root cause and forbids retrying
around it; a retry count above zero is that forbidden move expressed as configuration, and it
would let a genuinely intermittent failure reach `main` as a green check.
