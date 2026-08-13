# BeaverNest Specs

Gherkin behavioral specifications and C4 architecture documentation for
[BeaverNest](../../../README.md) — the walking-skeleton foundation (`beavernest-be`,
`beavernest-app`) proving the engineering harness end-to-end.

## Purpose

These specs define the **observable behavior** of the BeaverNest foundation and the C4
architecture it sits inside. They are the single source of truth for correctness and serve as the
contract between the `beavernest-be`/`beavernest-app` implementations and their consumers.

## Structure

```
specs/apps/beavernest/
├── README.md
├── product/          # PM-first foundation scope framing
├── system-context/    # C4 L1 — actors and external systems
├── containers/        # C4 L2 — deployable units + beavernest-contracts OpenAPI spec
├── components/        # C4 L3 — component-level detail (deferred to Phase 6/8)
└── behavior/           # Cross-cutting Gherkin
    ├── beavernest-be/gherkin/   # health, routing, persistence, development, recovery — 15 feature files
    └── beavernest-app/gherkin/       # workspace, retry, diagnostics, browser, cache — 6 feature files
```

## Running the Tests

```bash
# Validate the spec tree structure (domain subdirs, naming, README index)
npx nx run rhino-cli:specs:structure-validation

# Lint and bundle the OpenAPI contract
npx nx run beavernest-contracts:lint
npx nx run beavernest-contracts:bundle
```

## Adding New Specs

1. Create `specs/apps/beavernest/behavior/<product>-<surface>/gherkin/<domain>/<feature>.feature`
2. Update the relevant index (`behavior/README.md` or the surface's `gherkin/README.md`) with the
   new feature file
3. Verify: `npx nx run rhino-cli:specs:structure-validation`

## Related

- [product/](./product/README.md) — foundation scope
- [system-context/](./system-context/README.md) — C4 L1
- [containers/](./containers/README.md) — C4 L2
- [components/](./components/README.md) — C4 L3
- [behavior/](./behavior/README.md) — Gherkin scenarios
