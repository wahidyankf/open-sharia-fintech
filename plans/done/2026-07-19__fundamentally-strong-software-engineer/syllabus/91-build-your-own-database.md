# 91 · Build Your Own Database (By Example, Python †)

**prd row**: Pass 5 · Internals & Lead at Altitude · By Example · Python † · Learn 191 / Drill 291 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: demystify the database by rebuilding its core — a pager over a single file, a B-tree (or an
LSM alternative) for indexed storage, a write-ahead log for durability, a tiny SQL-ish query layer, and
crash recovery. This is the build-your-own tier of
[`36-database-internals-and-storage-engines`](./36-database-internals-and-storage-engines.md): that topic
explained B-trees, the WAL, the buffer pool, and MVCC; here you implement enough of them that a durable,
crash-safe key-value/table store stops being magic. `†`: Python, fully type-annotated (DD-39), verified
with `pytest`.

## Why this exists · the big idea

- **The problem before the solution**: "the database handles durability and consistency for you" is true
  and unhelpful until you have written the code that survives a crash mid-write — only then do the WAL,
  fsync, and page-at-a-time discipline stop being incantations and become mechanisms you can reason about.
- **Keep-this-if-you-forget-everything**: a database is a durable, ordered map built on three moves — put
  data in fixed-size pages, keep an index (B-tree/LSM) so lookups are logarithmic not linear, and write your
  intent to a log _before_ the data so a crash is recoverable. Everything else is optimization on top of
  those three.
- **Big ideas touched**: `consistency-latency-throughput` (the WAL/fsync boundary is exactly where you trade
  latency for durability, and page caching trades memory for throughput), `layering-and-leaks` (pager →
  B-tree → query layer is a clean stack, and the leaks — page splits, torn writes, recovery — are where the
  real learning is).

## Prerequisites

- **Prior topics**: [topic 36 Database Internals & Storage Engines](./36-database-internals-and-storage-engines.md)
  (B-tree vs LSM, the write-ahead log, buffer pool, MVCC — the concepts this topic makes concrete) and
  [topic 10 SQL Essentials](./10-sql-essentials.md) (the query surface you build a tiny version of).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** with type hints (pyright-clean spirit, DD-39);
  `pytest`; the standard library only for file I/O and `struct`-style packing (no external DB engine);
  Neovim/VSCode with the Python LSP (DD-17).
- **Assumed knowledge**: storage-engine concepts — pages, B-trees, the WAL, recovery (topic 36); SQL basics
  and what a query must do (topic 10); Python file/bytes handling and classes (topic 04).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the core structures — fixed-size pages behind a pager, B-tree (or LSM+SSTables)
  indexing, write-ahead logging with fsync at the durability boundary, and log-based crash recovery — are
  evergreen and correctly left version-unpinned. The design deliberately targets a single-file store with
  the standard library, so there is no third-party version to pin.
- 2026-07-12 — verified (SCOPE note for plan owner): full ACID with concurrent transactions (MVCC, locking)
  is a large stretch; the tractable target is single-writer durability + crash recovery, with MVCC/isolation
  named as the forward direction. Keep the query layer "SQL-ish" (a parsed subset), not a conformant SQL
  engine. (Petrov, _Database Internals_; cstack db_tutorial)

### DD-35 primary-source citations (fetched-and-read)

Every structure, algorithm, and scope claim below traces to a primary source fetched and read during
grounding. Unverifiable specifics are marked `[Needs Verification]` and never shipped as fact.

- **Pager + buffer pool** — fixed-size pages over a single file with a cache and eviction — is standard
  storage-engine architecture. Verified against Petrov, _Database Internals_ (2019) chs. 3–4 and CMU
  15-445 (Database Systems) buffer-pool lectures. (db.cs.cmu.edu/courses)
- **B-tree / B+tree** insert, search, and node splits (a split promotes a separator to the parent; a root
  split grows height) — verified against Petrov chs. 2–4; **SQLite** stores tables and indexes as B-trees.
  (sqlite.org/fileformat2.html)
