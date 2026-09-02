# web-ui-token Specs

The behavioral corpus for [web-ui-token](../../../libs/web-ui-token/README.md), the shared
design-token package.

A library owns exactly one surface, so the three corpus entries sit directly under the library
root rather than under an owner directory — see
[Logical Owner Corpus](../../../repo-governance/conventions/structure/specs-directory-structure/logical-owner-corpus.md).

## Structure

```
specs/libs/web-ui-token/
├── README.md
├── architecture.md     # the current, as-built library
└── behaviors/          # Gherkin feature files, one folder per capability
    └── tokens/
```

## Status

`test:unit` is an `echo` placeholder — no test runner is configured for this package yet. The
corpus is written ahead of that work so the structure validator sees the same shape here as
everywhere else.

- [Architecture](./architecture.md) — web-ui-token
- [Behaviors](./behaviors/README.md) — web-ui-token
