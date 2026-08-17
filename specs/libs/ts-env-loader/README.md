# ts-env-loader Specs

Gherkin behavioral specifications for
[ts-env-loader](../../../libs/ts-env-loader/README.md), the shared `.env.<APP_ENV>` tiered
env-file loader.

## Purpose

These specs define the **observable behavior** of the loader: how it resolves the current
`APP_ENV` tier, which single tier file it applies, why an already-set process-environment
variable always wins over a file value, why a missing tier file is not an error, and why a stray
auto-loaded env file beside a non-local tier file must fail loudly.

## Structure

```
specs/libs/ts-env-loader/
├── README.md
├── product/               # C4 L1 product framing
├── system-context/        # C4 L1 actors and consumers
├── containers/            # C4 L2 deployable units
├── components/            # C4 L3 component catalogue
└── behavior/
    └── gherkin/           # Gherkin feature files
        └── env-loader/
```

## Status

`test:unit` and `test:coverage` are real, already-wired `vitest` targets (see
`libs/ts-env-loader/project.json`) — every scenario in
[behavior/gherkin/env-loader/env-loader.feature](./behavior/gherkin/env-loader/env-loader.feature)
is exercised by `libs/ts-env-loader/src/env-loader.unit.test.ts` via `@amiceli/vitest-cucumber`.

- [Behavior — ts-env-loader](./behavior/README.md)
- [Components — ts-env-loader](./components/README.md)
- [Containers — ts-env-loader](./containers/README.md)
- [Product — ts-env-loader](./product/README.md)
- [System Context — ts-env-loader](./system-context/README.md)
