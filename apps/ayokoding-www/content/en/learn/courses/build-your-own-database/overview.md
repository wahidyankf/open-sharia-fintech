---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Build a deliberately small single-writer database: fixed-size pages, ordered indexing, a write-ahead log, crash recovery, and a parsed SQL-ish query subset.

This course assumes Database Internals & Storage Engines and SQL Essentials. It implements those established ideas without reteaching their theory; full SQL, concurrent ACID, locking, and MVCC are explicitly forward work.

## Outcomes

- Make page I/O, caching, and row serialization observable.
- Compare B-tree and LSM paths, then build representative pieces.
- Enforce WAL-before-data and an fsync commit boundary.
- Recover from a complete or incomplete log tail.
- Execute a deliberately narrow insert/select/where query surface.

## Sources

- [SQLite Database File Format](https://www.sqlite.org/fileformat2.html)
- [ARIES](https://doi.org/10.1145/128765.128770)
- [Let's Build a Simple Database](https://cstack.github.io/db_tutorial/)
