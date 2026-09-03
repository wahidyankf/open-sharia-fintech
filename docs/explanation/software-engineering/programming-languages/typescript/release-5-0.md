---
title: TypeScript 5.0 Release
description: OSE Platform compatibility note for the TypeScript 5.0 baseline
category: explanation
subcategory: prog-lang
tags:
  - typescript
  - release
  - version-strategy
principles:
  - explicit-over-implicit
  - reproducibility
version: "5.0"
lts_until: not-applicable
status: baseline
created: 2026-09-03
---

# TypeScript 5.0 Release

TypeScript 5.0 is the documented minimum for modern TypeScript guidance in this repository. It
introduced the standards-track decorators model, `const` type parameters, and stronger enum union
semantics used by the platform's baseline guidance.

Projects still pin an exact compiler version in their package manifest and lockfile; this baseline
does not override a project's checked-in version.

**Upstream reference**: [TypeScript 5.0 release notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-0.html)
