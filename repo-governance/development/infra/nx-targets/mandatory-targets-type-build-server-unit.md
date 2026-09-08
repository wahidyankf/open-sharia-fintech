---
description: Requirements for typecheck on statically typed projects, build on compiled/bundled projects, dev/start on server apps, and test:unit.
when_to_use: Use when determining which of these five conditional targets a given project type needs.
---

# Mandatory Targets — Type, Build, Server, and Unit-Test Requirements

## Statically Typed Projects

TypeScript and other statically typed projects:

| Target      | Requirement                                                                |
| ----------- | -------------------------------------------------------------------------- |
| `typecheck` | Run the type checker without emitting artifacts (`tsc --noEmit`, `mypy .`) |

**Statically typed backends declare `typecheck`** with `dependsOn: ["codegen"]` where contract codegen applies. The `ose-be` example: `dotnet build apps/ose-be/ose-be.fsproj -c Release`.

**Not required for dynamically typed languages** (plain JavaScript, Ruby) or languages where
compilation already enforces types and `build` covers it — except when an additional static
analysis pass is warranted.

## Compiled and Bundled Projects

Projects that produce artifacts from a compilation or bundling step (Rust, .NET, Next.js):

| Target  | Requirement                                                          |
| ------- | -------------------------------------------------------------------- |
| `build` | Produce production-ready artifacts; declare `outputs` for Nx caching |

**Not required for interpreted languages** (plain Node.js scripts) where the source is the deployable artifact.

## Apps with Development Servers

Next.js and Axum apps:

| Target | Requirement                                       |
| ------ | ------------------------------------------------- |
| `dev`  | Start local server with live-reload or watch mode |

## Apps with Production Server Mode

Next.js and Axum apps:

| Target  | Requirement                |
| ------- | -------------------------- |
| `start` | Serve the production build |

## Projects with Unit Tests

Rust, .NET, TypeScript apps:

| Target      | Requirement                                                          |
| ----------- | -------------------------------------------------------------------- |
| `test:unit` | Run only isolated unit tests; must not require any external services |
