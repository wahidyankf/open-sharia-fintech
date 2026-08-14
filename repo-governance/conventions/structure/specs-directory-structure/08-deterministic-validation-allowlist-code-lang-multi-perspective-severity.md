---
title: "Deterministic Validation: Allowlist, Code Lang, Multi-Perspective, Severity Audit"
description: The rhino-cli specs validation commands, the allowlist-driven default app selection, and the code_lang/gherkin/severity-downgrade fields DDD validators accept
when_to_use: Read this when running or configuring rhino-cli specs validate-* commands, or setting per-BC code_lang, multi-perspective gherkin, or DDD severity downgrades.
category: explanation
subcategory: conventions
tags:
  - conventions
  - specs
  - gherkin
  - directory-structure
  - organization
  - c4-diagrams
  - openapi
  - c4
created: 2026-04-02
---

# Deterministic Validation (rhino-cli)

The following `rhino-cli specs` commands validate the directory structure mechanically:

| Command                                    | What it checks                                                             |
| ------------------------------------------ | -------------------------------------------------------------------------- |
| `rhino-cli specs validate-tree <app>`      | Top-level folders match the canonical five — no flat-root artifacts remain |
| `rhino-cli specs validate-counts <folder>` | README count claims match actual `.feature` file counts                    |
| `rhino-cli specs validate-links <folder>`  | Markdown link integrity within the spec tree                               |
| `rhino-cli specs validate-adoption <app>`  | BDD/DDD/Contracts adoption gaps per surface profile                        |

These commands run as part of the `specs-quality-gate` workflow deterministic-offload pass. See [Deterministic Offload](./10-pre-push-ci-llm-validation-deterministic-offload-and-related-documentation.md#deterministic-offload) in the next section.

## Allowlist-driven default app selection

`validate-adoption`, `validate-tree`, `validate-counts`, and `validate-links` all accept the same three calling shapes:

- Positional `<folder>` or `<app>` — single-target legacy behavior preserved.
- `--apps <csv>` — multi-app validation across an explicit list.
- No positional, no flag — defaults to the `AppsWithDDD` allowlist (`organiclever`, `ose`).

The single source of truth for the allowlist is `apps/rhino-cli/src/internal/allowlist.rs`. Pre-push and CI surfaces invoke the four targets without arguments so adding a new app is a one-line edit there.

## Per-bounded-context `code_lang:` field (DDD validators)

`specs/apps/<app>/ddd/bounded-contexts.yaml` accepts an optional `code_lang: [<lang>, ...]` field per BC. Glossary code-identifier checks compute the file-extension glob list as the union of `SupportedLangGlobs[<lang>]` for every declared lang (e.g., `[fs]` → `*.fs`; `[ts, fs]` → `*.ts *.fs`). When omitted, the loader defaults to `[ts, tsx]` to preserve historical TS-only behaviour. Supported lang tags: `ts`, `tsx`, `fs`, `go`, `py`, `java`, `kt`, `rs`, `ex`, `exs`, `cs`, `clj`, `dart`.

## Multi-perspective `gherkin: []string` schema

`specs/apps/<app>/ddd/bounded-contexts.yaml` accepts both scalar and list forms for the `gherkin:` field. A scalar auto-converts to a single-element list at load time:

```yaml
gherkin: behavior/organiclever-app-web/gherkin/content # scalar (most BCs)
gherkin: # list (multi-perspective BCs)
  - behavior/organiclever-app-web/gherkin/content
  - behavior/organiclever-be/gherkin/content
```

The validator iterates every declared path in `checkGherkin`, `registeredGherkin`, and `gherkinRoots`. Glossary `Used in features` lookups resolve under any declared path (first-match-wins). This unblocks BCs that legitimately have both web and be gherkin trees (e.g., ayokoding's `content`, `search`, `i18n`, `navigation`).

## Severity audit log + env var

`OSE_RHINO_DDD_SEVERITY=warn` downgrades all `ddd bc` and `ddd ul` findings to warnings (exit 0 even when findings exist). Every honored downgrade emits a stderr audit line:

```
WARN: severity downgraded to "warn" via OSE_RHINO_DDD_SEVERITY env var
```

The legacy `ORGANICLEVER_RHINO_DDD_SEVERITY` env var was removed without a deprecation period in this same plan; every in-tree reference was renamed atomically. The flag form `--severity=warn|error` takes precedence over the env var.
