# Data Access, ORMs, and Query Builders (By Example, Python)

**Course ID**: `data-access-orms-and-query-builders` · **Format**: By Example · **Language**: Python.

**Short summary**: Using ORMs and query builders safely

**Scope note**: the three-tier spectrum from raw SQL → query builder → full ORM, the trade-offs each
tier buys, the N+1 problem, the identity-map and unit-of-work patterns, migrations, and when each tier
is the right call. `†`: fully type-annotated Python (DD-39) over the DB-API driver. The build-your-own
tier — reconstructing a minimal ORM so it stops being magic — is
[`28-build-your-own-orm-and-query-builder`](./build-your-own-orm-and-query-builder.md).

## Why this exists · the big idea

- **The problem before the solution**: hand-writing SQL and mapping every result row to an object by
  hand is tedious and error-prone; the object-relational impedance mismatch — objects have identity,
  references, and inheritance while tables have rows, keys, and joins — bred a generation of
  boilerplate mapping code.
- **Keep-this-if-you-forget-everything**: an ORM is an abstraction over SQL, not a replacement for
  understanding it — it buys productivity on CRUD and charges you the moment the query matters, so know
  which tier you're on and what it hides.
- **Big ideas touched**: `abstraction-and-its-cost` (each tier hides more SQL for more leverage, and
  the hidden SQL leaks as the N+1 and the accidental full-table scan), `coupling-vs-cohesion` (a
  repository/data-mapper layer keeps persistence concerns cohesive and decoupled from domain logic
  instead of scattering SQL through the codebase).

## Prerequisites

- **Prior topics**: [topic 10 SQL Essentials](./sql-essentials.md) and
  [topic 26 Advanced SQL & Query Performance](./advanced-sql-and-query-performance.md).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** (fully type-annotated); a local SQL
  database; the DB-API driver (PEP 249), a query builder, and an ORM library, each CVE-clean and
  pinned; Neovim/VSCode with the Python LSP (DD-17).
- **Assumed knowledge**: writing joins and reading an `EXPLAIN` plan (topics 10, 26); indexes and how
  they change a query plan (topic 26); reading a typed Python module (topic 04).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the patterns taught here (Active Record, Data Mapper, Unit of Work, Identity
  Map, Lazy Load, the N+1 problem) are stable, named in Fowler's PoEAA, and correctly unpinned. PEP 249
  (Python DB-API v2.0) remains the standard low-level driver contract.
- 2026-07-12 — verified: specific ORM/query-builder library names and versions move over time — keep
  the shipped text pattern-first and library-agnostic, and re-verify any named library at authoring
  time.
