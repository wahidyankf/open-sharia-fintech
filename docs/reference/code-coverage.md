---
title: Code Coverage Reference
description: How code coverage is measured, validated, and reported across all projects in the monorepo
category: reference
tags:
  - coverage
  - testing
  - quality
created: 2026-03-22
---

# Code Coverage Reference

How code coverage is measured and validated across all projects in the monorepo.

> **Note**: The polyglot demo apps (`a-demo-be-*`, `a-demo-fe-*`) and their
> per-language coverage tooling were removed from this repo on 2026-04-18. This page
> covers only the languages this repository still ships.

## Coverage Algorithm

Coverage is measured natively by each project's test runner. The standard
line-based algorithm counts:

- **COVERED**: hit count > 0 AND all branches taken (or no branches)
- **PARTIAL**: hit count > 0 but some branches not taken
- **MISSED**: hit count = 0
- **Coverage %** = `covered / (covered + partial + missed)`

Partial lines count as NOT covered.

## Per-Project Coverage Details

### Rust Projects

**Tool**: `cargo llvm-cov`
**Format**: LCOV at project `lcov.info`
**Threshold**: 90% line coverage

```bash
cargo llvm-cov --lib --fail-under-lines 90
```

### TypeScript Projects

**Tool**: Vitest with `@vitest/coverage-v8`
**Format**: LCOV at `coverage/lcov.info`

| Project              | Threshold | Exclusions |
| -------------------- | --------- | ---------- |
| organiclever-app-web | 70%       | None       |
| ayokoding-www        | 80%       | None       |
| ose-www              | 80%       | None       |
| wahidyankf-www       | 80%       | None       |

### F# Projects

**Tool**: NUnit / xUnit + Coverlet
**Format**: Cobertura XML (enforced via Coverlet threshold flags)

```bash
dotnet test --collect:"XPlat Code Coverage" \
  /p:Threshold=95 /p:ThresholdType=line /p:ThresholdStat=Total
```

| Project         | Threshold | Notes                      |
| --------------- | --------- | -------------------------- |
| organiclever-be | 95%       | Line coverage via Coverlet |
| ose-be          | 95%       | Line coverage via Coverlet |

## Thresholds

| Project Type         | Threshold | Rationale                               |
| -------------------- | --------- | --------------------------------------- |
| CLI tools (Rust)     | >= 90%    | Core business logic                     |
| Rust libraries       | >= 90%    | Shared utilities                        |
| organiclever-be      | >= 95%    | F#/Giraffe backend API                  |
| ose-be               | >= 95%    | F#/Giraffe backend API                  |
| organiclever-app-web | >= 70%    | Frontend app with MSW integration tests |
| ayokoding-www        | >= 80%    | Content platform with UI rendering code |
| ose-www              | >= 80%    | Content platform with UI rendering code |
| wahidyankf-www       | >= 80%    | Personal portfolio (Next.js)            |

## CI Integration

Coverage is measured during `test:quick` (part of the pre-push hook and the
[PR quality gate](../../.github/workflows/pr-quality-gate.yml), which also triggers on pushes to
`main`) via the native `test:coverage` Nx target per project.

### Pipeline Flow

1. `test:unit` runs tests and generates the coverage file
2. `test:coverage` enforces the threshold natively (per-project tool)
3. Both steps run sequentially inside `test:quick`

## Troubleshooting

### Coverage drops after adding a new file

New source files with no test coverage appear as 0% in the coverage report. Either
write tests or add the file to the appropriate exclusion config (language
tool config).

### Exclusions

Configure exclusions in each project's native coverage tool:

- **Rust**: `--ignore-filename-regex` flag in `cargo llvm-cov`
- **TypeScript**: `exclude` array in `vitest.config.ts`
- **C#/F#**: `[ExcludeFromCodeCoverage]` attribute on classes/methods

## Related Documentation

- [Three-Level Testing Standard](../../repo-governance/development/quality/three-level-testing-standard.md) - Coverage thresholds and testing levels
- [Project Dependency Graph](./project-dependency-graph.md) - Which projects depend on rhino-cli
- [Nx Configuration](./nx-configuration.md) - How test:quick targets are configured
