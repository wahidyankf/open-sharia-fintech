# ts-env-loader Specs

The behavioral corpus for [ts-env-loader](../../../libs/ts-env-loader/README.md), the shared
`.env.<APP_ENV>` tiered env-file loader.

A library owns exactly one surface, so the three corpus entries sit directly under the library
root rather than under an owner directory — see
[Logical Owner Corpus](../../../repo-governance/conventions/structure/specs-directory-structure/logical-owner-corpus.md).

## Structure

```
specs/libs/ts-env-loader/
├── README.md
├── architecture.md     # the current, as-built library
└── behaviors/          # Gherkin feature files, one folder per capability
    ├── env-loader/
    └── port-resolver/
```

## Status

`test:unit` and `test:coverage` are real `vitest` targets (see
`libs/ts-env-loader/project.json`). Every scenario in
[behaviors/env-loader/env-loader.feature](./behaviors/env-loader/env-loader.feature) is exercised
by `libs/ts-env-loader/src/env-loader.unit.test.ts`, and every scenario in
[behaviors/port-resolver/port-resolver.feature](./behaviors/port-resolver/port-resolver.feature)
by `libs/ts-env-loader/src/port-resolver.unit.test.ts` — both via `@amiceli/vitest-cucumber`.

- [Architecture](./architecture.md) — ts-env-loader
- [Behaviors](./behaviors/README.md) — ts-env-loader
