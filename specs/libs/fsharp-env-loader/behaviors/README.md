# Behaviors — fsharp-env-loader

Gherkin feature files for [fsharp-env-loader](../../../../libs/fsharp-env-loader/README.md), one
folder per capability.

```
specs/libs/fsharp-env-loader/behaviors/
├── env-tier/
│   └── env-tier.feature
└── port-resolver/
    └── port-resolver.feature
```

## Consumption

`nx run fsharp-env-loader:specs:behavior:coverage` consumes every scenario here through TickSpec,
bound by
`libs/fsharp-env-loader/tests/unit/Behavior/FsharpEnvLoaderBehaviorDriver.fs`.
