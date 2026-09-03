---
title: TypeScript 5.9 Release
description: OSE Platform compatibility note for the TypeScript 5.9 strategy target
category: explanation
subcategory: prog-lang
tags:
  - typescript
  - release
  - version-strategy
principles:
  - explicit-over-implicit
  - reproducibility
version: "5.9"
lts_until: not-applicable
status: strategy-target
created: 2026-09-03
---

# TypeScript 5.9 Release

TypeScript 5.9 is the documented strategy target for newer projects. Its relevant changes include a
smaller generated `tsconfig.json`, `import defer`, Node.js 20 module support, and compiler
performance improvements.

The repository package manifests and lockfile remain authoritative for whether an individual
project has adopted this target.

**Upstream reference**: [TypeScript 5.9 release notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-9.html)
