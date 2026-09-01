---
title: "Testing Contract Enforcement"
description: "The four machine-checked testing policies and the command that enforces each."
category: explanation
subcategory: development
tags:
  - testing
  - unit-tests
  - integration-tests
  - e2e-tests
  - bdd
  - gherkin
created: 2026-09-01
when_to_use: "Use when a test-contract check fails or when adding a project to the testing registry."
---

# Testing Contract Enforcement

Four policies in this standard are machine-checked rather than reviewed by reading. Each has one
command, one exit-code contract, and one corpus of documents that pins its diagnostics.

| Policy   | What it rejects                                                                                                                             | Command                                     |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| Layout   | An executable test outside its project's `tests/<level>/` root, in a forbidden directory, unselected by any runner glob, or selected by two | `test-contract layout validate --fixture`   |
| Coverage | A threshold below the 99% native floor, a missing threshold, a conflicting one, a placeholder target, or an incomplete aggregate            | `test-contract coverage validate --fixture` |
| BDD      | A feature, scenario, example, or step with no binding in an applicable adapter, and any binding that is ambiguous or unused                 | `test-contract bdd validate --fixture`      |
| Manifest | A retained `package.json` with no named direct consumer, and a script that only proxies an Nx target                                        | `test-contract manifest validate --fixture` |

Every command exits `0` on a valid document, `1` on a contract failure, and `2` on CLI or input
misuse. A contract failure prints its diagnostic code and the identity of the offending item; it
never rounds, summarises, or reports a percentage in place of the item.

## Registry

`repo-config.yml`'s `testing:` block is the single registry of projects, owners, corpora, and
runtime identities. It is a bijection with `nx show projects`: a project absent from the registry
and a registry row naming no project both fail `test-contract registry validate`. Add the row in
the same change that adds the project.

## Owner fixtures

Each owner declares four RED documents under
`apps/rhino-cli/tests/fixtures/test-contract/owners/<OWNER_ID>/`, one per policy, naming the
mutation and the diagnostic it must produce. They are the acceptance evidence an owner's migration
is judged against, so a fixture that stops loading removes that owner's signal rather than merely
failing a test. `test-contract validate --owner --check --fixture` resolves one and rejects a
fixture bound to a different check or filed under a different owner.

## Both repositories

`ose-public` and `ose-private` enforce the identical contract. `apps/rhino-cli/` and
`specs/apps/rhino/` are byte-identical across the two, so a policy change in one obligates the same
change in the other and a refreshed `apps/rhino-cli/parity-manifest.sha256`.