- **LSM alternative** — memtable + on-disk **SSTables** + **compaction** — verified against Petrov ch. 7 and
  Kleppmann, _Designing Data-Intensive Applications_ (2017) ch. 3. (dataintensive.net)
- **Write-ahead logging** — log the intent **before** mutating pages, `fsync` at the commit boundary, replay
  on startup — is the WAL protocol; **ARIES** (Mohan et al., "ARIES: A Transaction Recovery Method…", ACM
  TODS 1992) is the canonical redo/undo + checkpoint recovery algorithm this topic simplifies. (dl.acm.org/doi/10.1145/128765.128770)
- **Scope (verified)** — single-writer durability + crash recovery is the tractable target; **MVCC/isolation
  and concurrent ACID** are named as the forward direction, not implemented. The query layer is a **parsed
  SQL-ish subset** (`insert`/`select`/`where`), not a conformant SQL engine.
- **Reference implementations** — cstack's _Let's Build a Simple Database_ (SQLite-like, C) and Petrov are the
  grounding tutorials. (cstack.github.io/db_tutorial)
- **Implementation** — Python **fully type-annotated** (DD-39), **standard library only** (file I/O +
  `struct`-style packing, no third-party DB engine), tested with **pytest** including a simulated mid-write crash.

## Concepts

<!-- co-01 · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject). Each example below cites the co-NN it exercises. -->

- **co-01 · pages** — data is stored in fixed-size pages, the unit of I/O.
- **co-02 · pager** — the pager reads and writes pages by number over a single file.
- **co-03 · page-cache** — a buffer pool caches hot pages in memory; dirty pages flush back.
- **co-04 · cache-eviction** — a full cache evicts a page (e.g. LRU) to make room.
- **co-05 · page-layout** — a page has a header and slotted rows/cells.
- **co-06 · btree-structure** — a B-tree/B+tree of internal and leaf nodes indexes keys.
- **co-07 · btree-search** — lookup walks the tree in logarithmic, not linear, time.
- **co-08 · btree-insert** — insertion places a key in the correct leaf.
- **co-09 · node-split** — a full node splits, promoting a separator; a root split grows height.
- **co-10 · btree-ordered** — an in-order traversal yields keys sorted, enabling range scans.
- **co-11 · lsm-alternative** — an LSM engine: a memtable flushed to SSTables, merged by compaction.
- **co-12 · sstable** — a sorted string table is an immutable, sorted on-disk run.
- **co-13 · compaction** — merging SSTables reclaims space and drops tombstoned keys.
- **co-14 · wal** — the write-ahead log records mutations as append-only records.
- **co-15 · fsync** — `fsync` at the commit boundary is where durability is actually purchased.
- **co-16 · intent-before-data** — logging intent before mutating pages is what makes a crash recoverable.
- **co-17 · crash-recovery** — on startup, replay committed WAL records and truncate incomplete ones.
- **co-18 · aries-intuition** — redo committed work, undo uncommitted work (the ARIES idea, simplified).
- **co-19 · checkpoint** — a checkpoint bounds how far back recovery must replay.
- **co-20 · torn-writes** — a partial page write must be detectable so recovery can repair it.
- **co-21 · durability-tradeoff** — the WAL/fsync boundary trades latency for durability.
- **co-22 · sql-parse** — parse a SQL-ish subset into an executable form.
- **co-23 · insert-exec** — execute an `insert`, writing a row into the store.
- **co-24 · select-exec** — execute a `select`, reading rows back.
- **co-25 · where-filter** — a `where` predicate filters the returned rows.
- **co-26 · row-serialization** — rows are packed to and unpacked from page bytes.
- **co-27 · transaction-single-writer** — a single-writer transaction boundary groups durable writes.
- **co-28 · mvcc-forward** — MVCC/isolation for concurrency is named as the forward direction.
- **co-29 · free-list** — freed pages are tracked and reused via a free list.
- **co-30 · pytest-durability** — `pytest` covers each stage, including a simulated crash.

