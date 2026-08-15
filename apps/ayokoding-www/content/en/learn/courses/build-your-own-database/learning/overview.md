---
title: "Learning Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Concepts

1. **co-01 · pages** — data is stored in fixed-size pages, the unit of I/O.
2. **co-02 · pager** — the pager reads and writes pages by number over a single file.
3. **co-03 · page-cache** — a buffer pool caches hot pages; dirty pages flush back.
4. **co-04 · cache-eviction** — a full cache evicts a page to make room.
5. **co-05 · page-layout** — a page has a header and slotted rows or cells.
6. **co-06 · btree-structure** — a B-tree or B+tree indexes keys.
7. **co-07 · btree-search** — lookup walks the tree in logarithmic time.
8. **co-08 · btree-insert** — insertion places a key in the correct leaf.
9. **co-09 · node-split** — a full node splits and promotes a separator.
10. **co-10 · btree-ordered** — an in-order traversal yields sorted keys.
11. **co-11 · lsm-alternative** — an LSM uses memtables, SSTables, and compaction.
12. **co-12 · sstable** — an SSTable is an immutable sorted on-disk run.
13. **co-13 · compaction** — merging SSTables reclaims space and drops tombstones.
14. **co-14 · wal** — the write-ahead log records append-only mutations.
15. **co-15 · fsync** — fsync at commit is the durability boundary.
16. **co-16 · intent-before-data** — log intent before mutating durable pages.
17. **co-17 · crash-recovery** — startup replays committed records and ignores incomplete ones.
18. **co-18 · aries-intuition** — redo committed work and undo uncommitted work.
19. **co-19 · checkpoint** — a checkpoint bounds recovery replay.
20. **co-20 · torn-writes** — partial writes must be detectable.
21. **co-21 · durability-tradeoff** — WAL/fsync trades latency for durability.
22. **co-22 · sql-parse** — parse a SQL-ish subset.
23. **co-23 · insert-exec** — execute an insert into the store.
24. **co-24 · select-exec** — execute a select from the store.
25. **co-25 · where-filter** — where predicates filter rows.
26. **co-26 · row-serialization** — rows pack to and unpack from bytes.
27. **co-27 · transaction-single-writer** — one writer groups durable writes.
28. **co-28 · mvcc-forward** — MVCC/isolation is a forward direction.
29. **co-29 · free-list** — freed pages are tracked and reused.
30. **co-30 · pytest-durability** — pytest covers stages including simulated crashes.

All 78 example labels are contiguous, and each maps to the listed concepts. The capstone deliberately remains a single-writer teaching store.
