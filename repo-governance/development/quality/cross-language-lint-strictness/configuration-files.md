---
title: "Configuration files"
description: "Where each lint gate's configuration lives and what it pins or ignores."
category: development
subcategory: quality
tags:
  - lint
  - quality
  - ci
created: 2026-06-10
when_to_use: "Use when locating or editing a lint tool's configuration file (.shellcheckrc, .hadolint.yaml, .config/dotnet-tools.json)."
---

# Configuration files

- `.shellcheckrc` — `shell=bash`, `external-sources=true`; no repo-wide disables.
- `.hadolint.yaml` — `failure-threshold: warning`; `trustedRegistries`
  (`docker.io`, `mcr.microsoft.com`, `ghcr.io`); `ignored: [DL3008, DL3018]`
  (OS-package version-pinning is brittle — reproducibility comes from the pinned
  base-image tag, not per-package pins).
- `.config/dotnet-tools.json` — pins `fantomas`, `dotnet-fsharplint`, and
  `fsharp-analyzers` for `dotnet tool restore`.