## Worked examples

Colocated under `build-your-own-database/learning/code/`; Python (fully type-annotated, DD-39) + `pytest`
(DD-20/DD-30/DD-39). Durability is proven by killing the process mid-write and reopening. Contiguous `ex-01..ex-78`.
Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · define-page-size** — fix a 4096-byte page size — verify the constant is used everywhere. (co-01)
- **ex-02 · pager-open-file** — open a single database file for the pager — verify it opens/creates. (co-02)
- **ex-03 · pager-write-page** — write page `N` — verify bytes land at offset `N * page_size`. (co-02)
- **ex-04 · pager-read-page** — read page `N` — verify the bytes returned. (co-02)
- **ex-05 · page-roundtrip** — write then read a page — verify content survives. (co-02, co-01)
- **ex-06 · page-out-of-range** — read a page beyond EOF — verify a clean zero page / error, not a crash. (co-02)
- **ex-07 · page-header-layout** — encode a page header (type, cell count) — verify the fields. (co-05)
- **ex-08 · slotted-row** — store rows in slots within a page — verify slot offsets. (co-05)
- **ex-09 · page-cache-hit** — a cached page returns without disk I/O — verify no read occurs. (co-03)
- **ex-10 · page-cache-miss** — an uncached page loads from disk — verify it populates the cache. (co-03)
- **ex-11 · cache-lru-evict** — fill the cache then access — verify the LRU page is evicted. (co-04)
- **ex-12 · dirty-page-flush** — modify then flush a dirty page — verify it persists to disk. (co-03, co-02)
- **ex-13 · free-list-alloc** — allocate a page from the free list — verify a page number. (co-29)
- **ex-14 · free-list-reuse** — free then allocate — verify the freed page is reused. (co-29)
- **ex-15 · row-serialize** — pack a row to bytes — verify the byte layout. (co-26)
- **ex-16 · row-deserialize** — unpack a row from bytes — verify the fields. (co-26)
- **ex-17 · multiple-rows-page** — several rows in one page — verify all read back. (co-05, co-26)
- **ex-18 · page-full** — a full page rolls to a new page — verify overflow handling. (co-05)
- **ex-19 · pytest-pager** — a `pytest` over pager round-trip — verify it passes. (co-30)
- **ex-20 · pytest-cache-evict** — a `pytest` over eviction — verify it passes. (co-30, co-04)
- **ex-21 · typed-page-model** — a fully type-annotated page dataclass — verify `pyright`-clean typing. (co-05)
- **ex-22 · pager-file-header** — a db file header/magic on page 0 — verify it identifies the file. (co-05)
- **ex-23 · page-count-grow** — writing new pages grows the file — verify the page count. (co-02)
- **ex-24 · sync-to-disk** — flush all cached pages — verify data is on disk after. (co-15)
- **ex-25 · reopen-file** — reopen the file and read pages — verify data persists. (co-02)
- **ex-26 · pytest-row-serde** — a `pytest` over row serialize/deserialize — verify it passes. (co-30, co-26)

### Intermediate

