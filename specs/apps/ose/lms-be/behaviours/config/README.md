# config — ose-lms-be Gherkin Domain

Scenarios for the LMS backend config domain. Every scenario here is `@e2e-exempt`: port resolution
completes inside the startup process, before any public HTTP boundary exists to observe it through,
so the Unit adapter is the canonical proof rather than a fallback.

## Feature Files

- **[port-resolution.feature](./port-resolution.feature)** — Listener port resolution order and
  malformed-value rejection (3 scenarios)

## Related

- [Parent gherkin README](../README.md)
