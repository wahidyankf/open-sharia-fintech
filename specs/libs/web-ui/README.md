# web-ui Specs

The behavioral corpus for [web-ui](../../../libs/web-ui/README.md), the shared React component
library.

A library owns exactly one surface, so the three corpus entries sit directly under the library
root rather than under an owner directory — see
[Logical Owner Corpus](../../../repo-governance/conventions/structure/specs-directory-structure/logical-owner-corpus.md).

## Structure

```
specs/libs/web-ui/
├── README.md
├── architecture.md     # the current, as-built library
└── behaviors/          # Gherkin feature files, one folder per component
```

## Status

```bash
nx run web-ui:test:unit
```

Every scenario is consumed at the unit level by the matching `*.steps.tsx` file co-located with
its component under `libs/web-ui/src/`.

- [Architecture — web-ui](./architecture.md)
- [Behaviors — web-ui](./behaviors/README.md)