- **ex-27 · btree-leaf-node** — a leaf node layout of key/value cells — verify the encoding. (co-06)
- **ex-28 · btree-internal-node** — an internal node of separators + children — verify the encoding. (co-06)
- **ex-29 · btree-insert-leaf** — insert a key into a leaf — verify it is placed in order. (co-08)
- **ex-30 · btree-search-key** — search an existing key — verify the value found. (co-07)
- **ex-31 · btree-search-missing** — search a missing key — verify a not-found result. (co-07)
- **ex-32 · btree-ordered-scan** — in-order scan the tree — verify keys come out sorted. (co-10)
- **ex-33 · leaf-split** — insert into a full leaf — verify it splits into two. (co-09)
- **ex-34 · internal-split** — force an internal-node split — verify the separator promotes. (co-09)
- **ex-35 · root-split-grow** — split the root — verify the tree height increases by one. (co-09, co-06)
- **ex-36 · btree-many-inserts** — insert enough keys to force many splits — verify order preserved. (co-08, co-10)
- **ex-37 · btree-over-pager** — store B-tree nodes as pager pages — verify nodes persist. (co-06, co-02)
- **ex-38 · btree-delete** — delete a key — verify it is gone and order holds. (co-08)
- **ex-39 · range-scan** — scan a `[lo, hi]` key range — verify only in-range keys return. (co-10)
- **ex-40 · memtable-insert** — insert into an LSM memtable — verify in-memory sorted order. (co-11)
- **ex-41 · memtable-flush-sstable** — flush the memtable to an SSTable — verify the on-disk run. (co-11, co-12)
- **ex-42 · sstable-read** — read a key from an SSTable — verify the value. (co-12)
- **ex-43 · sstable-sorted** — inspect an SSTable — verify entries are sorted. (co-12)
- **ex-44 · lsm-lookup-order** — look up across memtable + SSTables — verify newest value wins. (co-11)
- **ex-45 · compaction-merge** — merge two SSTables — verify the merged run is sorted + deduped. (co-13)
- **ex-46 · compaction-tombstone** — compact a delete tombstone — verify the key is dropped. (co-13)
- **ex-47 · lsm-vs-btree-writeup** — `tradeoffs.md` on write/read amplification — verify it cites both engines. (co-11, co-06)
- **ex-48 · bloom-filter-taste** — a bloom filter to skip an SSTable miss — verify it avoids a read. (co-12)
- **ex-49 · pytest-btree-splits** — a `pytest` over split correctness — verify it passes. (co-30, co-09)
- **ex-50 · pytest-lsm-compaction** — a `pytest` over compaction — verify it passes. (co-30, co-13)
- **ex-51 · btree-height-log** — measure height vs key count — verify it stays logarithmic. (co-07)
- **ex-52 · pager-btree-persist** — reopen and query a B-tree — verify it survives reopen. (co-06, co-02)

### Advanced

- **ex-53 · wal-append** — append a mutation record to the WAL — verify it is on disk. (co-14)
- **ex-54 · wal-record-format** — encode a WAL record (lsn, page, before/after) — verify the layout. (co-14)
- **ex-55 · wal-before-page** — write the WAL record before mutating the page — verify ordering. (co-16)
- **ex-56 · fsync-on-commit** — `fsync` the WAL at commit — verify the flush is forced. (co-15)
- **ex-57 · crash-mid-write-sim** — kill the process mid-write — verify a partial state on disk. (co-17, co-20)
- **ex-58 · recovery-replay** — replay committed WAL records on startup — verify state restored. (co-17)
- **ex-59 · recovery-truncate** — truncate an incomplete trailing record — verify a clean tail. (co-17)
- **ex-60 · recovery-consistent-state** — reopen after a crash — verify a consistent state. (co-17)
- **ex-61 · lose-uncommitted** — after recovery — verify only uncommitted work was lost. (co-17, co-27)
- **ex-62 · redo-recovery** — redo a committed-but-unflushed change — verify it reappears. (co-18)
- **ex-63 · undo-recovery** — undo an uncommitted change — verify it is rolled back. (co-18)
- **ex-64 · checkpoint-write** — write a checkpoint record — verify it marks a safe point. (co-19)
- **ex-65 · checkpoint-bounds-replay** — recover from a checkpoint — verify replay starts there, not at file start. (co-19)
- **ex-66 · torn-write-detection** — detect a partial page write — verify the torn page is caught. (co-20)
- **ex-67 · durability-latency-measure** — measure fsync-on vs fsync-off latency — verify the tradeoff is visible. (co-21, co-15)
- **ex-68 · single-writer-txn** — a `begin`/`commit` transaction boundary — verify grouped durability. (co-27)
- **ex-69 · sql-tokenize** — tokenize a SQL-ish statement — verify the token stream. (co-22)
- **ex-70 · sql-parse-insert** — parse `insert into t values (...)` — verify the parsed form. (co-22, co-23)
- **ex-71 · sql-parse-select** — parse `select ... from t where ...` — verify the parsed form. (co-22, co-24)
- **ex-72 · exec-insert** — execute an `insert` into the store — verify the row persists. (co-23, co-26)
- **ex-73 · exec-select-all** — execute `select *` — verify all rows return. (co-24)
- **ex-74 · where-equality** — `where col = v` — verify only matching rows. (co-25)
- **ex-75 · where-comparison** — `where col > v` — verify the comparison filter. (co-25)
- **ex-76 · full-crash-cycle** — write → crash → reopen → select — verify committed rows survive. (co-17, co-24, co-27)
- **ex-77 · pytest-recovery** — a `pytest` simulating crash recovery — verify it passes. (co-30, co-17)
- **ex-78 · capstone-mini-db** — the capstone: pager + B-tree + WAL + recovery + query — verify end-to-end + survives a simulated crash + green tests. (co-02, co-06, co-14, co-17, co-24)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a minimal but durable database — a pager with a page cache, a B-tree (or LSM) index, a
  write-ahead log with crash recovery, and a tiny SQL-ish query layer — such that it survives a process kill
  mid-write and reopens with a consistent state, fully covered by `pytest`.
