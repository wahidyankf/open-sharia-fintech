# Behavior — ts-env-loader

Gherkin behavioral specifications for
[ts-env-loader](../../../../libs/ts-env-loader/README.md), the shared `APP_ENV` tier env-file
loader.

## Structure

```
specs/libs/ts-env-loader/behavior/
└── gherkin/
    └── env-loader/
        └── env-loader.feature
```

## Status

`test:unit` runs the real `vitest` suite (`libs/ts-env-loader/src/env-loader.unit.test.ts`) against
these scenarios via `@amiceli/vitest-cucumber` — see the top-level [README.md](../README.md).
