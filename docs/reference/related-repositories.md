---
title: "Related Repositories"
description: Ecosystem of sibling repositories in the open-sharia-enterprise ecosystem
category: reference
subcategory: ecosystem
tags:
  - reference
  - ose-primer
  - ose-private
  - ecosystem
  - cross-repo
created: 2026-04-18
---

# Related Repositories

This reference documents the external repositories that exist in the `open-sharia-enterprise` ecosystem, the relationships between them, and where to find authoritative source-of-truth for each concern.

The ecosystem consists of three independent sibling repositories. No parent coordination repository exists.

| Repository                                                 | Visibility | License     | Purpose                                                    |
| ---------------------------------------------------------- | ---------- | ----------- | ---------------------------------------------------------- |
| [`ose-public`](https://github.com/wahidyankf/ose-public)   | Public     | MIT         | Enterprise platform — upstream source of truth (this repo) |
| [`ose-primer`](https://github.com/wahidyankf/ose-primer)   | Public     | MIT         | Scaffolding template derived from `ose-public`             |
| [`ose-private`](https://github.com/wahidyankf/ose-private) | Private    | Proprietary | Infrastructure — self-hosted CI runner, `coralpolyp` app   |

## `ose-primer`

`ose-primer` ([github.com/wahidyankf/ose-primer](https://github.com/wahidyankf/ose-primer)) is a public, MIT-licensed template repository derived from `ose-public`. It packages the repository scaffolding (governance layer, AI agents, skills, conventions, CI harness, polyglot showcase) into a reusable starting point for teams building their own Sharia-compliant enterprise product on top of the same platform conventions.

### Upstream / downstream relationship

`ose-public` is **upstream**: all scaffolding originates here, then flows to `ose-primer` to keep the template current.

`ose-primer` is **downstream**: it receives scaffolding updates, but its product layer (anything a consumer builds on top) is never pulled back into `ose-public`. Generic improvements that consumers contribute to `ose-primer` (for example, new governance patterns, Skill definitions, or demo-app implementations) can flow back to `ose-public` when adopted.

Both directions — propagation (upstream → downstream) and adoption (downstream → upstream) — are maintained **manually**, typically driven by the [plan-multi-repo-parity-planning](../../repo-governance/workflows/plan/plan-multi-repo-parity-planning.md) and [plan-multi-repo-parity-planning-and-execution](../../repo-governance/workflows/plan/plan-multi-repo-parity-planning-and-execution.md) planning workflows, which survey both repos, record per-gap decisions, and author aligned plans. Paths that are product-specific (for example, `apps/organiclever-*` or `apps/ose-www`) are never propagated in either direction.

### Licensing

`ose-public` is **MIT throughout**. See [LICENSING-NOTICE.md](../../LICENSING-NOTICE.md) for details.

`ose-primer` is also **MIT throughout**. Only scaffolding, governance, agents, skills, and polyglot demo apps live in `ose-primer`; product-specific apps are excluded. Consumers who fork `ose-primer` can build proprietary or open products on top without any restrictions.

### Non-Goals for this document

- This document does not describe parity mechanics or release cadence. Those details live in the multi-repo parity planning workflows under `repo-governance/workflows/plan/`.
- This document does not enumerate every file-by-file classification. Per-gap classification is decided during each parity planning pass.
- This document does not describe how to clone, set up, or build `ose-primer` itself; that belongs in `ose-primer`'s own README.

### Where to look next

- [plan-multi-repo-parity-planning](../../repo-governance/workflows/plan/plan-multi-repo-parity-planning.md) — the planning workflow that surveys sibling repos and authors aligned parity plans.
- [ose-primer on GitHub](https://github.com/wahidyankf/ose-primer) — downstream template repository.

## `ose-private`

`ose-private` ([github.com/wahidyankf/ose-private](https://github.com/wahidyankf/ose-private)) is a **private, proprietary** repository hosting the operational infrastructure for the OSE Platform ecosystem. It is not publicly accessible.

### What lives in `ose-private`

- **Self-hosted GitHub Actions runner** — multi-arch Docker image with `launchd` supervisor, per-container resource caps, and stale-runner cleanup. Serves `ose-private`'s own CI exclusively; `ose-public` uses GitHub-hosted `ubuntu-latest`.
- **`coralpolyp`** — infrastructure orchestrator app (Rust/Axum backend, Next.js + Effect TS frontend). Purpose is proprietary and not described in public documentation.
- Infrastructure-only governance and conventions that diverge from `ose-public` norms.

### Relationship to `ose-public`

`ose-private` shares its root commit with `ose-public` (forked from the same origin). It has since diverged in stack and conventions. There is **no classifier-driven content sync** between `ose-public` and `ose-private` — neither propagation nor adoption flows apply. Any cross-repo work between them is performed manually on a case-by-case basis.

### Licensing

`ose-private` is **proprietary** (not MIT). It is listed here for ecosystem awareness; contributors to `ose-public` are not expected to have access.
