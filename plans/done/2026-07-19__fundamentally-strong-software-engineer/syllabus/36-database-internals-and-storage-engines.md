# 36 · Database Internals & Storage Engines (By Example, Python †)

**prd row**: Pass 3 · Build for the Real World · By Example · Python † · Learn 136 / Drill 236 · Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: what's under the database — B-tree versus LSM-tree storage engines, the write-ahead
log, the buffer pool, MVCC, and on-disk page layout. This explains the query-performance topic above
it (why an index is a B-tree, why writes are cheap in one engine and reads in another) and feeds the
build-your-own-database pass at [`91-build-your-own-database`](./91-build-your-own-database.md). `†`:
fully type-annotated Python examples (DD-39) that model the structures at small scale.

## Why this exists · the big idea

- **The problem before the solution**: treating the database as an opaque box means you can't explain
  why a workload is slow, why the same schema is fast on one engine and slow on another, or what
  actually happens on `COMMIT` — the abstraction hides exactly the costs you must reason about at
  scale.
- **Keep-this-if-you-forget-everything**: durability and performance come from the same few ideas — an
  append-only log for crash-safe writes, a page/buffer-pool cache for reads, and an index structure
  (B-tree or LSM) chosen to favor either reads or writes.
- **Big ideas touched**: `consistency-latency-throughput` (B-tree vs LSM is a read-latency-vs-write-
  throughput choice, and the WAL and buffer pool trade durability guarantees against latency),
  `layering-and-leaks` (the SQL abstraction leaks its storage engine — page size, index type, and MVCC
  version bloat all surface as performance you have to explain).

## Prerequisites

- **Prior topics**: [topic 10 SQL Essentials](./10-sql-essentials.md) and
  [topic 26 Advanced SQL & Query Performance](./26-advanced-sql-and-query-performance.md).
- **Tools & environment**: a macOS/Linux terminal; a local relational DB whose internals you can
  inspect (Postgres-style MVCC and/or an embedded B-tree/LSM store); a hex/page viewer; **Python 3.x**
  (fully type-annotated) to model the structures; Neovim/VSCode with the Python LSP (DD-17).
- **Assumed knowledge**: writing SQL and reading an `EXPLAIN` plan (topics 10, 26); how an index
  changes a query plan (topic 26); reading typed Python (topic 04).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28) and re-verified under the DD-35
> no-hallucination pass against primary sources (PostgreSQL/MySQL/SQLite/RocksDB docs + the founding papers).

- 2026-07-12 — verified: the internals taught here (B-tree and LSM-tree structure, write-ahead logging,
  buffer pool, MVCC, slotted-page layout) are long-settled, engine-independent concepts and correctly
  unpinned. The canonical WAL/recovery reference remains ARIES (1992) and the canonical LSM reference
  the O'Neil et al. paper (1996).
- 2026-07-12 — verified: specific engine defaults (page sizes, MVCC vacuum behavior, compaction
  strategy) vary by product and version — the file describes them as engine-dependent rather than
  asserting one product's numbers.
