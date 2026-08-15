---
title: "Capstone: Mini Database"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Build and test a minimal single-writer store in `code/`: a page pager/cache, ordered leaf chunks with split boundaries, JSON-line WAL records, recovery that ignores incomplete tails, and a narrow insert/select/where layer.

Run `pytest -q` inside `learning/capstone/code`. This capstone does not promise multi-process safety, MVCC, locking, full SQL, or production torn-write protection.
