---
description: "Phase 9 (full scope only): install the .NET SDK at the major version pinned by organiclever-be's global.json."
when_to_use: "Use when setting up .NET for the F# backends and libraries."
---

# Phase 9: .NET Ecosystem (Sequential)

**Condition**: `{input.scope} == full`

Required for: `organiclever-be`, `ose-be`, `crane-cli`, `fsharp-crane-core`, `fsharp-env-loader`

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
