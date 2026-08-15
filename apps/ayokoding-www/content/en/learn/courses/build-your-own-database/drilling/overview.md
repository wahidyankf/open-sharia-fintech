---
title: "Drilling Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

1. What is the ordinary unit of storage I/O? **Answer:** the fixed-size page.
2. What is the required WAL ordering? **Answer:** append and sync intent before data pages can become durable.
3. What is out of scope? **Answer:** concurrent MVCC/isolation and full SQL.

## Calculation practice

1. At what byte offset does page 7 begin when pages are 4096 bytes? **Answer:** 28672.
2. Estimate leaf capacity for fanout 64 and height 3. **Answer:** about 64^3 before occupancy adjustments.

## Scenario judgment

1. A trailing WAL record is incomplete after a crash. **Answer:** reject it, truncate the tail, and replay only complete committed records.
2. Heavy appends and rare reads suggest what evaluation? **Answer:** an LSM design, including its compaction/read costs.

## Design exercise

Design a single-writer event store with a pager, cache, WAL commit boundary, checkpoint, and range-query index. Explain recovery and why concurrent readers need later MVCC/isolation work.

## Automaticity checklist

- I calculate page offsets as page number times page size.
- I can state WAL before data and locate fsync.
- I distinguish committed redo from uncommitted undo.
- I compare B-tree read shape with LSM compaction shape.
- I reject query features outside this subset.
