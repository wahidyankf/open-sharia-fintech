# Build Your Own ORM and Query Builder (By Example, Python)

**Course ID**: `build-your-own-orm-and-query-builder` · **Format**: By Example · **Language**: Python.

**Short summary**: Implementing a small ORM and query builder

**Scope note**: the build-your-own tier of
[`27-data-access-orms-and-query-builders`](./data-access-orms-and-query-builders.md) — implement a
minimal ORM and query builder so the tier above stops being magic. You build a fluent query builder,
row→object mapping, an identity map, a unit of work, and lazy loading. `†`: fully type-annotated
Python (DD-39) over the DB-API driver.

## Why this exists · the big idea

- **The problem before the solution**: an ORM feels like magic until it surprises you — a silent N+1,
  a stale object, a write that didn't persist — and you can't debug what you can't picture, so the
  fastest way to demystify the abstraction is to rebuild its core.
- **Keep-this-if-you-forget-everything**: an ORM is a handful of small, comprehensible mechanisms — a
  query built as data, rows mapped to typed objects, one object per identity, changes tracked and
  flushed in a single transaction — none of which is magic once you've written it.
- **Big ideas touched**: `abstraction-and-its-cost` (building the abstraction yourself makes its cost
  concrete — you feel exactly what lazy loading buys and what it charges when it fans into an N+1).

## Prerequisites

- **Prior topics**: [topic 27 Data Access: ORMs & Query Builders](./data-access-orms-and-query-builders.md).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** (fully type-annotated); a local
  SQLite (or equivalent) database reached through the standard DB-API driver (PEP 249); `pytest`;
  Neovim/VSCode with the Python LSP (DD-17).
- **Assumed knowledge**: the three data-access tiers and the patterns they use — identity map, unit of
  work, lazy load, the N+1 (topic 27); parameterized SQL and joins (topics 10, 26); reading and writing
  typed Python (topic 04).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the patterns being rebuilt (query object, row mapper, identity map, unit of
  work, lazy load) are stable, named in Fowler's PoEAA, and correctly unpinned; the first-person
  SQLAlchemy architecture account (AOSA vol. II) remains the canonical reference for how a production
  Python ORM is actually structured.
- 2026-07-12 — verified: PEP 249 (Python DB-API v2.0) is the current standard driver contract the
  hand-built layer sits on; no version to pin.
