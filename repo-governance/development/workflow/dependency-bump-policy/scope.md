---
title: "Scope"
description: The manifest types and version pins this policy covers, and the workspace-internal references, lockfiles, and type-only deps it excludes.
category: explanation
subcategory: development
tags:
  - dependencies
  - security
  - versioning
  - reproducibility
  - workflow
created: 2026-05-15
when_to_use: Use when determining whether a specific manifest field or file falls under this policy.
---

# Scope

## What This Policy Covers

- All `package.json` `dependencies`, `devDependencies`, `peerDependencies`, `optionalDependencies` (npm)
- All `Cargo.toml` `[dependencies]` version entries (Rust)
- All `rust-toolchain.toml` compiler-channel pins (Rust toolchain)
- All `global.json` `sdk.version` and `*.csproj`/`*.fsproj` `<PackageReference>` (.NET)
- All `package.json` `volta` block (Node.js, npm)
- All `Dockerfile` `FROM` lines and `docker-compose*.yml` `image:` references (base images)
- All GitHub Actions `uses:` references and inline version pins (CI workflow files)
- All composite-action input defaults (`.github/actions/*/action.yml`)

## What This Policy Does NOT Cover

- Workspace-internal `*` references (`@open-sharia-enterprise/web-ui: "*"` etc.) — these resolve via npm workspaces to local paths, not the registry
- Lockfiles (`package-lock.json`, `go.sum`, etc.) — managed by tooling after manifest changes
- Type-only dev deps where the security surface is provably zero (exact pinning still recommended, but lower enforcement priority)
