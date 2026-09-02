# Behaviors — ts-env-loader

Gherkin feature files for [ts-env-loader](../../../../libs/ts-env-loader/README.md), one folder
per capability.

```
specs/libs/ts-env-loader/behaviors/
├── env-loader/
│   └── env-loader.feature
└── port-resolver/
    └── port-resolver.feature
```

## Consumption

`nx run ts-env-loader:test:unit` consumes every scenario here through
`@amiceli/vitest-cucumber`, one step file per feature under `libs/ts-env-loader/src/`.
