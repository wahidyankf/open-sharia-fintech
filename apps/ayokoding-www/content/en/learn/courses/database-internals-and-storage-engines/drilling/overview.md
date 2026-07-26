---
title: "Overview"
date: 2026-07-27T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the Database Internals and Storage Engines topic:
five fixed drills that force active recall instead of passive re-reading. Work through them in
order -- short-answer recall first, then scenario judgment, then hands-on repetition, then a
checklist to confirm real automaticity, and finally why/why-not prompts that test whether you can
explain the reasoning, not just execute the syntax. Every answer is hidden in a `<details>` block;
try each item yourself before opening it. Together, the five drills below touch every one of this
topic's 28 concepts and cite specific examples spanning all 80 worked examples in the Beginner,
Intermediate, and Advanced tiers, plus the capstone.

## Recall Q&A

Twenty-eight short-answer questions, one per concept (`co-01` through `co-28`). Answer from memory,
then check.

**Q1 (co-01 -- Fixed-Size Pages).** Why do databases read, write, and cache in fixed-size pages
instead of arbitrary byte ranges?

<details>
<summary>Answer</summary>

Fixed-size pages give I/O a well-defined unit -- the buffer pool, the B-tree's fanout math, and a
checksum all assume the same fixed unit; without it, none of those mechanisms would have a stable
size to reason about. Page size is engine-specific (Postgres 8 KB, InnoDB 16 KB), not universal
(Example 1).

</details>

**Q2 (co-02 -- Slotted-Page Layout).** Describe a slotted page's three regions and which two grow
toward each other.

<details>
<summary>Answer</summary>

A header, a slot array growing forward from right after the header, and tuple data growing backward
from the end of the page, with free space between the slot array and the tuple data. The slot array
and tuple data are the two regions that grow toward each other; the page is full exactly when they
meet (Examples 2, 3, 4, 6).

</details>

**Q3 (co-03 -- Variable-Length-Record Addressing).** Why does addressing a record by slot index,
not byte offset, matter for in-page compaction?

<details>
<summary>Answer</summary>

A byte offset changes whenever a compaction moves a record, which would invalidate any external
reference that stored the old offset. A slot index stays stable across a compaction because only the
slot array's own entry gets rewritten to point at the record's new location -- external references
never need to change (Examples 5, 7, 8).

</details>

**Q4 (co-04 -- Buffer Pool).** What does a buffer pool's page table map, and what two pieces of
bookkeeping does each frame carry?

<details>
<summary>Answer</summary>

The page table maps page-id to frame. Each frame carries a pin count (how many callers currently
depend on this page staying resident) and a dirty bit (whether the page has been modified since it
was loaded) (Examples 10, 13).

</details>

**Q5 (co-05 -- Page Eviction Policies).** How does CLOCK/second-chance differ from true LRU, and what
does LRU-K specifically defeat that plain LRU cannot?

<details>
<summary>Answer</summary>

CLOCK approximates LRU cheaply via one reference bit per frame instead of maintaining a full recency
ordering. LRU-K tracks the last K references (not just the most recent one), which is what lets it
tell a genuinely hot page apart from a page touched only once during a sequential scan -- plain LRU
cannot make that distinction and will evict hot pages during a scan (Examples 15, 16, 41).

</details>

**Q6 (co-06 -- Read-Path Buffer Hit/Miss).** Why is "pool first, disk only on a miss" the single
invariant every later mechanism in this topic depends on?

<details>
<summary>Answer</summary>

