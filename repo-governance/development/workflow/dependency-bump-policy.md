---
description: Three-path decision tree (LTS, 60-day soak, security waiver) governing every dependency bump across the polyglot monorepo.
when_to_use: Use whenever bumping a dependency, runtime, or base image version, to classify the path and pin exactly.
---

# Dependency Bump Stability & Safety Policy

Every dependency bump MUST satisfy three constraints before it is merged: (1) reproducibility via exact pinning, (2) stability via LTS-first or 60-day soak, and (3) security via CVE clearance. This rule prevents shipping fresh versions whose breakage profile is undiscovered while ensuring known vulnerabilities are patched.

## Contents

- [Principles and Conventions Implemented](./dependency-bump-policy/principles-and-conventions-implemented.md) — Why this policy exists.
- [Three-Path Decision Tree](./dependency-bump-policy/three-path-decision-tree.md) — Path A (LTS), Path B (60-day), Path C (waiver).
- [KEV Fast-Track and EPSS Escalation](./dependency-bump-policy/kev-fast-track-and-epss-escalation.md) — Actively-exploited-CVE overrides.
- [Selection Rules Within Every Path](./dependency-bump-policy/selection-rules-within-every-path.md) — Recency and functional stability.
- [Pinning Policy (Hard Rule)](./dependency-bump-policy/pinning-policy-hard-rule.md) — Exact-pin form per manifest.
- [CVE Clearance Process](./dependency-bump-policy/cve-clearance-process.md) — The five sources and the clearance status values.
- [Examples](./dependency-bump-policy/examples.md) — Worked Path A/B/C decisions.
- [Application Workflow](./dependency-bump-policy/application-workflow.md) — The twelve-step procedure.
- [Tools, Automation, and References](./dependency-bump-policy/tools-automation-and-references.md) — Enforcement tools and the full reference list.

## Cutoff Date Computation and Plan Duration

### Cutoff Date Computation

For every bump, the policy author MUST state the cutoff date in writing:

```
Today: <YYYY-MM-DD>
Cutoff: today − 60 days = <YYYY-MM-DD>
Eligible (Path B): versions released on or before <cutoff>
```

This ensures auditability when CVE or release dates are revisited.

### When the Plan Spans Many Days

If a plan with dependency bumps takes more than 60 days to merge, the cutoff drifts forward. Re-run the eligibility check before the final merge to catch newly-eligible versions or newly-disclosed CVEs.

## Scope

### What This Policy Covers

- All `package.json` `dependencies`, `devDependencies`, `peerDependencies`, `optionalDependencies` (npm)
- All `Cargo.toml` `[dependencies]` version entries (Rust)
- All `rust-toolchain.toml` compiler-channel pins (Rust toolchain)
- All `global.json` `sdk.version` and `*.csproj`/`*.fsproj` `<PackageReference>` (.NET)
- All `package.json` `volta` block (Node.js, npm)
- All `Dockerfile` `FROM` lines and `docker-compose*.yml` `image:` references (base images)
- All GitHub Actions `uses:` references and inline version pins (CI workflow files)
- All composite-action input defaults (`.github/actions/*/action.yml`)

### What This Policy Does NOT Cover

- Workspace-internal `*` references (`@open-sharia-enterprise/web-ui: "*"` etc.) — these resolve via npm workspaces to local paths, not the registry
- Lockfiles (`package-lock.json`, `go.sum`, etc.) — managed by tooling after manifest changes
- Type-only dev deps where the security surface is provably zero (exact pinning still recommended, but lower enforcement priority)
