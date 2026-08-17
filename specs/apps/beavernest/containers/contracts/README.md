# BeaverNest API Contract

OpenAPI 3.1 specification for the BeaverNest REST API.

## Purpose

This contract defines the exact shape of every request and response for `beavernest-be`, consumed
by `beavernest-app`. It is the single source of truth for API types for this phase.

## Quick Start

```bash
# Lint the contract
nx run beavernest-contracts:lint

# Bundle into a single resolved YAML
nx run beavernest-contracts:bundle
```

## File Structure

```
contracts/
├── README.md
├── openapi.yaml     # Full spec: health, readiness, and the shared Error schema
├── project.json     # Nx project targets
├── tests/
│   └── readiness-contract.sh # Assertion-only readiness contract guard
└── generated/        # Output (committed — regenerate via :bundle, drift caught in review)
    └── openapi-bundled.yaml
```

## Rules

- Two declared `GET` routes (`/api/v1/health`, `/api/v1/readiness`) — no write operations this phase
- Readiness exposes only the documented `200` ready and `503` not-ready bodies; both responses
  require `Cache-Control: no-store` and declare no response validator headers
- Every schema has a `description`
- Changes to this contract should stay in lockstep with the Gherkin scenarios in
  [../../behavior/beavernest-be/gherkin/](../../behavior/beavernest-be/gherkin/README.md)

## Related

- [../](../README.md) — containers index (C4 L2)
- [generated — BeaverNest Contracts](./generated/README.md)
- [tests — BeaverNest Contracts](./tests/README.md)