Every metric (hit ratio) and every higher-level mechanism (the WAL's materialization path, an
index's page fetch) assumes reads genuinely check memory before disk -- if that ordering were
violated, a hit ratio would be meaningless and disk-read counts would not reflect real cache
behavior (Examples 11, 12, 42).

</details>

**Q7 (co-07 -- B-Tree vs B+-Tree).** What's the structural difference between a B-tree and a
B+-tree, and which do most SQL "btree" indexes actually implement?

<details>
<summary>Answer</summary>

A B-tree stores values at every node; a B+-tree keeps values only in leaves, with the leaves linked
as siblings. Most SQL "btree" indexes (Postgres nbtree, InnoDB) are actually B+-trees, even though
their public API calls them "btree" (Examples 17, 22).

</details>

**Q8 (co-08 -- B-Tree Search and Fanout).** Why does fanout, not key count, determine how many pages
a lookup touches?

<details>
<summary>Answer</summary>

Tree height is approximately `log_fanout(N)` -- a higher fanout means each level can route among more
children, so the tree stays shallow even as N grows into the billions. A fanout in the hundreds keeps
a B-tree only 3-4 levels deep at realistic scale, which is why B-trees are the default on-disk index
structure (Example 19).

</details>

**Q9 (co-09 -- B-Tree Insert and Split).** What happens when a leaf overflows, and how far can that
effect propagate?

<details>
<summary>Answer</summary>

An overflowing leaf splits in two and promotes a separator key upward into its parent; if the parent
also overflows from that promotion, the split propagates further up, potentially all the way to the
root -- which is exactly how a B-tree grows one level taller while staying balanced (Examples 20,
44).

</details>

**Q10 (co-10 -- B-Tree Range Scan).** What do sibling links between leaves save a range scan from
having to do?

<details>
<summary>Answer</summary>

Without sibling links, crossing from one leaf to the next during a range scan would require
re-descending from the root -- an `O(log N)` cost paid again for every leaf boundary. Sibling links
turn a multi-leaf range scan into one descent plus a cheap linear walk across linked leaves (Example
21).

</details>

**Q11 (co-11 -- LSM Memtable and SSTable).** Why does buffering writes in an in-memory memtable and
flushing to an immutable SSTable turn random writes into sequential ones?

<details>
<summary>Answer</summary>

Many individual writes accumulate in the sorted memtable first; when it's flushed, the ENTIRE
memtable becomes one large, already-sorted, sequential write to a new immutable SSTable -- the many
small random writes never individually touch disk (Examples 23, 24).

</details>

**Q12 (co-12 -- LSM Read Path).** Why must an LSM read check the memtable, then SSTables newest to
oldest, and stop at the first match?

<details>
<summary>Answer</summary>

Because SSTables are immutable, an update or delete cannot modify an old value in place -- it can
only add a newer entry (or a tombstone) that shadows the older one. Checking newest-to-oldest and
stopping at the first match is exactly what makes the newest write win (Examples 25, 26).

</details>

**Q13 (co-13 -- LSM Compaction).** Name the two compaction strategies this topic covers and one
production system that defaults to each.

<details>
<summary>Answer</summary>

Leveled compaction (RocksDB's default) favors read cost and space at the expense of more write
amplification; size-tiered compaction (Cassandra's default) favors write cost at the expense of more
space and slower reads. Neither is universally better -- it's a workload bet (Examples 48, 49).

</details>

**Q14 (co-14 -- Amplification and the RUM Conjecture).** What does the RUM conjecture claim, and why
does it make "B-tree or LSM" a genuine engineering decision rather than a solved problem?

<details>
<summary>Answer</summary>

The RUM conjecture claims no single design can simultaneously minimize read, write, and space
amplification all at once -- improving one tends to cost one of the others. That's precisely why
choosing between a B-tree and an LSM tree is a real trade-off decided by the actual workload, not a
question with one universally correct answer (Examples 50, 51, 52).

</details>

**Q15 (co-15 -- Bloom Filter).** Why is a Bloom filter's asymmetry (false positives possible, false
negatives impossible) exactly the property an LSM read path needs?

<details>
<summary>Answer</summary>

A false negative would mean a read incorrectly skips an SSTable that actually contains the key --
that would silently produce a wrong answer, which is unacceptable. A false positive only causes an
unnecessary (but safe) SSTable check. That asymmetry is what makes a Bloom filter safe to rely on for
reducing read amplification (Examples 27, 28, 53).

</details>

**Q16 (co-16 -- Write-Ahead-Log Rule).** State the WAL rule precisely, and explain what could go
wrong if a page could reach disk before its log record.

<details>
<summary>Answer</summary>

A log record must reach stable storage before the page it describes is written. If a page could
reach disk first and the system crashed in between, there would be no log record to explain what
that on-disk change even was, with no way to reconstruct or verify it during recovery (Examples 29,
30).

</details>

**Q17 (co-17 -- LSN and pageLSN).** What question does comparing a log record's LSN against a page's
stored pageLSN answer during recovery?

<details>
<summary>Answer</summary>

Whether that specific log record's change is already reflected on the page. If the record's LSN is
less than or equal to the page's pageLSN, the change is already applied and redoing it again would be
wrong (or at least redundant) -- this comparison is what makes redo idempotent (Examples 31, 32).

</details>

**Q18 (co-18 -- ARIES Recovery Phases).** Name ARIES's three recovery phases in order, and what
"repeats history" means for the redo phase specifically.

<details>
<summary>Answer</summary>

Analysis, then redo, then undo. "Repeats history" means redo replays EVERY logged change, whether its
transaction eventually committed or not -- it does not try to distinguish winners from losers during
redo. That deliberate choice avoids the much harder problem of deciding transaction outcomes before
the log has even been fully processed; undo, which runs after redo, is what removes the losers'
effects (Examples 64, 65, 66, 67).

</details>

**Q19 (co-19 -- Redo vs Undo).** Which buffer policy makes redo necessary, which makes undo
necessary, and why does a real engine typically need both?

<details>
<summary>Answer</summary>

A no-force policy (a committed page need not reach disk at commit time) makes redo necessary, since a
committed change might still only exist in the log after a crash. A steal policy (an uncommitted
page CAN be written to disk before commit, e.g. under memory pressure) makes undo necessary, since an
uncommitted change might already be on disk. Real engines use steal + no-force for buffer-pool
flexibility, which is exactly why both redo and undo are needed together (Examples 33, 34).

</details>

**Q20 (co-20 -- Checkpointing).** What does a checkpoint bound, and what would happen to recovery
time without one?

<details>
<summary>Answer</summary>

A checkpoint bounds how far back in the log recovery must scan -- it records a known-consistent
point, so recovery only replays log records written after it. Without checkpoints, every recovery
would need to scan the log all the way back to the database's very first write, making recovery time
grow unboundedly with the database's age (Example 35).

</details>

**Q21 (co-21 -- MVCC Versions -- xmin/xmax).** What does an update do under MVCC instead of
overwriting a row in place, and what do xmin and xmax each record?

<details>
<summary>Answer</summary>

An update appends a brand-new row version rather than modifying the old one. xmin records the
transaction id that created a version; xmax records the transaction id that deleted it (or stays
unset if the version is still live) -- together they let the engine reconstruct exactly which
versions existed at any point in time (Examples 36, 38).

</details>

**Q22 (co-22 -- Snapshot-Read Non-Blocking).** State the snapshot visibility rule, and explain why it
means readers and writers never block each other.

<details>
<summary>Answer</summary>

A snapshot sees every version committed before it, and not yet deleted as of that point. Because this
rule only reads facts already recorded on each version (who created it, who deleted it) -- it never
needs to acquire a lock on a concurrently-running writer, and a writer never needs to wait for a
reader either (Examples 37, 39).

</details>

**Q23 (co-23 -- Version Bloat and Vacuum).** Why does MVCC's "never overwrite" design create a
cleanup problem, and what solves it?

<details>
<summary>Answer</summary>

Every update leaves the old version behind; once no active snapshot can still see a given dead
version, it serves no purpose but still occupies space. VACUUM (or an equivalent garbage-collection
pass) is what reclaims that space by removing versions no live snapshot can ever reference again
(Example 40).

</details>

**Q24 (co-24 -- Isolation Levels and Anomalies).** Map each of the four standard isolation levels to
the anomaly it stops permitting, and name the one anomaly snapshot isolation still allows.

<details>
<summary>Answer</summary>

Read-uncommitted permits dirty reads; read-committed stops dirty reads but permits non-repeatable
reads; repeatable-read stops non-repeatable reads but (in the classical definition) permits phantom
reads; serializable stops all of the above. PostgreSQL's `REPEATABLE READ` is actually snapshot
isolation, and snapshot isolation still permits write skew even though it blocks the classical
phantom-read pattern -- only true serializable (SSI) catches write skew (Examples 72, 73, 74, 75).

</details>

**Q25 (co-25 -- Concurrency Control -- 2PL and OCC).** What bet does 2PL make about contention versus
what bet OCC makes, and what does strict 2PL add on top of plain 2PL?

<details>
<summary>Answer</summary>

2PL pays a locking cost upfront on every access, betting that conflicts are common enough to be worth
preventing early. OCC pays nothing until a commit-time validation check, betting that conflicts are
rare. Strict 2PL adds the rule that write locks are held until commit (not released as soon as the
growing phase's own last access happens), which is exactly what prevents cascading aborts that plain
2PL still permits (Examples 68, 69, 70, 71).

</details>

**Q26 (co-26 -- Durability -- fsync and Torn Pages).** Why is a page write not atomic across a crash,
and name the two named mitigations this topic covers.

<details>
<summary>Answer</summary>

A page write can be physically interrupted mid-write by a crash, leaving a "torn" page that is
neither the old version nor the fully-written new one. PostgreSQL's full-page-writes and InnoDB's
doublewrite buffer are both mitigations that let recovery repair a torn page rather than merely
detect that it happened; fsync is what forces a write to genuinely reach stable storage in the first
place, and group commit amortizes that fsync cost across many transactions (Examples 60, 61, 62, 63).

</details>

**Q27 (co-27 -- Clustered vs Heap).** What does clustering a table on its primary key make cheap, and
what does it make more expensive?

<details>
<summary>Answer</summary>

Clustering (InnoDB's PK, SQLite's rowid tables) makes a primary-key lookup essentially free -- the
row itself lives right in the B+-tree leaf, no extra indirection needed. It makes secondary-index
maintenance more expensive, since a page split can change where a row physically lives, and every
secondary index's pointer would need updating. A heap (PostgreSQL) decouples the two by storing rows
separately, with secondary indexes pointing via a stable row-id/ctid (Examples 46, 47).

</details>

**Q28 (co-28 -- Column vs Row Store).** Why does a column store's layout make dictionary,
run-length, and delta encoding effective in a way row storage never would?

<details>
<summary>Answer</summary>

A column store lays out one column's values contiguously, all the same type, often with repeated or
slowly-changing values (an OLAP pattern) -- that contiguity and homogeneity is exactly what
dictionary encoding (mapping repeated values to small integer codes), run-length encoding (collapsing
consecutive repeats), and delta encoding (storing differences between consecutive monotonic values)
all exploit. Interleaved with other columns' unrelated values, as a row store does, none of those
patterns would hold (Examples 54, 55, 56, 57, 58, 59).

</details>

## Applied problems

Thirteen scenarios. Each describes a task without naming the mechanism or trade-off -- decide which
one applies, then check.

**AP1.** A team is choosing a page size for a new storage engine and debating whether 4 KB is simply
"the correct" size industry-wide.

<details>
<summary>Answer</summary>

Page size is engine-specific, not universal (co-01) -- Postgres and SQL Server use 8 KB, InnoDB uses
16 KB. The "correct" answer is a design trade-off (I/O granularity vs. internal fragmentation), not a
fixed industry constant (Example 1).

</details>

**AP2.** A buffer pool serving an analytics workload runs a large one-time table scan every night,
and the team notices genuinely hot, frequently-reused pages get evicted during that scan under the
current eviction policy.

<details>
<summary>Answer</summary>

This is exactly what plain LRU mishandles and LRU-K is built for (co-05) -- a one-time sequential
scan touches every page exactly once, which looks "recently used" to plain LRU and evicts genuinely
hot pages in the process; LRU-K's multi-reference history correctly distinguishes the two access
patterns (Example 41).

</details>

**AP3.** A new index type is being designed, and the team is deciding whether internal (non-leaf)
nodes should store actual row values or only routing keys.

<details>
<summary>Answer</summary>

This is the B-tree-vs-B+-tree decision (co-07) -- keeping values only in leaves (a B+-tree) makes
internal nodes smaller and more cacheable, and the leaf-sibling links this enables are what make
range scans fast; most production SQL "btree" indexes make this choice (Examples 17, 22).

</details>

**AP4.** An application needs to fetch every row with a timestamp between two bounds, and the current
index implementation re-descends from the root for every leaf boundary it crosses.

<details>
<summary>Answer</summary>

Sibling-linked leaves (co-10) fix exactly this -- once the scan reaches the first matching leaf, it
walks forward via sibling links instead of re-descending, turning a multi-leaf range scan into one
descent plus a cheap linear walk (Example 21).

</details>

**AP5.** A write-heavy time-series ingestion service is bottlenecked on random-write I/O to its
current B-tree-backed store.

<details>
<summary>Answer</summary>

An LSM-tree (co-11) is the workload-appropriate alternative -- buffering writes in an in-memory
memtable and flushing sorted, immutable SSTables converts many small random writes into large
sequential ones, which is precisely what a write-heavy ingestion workload needs (Examples 23, 24).

</details>

**AP6.** An LSM-backed store's point-read latency is dominated by checking SSTables that turn out not
to contain the requested key at all.

<details>
<summary>Answer</summary>

A per-SSTable Bloom filter (co-15) directly addresses this -- its no-false-negatives guarantee lets a
read safely skip any SSTable the filter reports as definitely lacking the key, cutting read
amplification without any risk of missing a real match (Examples 27, 28, 53).

</details>

**AP7.** A database must guarantee that a committed transaction's data survives a power loss the
instant after the client receives a commit acknowledgment.

<details>
<summary>Answer</summary>

This is the WAL rule plus fsync as a durability barrier (co-16, co-26) -- the commit acknowledgment
must not be sent until the transaction's log record has genuinely reached stable storage via fsync,
which is the only guarantee that survives a crash occurring the instant after (Examples 29, 30, 60).

</details>

**AP8.** After a crash, a recovery process needs to decide which of a transaction's writes to keep
and which to discard, without knowing in advance which transactions had committed.

<details>
<summary>Answer</summary>

ARIES's redo-then-undo phases (co-18, co-19) solve exactly this -- redo first repeats history,
replaying every logged change regardless of commit status, deferring the committed/uncommitted
question entirely; undo then rolls back only the uncommitted (loser) transactions' effects, using
compensation log records (Examples 64, 65, 66, 67).

</details>

**AP9.** A reporting query needs a long-running read to see a perfectly consistent snapshot of the
database, without blocking any concurrent writers for the query's whole duration.

<details>
<summary>Answer</summary>

MVCC's snapshot read (co-21, co-22) is designed for exactly this -- the snapshot visibility rule
lets the reporting query see versions committed before its snapshot point without ever taking a lock
a concurrent writer would have to wait on (Examples 36, 37, 38, 39).

</details>

**AP10.** Two concurrent transactions, under an isolation level the team assumed was "basically
serializable," each individually read a value the other is about to update, and both commit --
producing a result no serial execution of the two transactions could have produced.

<details>
<summary>Answer</summary>

This is write skew under snapshot isolation (co-24) -- PostgreSQL's `REPEATABLE READ` is actually
snapshot isolation, which blocks the classical phantom-read pattern but does NOT block write skew;
only true serializable (SSI) detects the rw-antidependency cycle and aborts one of the two
transactions (Examples 75, 76).

</details>

**AP11.** A high-contention workload with many transactions competing for the same small set of hot
rows is experiencing frequent transaction restarts under its current concurrency-control scheme.

<details>
<summary>Answer</summary>

This points toward 2PL over OCC (co-25) -- OCC's read/validate/write cycle bets that conflicts are
rare and pays for that bet with restarts whenever a conflict IS detected at validation time; under
genuinely high contention, that bet loses often, and 2PL's upfront locking (which simply makes a
conflicting transaction wait, rather than restart) tends to perform better (Examples 68, 69, 70).

</details>

**AP12.** During a crash-injection test, a page is found to contain a mix of old and new bytes --
neither the fully-old nor the fully-new version.

<details>
<summary>Answer</summary>

This is a torn page (co-26) -- a page write is not atomic across a crash, and full-page-writes (or a
doublewrite buffer) are the mitigation that lets recovery detect and repair exactly this mixed state,
by restoring the page from a full pre-image logged before the write began (Examples 62, 63).

</details>

**AP13.** An OLAP system needs to run "average value of this one column across a billion rows" as
fast as possible, and the team is deciding between a row-oriented and a column-oriented physical
layout.

<details>
<summary>Answer</summary>

A column store (co-28) is the correct layout for this access pattern -- laying the target column's
values contiguously means the aggregate query reads only the bytes for that one column, skipping
every other column entirely, and the layout also enables dictionary/run-length/delta compression that
a row store's interleaved layout cannot exploit (Examples 54, 55, 56).

</details>

## Code katas

Eight hands-on repetition drills. Each is a before/after `.py` file colocated under `drilling/code/`.
Every "before" script is a real, runnable Python program that misapplies the concept being drilled --
run it yourself, diagnose the bug from the observed behavior, fix it from memory, then compare your
fix against the "after" script and the model solution before checking your work against the
actually-executed output shown.

### Kata 1 -- Slotted-Page Layout: forgetting to write back pd_lower silently overwrites an earlier slot

_relates to co-02, co-03, Examples 2-4_

**Task.** `insert_record()` should give every inserted record its own, permanent slot. The version
below is broken: it never writes the advanced `pd_lower` back into the header, so the SAME slot
offset gets reused (and overwritten) by the next insert.

**Before** (`drilling/code/kata-01-slotted-page-stale-pd-lower/before/kata.py`)

```python
"""Kata 1 (before): insert_record forgets to WRITE BACK the new pd_lower, so slot count never advances."""

from __future__ import annotations

import struct

PAGE_SIZE = 64
HEADER_FORMAT = ">HH"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


def new_page() -> bytearray:
    page = bytearray(PAGE_SIZE)
    struct.pack_into(HEADER_FORMAT, page, 0, HEADER_SIZE, PAGE_SIZE)
    return page


def insert_record(page: bytearray, record: bytes) -> int:
    pd_lower, pd_upper = struct.unpack_from(HEADER_FORMAT, page, 0)
    slot_count = (pd_lower - HEADER_SIZE) // 4
    new_pd_upper = pd_upper - len(record)
    # BUG: pd_lower's advance is never computed OR written back -- see the "after" fix below
    page[new_pd_upper:pd_upper] = record
    struct.pack_into(">HH", page, pd_lower, new_pd_upper, len(record))
    # BUG: never packs (new_pd_lower, new_pd_upper) back into the header -- pd_lower stays STALE
    return slot_count


def read_record(page: bytearray, slot: int) -> bytes:
    slot_offset = HEADER_SIZE + slot * 4
    record_offset, record_length = struct.unpack_from(">HH", page, slot_offset)
    return bytes(page[record_offset : record_offset + record_length])


page = new_page()
slot_a = insert_record(page, b"first")
slot_b = insert_record(page, b"second")  # pd_lower never advanced, so this OVERWRITES slot 0's slot entry
print(slot_a, slot_b)
print(read_record(page, slot_a))  # expected b"first" -- but slot 0's entry was overwritten by the 2nd insert
```

**Observed (buggy) output** (captured by actually running the script above):

```text
0 0
b'second'
```

**After** (`drilling/code/kata-01-slotted-page-stale-pd-lower/after/kata.py`)

```python
"""Kata 1 (after): insert_record writes the new pd_lower/pd_upper back into the header every time."""

from __future__ import annotations

import struct

PAGE_SIZE = 64
HEADER_FORMAT = ">HH"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


def new_page() -> bytearray:
    page = bytearray(PAGE_SIZE)
    struct.pack_into(HEADER_FORMAT, page, 0, HEADER_SIZE, PAGE_SIZE)
    return page


def insert_record(page: bytearray, record: bytes) -> int:
    pd_lower, pd_upper = struct.unpack_from(HEADER_FORMAT, page, 0)
    slot_count = (pd_lower - HEADER_SIZE) // 4
    new_pd_upper = pd_upper - len(record)
    new_pd_lower = pd_lower + 4
    page[new_pd_upper:pd_upper] = record
    struct.pack_into(">HH", page, pd_lower, new_pd_upper, len(record))
    struct.pack_into(HEADER_FORMAT, page, 0, new_pd_lower, new_pd_upper)  # => commits the new boundaries
    return slot_count


def read_record(page: bytearray, slot: int) -> bytes:
    slot_offset = HEADER_SIZE + slot * 4
    record_offset, record_length = struct.unpack_from(">HH", page, slot_offset)
    return bytes(page[record_offset : record_offset + record_length])


page = new_page()
slot_a = insert_record(page, b"first")
slot_b = insert_record(page, b"second")
print(slot_a, slot_b)
print(read_record(page, slot_a))
```

<details>
<summary>Model solution</summary>

**Root cause**: the header's `pd_lower` field is the ONLY thing that tracks how many slots already
exist -- if it's never written back after an insert, the next insert recomputes the exact same
`slot_count` and reuses the exact same slot offset, silently clobbering the previous record's slot
entry. Packing `(new_pd_lower, new_pd_upper)` back into the header is what makes the slot array
genuinely grow.

**Run**: `python3 kata.py`

**Output**:

```text
0 1
b'first'
```

</details>

### Kata 2 -- Buffer Pool: evicting the first frame found instead of an unpinned one corrupts a live page

_relates to co-04, co-05, Examples 10, 13, 14_

**Task.** `BufferPool._evict()` should never remove a frame a caller is still actively using. The
version below is broken: it evicts whatever frame happens to be first in the dict, completely
ignoring pin count.

**Before** (`drilling/code/kata-02-buffer-pool-evicts-pinned-frame/before/kata.py`)

```python
"""Kata 2 (before): eviction picks the FIRST frame regardless of pin count, evicting one still in use."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Frame:
    page: bytes
    pin_count: int = 0


@dataclass
class BufferPool:
    capacity: int
    frames: dict[int, Frame] = field(default_factory=dict[int, Frame])
    disk_reads: int = 0

    def get_page(self, page_id: int) -> bytes:
        frame = self.frames.get(page_id)
        if frame is not None:
            frame.pin_count += 1
            return frame.page
        self.disk_reads += 1
        if len(self.frames) >= self.capacity:
            self._evict()
        self.frames[page_id] = Frame(page=f"page-{page_id}".encode(), pin_count=1)
        return self.frames[page_id].page

    def _evict(self) -> None:
        victim = next(iter(self.frames))  # BUG: picks the first frame found, never checking pin_count
        del self.frames[victim]


pool = BufferPool(capacity=1)
pool.get_page(1)  # page 1 loaded and PINNED -- a caller still depends on it
pool.get_page(2)  # forces an eviction; the buggy policy evicts page 1 even though it is still pinned
print(1 in pool.frames)  # expected True -- page 1 was pinned and should never have been evicted
```

**Observed (buggy) output** (captured by actually running the script above):

```text
False
```

**After** (`drilling/code/kata-02-buffer-pool-evicts-pinned-frame/after/kata.py`)

```python
"""Kata 2 (after): eviction only ever considers a frame whose pin_count is genuinely zero."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Frame:
    page: bytes
    pin_count: int = 0


@dataclass
class BufferPool:
    capacity: int
    frames: dict[int, Frame] = field(default_factory=dict[int, Frame])
    disk_reads: int = 0

    def get_page(self, page_id: int) -> bytes:
        frame = self.frames.get(page_id)
        if frame is not None:
            frame.pin_count += 1
            return frame.page
        self.disk_reads += 1
        if len(self.frames) >= self.capacity:
            self._evict()
        self.frames[page_id] = Frame(page=f"page-{page_id}".encode(), pin_count=1)
        return self.frames[page_id].page

    def _evict(self) -> None:
        for page_id, frame in list(self.frames.items()):  # => scan for an UNPINNED frame specifically
            if frame.pin_count == 0:
                del self.frames[page_id]
                return
        raise RuntimeError("buffer pool full and every frame is pinned -- cannot evict")


pool = BufferPool(capacity=1)
pool.get_page(1)  # page 1 loaded and pinned
try:
    pool.get_page(2)  # no unpinned victim exists -- fails LOUDLY instead of silently evicting a pinned page
except RuntimeError as error:
    print(error)
print(1 in pool.frames)
```

<details>
<summary>Model solution</summary>

**Root cause**: `_evict()` never consulted `pin_count` at all -- it just removed whatever frame
happened to be first in dict-iteration order, which can (and did) include a frame a caller is
actively depending on. Scanning specifically for an UNPINNED frame, and failing loudly with a
`RuntimeError` when none exists, is what makes the pin count a real safety guarantee rather than
decorative bookkeeping.

**Run**: `python3 kata.py`

**Output**:

```text
buffer pool full and every frame is pinned -- cannot evict
True
```

</details>

### Kata 3 -- B-Tree Leaf Insert: appending instead of sorting breaks a range scan's ordering guarantee

_relates to co-09, co-10, Examples 17, 20, 21_

**Task.** A B-tree leaf's `range_scan()` should always return results in sorted key order. The
version below is broken: `insert()` always appends, so the leaf is never actually kept sorted.

**Before** (`drilling/code/kata-03-btree-leaf-insert-not-sorted/before/kata.py`)

```python
"""Kata 3 (before): a B-tree leaf insert appends instead of sorting, breaking range_scan's ordering."""

from __future__ import annotations


def insert(leaf: list[tuple[int, int]], key: int, page_id: int) -> None:
    leaf.append((key, page_id))  # BUG: always appends -- the leaf is never actually kept SORTED by key


def range_scan(leaf: list[tuple[int, int]], low: int, high: int) -> list[tuple[int, int]]:
    return [(k, p) for k, p in leaf if low <= k <= high]  # relies on `leaf` already being sorted


leaf: list[tuple[int, int]] = []
for key in [5, 1, 9, 3, 7]:  # inserted out of order
    insert(leaf, key, page_id=key * 10)
print(range_scan(leaf, 1, 7))
print(range_scan(leaf, 1, 7) == sorted(range_scan(leaf, 1, 7)))  # expected True -- a range scan MUST be sorted
```

**Observed (buggy) output** (captured by actually running the script above):

```text
[(5, 50), (1, 10), (3, 30), (7, 70)]
False
```

**After** (`drilling/code/kata-03-btree-leaf-insert-not-sorted/after/kata.py`)

```python
"""Kata 3 (after): insert uses bisect.insort, so the leaf stays sorted by key after every insert."""

from __future__ import annotations

import bisect


def insert(leaf: list[tuple[int, int]], key: int, page_id: int) -> None:
    bisect.insort(leaf, (key, page_id))  # => keeps `leaf` sorted by key on every single insert


def range_scan(leaf: list[tuple[int, int]], low: int, high: int) -> list[tuple[int, int]]:
    return [(k, p) for k, p in leaf if low <= k <= high]


leaf: list[tuple[int, int]] = []
for key in [5, 1, 9, 3, 7]:
    insert(leaf, key, page_id=key * 10)
print(range_scan(leaf, 1, 7))
print(range_scan(leaf, 1, 7) == sorted(range_scan(leaf, 1, 7)))
```

<details>
<summary>Model solution</summary>

**Root cause**: `range_scan()`'s correctness depends entirely on `leaf` already being sorted -- it
never sorts anything itself, it just filters in existing order. An `insert()` that always appends
gives no such guarantee, so a range scan over out-of-order data returns results in whatever order
they happened to be inserted. `bisect.insort` is what actually maintains the sorted invariant that
`range_scan` silently relies on.

**Run**: `python3 kata.py`

**Output**:

```text
[(1, 10), (3, 30), (5, 50), (7, 70)]
True
```

</details>

### Kata 4 -- LSM Read Path: scanning SSTables oldest-first returns a stale value

_relates to co-12, Examples 25, 26_

**Task.** `lsm_read()` should always return the NEWEST value for a key across all SSTables. The
version below is broken: it scans SSTables oldest-to-newest and returns the first match, which is
the OLDEST value, not the newest.

**Before** (`drilling/code/kata-04-lsm-read-path-oldest-first/before/kata.py`)

```python
"""Kata 4 (before): the LSM read path checks SSTables OLDEST-to-newest, returning a stale value."""

from __future__ import annotations


def lsm_read(sstables_oldest_to_newest: list[dict[str, str]], key: str) -> str | None:
    for table in sstables_oldest_to_newest:  # BUG: scans oldest-first, so an OLDER value wins over a newer one
        if key in table:
            return table[key]
    return None


# sstables[0] is the OLDEST flush, sstables[-1] is the NEWEST -- "y" was updated in the newest table
sstables = [{"y": "original-value"}, {"y": "updated-value"}]
print(lsm_read(sstables, "y"))
print(lsm_read(sstables, "y") == "updated-value")  # expected True -- the NEWEST write must win
```

**Observed (buggy) output** (captured by actually running the script above):

```text
original-value
False
```

**After** (`drilling/code/kata-04-lsm-read-path-oldest-first/after/kata.py`)

```python
"""Kata 4 (after): the LSM read path checks SSTables NEWEST-to-oldest, so the newest write wins."""

from __future__ import annotations


def lsm_read(sstables_oldest_to_newest: list[dict[str, str]], key: str) -> str | None:
    for table in reversed(sstables_oldest_to_newest):  # => co-12: newest-to-oldest -- the first match wins
        if key in table:
            return table[key]
    return None


sstables = [{"y": "original-value"}, {"y": "updated-value"}]
print(lsm_read(sstables, "y"))
print(lsm_read(sstables, "y") == "updated-value")
```

<details>
<summary>Model solution</summary>

**Root cause**: LSM SSTables are immutable, so a newer write to the same key lives in a NEWER
SSTable, never overwriting the old one in place -- scanning oldest-first means the read stops at the
stale value the very first time it finds any match at all, never reaching the newer, correct one.
Scanning `reversed()` (newest-first) is the one-line fix that makes "the newest write wins" actually
true.

**Run**: `python3 kata.py`

**Output**:

```text
updated-value
True
```

</details>

### Kata 5 -- Write-Ahead Log: commit() flips the flag but never materializes the write

_relates to co-16, co-19, Examples 29, 33, 34_

**Task.** A committed write should be immediately readable. The version below is broken: `commit()`
marks a log record as committed but never actually applies it into the readable table.

**Before** (`drilling/code/kata-05-wal-commit-without-materialize/before/kata.py`)

```python
"""Kata 5 (before): commit() flips the committed flag but never materializes the write into storage."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WalRecord:
    txn_id: int
    key: str
    value: str
    committed: bool = False


@dataclass
class Engine:
    log: list[WalRecord] = field(default_factory=list[WalRecord])
    table: dict[str, str] = field(default_factory=dict[str, str])

    def append(self, txn_id: int, key: str, value: str) -> None:
        self.log.append(WalRecord(txn_id=txn_id, key=key, value=value))

    def commit(self, txn_id: int) -> None:
        for record in self.log:
            if record.txn_id == txn_id:
                record.committed = True  # BUG: marks committed but never writes into self.table

    def read(self, key: str) -> str | None:
        return self.table.get(key)


engine = Engine()
engine.append(txn_id=1, key="a", value="v1")
engine.commit(txn_id=1)
print(engine.read("a"))  # expected "v1" -- a committed write should be immediately readable
```

**Observed (buggy) output** (captured by actually running the script above):

```text
None
```

**After** (`drilling/code/kata-05-wal-commit-without-materialize/after/kata.py`)

```python
"""Kata 5 (after): commit() flips the flag AND materializes the write into the table."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WalRecord:
    txn_id: int
    key: str
    value: str
    committed: bool = False


@dataclass
class Engine:
    log: list[WalRecord] = field(default_factory=list[WalRecord])
    table: dict[str, str] = field(default_factory=dict[str, str])

    def append(self, txn_id: int, key: str, value: str) -> None:
        self.log.append(WalRecord(txn_id=txn_id, key=key, value=value))

    def commit(self, txn_id: int) -> None:
        for record in self.log:
            if record.txn_id == txn_id:
                record.committed = True
                self.table[record.key] = record.value  # => co-16: commit both durably logs AND materializes

    def read(self, key: str) -> str | None:
        return self.table.get(key)


engine = Engine()
engine.append(txn_id=1, key="a", value="v1")
engine.commit(txn_id=1)
print(engine.read("a"))
```

<details>
<summary>Model solution</summary>

**Root cause**: durability (the log record persisting) and visibility (the write becoming readable)
are two DIFFERENT guarantees that commit() must provide together -- the buggy version only provided
durability, flipping a flag on the already-logged record, but never actually applied the value into
the table readers query. A real commit path both marks the record committed AND materializes it.

**Run**: `python3 kata.py`

**Output**:

```text
v1
```

</details>

### Kata 6 -- MVCC: deleting by popping the version list destroys history a snapshot still needs

_relates to co-21, co-22, Examples 36, 37, 38_

**Task.** A snapshot taken BEFORE a delete should still see the row as it existed at that time. The
version below is broken: `delete()` physically removes the version instead of tagging it with
`xmax`, so even an earlier snapshot loses access to it.

**Before** (`drilling/code/kata-06-mvcc-delete-forgets-xmax/before/kata.py`)

```python
"""Kata 6 (before): delete() removes the version from the LIST instead of setting xmax, breaking history."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RowVersion:
    value: str
    xmin: int
    xmax: int | None = None


@dataclass
class Table:
    versions: list[RowVersion] = field(default_factory=list[RowVersion])

    def write(self, value: str, txn_id: int) -> None:
        self.versions.append(RowVersion(value=value, xmin=txn_id))

    def delete(self, txn_id: int) -> None:
        self.versions.pop()  # BUG: physically removes the version instead of tagging it with xmax

    def snapshot_read(self, snapshot_at: int) -> str | None:
        for version in reversed(self.versions):
            if version.xmin < snapshot_at and (version.xmax is None or version.xmax >= snapshot_at):
                return version.value
        return None


table = Table()
table.write("row-exists", txn_id=1)
old_snapshot = 2  # a snapshot taken BEFORE the delete below
table.delete(txn_id=2)
print(table.snapshot_read(old_snapshot))  # expected "row-exists" -- a snapshot BEFORE the delete must still see it
```

**Observed (buggy) output** (captured by actually running the script above):

```text
None
```

**After** (`drilling/code/kata-06-mvcc-delete-forgets-xmax/after/kata.py`)

```python
"""Kata 6 (after): delete() sets xmax on the live version instead of physically removing it."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RowVersion:
    value: str
    xmin: int
    xmax: int | None = None


@dataclass
class Table:
    versions: list[RowVersion] = field(default_factory=list[RowVersion])

    def write(self, value: str, txn_id: int) -> None:
        self.versions.append(RowVersion(value=value, xmin=txn_id))

    def delete(self, txn_id: int) -> None:
        self.versions[-1].xmax = txn_id  # => co-21: tags the version deleted -- history is never destroyed

    def snapshot_read(self, snapshot_at: int) -> str | None:
        for version in reversed(self.versions):
            if version.xmin < snapshot_at and (version.xmax is None or version.xmax >= snapshot_at):
                return version.value
        return None


table = Table()
table.write("row-exists", txn_id=1)
old_snapshot = 2
table.delete(txn_id=2)
print(table.snapshot_read(old_snapshot))
```

<details>
<summary>Model solution</summary>

**Root cause**: MVCC's entire visibility model depends on old versions staying PRESENT, just tagged
with the transaction that deleted them (`xmax`) -- physically removing a version the moment it's
deleted destroys the exact history an earlier snapshot needs to still see. Setting `xmax` instead of
popping is what lets a snapshot correctly answer "was this row visible AS OF my snapshot point,"
regardless of what happened after.

**Run**: `python3 kata.py`

**Output**:

```text
row-exists
```

</details>

### Kata 7 -- Repeatable Read: re-querying live state instead of a real snapshot lets a phantom through

_relates to co-24, Example 74_

**Task.** Two reads inside the SAME repeatable-read transaction should see the identical row count,
even if a concurrent transaction inserts a new matching row in between. The version below is broken:
it holds a reference to the live, mutable table instead of taking an actual snapshot.

**Before** (`drilling/code/kata-07-repeatable-read-misses-phantom/before/kata.py`)

```python
"""Kata 7 (before): a "repeatable read" that re-queries live state on every call is NOT actually snapshot-stable."""

from __future__ import annotations


class NaiveRepeatableRead:
    def __init__(self, table: list[dict[str, str]]) -> None:
        self.table = table  # BUG: holds a reference to the LIVE table, never actually takes a snapshot

    def count_rows(self, status: str) -> int:
        return sum(1 for row in self.table if row["status"] == status)  # re-reads live state every call


table: list[dict[str, str]] = [{"status": "open"}]
txn = NaiveRepeatableRead(table)
first_count = txn.count_rows("open")
table.append({"status": "open"})  # a concurrent transaction inserts a new matching row (a phantom)
second_count = txn.count_rows("open")
print(first_count, second_count)
print(first_count == second_count)  # expected True under repeatable read -- the SAME transaction's two reads must agree
```

**Observed (buggy) output** (captured by actually running the script above):

```text
1 2
False
```

**After** (`drilling/code/kata-07-repeatable-read-misses-phantom/after/kata.py`)

```python
"""Kata 7 (after): a real repeatable-read transaction takes an explicit COPY of the table at its start."""

from __future__ import annotations


class SnapshotRepeatableRead:
    def __init__(self, table: list[dict[str, str]]) -> None:
        self.snapshot = list(table)  # => co-24: an explicit copy taken NOW -- later inserts cannot affect it

    def count_rows(self, status: str) -> int:
        return sum(1 for row in self.snapshot if row["status"] == status)


table: list[dict[str, str]] = [{"status": "open"}]
txn = SnapshotRepeatableRead(table)
first_count = txn.count_rows("open")
table.append({"status": "open"})  # the concurrent insert still happens -- but txn's snapshot never sees it
second_count = txn.count_rows("open")
print(first_count, second_count)
print(first_count == second_count)
```

<details>
<summary>Model solution</summary>

**Root cause**: "repeatable read" is a promise about what a SNAPSHOT sees, not a promise that the
underlying data never changes -- holding a live reference to mutable state means every query re-reads
whatever the world looks like right now, which is exactly what a genuine snapshot is supposed to
prevent. Taking an explicit copy (or, in a real engine, resolving reads through MVCC's snapshot
visibility rule from co-22) is what makes the two reads inside one transaction agree.

**Run**: `python3 kata.py`

**Output**:

```text
1 1
True
```

</details>

### Kata 8 -- Strict 2PL: releasing a write lock right after the write, not at commit, permits a dirty read

_relates to co-25, Examples 68, 69_

**Task.** A second transaction should never be able to acquire a row's write lock while the first
transaction that wrote it is still uncommitted. The version below is broken: it releases the lock
immediately after the write completes, not at commit time.

**Before** (`drilling/code/kata-08-2pl-releases-lock-early/before/kata.py`)

```python
"""Kata 8 (before): a transaction releases its write lock as soon as it finishes writing, not at commit."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LockManager:
    held_by: dict[str, int] = field(default_factory=dict[str, int])

    def acquire(self, key: str, txn_id: int) -> bool:
        if key in self.held_by and self.held_by[key] != txn_id:
            return False
        self.held_by[key] = txn_id
        return True

    def release(self, key: str) -> None:
        self.held_by.pop(key, None)


locks = LockManager()
locks.acquire("row-1", txn_id=1)  # txn 1 acquires the write lock and writes row-1
locks.release("row-1")  # BUG: released immediately after the write, NOT held until commit (violates strict 2PL)

# txn 2 can now acquire the SAME row before txn 1 has committed -- a dirty read/write becomes possible
txn2_acquired_before_txn1_committed = locks.acquire("row-1", txn_id=2)
print(txn2_acquired_before_txn1_committed)
print(
    txn2_acquired_before_txn1_committed is False
)  # expected True (i.e. txn2 should NOT acquire it) under strict 2PL
```

**Observed (buggy) output** (captured by actually running the script above):

```text
True
False
```

**After** (`drilling/code/kata-08-2pl-releases-lock-early/after/kata.py`)

```python
"""Kata 8 (after): the write lock is held until an explicit commit() -- strict 2PL's defining rule."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LockManager:
    held_by: dict[str, int] = field(default_factory=dict[str, int])

    def acquire(self, key: str, txn_id: int) -> bool:
        if key in self.held_by and self.held_by[key] != txn_id:
            return False
        self.held_by[key] = txn_id
        return True

    def release(self, key: str) -> None:
        self.held_by.pop(key, None)


class StrictTwoPhaseTxn:
    def __init__(self, locks: LockManager, txn_id: int) -> None:
        self.locks = locks
        self.txn_id = txn_id
        self.held_keys: list[str] = []

    def write(self, key: str) -> bool:
        if not self.locks.acquire(key, self.txn_id):
            return False
        self.held_keys.append(key)  # => the lock is tracked, NOT released, until commit()
        return True

    def commit(self) -> None:
        for key in self.held_keys:  # => co-25: strict 2PL releases every lock only AT commit, all at once
            self.locks.release(key)
        self.held_keys.clear()


locks = LockManager()
txn1 = StrictTwoPhaseTxn(locks, txn_id=1)
txn1.write("row-1")
txn2_acquired_before_txn1_committed = locks.acquire("row-1", txn_id=2)  # txn1 has NOT committed yet
print(txn2_acquired_before_txn1_committed)
print(txn2_acquired_before_txn1_committed is False)
```

<details>
<summary>Model solution</summary>

**Root cause**: releasing a write lock as soon as the write itself is done (rather than holding it
until commit) is plain 2PL's shrinking phase starting too early -- it lets a second transaction
acquire and potentially read or overwrite data from a transaction that might still abort, which is
precisely the cascading-abort risk strict 2PL exists to close. Tracking every acquired lock and
releasing the whole set together, only inside `commit()`, is strict 2PL's defining rule.

**Run**: `python3 kata.py`

**Output**:

```text
False
True
```

</details>

## Self-check checklist

Work through this list without looking anything up. Every item should be something you can do from
memory, not something you'd need to search for.

**Pages and buffer pool (co-01 to co-06)**

- [ ] I can explain why page size is engine-specific rather than a universal constant, and pack/unpack
      a slotted page's header from memory (co-01, co-02).
- [ ] I can explain why a slot index, not a byte offset, is what stays stable across an in-page
      compaction (co-03).
- [ ] I can describe what a buffer pool's page table maps and what pin count and dirty bit each track
      (co-04).
- [ ] I can explain how CLOCK approximates LRU, and what specific access pattern LRU-K handles that
      plain LRU does not (co-05).
- [ ] I can state the buffer-pool read-path invariant ("pool first, disk only on a miss") and why a
      hit ratio is only meaningful because of it (co-06).

**B-tree indexing (co-07 to co-10)**

- [ ] I can explain the structural difference between a B-tree and a B+-tree, and name which one most
      SQL "btree" indexes actually are (co-07).
- [ ] I can compute an approximate B-tree height from a given fanout and key count (co-08).
- [ ] I can describe what happens on a leaf overflow, including how a split can propagate to the root
      (co-09).
- [ ] I can explain what sibling links between leaves save a range scan from having to redo (co-10).

**LSM-tree indexing (co-11 to co-15)**

- [ ] I can explain how a memtable-plus-SSTable design turns random writes into sequential ones
      (co-11).
- [ ] I can state the LSM read-path rule (memtable, then SSTables newest-to-oldest) and why it must
      stop at the first match (co-12).
- [ ] I can name both compaction strategies covered here and one production system defaulting to each
      (co-13).
- [ ] I can state the RUM conjecture and explain why B-tree-vs-LSM is a genuine trade-off, not a
      solved problem (co-14).
- [ ] I can explain a Bloom filter's false-positive/false-negative asymmetry and why that asymmetry is
      what makes it safe to rely on (co-15).

**Write-ahead logging and recovery (co-16 to co-20)**

- [ ] I can state the WAL rule precisely and explain what breaks if a page reaches disk before its
      log record (co-16).
- [ ] I can explain what comparing a log record's LSN against a page's pageLSN answers during recovery
      (co-17).
- [ ] I can name ARIES's three phases in order and explain what "repeats history" means for redo
      (co-18).
- [ ] I can explain which buffer policy (steal vs. no-force) makes redo necessary and which makes undo
      necessary (co-19).
- [ ] I can explain what a checkpoint bounds and what happens to recovery time without one (co-20).

**MVCC, isolation, and durability (co-21 to co-26)**

- [ ] I can explain what an update does under MVCC instead of overwriting in place, and what xmin and
      xmax each record (co-21).
- [ ] I can state the snapshot visibility rule and explain why it makes readers and writers
      non-blocking (co-22).
- [ ] I can explain why MVCC needs VACUUM (or equivalent) and what specifically it reclaims (co-23).
- [ ] I can map each of the four standard isolation levels to the anomaly it stops permitting, and
      name the anomaly snapshot isolation still allows (co-24).
- [ ] I can explain the contention bet 2PL makes versus the bet OCC makes, and what strict 2PL adds
      on top of plain 2PL (co-25).
- [ ] I can explain why a page write is not atomic across a crash, and name two mitigations this topic
      covers (co-26).

**Physical row/column layout (co-27 to co-28)**

- [ ] I can explain what a clustered index makes cheap and what it makes more expensive, versus a heap
      with secondary indexes (co-27).
- [ ] I can explain why a column store's layout makes dictionary, run-length, and delta encoding
      effective in a way row storage cannot (co-28).

## Elaborative interrogation & self-explanation

Eight why/why-not prompts. Answer in your own words before checking -- the goal is explaining the
reasoning, not reciting a definition. All eight trace back to this topic's cross-cutting big idea,
`consistency-latency-throughput`: nearly every mechanism here is a deliberate trade between a
durability or consistency guarantee and the latency or throughput it costs to provide it.

**W1.** Why does this topic insist the WAL rule be stated as "the log record reaches stable storage
BEFORE the page," rather than just "every write gets logged eventually"?

<details>
<summary>Answer</summary>

The ORDER is the entire guarantee -- "eventually logged" says nothing about what happens if a crash
lands between the page write and the (still-pending) log write, which is exactly the window where
data could be lost with no way to reconstruct it. Requiring the log record first means that at any
point a crash could occur, the log is always at least as up to date as any page, which is the
precondition every later recovery mechanism (LSN comparison, ARIES's phases) depends on.

</details>

**W2.** Why does this topic treat "B-tree or LSM" as a genuine engineering decision rather than
recommending one as generally superior?

<details>
<summary>Answer</summary>

Because the RUM conjecture names a real, unavoidable trade-off -- no single design minimizes read,
write, and space amplification simultaneously. A B-tree tends to favor read latency and in-place
update simplicity; an LSM tree tends to favor write throughput at the cost of read amplification
(mitigated by Bloom filters) and compaction overhead. Recommending one universally would mean
ignoring the actual workload, which is precisely the mistake the RUM conjecture warns against.

</details>

**W3.** Why does MVCC's "never overwrite, always append a new version" design necessarily create the
version-bloat problem that VACUUM exists to solve?

<details>
<summary>Answer</summary>

The entire benefit of MVCC (non-blocking snapshot reads) depends on old versions staying present long
enough for any snapshot that might still need them -- but that same design means dead versions
accumulate by construction, since nothing automatically removes a version the moment it's superseded.
VACUUM is the necessary other half of the trade: MVCC buys non-blocking concurrency at the cost of a
cleanup pass that a simpler "update in place" design would never have needed in the first place.

</details>

**W4.** Why is PostgreSQL's `REPEATABLE READ` (which is actually snapshot isolation) able to block a
phantom read yet still permit write skew?

<details>
<summary>Answer</summary>

Snapshot isolation's guarantee is about what each transaction READS -- both transactions see a
consistent snapshot, so neither observes a phantom row appearing mid-transaction. Write skew doesn't
require either transaction to see anything inconsistent; it only requires that each transaction reads
a value the OTHER is about to change and that neither's read technically conflicts with the other's
write under snapshot isolation's conflict-detection rules. Catching that requires reasoning about the
whole pair's write-read (rw-antidependency) relationship, which only true serializable (SSI)
actually checks.

</details>

**W5.** Why does strict 2PL hold write locks until commit, rather than releasing each lock as soon as
its own access is done (which would still technically satisfy plain 2PL's growing/shrinking-phase
rule)?

<details>
<summary>Answer</summary>

Plain 2PL's rule (never acquire a new lock after releasing any lock) prevents SOME anomalies, but
still allows a second transaction to acquire a just-released lock and read data from a first
transaction that has not yet committed -- if the first transaction later aborts, that second
transaction has now read (and possibly acted on) data that never should have existed, a cascading
abort. Holding every write lock until commit closes exactly that window, at the cost of longer lock
hold times.

</details>

**W6.** Why does a torn page specifically threaten a database's durability guarantee, when the page
write itself was "just one disk operation" from the application's point of view?

<details>
<summary>Answer</summary>

"One disk operation" from the application's view is not atomic at the hardware level -- disk sectors
are written incrementally, and a crash mid-write can leave a page that is neither the old, valid
version nor the new, valid version, but a genuinely corrupted mix of both. Because a checksum alone
can only DETECT this, not repair it, mitigations like full-page-writes exist specifically to give
recovery something (a full pre-image) to restore from, closing the gap between "detected corruption"
and "durable data."

</details>

**W7.** Why does this topic describe LRU-K as "a distinct algorithm," not merely "LRU with a bigger
window"?

<details>
<summary>Answer</summary>

Plain LRU makes its eviction decision from a SINGLE piece of information -- the one most recent
access. LRU-K deliberately tracks the last K references for each page and bases eviction on the
K-th-most-recent reference specifically, which is what lets it distinguish a page touched once during
a scan (whose K-th reference, if K > 1, doesn't exist or is very old) from a page touched repeatedly
by a hot workload. That's a genuinely different decision rule, not just a parameterized version of
the same one.

</details>

**W8.** Why does a clustered index make secondary-index maintenance more expensive, when the
secondary index doesn't directly store the row's data at all?

<details>
<summary>Answer</summary>

A clustered index physically locates the row inside its own B+-tree leaf, which means a leaf split
(or any operation that moves the row) changes the row's physical location -- and any secondary index
pointing at that row by its old physical location would now be wrong unless it's updated too. A heap
avoids this coupling by giving every row a stable, physical-location-independent identifier
(row-id/ctid) that a secondary index can point to without needing to track every clustered-index
reorganization.

</details>

---

← Previous: [Capstone](../learning/capstone/overview.md)
