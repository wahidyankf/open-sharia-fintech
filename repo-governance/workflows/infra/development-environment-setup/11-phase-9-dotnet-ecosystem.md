---
title: "Phase 9: .NET Ecosystem (Sequential)"
description: "Phase 9 (full scope only): install the .NET SDK at the major version pinned by organiclever-be's global.json."
when_to_use: "Use when setting up .NET for organiclever-be or the ose-primer polyglot demo apps."
---

# Phase 9: .NET Ecosystem (Sequential)

**Condition**: `{input.scope} == full`

Required for: `organiclever-be`; also polyglot demo apps in ose-primer (extracted 2026-04-18)

## 9.1 Install .NET SDK

```bash
# macOS
brew install dotnet

# Linux — https://learn.microsoft.com/en-us/dotnet/core/install/linux
```

The required major version comes from the path in `repo-config.yml` at
`doctor.dotnet-global-json`, then that file's `sdk.version` (currently
`apps/ose-be/global.json`).

**Success criteria**: `dotnet --version` shows a version with the same or higher major version
as `global.json`.
