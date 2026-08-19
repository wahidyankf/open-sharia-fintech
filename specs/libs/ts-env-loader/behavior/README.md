# Behavior — ts-env-loader

Gherkin behavioral specifications for
[ts-env-loader](../../../../libs/ts-env-loader/README.md), the shared `APP_ENV` tier env-file
loader and the repo-wide runtime port contract it exposes.

## Structure

```
specs/libs/ts-env-loader/behavior/
└── gherkin/
    ├── env-loader/
    │   └── env-loader.feature
    └── port-resolver/
        └── port-resolver.feature
```

## Status

`test:unit` runs the real `vitest` suites (`libs/ts-env-loader/src/env-loader.unit.test.ts` and
`libs/ts-env-loader/src/port-resolver.unit.test.ts`) against these scenarios via
`@amiceli/vitest-cucumber` — see the top-level [README.md](../README.md).

The port-resolver scenarios are mirrored one-for-one by
`libs/fsharp-env-loader/tests/unit/Tests/PortResolverTests.fs`, so the TypeScript and F# services
provably share one port contract rather than two lookalikes.