- 2026-07-18 — verified (authoring-time library re-check per the note above): SQLAlchemy 2.0.51 (2026-06-15)
  is current stable; no breaking changes to declarative `Mapped[]` mapping, `raiseload()`, or async
  session/engine patterns since 2.0.0. **Content note**: SQLAlchemy's own docs now describe
  `subqueryload()` as "mostly legacy," superseded by `selectinload()` — teach it in co-14/ex-39/ex-40 as
  the older/legacy third strategy, not co-equal with `selectinload`/`joinedload`. The `AsyncAttrs` mixin
  (`await obj.awaitable_attrs.rel`) is the documented escape hatch for ad hoc lazy access under async and
  is worth a mention alongside `raiseload()` in co-16/co-24. SQLAlchemy 2.1 is in beta (2.1.0b3,
  2026-06-27, Python ≥3.10 floor, greenlet no longer bundled by default) — irrelevant to the 2.0.x line
  taught here, but the natural re-verification trigger if this topic's shelf life needs to survive 2.1
  going stable. Source: [SQLAlchemy 2.0 changelog](https://docs.sqlalchemy.org/en/20/changelog/changelog_20.html),
  [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html).
- 2026-07-18 — verified: peewee 4.2.6 (2026-07-17) is current stable, actively maintained (5 releases in
  the last week), "Production/Stable" classifier, no deprecation of the Active-Record `.save()` API.
  PyPika 0.51.1 (2026-02-04) is current stable, not archived, but lightly staffed (192 open issues / 41
  open PRs against ~3 releases/year, no curated changelog) — **content note**: fine to teach as the
  query-builder contrast, but flag it as a lighter-weight dependency than the other three rather than a
  corporate-backed one. Alembic 1.18.5 (2026-06-25) is current stable; no breaking changes to
  `alembic init`/autogenerate/upgrade-downgrade. **Content note**: a previously-misdetected false-positive
  (PostgreSQL sequence defaults on non-PK columns flagged as changed on every autogenerate run) is now
  fixed in current Alembic — worth knowing if co-20/ex-51 discusses autogenerate noise. PEP 249 remains
  Final with no successor in development. Sources: [peewee CHANGELOG](https://github.com/coleifer/peewee/blob/master/CHANGELOG.md),
  [PyPika PyPI](https://pypi.org/project/PyPika/), [Alembic changelog](https://alembic.sqlalchemy.org/en/latest/changelog.html),
  [PEP 249](https://peps.python.org/pep-0249/).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

This topic sits on [topic 10 SQL Essentials](./sql-essentials.md) and
[topic 26 Advanced SQL](./advanced-sql-and-query-performance.md): it does not re-teach SQL — it teaches
the abstraction layers built over it (query builders, ORMs) and the trade-off each tier buys. SQLAlchemy
2.0.x is the Data-Mapper teaching engine; peewee is the Active-Record contrast; PyPika is the query-builder
contrast; Alembic drives migrations. All Python is fully type-annotated (DD-39).

- **co-01 · data-access-spectrum** — the raw-SQL → query-builder → ORM spectrum, and what each tier buys and hides.
- **co-02 · raw-sql-dbapi** — the PEP 249 DB-API: connection, cursor, execute, fetch, and manual row→object mapping.
- **co-03 · query-builder-core** — building queries as composable data structures rather than concatenated strings.
- **co-04 · query-builder-library-contrast** — how a standalone builder (PyPika) and SQLAlchemy Core differ in style and scope.
- **co-05 · parameterized-queries-and-emitted-sql** — placeholders keep values out of the SQL text; inspecting the emitted SQL + params.
- **co-06 · declarative-orm-mapping** — SQLAlchemy 2.0 `DeclarativeBase` + `Mapped[...]` typed column mapping.
- **co-07 · active-record-vs-data-mapper** — the object persists itself (peewee) vs a session/mapper persists it (SQLAlchemy).
- **co-08 · relationship-mapping** — one-to-many/foreign-key relationships and bidirectional `back_populates`.
- **co-09 · many-to-many-association** — association tables and association objects for M:N links.
- **co-10 · identity-map** — one Python object per primary key within a session, deduplicated across queries.
- **co-11 · session-object-states** — transient → pending → persistent → detached, plus expire/refresh.
- **co-12 · unit-of-work** — the session batches, orders, and flushes changes as one coordinated write.
- **co-13 · lazy-loading** — relationships fetched on first access, and the `DetachedInstanceError` when the session is gone.
- **co-14 · eager-loading-strategies** — `selectinload`, `joinedload`, and `subqueryload` and how each shapes the SQL.
- **co-15 · n-plus-1-problem** — one query fanning out into hundreds, diagnosed by query count and fixed by eager loading.
- **co-16 · raiseload-guard** — `raiseload()` turning an accidental lazy load into a loud error instead of a silent query.
- **co-17 · orm-transactions** — session commit/rollback, `begin()` scope, and nested savepoints.
- **co-18 · connection-pooling** — `pool_size`/`max_overflow`, pool exhaustion, and `pool_pre_ping` recovery.
- **co-19 · migrations-alembic-workflow** — versioned schema evolution with Alembic (`init`, revision, `upgrade`).
- **co-20 · autogenerate-migrations** — deriving a migration from a model↔schema diff, and why you still review it.
- **co-21 · migration-reversibility** — writing real `downgrade` paths and the expand-contract zero-downtime pattern.
- **co-22 · cascade-delete-orm** — ORM `cascade="all, delete-orphan"` vs database `ON DELETE CASCADE`.
- **co-23 · bulk-operations** — set-oriented bulk insert/update instead of per-object round trips.
- **co-24 · async-orm-session** — `create_async_engine` + `AsyncSession` and why lazy loading is forbidden there.
- **co-25 · orm-vs-raw-sql-tradeoff** — where the ORM's leverage helps (CRUD) and where raw SQL wins (reporting, bulk).
- **co-26 · query-builder-vs-orm-tradeoff** — composition + injection safety without the identity-map/change-tracking machinery.
- **co-27 · choosing-tier-per-workload** — matching CRUD / analytics / hot-path workloads to the right tier.

## Tensions & trade-offs — when NOT to reach for this

- **The ORM hides SQL until it can't**: the abstraction is productive for CRUD but leaks on the queries
  that matter — the N+1, the accidental full-table scan, the query you can't express — and then you
  need exactly the SQL you were avoiding (topic 26).
- **The query builder is often the sweet spot**: a full ORM buys identity map and change tracking you
  may not need; a query builder gives composition and injection safety without the object-graph
  machinery. Reach for the ORM when the domain is genuinely object-shaped, not by reflex.
- **When NOT**: analytics, reporting, and bulk operations are set-oriented — forcing them through an
  ORM's row-object model is slow and awkward, so drop to SQL for those.

## Lineage — why it beat the alternative

- The object-relational impedance mismatch spawned mountains of hand-written mapping code that was
  tedious and bug-prone. Fowler's _Patterns of Enterprise Application Architecture_ (2002) named the
  patterns — Active Record, Data Mapper, Unit of Work, Identity Map — that ORMs then productized, while
  the DB-API contract (PEP 249) gave Python a uniform driver layer to build on. The ORM won for
  CRUD-heavy applications by collapsing the boilerplate; it is precisely the abstraction whose cost the
  next topic makes concrete by rebuilding it —
  [`28-build-your-own-orm-and-query-builder`](./build-your-own-orm-and-query-builder.md) — and it
  rests on the query-performance foundation of
  [`26-advanced-sql-and-query-performance`](./advanced-sql-and-query-performance.md).

## Worked examples

Colocated under `data-access/learning/code/`; runnable against a local DB, fully type-annotated Python
(DD-20/DD-30/DD-34/DD-39). Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises; every concept
above is exercised by ≥1 example.

### Beginner

- **ex-01 · spectrum-same-query-three-ways** — stub "list orders with customer" at all three tiers — verify each returns the same rows. (co-01)
- **ex-02 · dbapi-connect-cursor** — `sqlite3` connect/cursor/execute/fetchall — verify rows returned. (co-02)
- **ex-03 · dbapi-parameterized** — a parameterized query with placeholders — verify no string interpolation. (co-02, co-05)
- **ex-04 · dbapi-row-to-dataclass** — map cursor rows to a typed dataclass — verify typed objects. (co-02)
- **ex-05 · dbapi-executemany** — batch insert via `executemany` — verify N rows inserted. (co-02)
- **ex-06 · dbapi-transaction-commit** — commit/rollback around writes — verify rollback undoes. (co-02, co-17)
- **ex-07 · querybuilder-select** — PyPika builds a `SELECT` — verify the emitted SQL. (co-03, co-05)
- **ex-08 · querybuilder-where-compose** — compose `WHERE` conditions programmatically — verify parameterized SQL. (co-03, co-05)
- **ex-09 · querybuilder-join** — build a two-table join — verify the `JOIN` SQL emitted. (co-03)
- **ex-10 · querybuilder-execute** — run a built query via the DB-API — verify results. (co-03)
- **ex-11 · querybuilder-vs-string-safety** — builder vs f-string concatenation — verify the builder escapes input. (co-05)
- **ex-12 · sqlalchemy-core-table** — define a Core `Table` + metadata — verify the schema is created. (co-04, co-03)
- **ex-13 · sqlalchemy-core-select** — a Core `select()` construct — verify emitted SQL + rows. (co-03, co-05)
- **ex-14 · declarative-model-basic** — `DeclarativeBase` + `Mapped[]` columns — verify the table maps. (co-06)
- **ex-15 · declarative-typed-columns** — `Mapped[int]`/`Mapped[str]` typed mapping — verify types on load. (co-06)
- **ex-16 · orm-insert-object** — add an object, commit — verify the row persisted. (co-06, co-17)
- **ex-17 · orm-query-select** — `session.execute(select(Model))` — verify objects returned. (co-06)
- **ex-18 · orm-update-object** — mutate + commit — verify `UPDATE` emitted. (co-06, co-12)
- **ex-19 · orm-delete-object** — `session.delete` + commit — verify `DELETE` emitted. (co-06)
- **ex-20 · activerecord-peewee-model** — peewee `Model.create`/`save` (Active Record) — verify the row persisted. (co-07)
- **ex-21 · activerecord-vs-datamapper** — the same write in peewee (AR) vs SQLAlchemy (DM) — verify the object-saves-itself vs session contrast. (co-07)
- **ex-22 · relationship-one-to-many** — `relationship()` customer→orders — verify navigation loads children. (co-08)
- **ex-23 · relationship-back-populates** — bidirectional `back_populates` — verify both sides linked. (co-08)
- **ex-24 · foreign-key-mapping** — `ForeignKey` + `mapped_column` — verify the FK constraint. (co-08)
- **ex-25 · many-to-many-assoc-table** — an association `Table` for M:N — verify link rows. (co-09)
- **ex-26 · many-to-many-navigate** — navigate both sides of an M:N — verify related collections. (co-09)
- **ex-27 · identity-map-same-object** — query the same PK twice in a session — verify the same Python object (`is`). (co-10)
- **ex-28 · session-lifecycle-begin** — open session, add, commit, close — verify the basic lifecycle. (co-11, co-17)

### Intermediate

- **ex-29 · session-states-transient-pending** — observe transient→pending→persistent — verify via `inspect()`. (co-11)
- **ex-30 · session-expire-refresh** — `expire` + `refresh` reloads from the DB — verify fresh values. (co-11)
- **ex-31 · unit-of-work-flush-order** — add several, flush, observe ordered `INSERT`s — verify UoW orders by dependency. (co-12)
- **ex-32 · unit-of-work-dirty-tracking** — mutate a persistent object, flush — verify only changed columns in the `UPDATE`. (co-12)
- **ex-33 · unit-of-work-autoflush** — a query triggers autoflush of pending — verify pending written before the select. (co-12)
- **ex-34 · lazy-loading-default** — access a relationship, observe the extra `SELECT` — verify the lazy query fires. (co-13)
- **ex-35 · lazy-loading-detached-error** — access a lazy attr after the session closes — verify `DetachedInstanceError`. (co-13, co-11)
- **ex-36 · n-plus-1-reproduce** — loop over parents accessing children — verify N+1 queries emitted. (co-15, co-13)
- **ex-37 · eager-selectinload** — `selectinload()` — verify two queries, not N+1. (co-14, co-15)
- **ex-38 · eager-joinedload** — `joinedload()` single-query join — verify one query. (co-14, co-15)
- **ex-39 · eager-subqueryload** — the `subqueryload` strategy — verify a batched load. (co-14)
- **ex-40 · eager-strategy-contrast** — contrast selectin vs joined vs subquery — verify query-count/shape differ. (co-14)
- **ex-41 · raiseload-guard** — `raiseload()` forbidding lazy loads — verify it raises on accidental lazy access. (co-16)
- **ex-42 · n-plus-1-count-assert** — assert the query count with an event listener — verify count before/after the fix. (co-15)
- **ex-43 · orm-transaction-commit-rollback** — `session.begin()` context, rollback on error — verify atomicity. (co-17)
- **ex-44 · orm-nested-savepoint** — `begin_nested()` savepoint — verify partial rollback. (co-17)
- **ex-45 · connection-pool-basics** — engine `pool_size`/`max_overflow` — verify connections reused. (co-18)
- **ex-46 · pool-exhaustion** — exhaust the pool, observe the timeout — verify `QueuePool` timeout. (co-18)
- **ex-47 · pool-pre-ping** — `pool_pre_ping` recovers stale connections — verify recovery. (co-18)
- **ex-48 · alembic-init** — `alembic init` + configure — verify `env.py` + versions dir. (co-19)
- **ex-49 · alembic-first-migration** — hand-write a create-table migration — verify `upgrade` creates the table. (co-19)
- **ex-50 · alembic-upgrade-downgrade** — upgrade then downgrade — verify the schema round-trips. (co-19, co-21)
- **ex-51 · alembic-autogenerate** — autogenerate from a model diff — verify generated ops match the models. (co-20)
- **ex-52 · alembic-autogen-review** — review + edit an autogen migration — verify a manual correction of a missed change. (co-20)
- **ex-53 · migration-reversible-data** — a data migration with a real `downgrade` — verify reversibility. (co-21)
- **ex-54 · migration-irreversible-guard** — a drop-column migration that raises in `downgrade` — verify the explicit non-reversible marker. (co-21)
- **ex-55 · cascade-delete-orm** — `cascade="all, delete-orphan"` — verify children deleted with the parent. (co-22)
- **ex-56 · cascade-vs-db-fk** — ORM cascade vs DB `ON DELETE CASCADE` — verify the behavioral contrast. (co-22)

### Advanced

- **ex-57 · bulk-insert-orm** — `insert().values()` / bulk mappings — verify a fast bulk write. (co-23)
- **ex-58 · bulk-update-core** — Core `update()` vs per-object — verify a single `UPDATE` for many rows. (co-23)
- **ex-59 · bulk-vs-orm-perf** — measure bulk Core vs an ORM loop — verify bulk is far faster. (co-23, co-25)
- **ex-60 · async-engine-session** — `create_async_engine` + `AsyncSession` — verify an async query round-trips. (co-24)
- **ex-61 · async-eager-loading** — async with `selectinload` (no lazy) — verify eager avoids the async lazy pitfall. (co-24, co-14)
- **ex-62 · async-lazy-forbidden** — a lazy access under async — verify it raises (must eager-load). (co-24, co-16)
- **ex-63 · async-concurrent-sessions** — `asyncio.gather` over multiple sessions — verify concurrency. (co-24)
- **ex-64 · orm-vs-raw-crud** — the same CRUD in ORM vs raw SQL — verify the ORM is shorter, raw more explicit. (co-25)
- **ex-65 · orm-vs-raw-reporting** — a reporting query: ORM awkward vs raw SQL clean — verify raw wins for set ops. (co-25, co-27)
- **ex-66 · querybuilder-vs-orm-dynamic** — a dynamic-filter query: builder vs ORM — verify the builder composes without the object graph. (co-26)
- **ex-67 · querybuilder-vs-orm-tradeoff** — contrast builder (no identity map) vs ORM (change tracking) — verify a feature/cost table. (co-26)
- **ex-68 · choosing-tier-crud** — a CRUD workload → ORM recommendation — verify the decision + rationale. (co-27)
- **ex-69 · choosing-tier-analytics** — an analytics workload → raw-SQL recommendation — verify the decision. (co-27)
- **ex-70 · choosing-tier-hot-path** — a hot path → query-builder/raw recommendation — verify the decision. (co-27)
- **ex-71 · hybrid-orm-plus-raw** — ORM for CRUD + a raw-SQL escape hatch (`session.execute(text())`) — verify both in one app. (co-25, co-27)
- **ex-72 · identity-map-across-queries** — the identity map dedups across two queries — verify one instance. (co-10)
- **ex-73 · relationship-lazy-strategies-config** — configure the default lazy strategy per relationship — verify the configured behavior. (co-13, co-14)
- **ex-74 · self-referential-relationship** — an adjacency-list self-FK tree — verify parent/child navigation. (co-08)
- **ex-75 · association-object-m2m** — an association object with extra columns on an M:N — verify the extra attribute persists. (co-09)
- **ex-76 · migration-zero-downtime** — an expand-contract migration — verify the additive step then the cleanup. (co-21, co-19)
- **ex-77 · connection-pool-tuning** — tune the pool for a concurrency target, measure — verify throughput at target. (co-18)
- **ex-78 · capstone-preview-three-tier** — thread all three tiers + N+1 fix + migration — verify end-to-end. (co-01, co-15, co-19, co-25)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: implement the same small domain (customers/orders) across all three tiers — raw SQL, query
  builder, ORM — expose and fix an N+1, and ship a reversible migration, so each tier's trade-off is
  demonstrated rather than asserted.
- **Concepts exercised**: [ ] raw SQL via the DB-API (co-02) [ ] a query builder (co-03) [ ] an ORM with
  identity map + unit of work (co-06, co-10, co-12) [ ] an N+1 reproduced then fixed with eager loading
  (co-15, co-14) [ ] a forward + rollback migration (co-19, co-21) [ ] fully type-annotated Python.
- **Ordered steps**:
  1. `.../learning/capstone/code/tier1_sql.py` — the query in raw parameterized SQL with typed row
     mapping. Verify results match a known fixture and no string interpolation is used.
  2. `.../tier2_builder.py` and `.../tier3_orm.py` — the same query via builder and ORM. Verify
     identical results and capture the emitted SQL for each.
  3. Reproduce an N+1 on the ORM path, then fix it with eager loading. Verify the query count drops
     from N+1 to a small constant.
  4. `.../migrations/` — a forward migration plus its rollback. Verify migrate-then-rollback returns
     the schema to its starting state.
- **Acceptance criteria**: all three tiers return identical correct results; the N+1 is measurably
  eliminated; the migration applies and rolls back cleanly; the Python is fully type-annotated.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Patterns of Enterprise Application Architecture** — Martin Fowler, with David Rice, Matthew
  Foemmel, Edward Hieatt, Robert Mee, Randy Stafford (2002). Named and codified the Active Record, Data
  Mapper, Unit of Work, and Identity Map patterns underlying every modern ORM.

**Papers & articles**

- **OrmHate** — Martin Fowler (2012). Canonical defense-and-critique of ORMs, addressing the
  object-relational impedance mismatch directly. <https://martinfowler.com/bliki/OrmHate.html>
- **Active Record** — Martin Fowler, _PoEAA_ online catalog (2002). Canonical definition of the Active
  Record pattern used by Rails and the Django ORM.
  <https://martinfowler.com/eaaCatalog/activeRecord.html>
- **Data Mapper** — Martin Fowler, _PoEAA_ online catalog (2002). Canonical definition of the Data
  Mapper pattern used by Hibernate, Doctrine, and SQLAlchemy's ORM layer.
  <https://martinfowler.com/eaaCatalog/dataMapper.html>
- **PEP 249 — Python Database API Specification v2.0** — Marc-André Lemburg (1999). The standard
  low-level interface that Python ORMs and query builders are built on top of.
  <https://peps.python.org/pep-0249/>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Data depth — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Data depth — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 6 · Databases & data depth.

> _Content originated in the now-closed FS-SE plan (topic 27); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
