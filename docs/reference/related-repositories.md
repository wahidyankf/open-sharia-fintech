---
title: "Related Repositories"
description: "How the Open Sharia Enterprise repositories differ and where to begin."
category: reference
subcategory: ecosystem
tags:
  - reference
  - ecosystem
  - ose-primer
created: 2026-04-18
---

# Related Repositories

The OSE ecosystem has three sibling repositories. Each has a different job, so choose the one that
matches what you are trying to understand rather than treating them as interchangeable copies.

| Repository                                               | Visibility  | Role                                                            | Start there when…                                                  |
| -------------------------------------------------------- | ----------- | --------------------------------------------------------------- | ------------------------------------------------------------------ |
| [`ose-public`](https://github.com/wahidyankf/ose-public) | Public, MIT | The OSE product platform and its public research                | You want to understand or run OSE itself.                          |
| [`ose-primer`](https://github.com/wahidyankf/ose-primer) | Public, MIT | A reusable polyglot Nx starter built from OSE practices         | You want a starting point for a different product.                 |
| `ose-private`                                            | Private     | Authorized product operations and local CoralPolyp sandbox work | You are an authorized maintainer following its private onboarding. |

## The two reader paths that matter most

- Choose **OSE Public** when the question is about the OSE product, its public website, research, or
  product engineering. Start with [Getting started with OSE Public](../tutorials/getting-started-with-ose-public.md).
- Choose **OSE Primer** when the question is how to adopt the governance, testing, automation, and
  reference-app foundation in a new repository. Its README is the authoritative onboarding path.

`ose-private` is not a public setup target. Its documentation and local sandbox instructions are
available only to authorized maintainers; public documentation intentionally does not describe its
internal implementation, access model, or operational layout.

## Shared boundaries

`ose-public` and `ose-primer` share selected governance and tooling content, but their positioning is
deliberately different: the former is the product platform; the latter is a starter. Their content
parity is planned and reviewed, not assumed from folder names.

The `apps/rhino-cli` source must stay byte-identical across `ose-public`, `ose-primer`, and
`ose-private` — the same three-repository family this page describes. See the
[SDLC gate standard](./sdlc-gate-standard.md#rhino-cli-byte-identity-boundary) for the policy.

## Sync cadence across repos

Content parity and the `rhino-cli` byte-identity boundary above answer **what** stays identical;
this answers **how often** each sibling repo is brought current with `ose-public` — the two siblings
differ, and the difference is deliberate, not an oversight:

- **`ose-private`** — kept **in real time**. `rhino-cli` and the shared `repo-governance/` content
  (conventions, workflows, agent definitions) propagate to `ose-private` as they land in
  `ose-public`, not on a batched schedule. This repo backs live authorized-maintainer and
  infrastructure operations, so governance and tooling drift there is costly immediately, not just
  eventually.
- **`ose-primer`** — kept on a **delayed** sync. As the reusable polyglot starter, `ose-primer` does
  not need every `ose-public` governance change the moment it lands; batching updates conserves the
  review and propagation cost of a sync that public downstream adopters do not need on a real-time
  cadence.

For portable governance, agent, and skill changes, public is the source, `ose-private` is reconciled
immediately, and Primer receives its companion delivery in the same plan unless a plan explicitly
records a bounded delay. Verify the portable manifest byte-for-byte; list private-only operational
exceptions explicitly. Across all three repos, preserve active goals during runner contention and
remove only each plan's own verified worktree immediately after that repository's final delivery.

## Contribution and access boundaries

External contribution intake is closed across this coordinated delivery. Public readers can explore,
fork, and learn from the MIT repositories, but should not expect an external pull-request intake or
access to private systems.
