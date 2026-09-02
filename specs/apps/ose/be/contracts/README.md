# OSE Application API Contract

OpenAPI 3.1 specification for the OSE Application (Governance, Risk, and Compliance) platform REST API.

## Purpose

This contract defines the exact shape of every request and response for the OSE Application backend
(`ose-be`) and frontend (`ose-app-web`). It is the **single source of truth** for API
types — code generators produce language-specific types from this spec.

## Quick Start

```bash
# Lint the contract (bundles first, then runs Spectral)
nx run ose-contracts:lint

# Bundle into single resolved YAML + JSON
nx run ose-contracts:bundle

# Generate browsable API documentation
nx run ose-contracts:docs
# Open specs/apps/ose/be/contracts/generated/docs/index.html
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
2. Run `nx run ose-contracts:lint` to validate
3. Run `nx run ose-contracts:bundle` to regenerate the bundled spec
4. Run codegen for affected apps: `nx affected -t codegen`
5. Fix any compile errors in affected apps
6. Commit the contract changes (generated code is gitignored)

## Nx Cache Integration

Generated contract paths are explicit Nx cache inputs for `test:unit` and `test:quick` in both
`ose-be` and `ose-app-web`. This ensures that re-running codegen (which changes the
generated files) triggers a cache miss and re-runs affected test targets.

## Adoption Status

| App         | Codegen target | generated-contracts in inputs |
| ----------- | :------------: | :---------------------------: |
| ose-be      |      yes       |              yes              |
| ose-app-web |      yes       |              yes              |

## Rules

- All JSON field names use **strict camelCase** — zero exceptions
- Every schema must have a `description`
- Changes to this contract trigger codegen for both apps via Nx dependency graph

- [generated](./generated/README.md) — OSE Contracts
- [paths](./paths/README.md) — OSE Contracts
- [schemas](./schemas/README.md) — OSE Contracts
