# Example 45: A Cost-and-Scope Recommendation

_Traces to: `co-20`, `co-22`._

A scoped, written recommendation -- the `co-22` deliverable: NAME the force that decides self-host vs
managed for a given workload, with a rule the reader can apply.

## The rule (one sentence, with a named force)

Self-host when the workload is STATELESS, the team is LEARNING the substrate, or the monthly spend at
a managed tier would exceed the cost of a VM plus your own on-call; otherwise stay managed.

## Applied to three concrete workloads

- **A personal blog** (stateless, solo, learning) -- SELF-HOST. Force: the point IS to see the
  primitives; cost ~$5/mo beats a $20/mo tier.
- **A SaaS with a Postgres the team depends on** (stateful, HA-adjacent) -- MANAGED. Force: a
  stateful, must-not-lose-data system is a poor first self-host; managed Postgres absorbs backups and
  failover you would otherwise own at 3am.
- **A compliance-bound API** (audit, PCI) -- MANAGED (certified platform). Force: a self-host does
  not inherit a vendor's compliance cert; re-deriving one is far more expensive than the managed tier
  that already has it.

## Why naming the force matters

"We should self-host this" WITHOUT naming the specific force is a decision waiting to become an
incident. The discipline is to state WHICH dimension -- control, cost, state, compliance, learning --
is doing the deciding, and to revisit it when that dimension changes.

## Acceptance check

This file names a concrete rule and applies it to three workloads (`co-20`/`co-22`).
