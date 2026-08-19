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
provably accept and reject the same port values. That F# suite carries `@covers` markers pointing at
the feature file in **this** directory on purpose: the port contract is one contract, so it gets one
feature file, and duplicating it under `specs/libs/fsharp-env-loader/` would create exactly the
second source of truth the pairing exists to prevent. The F# suite adds a few argv-spelling cases
(`--port=N`, a trailing bare `--port`) that have no Gherkin counterpart because they concern F#'s
own `argv` array rather than the shared resolution rule.
