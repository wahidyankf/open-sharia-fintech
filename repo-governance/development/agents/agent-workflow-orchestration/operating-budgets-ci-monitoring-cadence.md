---
description: "Defines the cadence for monitoring CI and GitHub Actions while an orchestrated task runs."
when_to_use: Use when deciding how often to poll CI status during an orchestrated multi-step task.
---

# Operating Budgets — CI and GitHub Actions Monitoring Cadence

When monitoring or polling CI or GitHub Actions — run status, job logs, or workflow conclusions — never poll faster than once every two (2) minutes. This is a hard floor that protects the provider's rate limiter, which takes longer to recover from than simply waiting. The operational default is more conservative still: see the [CI Monitoring Convention](../../workflow/ci-monitoring.md) for the required mechanics — scheduled wakeups, a single status check per wakeup, no stream-watching, and rate-limit recovery.
