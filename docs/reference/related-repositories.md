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

The OSE ecosystem has four sibling repositories. Each has a different job, so choose the one that
matches what you are trying to understand rather than treating them as interchangeable copies.

| Repository                                                 | Visibility  | Role                                                            | Start there when…                                                  |
| ---------------------------------------------------------- | ----------- | --------------------------------------------------------------- | ------------------------------------------------------------------ |
| [`ose-public`](https://github.com/wahidyankf/ose-public)   | Public, MIT | The OSE product platform and its public research                | You want to understand or run OSE itself.                          |
| [`ose-primer`](https://github.com/wahidyankf/ose-primer)   | Public, MIT | A reusable polyglot Nx starter built from OSE practices         | You want a starting point for a different product.                 |
| `ose-private`                                              | Private     | Authorized product operations and local CoralPolyp sandbox work | You are an authorized maintainer following its private onboarding. |
| [`beaver-nest`](https://github.com/wahidyankf/beaver-nest) | Public, MIT | A separate product in the wider ecosystem                       | You want to work on BeaverNest.                                    |

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
`ose-private`. BeaverNest uses a fork and is outside that identity boundary. See the
[SDLC gate standard](./sdlc-gate-standard.md#rhino-cli-byte-identity-boundary) for the policy.

## Contribution and access boundaries

External contribution intake is closed across this coordinated delivery. Public readers can explore,
fork, and learn from the MIT repositories, but should not expect an external pull-request intake or
access to private systems.