- **Concepts exercised**: [ ] a pager + page cache over a single file (co-01, co-02, co-03, co-04) [ ] a
  B-tree (or LSM) index with splits (co-06, co-09, co-11) [ ] a write-ahead log with fsync (co-14, co-15,
  co-16) [ ] crash recovery on startup (co-17, co-18) [ ] a SQL-ish `insert`/`select`/`where` layer (co-22,
  co-23, co-24, co-25) [ ] durability under a simulated crash (co-20, co-27) [ ] `pytest` coverage of each
  stage (co-30).
- **Ordered steps**:
  1. `.../learning/capstone/code/pager.py` — fixed-size pages + a page cache over one file. Verify pages
     round-trip and eviction works (tests).
  2. `btree.py` — a B-tree with insert/search and node splitting on top of the pager. Verify ordered lookups
     stay correct across enough inserts to force splits (tests).
  3. `wal.py` + `recovery.py` — write-ahead logging with fsync and startup replay/truncate. Verify a process
     killed mid-write reopens to a consistent state, losing only uncommitted work (tests).
  4. `query.py` — parse and execute a SQL-ish `insert`/`select`/`where` subset against the store. Verify
     queries return correct rows and a full write → crash → reopen → select cycle is intact.
- **Acceptance criteria**: the pager/cache and B-tree behave under load; the WAL makes writes durable;
  recovery restores consistency after a mid-write kill; the query subset executes correctly; `pytest` covers
  each stage.
- **Done bar**: runnable end-to-end + survives a simulated crash + tests green + web-verified.

## Read more

**Books**

- **Database Internals** — Alex Petrov (2019). Canonical modern deep dive into storage engines (B-trees,
  LSM-trees) and distributed data systems — the blueprint for what you build here.
- **Designing Data-Intensive Applications** — Martin Kleppmann (2017). The field-defining book on the
  principles behind reliable, scalable data systems.

**Papers & articles**

- **Build Your Own Database From Scratch in Go** — James Smith. Widely cited incremental guide building a
  B+tree-based database; the key-value-store portion is free on the author's site (the full relational
  chapters are in the paid edition). <https://build-your-own.org/database/>
- **Let's Build a Simple Database** — cstack. Free, complete, widely referenced tutorial implementing a
  SQLite-like database from scratch in C. <https://cstack.github.io/db_tutorial/>
- **Architecture of a Database System** — Joseph M. Hellerstein, Michael Stonebraker, James Hamilton (2007).
  Highly cited survey of DBMS-internals architecture; free official PDF.
  <http://db.cs.berkeley.edu/papers/fntdb07-architecture.pdf>

---

← Previous: [90 · Build Your Own Git](./90-build-your-own-git.md) · Next: [92 · Build Your Own Raft / Replicated KV](./92-build-your-own-raft.md) →
