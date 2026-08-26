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

| Repository                                               | Visibility  | Role                                                  | Start there when…                                                  |
| -------------------------------------------------------- | ----------- | ----------------------------------------------------- | ------------------------------------------------------------------ |
| [`ose-public`](https://github.com/wahidyankf/ose-public) | Public, MIT | The OSE product platform and its public research      | You want to understand or run OSE itself.                          |
| `ose-private`                                            | Private     | Authorized product operations and infrastructure work | You are an authorized maintainer following its private onboarding. |

## The reader path that matters most

Choose **OSE Public** when the question is about the OSE product, its public website, research, or
product engineering. Start with [Getting started with OSE Public](../tutorials/getting-started-with-ose-public.md).

`ose-private` is not a public setup target. Its documentation and local sandbox instructions are
available only to authorized maintainers; public documentation intentionally does not describe its
internal implementation, access model, or operational layout.

## Repositories outside the parity set

Some repositories share history with `ose-public` without sharing obligations. **They carry no sync
obligation in either direction**, sit outside the `rhino-cli` byte-identity boundary, and are not
propagation targets for governance, agent, skill, or workflow changes. No gate, agent, or workflow
here may treat one as a parity peer.

### BeaverNest moved out

[`beaver-nest`](https://github.com/wahidyankf/beaver-nest) is where the BeaverNest product now
lives. It used to be developed here as `apps/beavernest-app` (Flutter Web) and `apps/beavernest-be`
(F#/Giraffe), with a matching `specs/apps/beavernest/` spec tree, an `infra/dev/beavernest-app/`
Compose stack, and two deployer agents. **All of that was removed from `ose-public`**; the product
was rebuilt on Phoenix LiveView and Elixir in its own repository.

BeaverNest is a continuously used, family-only production product. Its scope ends at the family
boundary: "production" means real ongoing family use, not public or general-purpose availability.
It targets one continuously available family environment rather than separate staged environments;
Phoenix LiveView is the current fit for that operating model.
It also serves as an applied lab for learning how AI-assisted coding can support everyday family
activities and development with a
[dynamically typed language such as Elixir](https://hexdocs.pm/elixir/typespecs.html). Useful
learnings can flow back selectively into `ose-public` and other OSE products; this knowledge
transfer creates no parity or automatic propagation obligation.

It carries no `rhino-cli` at all, so there is nothing for the byte-identity boundary to cover, and
`rhino-cli`'s parity gate asserts that the boundary never names it — see
`apps/rhino-cli/src/application/parity.rs`.

If you are looking for BeaverNest code, issues, or plans, go to that repository. Anything still
naming BeaverNest here is a historical record — an archived plan under [`plans/done/`](../../plans/done/README.md)
or a published update post — not live work.

This routing is **unenforced by decision**: determining whether proposed work belongs to the
family product requires human product judgment.

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
exceptions explicitly.

### Private-only operational exceptions

- **Elixir/Erlang CI toolchain provisioning.** `ose-public`'s `rust` job in `pr-quality-gate.yml`
  installs Erlang/Elixir via `erlef/setup-beam` and sets `RHINO_REQUIRE_ELIXIR=1`, so the two
  Elixir formatter-wrapper tests in `apps/rhino-cli/tests/gate_format_verify_wrappers.rs` run for
  real on every push. `ose-private` carries no Elixir source and provisions no such toolchain, so
  those same byte-identical tests self-skip there instead — a deliberate, not accidental,
  divergence: nothing in `ose-private` needs the coverage the toolchain would exercise.

## Contribution and access boundaries

External contribution intake is closed across this coordinated delivery. Public readers can explore,
fork, and learn from the MIT repositories, but should not expect an external pull-request intake or
access to private systems.