- 2026-07-12 — DD-35 primary-source pass (author fetched and read each cited page):
  - **Slotted page** — PostgreSQL 18 docs (storage-page-layout): 24-byte header, `ItemIdData` slot array
    grows from the front, tuple data grows from the back, free space between; a slot index is a stable
    long-term handle even after in-page compaction. Page size is engine-specific (**Postgres/SQL Server
    8 KB, InnoDB 16 KB**) — do not present 8 KB as universal.
  - **Buffer pool** — pin count + dirty bit per frame; a dirty page is flushed (or its WAL made durable)
    before its frame is reused. **CLOCK/second-chance** approximates LRU via a per-frame reference bit; it
    is an approximation, not exact LRU. **LRU-K** (O'Neil et al., SIGMOD 1993) is a distinct algorithm, not
    "LRU with K frames".
  - **B-tree vs B+-tree** — a B+-tree keeps values only in leaves with linked siblings for range scans;
    PostgreSQL's `nbtree` (Lehman & Yao) and InnoDB are B+-trees though their public API says "btree".
    SQLite `WITHOUT ROWID` tables are a genuine classical-B-tree counter-example.
  - **LSM** — memtable (RocksDB default = skiplist) → immutable sorted SSTables; read checks memtable then
    SSTables newest→oldest; compaction is **leveled** (RocksDB default) vs **size-tiered** (Cassandra). The
    amplification trade-off is the **RUM conjecture** (Read/Update/Memory — a _conjecture_, not a law).
  - **Bloom filter** — false positives possible, false **negatives impossible**; per-SSTable, skips files
    that definitely lack a key.
  - **WAL / ARIES** (Mohan et al. 1992) — log record durable _before_ the page (WAL rule); LSN + pageLSN;
    three phases **analysis → redo → undo**. ARIES **"repeats history"**: redo replays _all_ logged changes
    (committed or not), _then_ undo rolls back losers via Compensation Log Records — do not teach "redo skips
    uncommitted".
  - **MVCC** — row versions tagged `xmin`/`xmax` (PostgreSQL terms); a snapshot sees versions committed
    before it and not yet deleted; readers don't block writers. Dead versions need VACUUM/GC. PostgreSQL
    `REPEATABLE READ` **is snapshot isolation** and permits **write skew** (Berenson et al. 1995); true
    `SERIALIZABLE` (SSI, 9.1+) catches it.
  - **Durability** — a page write is **not atomic** across a crash (torn page); mitigations are PostgreSQL
    **full-page-writes** and InnoDB **doublewrite buffer**; `fsync` forces durability, **group commit**
    batches it. `[Needs Verification]` — InnoDB-specific checksum algorithm not fetched from a primary page.
  - **Clustered vs heap** — InnoDB clusters rows in the PK B+-tree leaf; PostgreSQL uses a heap with
    `ctid`(page, slot) row pointers; SQLite rowid tables cluster on rowid. **Row store** (OLTP) vs **column
    store** (OLAP: dictionary / run-length / delta encoding) — C-Store, Stonebraker et al. 2005.
  - `[Needs Verification]` — illustrative fanout/height figures (e.g. fanout 200–500 → height 3–4 for 1e9
    keys) are pedagogical, not vendor constants; teach as illustrative.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject topic). Each example below cites the co-NN it exercises. -->

