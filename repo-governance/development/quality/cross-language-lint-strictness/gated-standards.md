---
title: "Gated standards"
description: "The table of every currently-gated artifact type, its linter, threshold/config, and CI job."
category: development
subcategory: quality
tags:
  - lint
  - quality
  - ci
created: 2026-06-10
when_to_use: "Use when checking which linter and CI job gates a given artifact type (shell, Dockerfile, GitHub Actions YAML, F#, Markdown, formatting)."
---

# Gated standards

| Artifact            | Tool         | Threshold / config                                      | CI job       |
| ------------------- | ------------ | ------------------------------------------------------- | ------------ |
| Shell scripts       | `shellcheck` | `--severity=warning`; root `.shellcheckrc`              | `shellcheck` |
| Dockerfiles         | `hadolint`   | `--failure-threshold warning`; root `.hadolint.yaml`    | `hadolint`   |
| GitHub Actions YAML | `actionlint` | non-zero on any finding (embeds shellcheck)             | `actionlint` |
| F# projects         | TWAE         | `TreatWarningsAsErrors` on every `.fsproj`              | `dotnet`     |
| F# projects         | analyzers    | G-Research.FSharp.Analyzers, `GRA-*` `--treat-as-error` | `dotnet`     |
| F# formatting       | `fantomas`   | `fantomas --check`                                      | `dotnet`     |
| Markdown            | markdownlint | see [markdown.md](.././markdown.md)                     | `markdown`   |
| Formatting          | Prettier     | `prettier --check`                                      | `format`     |

The `shellcheck`, `hadolint`, and `actionlint` jobs are **always-run** (their artifacts
are not Nx-tagged projects, so they are not gated by language detection). The F#
gates ride the existing Nx `lint`/`typecheck`/`test:quick` targets, which the
`dotnet` quality-gate job already runs, so no separate F# lint job is required.
