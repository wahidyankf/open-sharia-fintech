---
title: "Parity Checklist — Affected-First PR-Gate Principle"
description: Why PR checks scope to nx affected, and the exceptions.
category: explanation
subcategory: development
tags: [ci-cd, nx]
created: 2026-03-31
when_to_use: Use when adding a PR-gate check and deciding its scope.
---

# Parity Checklist — Affected-First PR-Gate Principle

The PR quality gate runs `nx affected` for all per-project checks so only changed projects pay
the cost of typecheck, lint, test, and coverage on each PR. Whole-repo checks that cannot be
scoped to affected projects are an explicit exception and must be justified.

| Check                       | Target / Command                               | Why whole-repo                                                        |
| --------------------------- | ---------------------------------------------- | --------------------------------------------------------------------- |
| Markdown linting            | `npm run lint:md`                              | Links reference cross-project paths; partial scans miss broken links  |
| Mermaid validation          | `rhino-cli:mermaid:validation`                 | Width rules apply across all `.md` files; a fix in one breaks another |
| Link validation             | `rhino-cli:links:validation`                   | Cross-project and external links must resolve globally                |
| Heading hierarchy           | `rhino-cli:headings:hierarchy-validation`      | Cross-file anchor references cannot be validated in isolation         |
| Governance vendor audit     | `rhino-cli:governance:vendor-audit-validation` | Scans `repo-governance/` globally for vendor-specific content leakage |
| Cross-vendor parity         | `rhino-cli:cross-vendor:parity-validation`     | All three harness binding trees are compared; scoping breaks the diff |
| Harness bindings validation | `npm run harness:bindings-validation`          | Binding parity is a whole-repo property; partial sync leaves gaps     |
| Env validation              | `rhino-cli:env:validation`                     | All `.env.example` files checked against a global schema              |

Any new whole-repo check added to CI or pre-push must be listed here with its justification before
it lands.