- **co-01 · fixed-size-pages** — databases read, write, and cache in fixed-size pages (the unit of I/O); page size is engine-specific (Postgres 8 KB, InnoDB 16 KB).
- **co-02 · slotted-page-layout** — a page is a header + a slot array growing from the front + tuple data growing from the back, with free space between.
- **co-03 · variable-length-record-addressing** — records are addressed by slot index, not byte offset, so a tuple can move within a page (compaction) without invalidating references.
- **co-04 · buffer-pool** — an in-memory cache of hot pages; a page table maps page-id → frame, each frame carrying a pin count and a dirty bit.
- **co-05 · page-eviction-policies** — LRU, CLOCK/second-chance (a reference bit approximates LRU), and LRU-K choose a victim frame; a dirty victim is flushed (or WAL-durable) before reuse.
- **co-06 · read-path-buffer-hit-miss** — a read checks the buffer pool first; a miss loads the page from disk into a free or evicted frame.
- **co-07 · btree-vs-bplustree** — a B-tree stores values at every node; a B+-tree keeps values only in leaves with linked siblings; most SQL "btree" indexes (Postgres nbtree, InnoDB) are B+-trees.
- **co-08 · btree-search-and-fanout** — tree height ≈ log_fanout(N); high fanout makes a shallow tree so a lookup touches few pages.
- **co-09 · btree-insert-and-split** — a leaf overflow splits and promotes a separator key upward, keeping the tree balanced; splits can propagate to the root.
- **co-10 · btree-range-scan** — sibling-linked leaves let a range scan walk leaves in order without re-descending from the root.
- **co-11 · lsm-memtable-and-sstable** — writes buffer in an in-memory sorted memtable (skiplist), then flush to immutable sorted SSTables on disk.
- **co-12 · lsm-read-path** — a read checks the memtable, then SSTables newest→oldest; a newer version (or tombstone) shadows older ones.
- **co-13 · lsm-compaction** — SSTables are merged to reclaim space and bound read cost; leveled (RocksDB) vs size-tiered (Cassandra) are the two strategies.
- **co-14 · amplification-rum** — read/write/space amplification trade off against each other (the RUM conjecture); B-tree vs LSM is a bet on the workload, not a universal winner.
- **co-15 · bloom-filter** — a probabilistic per-SSTable membership filter with possible false positives but no false negatives, letting a read skip SSTables that definitely lack a key.
- **co-16 · write-ahead-log-rule** — a log record reaches stable storage before its page is written (the WAL invariant), making writes crash-safe.
- **co-17 · lsn-and-pagelsn** — monotonic log sequence numbers order the log; a page's pageLSN tells recovery whether a log record is already applied.
- **co-18 · aries-recovery-phases** — recovery runs analysis → redo (repeat history: replay all logged changes) → undo (roll back losers via compensation log records).
- **co-19 · redo-vs-undo** — redo re-applies changes so committed work survives; undo rolls back uncommitted work; the steal/no-force buffer policy is why both are needed.
- **co-20 · checkpointing** — periodic checkpoints bound how far back recovery must scan the log.
- **co-21 · mvcc-versions-xmin-xmax** — each row version carries creating/deleting transaction ids (xmin/xmax); an update writes a new version rather than overwriting.
- **co-22 · snapshot-read-non-blocking** — a snapshot sees versions committed before it and not yet deleted, so readers don't block writers and writers don't block readers.
- **co-23 · version-bloat-and-vacuum** — dead versions accumulate and must be garbage-collected (VACUUM) to reclaim space.
- **co-24 · isolation-levels-and-anomalies** — read-uncommitted/committed/repeatable-read/serializable map to dirty/non-repeatable/phantom reads; snapshot isolation still permits write skew.
- **co-25 · concurrency-control-2pl-occ** — two-phase locking (growing/shrinking; strict 2PL holds write locks to commit) and optimistic concurrency control (read/validate/write) are alternatives or complements to MVCC.
- **co-26 · durability-fsync-torn-page** — a page write is not atomic across a crash (torn page); fsync, group commit, and full-page-writes / doublewrite buffer make writes durable.
- **co-27 · clustered-vs-heap** — a clustered index stores the row in the B+-tree leaf (InnoDB PK, SQLite rowid); a heap stores rows separately with secondary indexes pointing via row-id/ctid (Postgres).
- **co-28 · column-vs-row-store** — a row store lays out tuples contiguously (OLTP); a column store lays out columns contiguously (OLAP), enabling scan pruning and compression (dictionary/RLE/delta).

## Tensions & trade-offs — when NOT to reach for this

- **B-tree vs LSM is a workload bet, not a winner**: LSM wins write-heavy/ingest workloads and
  compresses well but pays on reads and suffers unpredictable compaction stalls; B-trees win
  read-heavy/point-lookup workloads but amplify random writes. Choosing by fashion instead of by
  workload is the mistake.
- **Internals knowledge can be premature**: for most CRUD apps the engine's defaults are fine, and
  reaching for storage-engine tuning before a measured bottleneck is effort spent where it doesn't pay
  — go through topic 26's `EXPLAIN`-driven approach first.
- **When NOT to go deeper**: if you're neither operating the database at scale nor picking the engine,
  the leaky details (compaction tuning, vacuum, WAL sizing) are someone else's job — learn enough to
  reason, not to reinvent.

