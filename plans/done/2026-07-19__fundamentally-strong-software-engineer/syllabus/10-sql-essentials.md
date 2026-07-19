# 10 · SQL Essentials (By Example, SQL + Python †)

**prd row**: Pass 1 · Core Foundations · By Example · SQL + Python † (SQLite) · Learn 110 / Drill
210 · Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: the **usable slice** — schema design + core queries + safe access from Python via SQLite,
all from the CLI. Window functions, CTEs, indexing strategy, and isolation levels are deferred to
[`26-advanced-sql-and-query-performance`](./26-advanced-sql-and-query-performance.md) (DD-11). SQLite is
public-domain (Tier-1, DD-21).

## Why this exists · the big idea

- **The problem before the solution**: application data outlives the process that made it and must be
  queried, related, and kept consistent — an in-memory structure cannot do that.
- **Keep-this-if-you-forget-everything**: declare _what_ result you want and let the engine decide _how_
  to get it; the relational model separates your intent from the storage machinery.
- **Big ideas touched**: `mechanism-vs-policy` — SQL is declarative policy (the result you want), the
  query planner is the mechanism (how it is fetched); normalization keeps one fact in one place.

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./04-just-enough-python.md) (Python drives DB access).
- **Tools & environment**: a macOS/Linux terminal; **SQLite** (`sqlite3 --version`, bundled with Python's
  `sqlite3` module); **Python 3.x** with `pytest` in a `venv`. `psql`/PostgreSQL only for the
  cross-reference note (not required).
- **Assumed knowledge**: reading/writing basic Python; no prior SQL or database background required.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: current SQLite **3.53.3** (2026-06-26); **public-domain** (no license needed).
  Python `sqlite3` parameterized queries support `?` (qmark, sequence param) and `:name` (named, dict
  param) — both current. Note the SQLite version bundled with a given Python build varies; phrase the
  topic to read `sqlite3.sqlite_version` at runtime rather than asserting a fixed bundled version.
  (sqlite.org / docs.python.org)
- 2026-07-14 — re-verified: no drift since 2026-07-12. SQLite remains **3.53.3** (2026-06-26, still
  latest per sqlite.org/changes.html) and public-domain (sqlite.org/copyright.html). Python `sqlite3`
  API surface (`connect`/`cursor`/`execute`/`commit`/`close`, `?`/`:name` placeholders, `with conn:`
  auto-commit/rollback, `sqlite3.Row`, `executemany`, `sqlite3.sqlite_version`) unchanged, no
  deprecations (docs.python.org/3/library/sqlite3.html). UPSERT, foreign-key pragma/CASCADE/RESTRICT,
  SAVEPOINT/ROLLBACK TO, PRAGMA user_version/integrity_check/foreign_key_check, and CLI dot-commands
  (`.tables`/`.schema`/`.mode`/`.output`) all confirmed unchanged against sqlite.org primary docs.

### DD-35 primary-source citations (fetched-and-read)

