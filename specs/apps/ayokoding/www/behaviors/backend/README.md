# AyoKoding API Gherkin Specs

Gherkin feature files for the AyoKoding tRPC API surface, organized by bounded context.
Each folder maps to one bounded context from the
bounded-context map.

The slug `api` is a **perspective slug**, not a container. There is no separate API
container — tRPC procedures execute inside the same `web` container's Next.js server.
The `organiclever` peer keeps the slug `be` because `organiclever-be` is a real F#/Giraffe
container; ayokoding renamed `be` → `api` because it has no separate backend service.

## Structure

```
specs/apps/ayokoding/www/behaviors/backend/
├── content/                # tRPC content procedures
│   └── content-api.feature
├── search/                 # tRPC search procedure
│   └── search-api.feature
├── navigation/             # tRPC navigation tree procedure
│   └── navigation-api.feature
├── i18n/                   # tRPC locale data procedure
│   └── i18n-api.feature
└── health/                 # tRPC liveness probe
    └── health-check.feature
```

## Ubiquitous Language

Every domain term used in step text is defined in
ubiquitous-language/. Gherkin steps use only
glossary terms; code identifiers (procedure names, schema fields) match the
`Code identifier(s)` column verbatim.

## Conventions

- **File naming**: `[domain-capability].feature` (kebab-case)
- **Step language**: HTTP-semantic only — `the client calls X`, `the response should …`,
  `status code` (no UI verbs like clicks or types)
- **User story block**: Every `Feature:` block opens with `As a … / I want … / So that …`
- **Background**: Use `Given the API is running` as the first Background step
- **Term discipline**: Step text uses glossary terms and procedure names verbatim

## Relationship to the web perspective

These specs are the **HTTP counterpart** to
[www/behaviors/frontend/](../frontend/README.md). Both perspectives execute inside the
same `web` Next.js container; the split is a slug, not a container boundary.

- **api**: HTTP-semantic (the client calls, response shape, status codes)
- **web**: UI-semantic (clicks, types, sees, navigates, form submissions)

`apps/ayokoding-www-be-e2e` consumes these specs via Playwright-BDD step definitions.

## Related

- **Ubiquitous language**: ubiquitous-language/
- **Bounded-context map**: bounded-context-map.md
- **Web counterpart**: [frontend behaviors](../frontend/README.md)
- **Parent**: [behaviors](../README.md)

- [content — ayokoding-be Gherkin Domain](./content/README.md)
- [health — ayokoding-be Gherkin Domain](./health/README.md)
- [i18n — ayokoding-be Gherkin Domain](./i18n/README.md)
- [navigation — ayokoding-be Gherkin Domain](./navigation/README.md)
- [search — ayokoding-be Gherkin Domain](./search/README.md)
