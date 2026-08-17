---
title: "Related Repositories"
description: "How the Open Sharia Enterprise repositories differ and where to begin."
category: reference
subcategory: ecosystem
tags:
  - reference
  - ecosystem
created: 2026-04-18
---

# Related Repositories

The OSE ecosystem has two sibling repositories under active coordination. Each has a different job,
so choose the one that matches what you are trying to understand rather than treating them as
interchangeable copies.

| Repository                                               | Visibility  | Role                                                            | Start there when…                                                  |
| -------------------------------------------------------- | ----------- | --------------------------------------------------------------- | ------------------------------------------------------------------ |
| [`ose-public`](https://github.com/wahidyankf/ose-public) | Public, MIT | The OSE product platform and its public research                | You want to understand or run OSE itself.                          |
| `ose-private`                                            | Private     | Authorized product operations and local CoralPolyp sandbox work | You are an authorized maintainer following its private onboarding. |

## The reader path that matters most

Choose **OSE Public** when the question is about the OSE product, its public website, research, or
product engineering. Start with [Getting started with OSE Public](../tutorials/getting-started-with-ose-public.md).

`ose-private` is not a public setup target. Its documentation and local sandbox instructions are
available only to authorized maintainers; public documentation intentionally does not describe its
internal implementation, access model, or operational layout.

## Repositories outside the parity set

[`ose-primer`](https://github.com/wahidyankf/ose-primer) is a public MIT polyglot Nx starter that
grew out of earlier OSE practice. **It carries no sync obligation in either direction.** It is not
part of the `rhino-cli` byte-identity boundary, it is not a propagation target for governance,
agent, skill, or workflow changes, and it is free to diverge from `ose-public` without that
divergence being a defect. No gate, agent, or workflow here may treat it as a parity peer. The same
holds for `beaver-nest`, which carries its own fork of `rhino-cli`.

## Shared boundaries

The `apps/rhino-cli` source must stay byte-identical across `ose-public` and `ose-private` — the
parity pair this page describes. See the
[SDLC gate standard](./sdlc-gate-standard.md#rhino-cli-byte-identity-boundary) for the policy.

`parity manifest validate` compares a repo's own committed manifest against that same repo's
tracked boundary only — it never fetches or compares against the sibling repo. Rolling a `rhino-cli`
change out to one repo while deferring it in the other therefore produces **silent drift**, not a red
gate in either repo; each repo's manifest stays internally consistent even while the two diverge
from each other. Verify parity across the pair by diffing the boundary directly, not by trusting
a green `parity manifest validate` in either repo.

## Sync cadence

Content parity and the `rhino-cli` byte-identity boundary above answer **what** stays identical;
this answers **how often** `ose-private` is brought current with `ose-public`.

**`ose-private` is kept in real time.** `rhino-cli` and the shared `repo-governance/` content
(conventions, workflows, agent definitions) propagate to `ose-private` as they land in `ose-public`,
not on a batched schedule. That repo backs live authorized-maintainer and infrastructure operations,
so governance and tooling drift there is costly immediately, not just eventually.

For portable governance, agent, and skill changes, public is the source and `ose-private` is
reconciled immediately. Verify the portable manifest byte-for-byte; list private-only operational
exceptions explicitly. Across both repos, preserve active goals during runner contention and remove
only each plan's own verified worktree immediately after that repository's final delivery.

## Contribution and access boundaries

External contribution intake is closed across this coordinated delivery. Public readers can explore,
fork, and learn from the MIT repositories, but should not expect an external pull-request intake or
access to private systems.