> A `web-researcher` re-grounding sweep on 2026-07-12 fetched and read the primary sources below and
> verified every concrete, checkable claim in this topic against them. SQLite claims trace to
> **sqlite.org** official docs; Python DB-API claims to **docs.python.org**; dialect-agnostic SQL
> semantics (JOIN/GROUP BY/HAVING/NULL/COALESCE) to **postgresql.org** current docs (standard
> relational-algebra behavior shared with SQLite); the relational-model citation to the **ACM** record
> of Codd 1970. No factual errors were found in the technical body; two internal fixes were applied
> (prd-row Learn/Drill IDs `108/208`→`110/210` to match [`prd.md`](../prd.md), a copy-paste artifact
> from topic 8; and ex-45's normal-form label tightened to 1NF).

- **SQLite version + license** (Accuracy note) — current **3.53.3** (2026-06-26); **public domain**.
  Sources: [SQLite release 3.53.3](https://sqlite.org/releaselog/3_53_3.html),
  [SQLite Copyright](https://www.sqlite.org/copyright.html).
- **`INTEGER PRIMARY KEY` aliases `rowid`, auto-assigns on insert** (co-02) — verbatim from
  [CREATE TABLE](https://www.sqlite.org/lang_createtable.html): a single-column `INTEGER` primary key
  "becomes an alias for the rowid"; a NULL insert into it makes the engine "choose an integer value…
  automatically".
- **Type affinity — TEXT/NUMERIC/INTEGER/REAL/BLOB** (co-06) —
  [Datatypes In SQLite](https://sqlite.org/datatype3.html).
- **Foreign keys off by default; `PRAGMA foreign_keys=ON`; `ON DELETE CASCADE`/`RESTRICT`** (co-03,
  ex-66/67) — [SQLite Foreign Key Support](https://www.sqlite.org/foreignkeys.html): "Foreign key
  constraints are disabled by default"; CASCADE "propagates the delete… to each dependent child key",
  RESTRICT prohibits deleting a parent with existing children.
- **Inner vs left-outer join semantics** (co-13/14, ex-28/31) —
  [PostgreSQL Tutorial · Joins](https://www.postgresql.org/docs/current/tutorial-join.html): the left
  table's rows appear "at least once"; unmatched right columns are substituted with NULL.
- **`WHERE` (pre-aggregate) vs `HAVING` (post-aggregate)** (co-16, ex-38/39) —
  [PostgreSQL Tutorial · Aggregate Functions](https://www.postgresql.org/docs/current/tutorial-agg.html).
- **NULL three-valued logic; `= NULL` never matches; use `IS NULL`** (co-17, ex-41/43) —
  [PostgreSQL · Comparison Operators](https://www.postgresql.org/docs/current/functions-comparison.html):
  "`7 = NULL` yields null… Do not write `expression = NULL`."
- **`COALESCE` returns first non-NULL** (co-17, ex-42) —
  [PostgreSQL · Conditional Expressions](https://www.postgresql.org/docs/current/functions-conditional.html).
- **`count(*)` counts rows; `count(col)` excludes NULLs** (ex-40); **`group_concat(X, sep)`** (ex-70) —
  [SQLite · Built-in Aggregate Functions](https://sqlite.org/lang_aggfunc.html).
- **`SAVEPOINT`/`ROLLBACK TO` — partial undo, transaction stays open** (co-18, ex-68) —
  [SQLite SAVEPOINT](https://sqlite.org/lang_savepoint.html): "ROLLBACK TO… does not cancel the
  transaction."
- **Python `sqlite3` — `connect/cursor/execute/commit/close`; `?` qmark + `:name` named placeholders;
  `with conn:` auto-commit/rollback; `sqlite3.Row` name access** (co-19/20/21, ex-50/53) —
  [sqlite3 module docs](https://docs.python.org/3/library/sqlite3.html) (Placeholders, Connection
  context manager, Row objects sections).
- **`INSERT … ON CONFLICT(col) DO UPDATE SET` upsert** (co-10/11, ex-55) —
  [SQLite UPSERT](https://www.sqlite.org/lang_upsert.html) (added 3.24.0, 2018 — well before the pin).
- **`ALTER TABLE ADD COLUMN … DEFAULT`; `PRAGMA user_version` migration tracking;
  `PRAGMA integrity_check` + `PRAGMA foreign_key_check`; CLI dot-commands `.tables/.schema/.mode/.output`**
  (co-22/24, ex-59/61/75/76) — [ALTER TABLE](https://www.sqlite.org/lang_altertable.html),
  [Pragma statements](https://www.sqlite.org/pragma.html) (integrity_check "does not find FOREIGN KEY
  errors; use PRAGMA foreign_key_check"), [SQLite CLI](https://www.sqlite.org/cli.html).
- **Normalization 1NF/2NF/3NF definitions** (co-05) — cross-checked against the Read-more books
  (Silberschatz/Korth/Sudarshan 7th ed. 2019; C.J. Date 3rd ed. 2015) and textbook consensus; ex-45
  fixed to label the repeating-group split as **1NF** specifically (2NF concerns partial dependency on
  a composite key, not demonstrated by the split alone).
- **Read-more citations verified** — [Database System Concepts 7th ed.](https://www.db-book.com/)
  (ISBN 9780078022159);
  [SQL and Relational Theory 3rd ed.](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/);
  [Joe Celko's SQL for Smarties 5th ed.](https://shop.elsevier.com/books/joe-celkos-sql-for-smarties/celko/978-0-12-800761-7)
  (Celko co-wrote SQL-89/92 per ANSI X3H2); Codd 1970 "A relational model of data for large shared data
  banks", _CACM_ 13(6):377–387, [DOI 10.1145/362384.362685](https://dl.acm.org/doi/10.1145/362384.362685).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By Example band). Each example below cites the co-NN it exercises. -->

- **co-01 · relational-model** — Data is modeled as tables (relations) of rows and typed columns; every
  fact lives in exactly one place, related by key values rather than in-memory pointers.
- **co-02 · primary-keys** — A primary key uniquely identifies each row; `INTEGER PRIMARY KEY` aliases
  SQLite's `rowid` and auto-assigns on insert.
- **co-03 · foreign-keys** — A foreign key constrains a column to reference an existing primary key, and
  (with `PRAGMA foreign_keys=ON`) rejects orphans and drives `ON DELETE` actions.
- **co-04 · constraints** — `NOT NULL`, `UNIQUE`, `CHECK`, and `DEFAULT` declare invariants the engine
  enforces on every write.
- **co-05 · normalization** — Splitting repeating groups and transitive dependencies into separate tables
  (1NF→2NF→3NF) keeps one fact in one place and prevents update anomalies.
- **co-06 · column-types** — SQLite uses type affinity (INTEGER/TEXT/REAL/BLOB/NUMERIC), so declared types
  guide but do not rigidly enforce storage class; `typeof()` reveals the actual class.
- **co-07 · ddl-create-table** — `CREATE TABLE` defines a relation's columns, types, and constraints;
  `.schema` shows the stored definition.
- **co-08 · select-projection-filtering** — `SELECT` chooses columns (projection) and `WHERE` chooses rows
  (selection) using comparison, `AND`/`OR`, `LIKE`, `IN`, `CASE`, and subqueries.
- **co-09 · ordering-and-limiting** — `ORDER BY` sorts the result and `LIMIT`/`OFFSET` slice it for paging.
- **co-10 · insert** — `INSERT` adds one or many rows; an `ON CONFLICT` clause turns it into an upsert.
- **co-11 · update** — `UPDATE ... SET ... WHERE` mutates matching rows; an absent `WHERE` touches every row.
- **co-12 · delete** — `DELETE ... WHERE` removes matching rows.
- **co-13 · inner-join** — An inner join returns only rows with matches on the join key across tables — the
  workhorse for recombining normalized data (including self-joins).
- **co-14 · outer-join** — A `LEFT JOIN` keeps every left row, filling unmatched right columns with NULL,
  enabling anti-joins and "missing rows" reports.
- **co-15 · aggregation** — `GROUP BY` collapses rows into groups summarized by
  `COUNT`/`SUM`/`AVG`/`MIN`/`MAX`/`GROUP_CONCAT`.
- **co-16 · having-filter** — `HAVING` filters groups after aggregation, unlike `WHERE` which filters rows
  before it.
- **co-17 · null-semantics** — NULL means "unknown", so comparisons yield three-valued logic; test with
  `IS NULL`/`IS NOT NULL` and substitute with `COALESCE`.
- **co-18 · transactions** — A transaction (`BEGIN`/`COMMIT`/`ROLLBACK`, savepoints) makes a group of
  writes atomic — all apply or none do.
- **co-19 · python-sqlite3-connection** — Python's `sqlite3.connect` opens a connection; `.cursor()` /
  `.execute()` run SQL and `.commit()` / `.close()` finalize it.
- **co-20 · parameterized-queries** — Passing values as `?` (qmark) or `:name` (named) placeholders — never
  string interpolation — neutralizes SQL injection.
- **co-21 · cursor-and-results** — A cursor iterates results via `fetchone`/`fetchall`/`executemany`;
  `row_factory = sqlite3.Row` gives column-name access.
- **co-22 · schema-migration** — An additive migration (`ALTER TABLE ADD COLUMN` with a default, tracked by
  `PRAGMA user_version`) evolves a live schema without breaking existing rows.
- **co-23 · n-plus-1-avoidance** — Replacing a per-row query loop with a single join or a batched
  `IN (...)` fetch collapses N+1 round-trips into one.
- **co-24 · cli-usage** — The `sqlite3` CLI drives a database with dot-commands (`.tables`, `.schema`,
  `.mode`, `.output`, `< file.sql`) and `PRAGMA` checks — no GUI.

## Worked examples

Colocated under `sql-essentials/learning/code/`; `.sql` scripts run via `sqlite3` and Python access
scripts run via `python3` with static type hints (DD-20/DD-30/DD-34/DD-39). Each cites the `co-NN` it exercises.
Contiguous `ex-01..ex-80`.

### Beginner

- **ex-01 · create-author-table** — `CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL)`, then
  `.schema author` — verify the stored definition lists the column and PK. (co-07, co-02, co-01)
- **ex-02 · open-database-cli** — open a fresh DB with `sqlite3 app.db` and run `.tables` — verify the
  prompt opens and lists no tables yet. (co-24)
- **ex-03 · insert-single-row** — `INSERT INTO author(name) VALUES('Ada')`, then `SELECT * FROM author` —
  verify exactly one row returns. (co-10)
- **ex-04 · insert-multiple-rows** — one multi-row `INSERT ... VALUES (...),(...),(...)` — verify
  `SELECT count(*)` returns 3. (co-10)
- **ex-05 · select-all-columns** — `SELECT * FROM book` — verify every column and row of the relation is
  returned. (co-08, co-01)
- **ex-06 · select-projection** — `SELECT title FROM book` — verify only the `title` column appears.
  (co-08)
- **ex-07 · where-equality** — `SELECT * FROM book WHERE id = 1` — verify a single matching row. (co-08)
- **ex-08 · where-comparison** — `SELECT * FROM book WHERE price > 10` — verify only rows above the
  threshold. (co-08)
- **ex-09 · where-and-or** — `WHERE price > 10 AND author_id = 1` — verify combined boolean filtering.
  (co-08)
- **ex-10 · where-like-prefix** — `WHERE title LIKE 'The %'` — verify prefix pattern matches. (co-08)
- **ex-11 · where-in-set** — `WHERE id IN (1, 3, 5)` — verify set-membership filtering. (co-08)
- **ex-12 · order-by-ascending** — `SELECT * FROM book ORDER BY title ASC` — verify alphabetical ordering.
  (co-09)
- **ex-13 · order-by-descending** — `ORDER BY price DESC` — verify most-expensive-first ordering. (co-09)
- **ex-14 · limit-rows** — `SELECT * FROM book LIMIT 2` — verify at most two rows return. (co-09)
- **ex-15 · limit-offset-paging** — `LIMIT 2 OFFSET 2` — verify the second page of two rows. (co-09)
- **ex-16 · select-distinct** — `SELECT DISTINCT author_id FROM book` — verify duplicate values collapse.
  (co-08)
- **ex-17 · type-affinity** — insert `'42'` into an INTEGER column and check `typeof(col)` — verify SQLite
  stores it as integer per affinity. (co-06)
- **ex-18 · not-null-constraint** — attempt `INSERT INTO author(name) VALUES(NULL)` — verify a `NOT NULL`
  constraint error. (co-04)
- **ex-19 · unique-constraint** — insert a duplicate into a `UNIQUE` column — verify a UNIQUE constraint
  error. (co-04)
- **ex-20 · default-value** — a column declared `DEFAULT 'active'`; insert omitting it — verify the default
  is applied. (co-04)
- **ex-21 · check-constraint** — `CHECK(price >= 0)`; insert a negative price — verify the row is rejected.
  (co-04)
- **ex-22 · autoincrement-rowid** — insert two rows without an id into `INTEGER PRIMARY KEY` — verify ids
  auto-assign 1, 2. (co-02)
- **ex-23 · update-one-row** — `UPDATE book SET price = 15 WHERE id = 1` — verify only that row changed.
  (co-11)
- **ex-24 · update-all-rows** — `UPDATE book SET in_stock = 1` (no `WHERE`) — verify every row changed.
  (co-11)
- **ex-25 · delete-row** — `DELETE FROM book WHERE id = 2` — verify the row is gone and count drops by one.
  (co-12)
- **ex-26 · declare-foreign-key** — `book.author_id INTEGER REFERENCES author(id)`; run `.schema book` —
  verify the FK clause appears. (co-03)
- **ex-27 · enforce-foreign-key** — `PRAGMA foreign_keys=ON`, then insert a book with a nonexistent
  `author_id` — verify the orphan is rejected. (co-03)
- **ex-28 · inner-join-two-tables** — `SELECT book.title, author.name FROM book JOIN author ON
book.author_id = author.id` — verify each book pairs with its author. (co-13)
- **ex-29 · python-connect-and-query** — `conn: sqlite3.Connection = sqlite3.connect('app.db')`, run a
  `SELECT`, `rows: list[tuple[int, str]] = cur.fetchall()` — verify the script prints the rows. (co-19, co-21)
- **ex-30 · python-parameterized-insert** — `cur.execute("INSERT INTO author(name) VALUES (?)", (name,))`
  with typed `name: str` — verify the value inserts without string interpolation. (co-20)

### Intermediate

- **ex-31 · left-join-unmatched** — `SELECT author.name, book.title FROM author LEFT JOIN book ON ...` —
  verify authors with no books appear with a NULL title. (co-14)
- **ex-32 · join-with-aliases** — alias tables (`FROM book b JOIN author a ON b.author_id = a.id`) — verify
  the aliased query returns the same result more readably. (co-13)
- **ex-33 · three-table-join** — join `book`, `author`, and `publisher` — verify combined columns across
  three relations. (co-13)
- **ex-34 · group-by-count** — `SELECT author_id, count(*) FROM book GROUP BY author_id` — verify per-author
  book counts. (co-15)
- **ex-35 · group-by-sum** — `SELECT author_id, sum(price) FROM book GROUP BY author_id` — verify per-group
  totals. (co-15)
- **ex-36 · group-by-avg** — `SELECT author_id, avg(price) FROM book GROUP BY author_id` — verify per-group
  averages. (co-15)
- **ex-37 · min-max-aggregate** — `SELECT min(price), max(price) FROM book` — verify the cheapest and
  dearest values. (co-15)
- **ex-38 · having-filter-groups** — `GROUP BY author_id HAVING count(*) > 1` — verify only authors with
  more than one book appear. (co-16)
- **ex-39 · where-plus-having** — `WHERE in_stock = 1 ... GROUP BY ... HAVING sum(price) > 20` — verify the
  row filter applies before, the group filter after, aggregation. (co-16, co-08)
- **ex-40 · count-star-vs-column** — compare `count(*)` with `count(nullable_col)` — verify the column count
  excludes NULLs. (co-15, co-17)
- **ex-41 · null-is-null** — `SELECT * FROM book WHERE published_year IS NULL` — verify rows with unknown
  year match. (co-17)
- **ex-42 · null-coalesce** — `SELECT coalesce(published_year, 0) FROM book` — verify NULLs are substituted
  with 0. (co-17)
- **ex-43 · null-three-valued** — `SELECT * FROM book WHERE published_year = NULL` — verify it returns no
  rows (never use `= NULL`). (co-17)
- **ex-44 · aggregate-over-join** — `... FROM author a JOIN book b ON ... GROUP BY a.name` — verify a
  per-author total computed across the join. (co-15, co-13)
- **ex-45 · normalize-repeating-group** — split a comma-list column into a child table — verify the 1NF
  form removes the repeating group (atomicity — 1NF specifically; 2NF concerns partial dependency on a
  composite key, not demonstrated by this split alone). (co-05)
- **ex-46 · normalize-transitive-dep** — extract a lookup table to remove a transitive dependency — verify
  the 3NF form holds one fact per place. (co-05)
- **ex-47 · python-named-params** — `cur.execute("... WHERE name = :name", {"name": name})` with typed dict
  — verify named binding. (co-20)
- **ex-48 · python-executemany** — `cur.executemany("INSERT ... VALUES (?)", rows)` with
  `rows: list[tuple[str]]` — verify bulk insert of all rows. (co-21, co-10)
- **ex-49 · python-fetchone-loop** — iterate with `while (row := cur.fetchone()) is not None` (typed) —
  verify streamed row-by-row consumption. (co-21)
- **ex-50 · python-row-factory** — set `conn.row_factory = sqlite3.Row`, access `row["name"]` — verify
  column-name access instead of positional. (co-21)
- **ex-51 · transaction-commit** — `conn.execute("BEGIN")`, insert, `conn.commit()` — verify the write
  persists in a new connection. (co-18)
- **ex-52 · transaction-rollback** — insert then `conn.rollback()` — verify the DB is unchanged. (co-18)
- **ex-53 · transaction-context-manager** — `with conn:` block that raises — verify the auto-rollback
  leaves no partial write. (co-18)
- **ex-54 · injection-safe-vs-unsafe** — contrast an f-string query with a `?`-parameterized one against
  input `"'; DROP TABLE book;--"` — verify only the parameterized form is safe. (co-20)
- **ex-55 · upsert-on-conflict** — `INSERT ... ON CONFLICT(id) DO UPDATE SET ...` — verify a second insert
  updates rather than errors. (co-10, co-11)
- **ex-56 · subquery-in-where** — `WHERE author_id IN (SELECT id FROM author WHERE country = 'UK')` —
  verify filtering by a subquery result. (co-08)
- **ex-57 · self-join** — join `employee` to itself on `manager_id` — verify each employee pairs with its
  manager. (co-13)
- **ex-58 · case-expression** — `SELECT title, CASE WHEN price > 20 THEN 'premium' ELSE 'standard' END` —
  verify the conditional derived column. (co-08)

### Advanced

- **ex-59 · migration-add-column** — `ALTER TABLE book ADD COLUMN edition INTEGER DEFAULT 1` — verify
  existing rows gain the default and remain valid. (co-22)
- **ex-60 · migration-backfill** — after adding a nullable column, `UPDATE` to backfill computed values —
  verify all rows populated. (co-22, co-11)
- **ex-61 · migration-version-tracking** — read/set `PRAGMA user_version` around a migration — verify the
  version bumps so migrations are idempotent. (co-22, co-24)
- **ex-62 · n-plus-1-demonstrated** — Python loop issuing one `SELECT` per parent, counting queries — verify
  N+1 round-trips occur. (co-23)
- **ex-63 · n-plus-1-fixed-join** — replace the loop with a single `JOIN` query — verify one query returns
  the same data. (co-23, co-13)
- **ex-64 · n-plus-1-fixed-in** — batch children with one `WHERE id IN (?, ?, ...)` fetch — verify a single
  round-trip. (co-23, co-20)
- **ex-65 · composite-primary-key** — `PRIMARY KEY(book_id, tag_id)` on a junction table — verify a
  duplicate pair is rejected. (co-02, co-05)
- **ex-66 · cascade-delete** — `REFERENCES author(id) ON DELETE CASCADE`; delete an author — verify its
  books are removed too. (co-03)
- **ex-67 · restrict-delete** — `ON DELETE RESTRICT`; delete a referenced author — verify the delete is
  blocked. (co-03)
- **ex-68 · savepoint-partial-rollback** — `SAVEPOINT sp` ... `ROLLBACK TO sp` inside a larger transaction
  — verify only the inner work is undone. (co-18)
- **ex-69 · python-report-function** — a typed `def report(conn: sqlite3.Connection) -> list[tuple[str,
int]]` running a `GROUP BY` — verify the returned rows match hand-computed expectations. (co-15, co-21)
- **ex-70 · group-concat** — `SELECT author_id, group_concat(title, '; ') FROM book GROUP BY author_id` —
  verify titles concatenate per group. (co-15)
- **ex-71 · anti-join-missing** — `LEFT JOIN ... WHERE right.id IS NULL` — verify authors with zero books
  are isolated. (co-14, co-17)
- **ex-72 · atomic-transfer** — a two-row debit/credit inside one transaction that rolls back on failure —
  verify all-or-nothing (no half-applied transfer). (co-18)
- **ex-73 · python-dal-module** — a typed data-access module wrapping parameterized CRUD, tested with
  `pytest` on a seeded fixture DB — verify the suite is green. (co-19, co-20)
- **ex-74 · seed-from-sql-file** — `sqlite3 app.db < seed.sql` — verify the seeded row count via a
  follow-up `SELECT count(*)`. (co-24, co-10)
- **ex-75 · export-query-to-csv** — `.mode csv` + `.output out.csv` then a `SELECT` — verify the CSV file
  contains the result rows. (co-24)
- **ex-76 · integrity-checks** — `PRAGMA integrity_check` and `PRAGMA foreign_key_check` — verify both
  report no problems. (co-24, co-03)
- **ex-77 · design-3nf-schema** — design a 3–4 table 3NF schema (author/book/publisher/tag) with PK/FK
  constraints — verify no transitive dependency remains. (co-05, co-07, co-01)
- **ex-78 · correlated-subquery** — `SELECT title, (SELECT count(*) FROM review r WHERE r.book_id =
book.id) FROM book` — verify a per-row computed count. (co-08)
- **ex-79 · report-join-group-having** — a single query joining, grouping, and `HAVING`-filtering an
  aggregate report — verify it matches expected values. (co-15, co-16, co-13)
- **ex-80 · pytest-rollback-integration** — a `pytest` case that forces a failing transaction and asserts
  the DB row count is unchanged — verify green. (co-18, co-19)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: design and populate a small normalized SQLite database (3–4 tables) and ship a Python data
  access layer with parameterized queries, a reporting aggregation, and a transaction that rolls back on
  error — runnable from the CLI end-to-end.
- **Concepts exercised**: [ ] 3NF schema with PK/FK constraints [ ] `CREATE TABLE` DDL [ ] joins +
  `GROUP BY`/`HAVING` report [ ] parameterized queries (no string interpolation) [ ] commit/rollback
  transaction [ ] a safe additive migration.
- **Ordered steps**:
  1. `.../learning/capstone/code/schema.sql` + `seed.sql` — apply via `sqlite3 app.db < schema.sql`.
     Verify `.tables` lists all tables with FKs.
  2. `dal.py` — parameterized CRUD + a `GROUP BY` report function. Verify `pytest` on a seeded fixture DB.
  3. A transaction that partially fails and rolls back. Verify the DB is unchanged after the failure.
  4. `migrate_add_column.sql` — an additive column with a default. Verify existing rows still valid.
- **Acceptance criteria**: `pytest` green; the report matches hand-computed expected values; the rollback
  leaves no partial write; no query uses string interpolation (injection-safe).
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Database System Concepts** — Silberschatz, Korth, Sudarshan (7th ed., 2019). Standard textbook on the relational model, SQL, and database system design.
- **SQL and Relational Theory** — C.J. Date (3rd ed., 2015). Rigorous treatment of the relational model underlying SQL, clarifying where SQL diverges from theory.
- **Joe Celko's SQL for Smarties: Advanced SQL Programming** — Joe Celko (5th ed., 2014). Classic advanced-technique reference from an SQL-89/92 standards co-author.

**Papers & articles**

- **"A Relational Model of Data for Large Shared Data Banks"** — E.F. Codd (1970, CACM). Foundational paper introducing the relational model. <https://dl.acm.org/doi/10.1145/362384.362685>

---

← Previous: [9 · Project Management](./09-project-management.md) · Next: [11 · Backend Essentials](./11-backend-essentials.md) →