- 2026-07-18 — verified (authoring-time re-check): PEP 249 status unchanged (Final, no successor). The
  AOSA vol. II SQLAlchemy chapter is still live at its usual URL and remains the best available
  first-person account, though it describes pre-1.0 SQLAlchemy (0.7, 2011) — no newer/better first-person
  written account of a Python ORM's internals was found, so keep citing it but don't imply it reflects
  current SQLAlchemy 2.0 architecture. **Content note**: `pytest` (not a generic "test runner") is this
  repo's actual convention for By-Example topics with tests — tightened the Tools & environment line
  above accordingly; current stable is `pytest==9.1.1`. **Content note (stdlib `sqlite3`, Python
  3.13/3.14)**: `sqlite3.connect()`'s optional args (`timeout`, `detect_types`, `isolation_level`,
  `check_same_thread`, `factory`, `cached_statements`, `uri`) are deprecated as positional — pass them as
  keywords in any authored example that sets them; an unclosed `Connection` now emits a `ResourceWarning`
  on GC (reinforces always using a context manager, relevant to co-15/co-25). No breaking change applies
  to the `?`-placeholder / `row_factory`-assignment style this topic is scoped to use. Source:
  [AOSA SQLAlchemy chapter](https://aosabook.org/en/v2/sqlalchemy.html),
  [PEP 249](https://peps.python.org/pep-0249/), [sqlite3 docs](https://docs.python.org/3/library/sqlite3.html),
  [pytest PyPI](https://pypi.org/project/pytest/).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject By-Example). Each example below cites the co-NN it exercises. -->

This build-your-own tier re-implements the mechanisms topic 27 uses as a black box; it does not
re-teach the tier's semantics (identity map, unit of work, lazy load, N+1 — owned by topic 27) but
rebuilds them so they stop being magic.

- **co-01 · sql-as-data** — Representing a query as a data structure (a clause tree) rather than a string is what makes it safely composable and inspectable before execution.
- **co-02 · parameterized-sql** — Emitting `?`/`%s` placeholders with a separate bound-parameter list, never interpolating values, is the one non-negotiable safety property of a hand-built builder.
- **co-03 · immutable-fluent-builder** — Each builder method returns a new builder rather than mutating in place, so a partially-built query can be branched and reused without aliasing bugs.
- **co-04 · select-clause-composition** — A SELECT is assembled from independent columns/from/join fragments that each contribute SQL text and parameters to the final compile.
- **co-05 · where-clause-composition** — Predicates combine with AND/OR into a boolean tree that compiles to a parameterized WHERE, each leaf contributing one placeholder.
- **co-06 · order-limit-composition** — ORDER BY, LIMIT, and OFFSET are trailing clauses appended after WHERE, with LIMIT/OFFSET themselves parameterized.
- **co-07 · insert-update-delete-builders** — The same clause-as-data approach extends to INSERT/UPDATE/DELETE, each emitting its own parameterized statement shape.
- **co-08 · compile-to-sql-and-params** — A single `compile()` walk turns the clause tree into a `(sql_string, params)` pair — the boundary between the builder and the driver.
- **co-09 · table-metadata-registration** — A central table/column metadata registry (name, columns, types, primary key) is the shared schema the builder and mapper both read from.
- **co-10 · row-to-object-mapping** — A mapper turns a driver result row (a tuple or dict) into a typed domain object by column-to-attribute assignment.
- **co-11 · object-to-row-mapping** — The inverse mapping reads a domain object's attributes back into a column→value dict for INSERT/UPDATE.
- **co-12 · type-coercion-on-load** — Per-column type converters coerce raw driver values (`0/1`→`bool`, ISO string→`date`) on load and back on store.
- **co-13 · identity-map** — A per-session `{(table, pk): object}` cache guarantees one in-memory object per primary key, so two loads of the same row return the identical instance.
- **co-14 · weak-reference-identity-map** — Backing the identity map with a `WeakValueDictionary` lets unreferenced objects be garbage-collected instead of leaking for the session's lifetime.
- **co-15 · session-as-transaction-boundary** — The session owns one connection and demarcates a transaction: everything between `begin` and `commit`/`rollback` is one unit.
- **co-16 · unit-of-work-new-tracking** — The session records objects added via `add()` as "new" so they become INSERTs at flush.
- **co-17 · unit-of-work-dirty-tracking** — Comparing an object's current attributes against a snapshot taken at load detects "dirty" objects needing UPDATE, so only changed rows are written.
- **co-18 · unit-of-work-deleted-tracking** — Objects marked deleted are recorded so they become DELETEs, distinct from merely dropping the reference.
- **co-19 · flush-ordering** — The unit of work orders INSERTs before dependent rows and DELETEs after, respecting foreign-key dependencies so a flush never violates a constraint.
- **co-20 · atomic-transaction-flush** — A flush wraps all new/dirty/deleted writes in one transaction that commits together or rolls back together on any error.
- **co-21 · descriptor-protocol-lazy-load** — A Python descriptor (PEP 487 `__set_name__` / `__get__`) on the relationship attribute defers the child query until the attribute is first accessed.
- **co-22 · n-plus-1-from-lazy-loading** — Iterating N parents and touching a lazy relationship on each issues N extra queries — the N+1 you now cause yourself, and can now see in the query log.
- **co-23 · connection-cursor-wiring** — The whole layer sits on the PEP 249 connect→cursor→execute→fetch contract; the builder produces exactly what `cursor.execute(sql, params)` consumes.
- **co-24 · schema-migration-runner** — A tiny migration runner applies ordered, versioned schema-change scripts and records which have run, so the hand-built stack can evolve its schema.
- **co-25 · fully-typed-builder-api** — Generics and `Mapped[]`-style typing give the builder and mapper a fully type-annotated public API the type checker can verify end to end.

## Worked examples

Colocated under `build-your-own-orm/learning/code/`; each component is built and unit-tested against a
local SQLite database, fully type-annotated Python (DD-20/DD-30/DD-34/DD-39). Contiguous `ex-01..ex-78`.
Every example cites the `co-NN` it exercises; every concept above is exercised by ≥1 example.

### Beginner

- **ex-01 · clause-as-data-node** — represent a single column reference as a data node, not a string — verify it stores the column name and renders lazily. (co-01)
- **ex-02 · render-column-node** — render a column node to SQL text — verify it emits the `users.id` fragment. (co-01)
- **ex-03 · placeholder-not-interpolation** — bind a literal value as a parameter node — verify the SQL carries `?` and the value lands in the params list. (co-02)
- **ex-04 · params-collected-in-order** — compile a query with two bound values — verify the params list is ordered left-to-right. (co-02, co-08)
- **ex-05 · builder-returns-new-instance** — call `.where()` on a builder — verify the original builder is unchanged (immutability). (co-03)
- **ex-06 · branch-a-partial-query** — build a base query then branch two variants — verify each variant compiles independently. (co-03)
- **ex-07 · select-columns** — `select("id", "name")` — verify the SELECT clause lists both columns. (co-04)
- **ex-08 · select-from-table** — add `.from_("users")` — verify the FROM clause. (co-04)
- **ex-09 · select-star-default** — `select()` with no columns — verify it emits `SELECT *`. (co-04)
- **ex-10 · select-with-join** — `.join("orders", on=...)` — verify the JOIN fragment and ON predicate. (co-04)
- **ex-11 · where-equals** — `.where(col("age") == 30)` — verify `WHERE age = ?` plus param `30`. (co-05)
- **ex-12 · where-and** — combine two predicates with AND — verify `a = ? AND b = ?`. (co-05)
- **ex-13 · where-or** — combine two predicates with OR — verify `(a = ? OR b = ?)`. (co-05)
- **ex-14 · where-comparison-operators** — `<`, `>`, `!=`, `IN` — verify each emits the correct operator and params. (co-05)
- **ex-15 · where-nested-boolean-tree** — `(a AND (b OR c))` — verify the parenthesized compile and param order. (co-05, co-08)
- **ex-16 · order-by-clause** — `.order_by("name")` — verify a trailing `ORDER BY name`. (co-06)
- **ex-17 · order-by-desc** — `.order_by("name", desc=True)` — verify `ORDER BY name DESC`. (co-06)
- **ex-18 · limit-offset** — `.limit(10).offset(20)` — verify `LIMIT ? OFFSET ?` plus params `10, 20`. (co-06)
- **ex-19 · insert-builder** — `insert("users").values(...)` — verify `INSERT INTO users (...) VALUES (?, ?)`. (co-07)
- **ex-20 · update-builder** — `update("users").set(...).where(...)` — verify `UPDATE ... SET ... WHERE ...` plus params. (co-07)
- **ex-21 · delete-builder** — `delete("users").where(...)` — verify `DELETE FROM users WHERE ...`. (co-07)
- **ex-22 · compile-returns-sql-and-params** — `.compile()` on a full query — verify it returns a `(sql, params)` tuple. (co-08)
- **ex-23 · compile-is-pure** — compile the same query twice — verify identical output with no side effects. (co-08, co-03)
- **ex-24 · execute-over-cursor** — pass a compiled `(sql, params)` to a DB-API cursor — verify rows returned. (co-23)
- **ex-25 · connect-cursor-lifecycle** — open connection, cursor, execute, close — verify the PEP 249 flow. (co-23)
- **ex-26 · builder-typed-api** — annotate builder methods with return types — verify `pyright` passes on a query chain. (co-25)

### Intermediate

- **ex-27 · register-table-metadata** — register a `users` table (columns, pk) in a metadata registry — verify the registry returns the column list. (co-09)
- **ex-28 · metadata-drives-select** — build a `SELECT *` from metadata columns — verify column order matches registration. (co-09, co-04)
- **ex-29 · primary-key-from-metadata** — read a table's pk column from metadata — verify it identifies `id`. (co-09)
- **ex-30 · row-tuple-to-object** — map a result tuple to a `User` dataclass — verify attributes assigned by column order. (co-10)
- **ex-31 · row-dict-to-object** — map a dict row to an object — verify assignment by column name. (co-10)
- **ex-32 · map-multiple-rows** — map a `fetchall` result to a list of objects — verify count and field values. (co-10)
- **ex-33 · object-to-insert-values** — read a `User` object's attrs into a column→value dict — verify the dict matches the columns. (co-11)
- **ex-34 · object-to-update-set** — build an UPDATE SET dict from a changed object — verify only column values present. (co-11)
- **ex-35 · roundtrip-object-row-object** — object → row → object — verify the result equals the original. (co-10, co-11)
- **ex-36 · type-coerce-bool-on-load** — coerce driver `0/1` to `bool` on load — verify the attribute is `True`/`False`. (co-12)
- **ex-37 · type-coerce-date-on-load** — coerce an ISO string to `date` — verify a `date` instance. (co-12)
- **ex-38 · type-coerce-on-store** — coerce `bool`/`date` back to driver types on store — verify stored value is `0/1`/string. (co-12)
- **ex-39 · custom-type-converter** — register a converter for a JSON column — verify `dict` ⇄ json text. (co-12)
- **ex-40 · identity-map-same-instance** — load pk 1 twice in one session — verify `a is b`. (co-13)
- **ex-41 · identity-map-different-keys** — load pk 1 and pk 2 — verify distinct instances. (co-13)
- **ex-42 · identity-map-miss-then-hit** — first load populates the map, second hits the cache — verify the second issues no query. (co-13)
- **ex-43 · identity-map-key-shape** — key by `(table, pk)` — verify the same pk across two tables is not conflated. (co-13)
- **ex-44 · weak-value-identity-map** — back the map with `WeakValueDictionary` — verify the entry drops after the object is GC'd. (co-14)
- **ex-45 · weak-map-no-leak** — load many rows then drop refs — verify the map shrinks under GC. (co-14)
- **ex-46 · session-owns-connection** — the session holds one connection — verify all queries share it. (co-15)
- **ex-47 · session-begin-commit** — begin, write, commit — verify the row persists after commit. (co-15)
- **ex-48 · session-rollback** — begin, write, rollback — verify the row is absent. (co-15)
- **ex-49 · session-scope-context-manager** — `with Session() as s:` — verify commit on clean exit, rollback on exception. (co-15)
- **ex-50 · load-snapshot-for-dirty** — snapshot attrs at load — verify a snapshot is stored per object. (co-17)
- **ex-51 · identity-map-feeds-mapper** — the mapper checks the identity map before constructing — verify a cached object is reused. (co-13, co-10)
- **ex-52 · metadata-typed-columns** — annotate metadata columns with Python types — verify the type drives the coercer. (co-12, co-09)
- **ex-53 · builder-plus-mapper-select** — compose a builder query, execute, map rows — verify a list of typed objects. (co-08, co-10)
- **ex-54 · typed-session-api** — annotate `session.get[T](pk) -> T` generically — verify `pyright` infers the return type. (co-25)

### Advanced

- **ex-55 · uow-track-new** — `session.add(obj)` — verify the object is recorded in the new-set. (co-16)
- **ex-56 · uow-new-becomes-insert** — flush a new object — verify an INSERT is emitted. (co-16, co-20)
- **ex-57 · uow-track-dirty** — mutate a loaded object — verify dirty detection against the snapshot. (co-17)
- **ex-58 · uow-dirty-only-changed-cols** — change one field — verify the UPDATE sets only that column. (co-17)
- **ex-59 · uow-clean-object-no-write** — flush an unchanged object — verify no UPDATE is emitted. (co-17)
- **ex-60 · uow-track-deleted** — `session.delete(obj)` — verify it is recorded in the deleted-set. (co-18)
- **ex-61 · uow-deleted-becomes-delete** — flush a deleted object — verify a DELETE is emitted. (co-18, co-20)
- **ex-62 · flush-order-insert-before-child** — insert parent then FK child — verify the parent INSERT precedes the child. (co-19)
- **ex-63 · flush-order-delete-child-before-parent** — delete child before parent — verify the order respects the FK. (co-19)
- **ex-64 · flush-atomic-commit** — a mixed new/dirty/deleted flush — verify one transaction commits all. (co-20)
- **ex-65 · flush-atomic-rollback** — error mid-flush — verify the entire flush rolls back with no partial write. (co-20)
- **ex-66 · flush-clears-tracking** — after commit — verify the new/dirty/deleted sets reset. (co-16, co-20)
- **ex-67 · lazy-descriptor-defers** — define a relationship as a descriptor — verify the child query is not issued until access. (co-21)
- **ex-68 · lazy-descriptor-set-name** — `__set_name__` binds the attr name — verify the descriptor knows its field. (co-21)
- **ex-69 · lazy-loads-once** — access a lazy attr twice — verify only one query (cached after first). (co-21, co-13)
- **ex-70 · n-plus-1-observable** — iterate N parents, touch the lazy child each — verify N+1 queries in the log. (co-22)
- **ex-71 · n-plus-1-fix-eager** — add an eager batch load — verify it collapses to 2 queries. (co-22, co-14)
- **ex-72 · migration-runner-apply** — apply ordered migration scripts — verify the schema changed. (co-24)
- **ex-73 · migration-runner-version-table** — record applied versions — verify a re-run skips applied ones. (co-24)
- **ex-74 · migration-runner-order** — apply out-of-order files — verify they run in version order. (co-24)
- **ex-75 · wire-full-stack-select** — metadata + builder + mapper + identity map end to end — verify typed objects from a real query. (co-08, co-10, co-13, co-23)
- **ex-76 · wire-full-stack-write** — session + unit of work + builder on the write path — verify an atomic persist. (co-15, co-16, co-20)
- **ex-77 · typed-end-to-end** — run `pyright` over the whole hand-built stack — verify zero type errors. (co-25)
- **ex-78 · capstone-preview-mini-orm** — run the customers/orders scenario over the mini-ORM — verify the same result as topic 27's ORM tier. (co-13, co-20, co-22, co-24)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a working miniature ORM — query builder, mapper, identity map, unit of work, lazy
  loading — over the DB-API, and use it to run the same customers/orders scenario from topic 27,
  proving you can rebuild the abstraction you were using.
- **Concepts exercised**: [ ] a fluent query builder emitting parameterized SQL (co-01..co-08) [ ]
  table metadata + row→object mapping with type coercion (co-09..co-12) [ ] an identity map, weak-ref
  backed (co-13, co-14) [ ] a session transaction boundary + unit of work with a single-transaction
  atomic flush (co-15..co-20) [ ] descriptor-based lazy loading and the N+1 it causes (co-21, co-22)
  [ ] a schema migration runner (co-24) [ ] fully type-annotated Python end to end (co-23, co-25).
- **Ordered steps**:
  1. `.../learning/capstone/code/query_builder.py` — the builder. Verify a composed query produces the
     expected SQL string and bound parameters, with no interpolation.
  2. `.../mapper.py` + `.../identity_map.py` — mapping and the identity map. Verify loading the same
     primary key twice returns the identical object instance.
  3. `.../unit_of_work.py` — track and flush changes. Verify a session with mixed new/dirty/deleted
     objects commits in one transaction and rolls back atomically on error.
  4. `.../lazy.py` — a lazy relationship. Verify it loads on first access and demonstrate the N+1 it
     can cause.
- **Acceptance criteria**: the builder emits safe parameterized SQL; the identity map de-duplicates by
  key; the unit of work flushes atomically; lazy loading defers correctly and the N+1 is observable.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Patterns of Enterprise Application Architecture** — Martin Fowler et al. (2002). The design
  blueprint — Active Record, Data Mapper, Unit of Work, Identity Map, Query Object, Lazy Load — for
  implementing an ORM from scratch.

**Papers & articles**

- **SQLAlchemy** (chapter) — Michael Bayer, in _The Architecture of Open Source Applications, Volume
  II_ (2012). First-person account by SQLAlchemy's creator of how a production-grade Python ORM and
  query builder is actually architected. <https://aosabook.org/en/v2/sqlalchemy.html>
- **PEP 249 — Python Database API Specification v2.0** — Marc-André Lemburg (1999). The DB-API contract
  any hand-built ORM or query builder must sit on top of. <https://peps.python.org/pep-0249/>
- **OrmHate** — Martin Fowler (2012). Essential framing of what a hand-built ORM must solve, and why
  the problem is harder than it looks. <https://martinfowler.com/bliki/OrmHate.html>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Data depth — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Data depth — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 6 · Databases & data depth.

> _Content originated in the now-closed FS-SE plan (topic 28); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
