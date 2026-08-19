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

**Known gap: the F# markers are not mechanically enforced.** `libs/fsharp-env-loader` has no
`specs:behavior:coverage` target, so nothing fails if a scenario here is renamed and the F# side goes
stale — the pairing above was verified by hand. Simply adding the target does not work:
`behavior-coverage validate` matches Gherkin _step text_ against step definitions, and these xUnit
tests carry only scenario-level `@covers` markers, so it reports every step as a gap. Closing this
properly means giving the library a step-definition harness in the shape of
`libs/fsharp-crane-core/tests/unit/Tests/PdfToMarkdownRoutingSteps.fs` (`[<Given>]`-attributed
steps), which is its own piece of work rather than a spec-file edit.
