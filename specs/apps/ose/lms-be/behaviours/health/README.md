# health — ose-lms-be Gherkin Domain

Scenarios for the LMS backend health domain, covering both the service's own probe and the
Actuator surface exposed alongside it.

## Feature Files

- **[health.feature](./health.feature)** — Service liveness probe (1 scenario)
- **[actuator.feature](./actuator.feature)** — Actuator exposes health and nothing else (2 scenarios)

## Related

- [Parent gherkin README](../README.md)
