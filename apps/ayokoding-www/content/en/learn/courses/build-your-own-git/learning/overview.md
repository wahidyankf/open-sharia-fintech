---
title: "Learning Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Concepts

1. **co-01 · content-addressing** — a hash identifies content.
2. **co-02 · sha-hashing** — object IDs derive from a digest.
3. **co-03 · blob-object** — blobs store raw content.
4. **co-04 · tree-object** — trees describe snapshots.
5. **co-05 · commit-object** — commits bind tree and history.
6. **co-06 · tag-object** — annotated tags name objects.
7. **co-07 · object-header** — type and size prefix object bytes.
8. **co-08 · zlib-compression** — loose objects are compressed.
9. **co-09 · loose-object-path** — prefix directory locates objects.
10. **co-10 · hash-object** — hashing writes and reports objects.
11. **co-11 · cat-file** — reading exposes type and payload.
12. **co-12 · tree-serialization** — entries have a stable encoding.
13. **co-13 · tree-parse** — tree bytes decode to entries.
14. **co-14 · commit-serialization** — commits serialize metadata.
15. **co-15 · commit-parent** — parent links form a DAG.
16. **co-16 · refs** — refs name object IDs.
17. **co-17 · head** — HEAD selects current state.
18. **co-18 · symbolic-ref** — HEAD may name another ref.
19. **co-19 · branch** — branch refs move.
20. **co-20 · index-format** — staging holds sorted entries.
21. **co-21 · staging** — adding maps paths to blobs.
22. **co-22 · index-to-tree** — index becomes a tree.
23. **co-23 · commit-porcelain** — commit snapshots staged state.
24. **co-24 · log-walk** — log follows parents.
25. **co-25 · checkout** — checkout materializes a tree.
26. **co-26 · status** — status compares working/index/HEAD.
27. **co-27 · diff** — diff reports content changes.
28. **co-28 · safety-boundaries** — teaching stores stay isolated.
29. **co-29 · deterministic-fixtures** — fixed metadata makes results testable.
30. **co-30 · plumbing-porcelain** — small commands compose user operations.

All 78 examples have isolated Python artifacts.
