# BeaverNest product persistence slice

One-line summary: introduce the first concrete BeaverNest feature that durably stores and retrieves
product data on the explicit SQLite foundation delivered by the `beavernest-app-setup` plan.

> Idea, added 2026-07-31 from `beaver-nest`'s `baseerah-repo-reset` plan; narrowed 2026-08-02 when
> the infrastructure-only SQLite foundation became its own active plan (`beaver-nest-app-setup`).
> Carried into `ose-public` 2026-08-10 by the `beaver-nest-repo-consolidation` plan's idea-triage
> step as part of the BeaverNest product port; renamed from `beaver-nest-persistence-layer` to
> `beavernest-persistence-layer` to match this repo's single-token domain naming
> ([File Naming Convention](../../../repo-governance/conventions/structure/file-naming.md)).

## Problem / context

The `beavernest-app-setup` plan (carried into
[`plans/done/2026-08-10__beavernest-app-setup`](../../done/2026-08-10__beavernest-app-setup/README.md),
closed delivered-as-descoped) deliberately created SQLite configuration, migrations, readiness,
durability, and recovery without a domain table. That avoids inventing a generic note, capture, or
settings model before a product behavior needs one, but it also means BeaverNest still cannot
remember real product data after the foundation lands.

## Why now

Not yet. Promote this brief together with the first assistant/content capability whose value depends
on durable state. The feature must drive aggregate shape, queries, audit actor, retention, and
soft-delete behavior.

## Prior art / precedents

- [`beavernest-app-setup`](../../done/2026-08-10__beavernest-app-setup/README.md) — delivered SQLite,
  DbUp, single-host, no-ORM, backup, and real-database test boundaries (closed
  delivered-as-descoped; the SQLite foundation itself shipped).
- [BeaverNest — Product](../../../specs/apps/beavernest/product/README.md) — names the assistant,
  content, posting, and workflow capabilities that may supply the first stateful slice.
- [Functional Programming](../../../repo-governance/development/pattern/functional-programming.md) —
  requires pure domain logic and an explicit imperative persistence edge.
- [Database Audit Trail](../../../repo-governance/development/pattern/database-audit-trail.md) —
  applies to every future domain table.

## Proposed direction (sketch)

Choose one minimal stateful behavior, design its table and repository port with the behavior, use
explicit parameterized SQL, and add a query builder only if measured query composition makes direct
SQL materially worse. Apply a forward-only DbUp migration and test against real disposable SQLite
files at integration/E2E levels.

## Rough scope & non-goals

In scope: one concrete product aggregate with durable create/read behavior, audit fields, migration,
repository boundary, and restart/backup coverage.

Out of scope: generic persistence abstractions, an ORM, selecting a query builder without need,
multi-tenant ownership, PostgreSQL, or a catch-all key/value table.

## Risks & open questions

- Which real capability supplies the first aggregate?
- What actor value is honest while the app has one VPN-trusted shared workspace and no identities?
- Does the behavior require update/soft-delete now, or only create/read?
- Are direct parameterized queries sufficient, or does concrete dynamic composition justify a query
  builder?

## What success looks like + promotion signal

Success means BeaverNest durably stores and retrieves real product data through one useful user
behavior, not merely a migration journal or diagnostic setting. Promote only when that behavior has
been selected and its lifecycle can be specified in Gherkin.
