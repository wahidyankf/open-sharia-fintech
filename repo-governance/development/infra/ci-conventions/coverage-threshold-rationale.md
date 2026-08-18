---
title: "Coverage Threshold Rationale"
description: Why coverage thresholds differ by project type.
category: explanation
subcategory: development
tags: [ci-cd, testing, coverage]
created: 2026-03-31
when_to_use: Use when checking a project's required coverage threshold.
---

# Coverage Threshold Rationale

Coverage thresholds are enforced by the native `test:coverage` Nx target as part of `test:quick`.
Thresholds differ by project type to reflect the realistic upper bound achievable through mocked
unit tests.

| Threshold | App Types                                                | Rationale                                                                                                                                                                       |
| --------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **90%**   | BE API backends (`organiclever-be`), CLI apps, Rust libs | Core business logic with high mock isolation. Service functions operate on pure data structures; 90% is achievable without heroic effort.                                       |
| **80%**   | Content platforms (`ayokoding-www`, `ose-www`)           | Significant UI rendering code and Next.js route handlers that are harder to unit-test. Some RSC rendering paths are excluded by design.                                         |
| **70%**   | FE apps (`organiclever-app-web`)                         | API, auth, and query layers are mocked by design; the mock boundaries limit what can be covered by unit tests. Lower threshold reflects this intentional architecture decision. |

Coverage is measured via the appropriate reporter for each language and converted to LCOV or
JaCoCo XML. Coverage enforcement runs inside each project's native `test:coverage` Nx target. See
`CLAUDE.md` for the exact command per language.