## Lineage — why it beat the alternative

- Early databases wrote updates in place and hoped a crash didn't strike mid-write; the write-ahead log
  (formalized by ARIES, 1992) made durability and recovery correct by logging intent before mutating
  pages, and it remains the backbone of relational engines. The B-tree ruled indexing for decades
  because disks favored its shallow, read-optimized structure; the LSM-tree (O'Neil et al., 1996) then
  won the write-heavy, internet-scale workloads behind Bigtable, Cassandra, and RocksDB by turning
  random writes into sequential ones. The through-line — a log for durability, a structure chosen for
  the read/write balance — is exactly what [`91-build-your-own-database`](./91-build-your-own-database.md)
  reconstructs, and it explains the query-performance behavior taught in
  [`26-advanced-sql-and-query-performance`](./26-advanced-sql-and-query-performance.md).

## Worked examples

Colocated under `database-internals-and-storage-engines/learning/code/` as runnable, fully
type-annotated Python (DD-20/DD-30/DD-34/DD-39) that models each internal at small scale. Contiguous
`ex-01..ex-80`. Every example cites the `co-NN` it exercises; every concept above is exercised by
≥ 1 example.

### Beginner

- **ex-01 · fixed-size-page-alloc** — allocate a 4 KB page as a `bytearray` — verify `len(page)` equals the page size constant. (co-01)
- **ex-02 · page-header-pack-unpack** — pack `pd_lower`/`pd_upper` into a page header with `struct` — verify unpack round-trips the values. (co-02)
- **ex-03 · slot-array-append** — append a `(offset, length)` slot to the front-growing slot array — verify slot count increments and `pd_lower` advances. (co-02)
- **ex-04 · insert-fixed-record** — insert a fixed-size record from the back of the page — verify `pd_upper` decreases by the record size. (co-02)
- **ex-05 · read-record-by-slot** — read a record via its slot index — verify the bytes equal what was inserted. (co-03)
- **ex-06 · free-space-guard** — compute free space `pd_upper - pd_lower` — verify insert raises when free space < record size. (co-02)
- **ex-07 · variable-length-records** — pack two variable-length strings addressed by slot — verify each reads back at its own length. (co-03)
- **ex-08 · in-page-compaction** — delete a middle record and compact tuple data — verify a surviving slot still resolves to correct bytes. (co-03)
- **ex-09 · page-checksum-detect** — compute a CRC over a page — verify flipping one byte changes the checksum. (co-26)
- **ex-10 · page-table-lookup** — map page-id → frame in a dict — verify a lookup returns the resident frame. (co-04)
- **ex-11 · buffer-fetch-miss** — fetch a non-resident page from a fake disk dict — verify the miss counter increments and the page loads. (co-06)
- **ex-12 · buffer-fetch-hit** — fetch a resident page — verify no disk read (hit counter increments). (co-06)
- **ex-13 · pin-count-guard** — pin a page then request eviction — verify a pinned page is never chosen as victim. (co-04)
- **ex-14 · dirty-flush-on-evict** — mark a page dirty and evict it — verify it is written to the fake disk before the frame is reused. (co-05)
- **ex-15 · lru-eviction** — evict under an LRU policy — verify the least-recently-used frame is chosen. (co-05)
- **ex-16 · clock-second-chance** — evict under CLOCK with a reference bit — verify a recently-referenced page survives one hand sweep. (co-05)
- **ex-17 · btree-leaf-sorted-insert** — insert keys into a leaf node — verify keys stay sorted after each insert. (co-07)
- **ex-18 · btree-point-lookup** — search a single-leaf tree — verify a present key is found and an absent key returns `None`. (co-08)
- **ex-19 · btree-height-fanout** — build a tree of fanout `f` over `N` keys — verify height equals `ceil(log_f(N))`. (co-08)
- **ex-20 · btree-leaf-split** — insert past leaf capacity — verify a split yields two leaves plus a promoted separator key. (co-09)
- **ex-21 · btree-range-scan** — link leaves and scan a key range — verify the scan returns contiguous sorted keys. (co-10)
- **ex-22 · bplus-values-in-leaves** — build a B+-tree — verify internal nodes carry keys only and values live in leaves. (co-07)
- **ex-23 · memtable-sorted-insert** — insert into a sorted memtable — verify iteration yields keys in sorted order. (co-11)
- **ex-24 · memtable-flush-to-sstable** — flush the memtable to an immutable segment — verify the segment is sorted and the memtable is cleared. (co-11)
- **ex-25 · lsm-read-newest-first** — read across memtable + segments newest→oldest — verify the newest write shadows older ones. (co-12)
- **ex-26 · lsm-tombstone-delete** — write a delete tombstone — verify a read after the tombstone returns not-found. (co-12)
- **ex-27 · bloom-filter-membership** — add keys to a bloom filter and query — verify a present key always reports positive. (co-15)
- **ex-28 · bloom-no-false-negative** — query every added key over many keys — verify none is ever reported absent. (co-15)

### Intermediate

- **ex-29 · append-only-log-replay** — append log records to a file and replay — verify records replay in append order. (co-16)
- **ex-30 · wal-before-page-guard** — refuse to flush a page whose log record isn't yet durable — verify the ordering guard raises. (co-16)
- **ex-31 · lsn-monotonic-assign** — assign LSNs to records — verify each new LSN is strictly greater than the previous. (co-17)
- **ex-32 · pagelsn-skip-applied** — compare a log record's LSN to a page's pageLSN during redo — verify an already-applied record is skipped. (co-17)
- **ex-33 · wal-redo-committed** — replay the log after a crash — verify committed writes are re-applied. (co-19)
- **ex-34 · wal-undo-uncommitted** — roll back the log after a crash — verify uncommitted writes are undone. (co-19)
- **ex-35 · checkpoint-bounds-replay** — write a checkpoint record then crash — verify redo scans only from the checkpoint forward. (co-20)
- **ex-36 · row-version-xmin-xmax** — tag a row version with xmin/xmax — verify an update sets xmax on the old version and xmin on the new. (co-21)
- **ex-37 · snapshot-visibility-rule** — apply snapshot visibility to versions — verify a snapshot before a commit cannot see that commit. (co-22)
- **ex-38 · update-creates-new-version** — update a row under MVCC — verify a new version is appended, not overwritten in place. (co-21)
- **ex-39 · readers-dont-block-writers** — run a snapshot read concurrent with a write — verify the reader completes without waiting on the writer's lock. (co-22)
- **ex-40 · dead-version-gc-vacuum** — mark then vacuum dead versions — verify reclaimed slots drop from the live set. (co-23)
- **ex-41 · lru-k-vs-lru** — compare LRU-K to plain LRU on a scan-then-hot access pattern — verify LRU-K keeps the hot page LRU evicts. (co-05)
- **ex-42 · buffer-pool-hit-ratio** — run a workload through the pool — verify computed hit ratio equals hits ÷ (hits + misses). (co-06)
- **ex-43 · btree-bulk-load** — bulk-load sorted keys bottom-up — verify the resulting tree answers the same lookups as insert-one-by-one. (co-08)
- **ex-44 · btree-internal-split-propagate** — force splits up to the root — verify tree height increases by one and the root has two children. (co-09)
- **ex-45 · btree-delete-underflow** — delete until a leaf underflows — verify a merge or borrow keeps the tree valid. (co-09)
- **ex-46 · clustered-index-leaf-holds-row** — store the full row in the B+-tree leaf — verify a PK lookup returns the row without a second fetch. (co-27)
- **ex-47 · heap-secondary-index-pointer** — index into a heap via a `(page, slot)` pointer — verify the secondary index resolves to the heap row. (co-27)
- **ex-48 · lsm-size-tiered-compaction** — compact same-size SSTables into one — verify the merged segment count drops and keys survive. (co-13)
- **ex-49 · lsm-leveled-compaction** — push an SSTable down a level merging overlaps — verify no key overlap remains within the level. (co-13)
- **ex-50 · write-amplification-count** — count bytes written across compactions — verify write amplification > 1 for an LSM ingest. (co-14)
- **ex-51 · read-amplification-count** — count SSTables touched for a point read — verify read amplification grows with segment count. (co-14)
- **ex-52 · space-amplification-measure** — measure live vs on-disk bytes before compaction — verify space amplification > 1 with stale versions present. (co-14)
- **ex-53 · bloom-reduces-read-amp** — add bloom filters to the read path — verify fewer SSTables are opened for absent keys. (co-15)
- **ex-54 · row-store-tuple-contiguous** — lay out rows tuple-by-tuple — verify one row's fields are byte-adjacent. (co-28)
- **ex-55 · column-store-column-contiguous** — lay out the same data column-by-column — verify one column's values are byte-adjacent. (co-28)
- **ex-56 · column-scan-fewer-bytes** — scan one column in each layout — verify the column store reads fewer bytes for a single-column aggregate. (co-28)

### Advanced

- **ex-57 · dictionary-encoding** — dictionary-encode a low-cardinality column — verify decode round-trips and encoded size is smaller. (co-28)
- **ex-58 · run-length-encoding** — RLE-encode a sorted/repetitive column — verify decode round-trips and runs collapse. (co-28)
- **ex-59 · delta-encoding-timestamps** — delta-encode a monotonic timestamp column — verify decode round-trips and deltas are small integers. (co-28)
- **ex-60 · fsync-simulated-durability** — model fsync as a durability barrier — verify data before the last fsync survives a simulated crash and data after does not. (co-26)
- **ex-61 · group-commit-batch-fsync** — batch N commits into one fsync — verify all N are durable after a single barrier. (co-26)
- **ex-62 · torn-page-simulation** — crash mid-page-write leaving half-old/half-new bytes — verify the torn page is detected by checksum. (co-26)
- **ex-63 · full-page-write-recovery** — log a full-page image on first write after checkpoint — verify a torn page is repaired from the log image. (co-26)
- **ex-64 · aries-analysis-phase** — scan the log from the checkpoint — verify the transaction table and dirty-page table are reconstructed. (co-18)
- **ex-65 · aries-redo-repeat-history** — redo all logged changes regardless of commit — verify pages reach their pre-crash state. (co-18)
- **ex-66 · aries-undo-with-clr** — undo loser transactions writing compensation records — verify a re-crash during undo resumes correctly. (co-18)
- **ex-67 · crash-recovery-end-to-end** — run analysis+redo+undo on a crashed log — verify committed data survives and uncommitted data is gone. (co-19)
- **ex-68 · two-phase-locking** — acquire in a growing phase, release in a shrinking phase — verify no lock is acquired after the first release. (co-25)
- **ex-69 · strict-2pl-no-cascade** — hold write locks to commit — verify no dirty read of an uncommitted write is possible (no cascading abort). (co-25)
- **ex-70 · occ-read-validate-write** — run optimistic read/validate/write — verify a conflicting concurrent commit fails validation and retries. (co-25)
- **ex-71 · deadlock-detection-waitfor** — build a wait-for graph — verify a cycle is detected and one transaction is chosen as victim. (co-25)
- **ex-72 · dirty-read-demo** — expose an uncommitted write under read-uncommitted — verify the anomaly appears, then vanishes under read-committed. (co-24)
- **ex-73 · non-repeatable-read-demo** — re-read a row across a concurrent commit — verify the value changes under read-committed and is stable under repeatable-read. (co-24)
- **ex-74 · phantom-read-demo** — re-run a range query across a concurrent insert — verify a phantom row appears under repeatable-read. (co-24)
- **ex-75 · write-skew-under-snapshot** — two transactions each read then write disjoint rows — verify snapshot isolation permits the skew. (co-24)
- **ex-76 · serializable-prevents-write-skew** — run the same pair under serializable — verify one transaction aborts, preventing the skew. (co-24)
- **ex-77 · btree-vs-lsm-write-throughput** — measure writes/sec on both engines under random inserts — verify the LSM sustains higher write throughput. (co-14)
- **ex-78 · btree-vs-lsm-read-latency** — measure point-read cost on both under a read-heavy load — verify the B-tree answers in fewer page reads. (co-14)
- **ex-79 · workload-picks-engine** — feed a write-heavy vs read-heavy workload to a chooser — verify it selects LSM then B-tree respectively. (co-14)
- **ex-80 · mini-storage-engine-integration** — wire pages + a B-tree index + a WAL + a snapshot read together — verify a keyed write survives a crash and a snapshot read stays consistent under a concurrent writer. (co-01, co-07, co-16, co-21)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: model the core of a storage engine — a paged B-tree or LSM index, a write-ahead log with
  recovery, and a snapshot read — proving you understand how a database achieves durability and how the
  index choice sets the read/write trade-off.
- **Concepts exercised**: [ ] a slotted-page layout (co-02, co-03) [ ] a B-tree or LSM index (co-07,
  co-11) [ ] a buffer-pool read path (co-04, co-06) [ ] a write-ahead log (co-16, co-17) [ ] crash
  recovery (redo/undo) (co-18, co-19) [ ] an MVCC snapshot read (co-21, co-22) [ ] fully
  type-annotated Python.
- **Ordered steps**:
  1. `.../learning/capstone/code/pages.py` — page pack/unpack + a buffer pool. Verify a record
     round-trips through a page and a hot page is served from the pool, not disk.
  2. `.../index.py` — a B-tree (or LSM) index over the pages. Verify point lookups and a range scan
     return correct results.
  3. `.../wal.py` — write-ahead logging with a simulated crash + restart. Verify committed writes
     survive the crash and uncommitted ones do not (redo/undo).
  4. `.../mvcc.py` — a snapshot read. Verify a reader sees a consistent snapshot while a concurrent
     writer proceeds.
- **Acceptance criteria**: pages round-trip; the index answers lookups and ranges; the WAL recovers
  committed data after a crash; the snapshot read stays consistent under a concurrent write.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Database Internals: A Deep Dive into How Distributed Data Systems Work** — Alex Petrov (2019). The
  modern canonical text on storage engines, B-trees, LSM-trees, and distributed consensus.
- **Designing Data-Intensive Applications** — Martin Kleppmann (2017). Covers storage-engine internals
  — indexing structures, WAL, replication — as a core part of its systems treatment.
- **Readings in Database Systems, 5th Edition (The Red Book)** — Peter Bailis, Joseph M. Hellerstein,
  Michael Stonebraker, eds. (2015). Free, curated collection of foundational and modern database-systems
  papers with expert commentary. <http://www.redbook.io/>

**Papers & articles**

- **The Log-Structured Merge-Tree (LSM-Tree)** — Patrick O'Neil, Edward Cheng, Dieter Gawlick,
  Elizabeth O'Neil (1996). The original paper defining the LSM-tree structure behind Bigtable,
  Cassandra, RocksDB, and LevelDB. <https://link.springer.com/article/10.1007/s002360050048>
- **ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks
  Using Write-Ahead Logging** — C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh, Peter Schwarz
  (1992). The canonical write-ahead-logging and recovery algorithm implemented by most production
  relational databases. <https://dl.acm.org/doi/10.1145/128765.128770>

---

← Previous: [35 · Graph Databases](./35-graph-databases.md) · Next: [37 · Data Engineering](./37-data-engineering.md) →
