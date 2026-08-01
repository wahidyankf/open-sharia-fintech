---
title: "Related Repositories"
description: Ecosystem of sibling repositories in the open-sharia-enterprise ecosystem
category: reference
subcategory: ecosystem
tags:
  - reference
  - ose-primer
  - ose-private
  - beaver-nest
  - ecosystem
  - cross-repo
created: 2026-04-18
---

# Related Repositories

This reference documents the external repositories that exist in the `open-sharia-enterprise` ecosystem, the relationships between them, and where to find authoritative source-of-truth for each concern.

The ecosystem consists of four independent sibling repositories. No parent coordination repository exists.

| Repository                                                 | Visibility | License     | Purpose                                                    |
| ---------------------------------------------------------- | ---------- | ----------- | ---------------------------------------------------------- |
| [`ose-public`](https://github.com/wahidyankf/ose-public)   | Public     | MIT         | Enterprise platform — upstream source of truth (this repo) |
| [`ose-primer`](https://github.com/wahidyankf/ose-primer)   | Public     | MIT         | Scaffolding template derived from `ose-public`             |
| [`ose-private`](https://github.com/wahidyankf/ose-private) | Private    | Proprietary | Infrastructure — self-hosted CI runner, `coralpolyp` app   |
| [`beaver-nest`](https://github.com/wahidyankf/beaver-nest) | Public     | MIT         | BeaverNest — personal operating layer product on OSE       |

Three of the four — `ose-public`, `ose-primer`, and `ose-private` — form the **parity loop** whose generic content is kept aligned. `beaver-nest` is a full family member that stands **outside** that loop.

## Terminology — "the OSE repos"

When a request says **"all of the OSE repositories"**, **"all of the OSE repos"**, **"all four
repos"**, or any equivalent collective phrase, it means exactly these four, and nothing else:

| #   | Repository    |
| --- | ------------- |
| 1   | `ose-public`  |
| 2   | `ose-primer`  |
| 3   | `ose-private` |
| 4   | `beaver-nest` |

Four consequences worth stating, because each has been a real source of ambiguity:

- **`beaver-nest` is always included.** The collective term is **not** a synonym for the three-repo
  parity loop. `beaver-nest` sits outside that loop but is a full family member.
- **Only these four.** Other repositories that happen to sit in the same parent directory on a
  developer machine are not part of the set.
- **A change is incomplete until it lands in all four.** "Applied to the OSE repos" means four
  repositories, not "the ones where it was convenient".
- **Landing in all four is not the same as landing identically in all four.** Each repository's
  footprint differs — a convention may reference a document one repo does not have, or govern a
  surface that is empty there. Adapt per repository and say what differed; do not skip the repo, and
  do not force an artefact that does not fit it.

If a change genuinely should not apply to one of the four, name which one and why. Silently narrowing
the set is the failure this definition exists to prevent.

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

## `beaver-nest`

`beaver-nest` ([github.com/wahidyankf/beaver-nest](https://github.com/wahidyankf/beaver-nest)) is a public, MIT-licensed repository hosting **BeaverNest** — a personal operating layer covering an AI assistant, a content builder, a posting helper, and a personal workflow engine. It is a product built **within** the Open Sharia Enterprise ecosystem, not a replacement for it.

### Relationship to `ose-public`

`beaver-nest` scaffolded from this ecosystem — its governance tree, agent catalog, skills, conventions, and CI harness all originate in `ose-public` lineage. It is nonetheless a **fourth repository standing outside the parity loop**: it does not participate in cross-repo parity syncs in either direction, and no parity plan targets it. Adopting an `ose-public` change into `beaver-nest` is a deliberate, separately-planned decision made inside that repository.

Its product surface (`apps/beaver-nest-fe`, `apps/beaver-nest-be`) is product-specific and never flows back here.

### `apps/rhino-cli` boundary

`apps/rhino-cli` must be byte-identical across the three parity repositories per the [SDLC Gate Standard](./sdlc-gate-standard.md#rhino-cli-byte-identity-boundary). `beaver-nest` carries a **fork** of that shared tool which is explicitly **not** bound by the byte-identity rule.

### Licensing

`beaver-nest` is **MIT throughout**, matching `ose-public` and `ose-primer`.
