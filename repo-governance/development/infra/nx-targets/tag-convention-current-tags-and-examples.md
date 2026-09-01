---
title: "Tag Convention — Tags, Examples, and Anti-Patterns"
description: The current per-project tag table, two worked tag-declaration examples, and the tag anti-patterns to avoid.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when copying an existing project's tag set as a template or checking a new tag set against known anti-patterns.
---

# Tag Convention — Tags, Examples, and Anti-Patterns

## Current Project Tags

| Project                    | Tags                                                                     |
| -------------------------- | ------------------------------------------------------------------------ |
| `ayokoding-www`            | `["type:app", "platform:nextjs", "lang:ts", "domain:ayokoding"]`         |
| `rhino-cli`                | `["type:app", "platform:cli", "lang:rust", "domain:tooling"]`            |
| `organiclever-app-web`     | `["type:app", "platform:nextjs", "lang:ts", "domain:organiclever"]`      |
| `organiclever-be`          | `["type:app", "platform:giraffe", "lang:dotnet", "domain:organiclever"]` |
| `organiclever-app-web-e2e` | `["type:e2e", "platform:playwright", "lang:ts", "domain:organiclever"]`  |
| `organiclever-be-e2e`      | `["type:e2e", "platform:playwright", "lang:ts", "domain:organiclever"]`  |
| `ose-www`                  | `["type:app", "platform:nextjs", "lang:ts", "domain:ose"]`               |
| `ts-env-loader`            | `["type:lib", "lang:ts", "domain:config"]`                               |

## Example: Complete Tag Declaration

An F#/Giraffe backend app declares all four dimensions:

```json
{
  "name": "organiclever-be",
  "tags": ["type:app", "platform:giraffe", "lang:dotnet", "domain:organiclever"]
}
```

A library has no platform boundary, so it omits `platform:` and declares the other three:

```json
{
  "name": "ts-env-loader",
  "tags": ["type:lib", "lang:ts", "domain:config"]
}
```

## Anti-Patterns

- **Omitting required dimensions**: Every project must declare `type:` and `domain:`. Omitting them breaks graph queries and boundary rules that rely on these dimensions.
- **Inventing non-standard values**: Adding values outside the controlled vocabulary (e.g., `platform:express`, `lang:javascript`, `domain:internal`) fragments the tag space. Add new values only by updating this convention.
- **Using a non-prefixed format**: Tags must use the `dimension:value` prefix format (e.g., `type:app`). Bare tags such as `app` or `golang` are not queryable by dimension.
- **Adding a `stack:` dimension**: The four-dimension scheme captures type, platform, language, and domain. A separate `stack:` field duplicates `platform:` and `lang:` without adding information. Use the defined dimensions instead.
- **Tagging apps with `domain:tooling` when they belong to a product**: `domain:tooling` is for general-purpose dev utilities with no product affiliation. An app that serves a specific product must carry that product's domain tag.
