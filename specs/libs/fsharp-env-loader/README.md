# fsharp-env-loader Specs

The behavioral corpus for [fsharp-env-loader](../../../libs/fsharp-env-loader/README.md), the
shared `.env.<APP_ENV>` tiered env-file loader and runtime port resolver for this repo's F#
backends (`ose-be`, `organiclever-be`).

A library owns exactly one surface, so the two corpus entries sit directly under the library root
rather than under an owner directory — see
[Logical Owner Corpus](../../../repo-governance/conventions/structure/specs-directory-structure/logical-owner-corpus.md).

## Structure

```
specs/libs/fsharp-env-loader/
├── README.md
├── architecture.md     # the current, as-built library
└── behaviors/          # Gherkin feature files, one folder per capability
    ├── env-tier/
    └── port-resolver/
```

## Status

`test:unit` and `test:coverage` are real `dotnet test` targets (see
`libs/fsharp-env-loader/project.json`). Every scenario in
[behaviors/env-tier/env-tier.feature](./behaviors/env-tier/env-tier.feature) and every scenario in
[behaviors/port-resolver/port-resolver.feature](./behaviors/port-resolver/port-resolver.feature) is
driven by
`libs/fsharp-env-loader/tests/unit/Behavior/FsharpEnvLoaderBehaviorDriver.fs` via TickSpec.

- [Architecture — fsharp-env-loader](./architecture.md)
- [Behaviors — fsharp-env-loader](./behaviors/README.md)
