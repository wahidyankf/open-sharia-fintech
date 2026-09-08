# Islamic Tools API Contract

OpenAPI 3.1 specification for the Islamic tools Sharia-compliance REST API.

## Purpose

This contract defines the exact shape of every request and response for `islamic-be`. It is the
**single source of truth** for API types — `oapi-codegen` produces the Go `ServerInterface` from it,
and the router satisfies that interface, so a handler cannot drift from the published specification
without failing to compile.

## Quick Start

```bash
# Lint the contract (bundles first, then runs Spectral)
nx run islamic-contracts:lint

# Bundle into single resolved YAML + JSON
nx run islamic-contracts:bundle

# Generate browsable API documentation
nx run islamic-contracts:docs
# Open specs/apps/islamic/be/contracts/generated/docs/index.html
```

## File Structure

```
contracts/
├── openapi.yaml          # Root spec with $ref mappings
├── .spectral.yaml        # Linting rules (camelCase enforcement)
├── project.json          # Nx project targets
├── paths/                # Endpoint definitions by domain
│   └── health.yaml       # GET /api/v1/health
├── schemas/              # Data type definitions
│   ├── health.yaml       # HealthResponse
│   └── error.yaml        # ErrorResponse
└── generated/            # Output (gitignored)
    ├── openapi-bundled.yaml
    ├── openapi-bundled.json
    └── docs/index.html
```

## Modifying the Contract

1. Edit the relevant file in `schemas/` or `paths/`
2. Run `nx run islamic-contracts:lint` to validate
3. Run `nx run islamic-contracts:bundle` to regenerate the bundled spec
4. Run codegen for the service: `nx run islamic-be:codegen`
5. Fix any compile errors — a diverged handler stops satisfying `ServerInterface`
6. Commit the contract changes (generated code is gitignored)

## Relationship to the ose-be contract

`.spectral.yaml` is byte-identical to `specs/apps/ose/be/contracts/.spectral.yaml` by intent: the
two services publish under one platform and should not disagree about what a well-formed contract
looks like. The specifications themselves share no components — `islamic-be` is a separate product
line and a shared component would couple their release cadences.

## Rules

- All JSON field names use **strict camelCase** — zero exceptions
- Every schema must have a `description`
- Changes to this contract trigger codegen for `islamic-be` via the Nx dependency graph

- [generated](./generated/README.md) — Islamic Contracts
- [paths](./paths/README.md) — Islamic Contracts
- [schemas](./schemas/README.md) — Islamic Contracts
