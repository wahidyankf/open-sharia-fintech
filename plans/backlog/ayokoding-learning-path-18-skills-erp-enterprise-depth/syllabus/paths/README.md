# Path Mirrors — Terminal Orderings for Both ERP Paths

This folder holds the **path mirrors** — the human-readable authoritative orderings each machine
manifest's `courseOrder` is grown to at this plan's own terminal checkpoint. Unlike plan 17's own
mirrors (15 ids, identical for both paths), these two files carry the **full terminal ordering** —
27 ids for `conventional-erp`, 30 for `sharia-erp` — with positions 1-15 **referencing** plan 17's
corpus by id (never copying its files) and positions 16-30 naming this plan's own courses.

## The two mirrors

- [`manifest-skills-conventional-erp.md`](./manifest-skills-conventional-erp.md) — the authoritative
  **27-id** terminal ordering `<CONVMAN>` is grown to. Terminal boundary: **Dangerous 3** at
  `erp-analytics-and-reporting`.
- [`manifest-skills-sharia-erp.md`](./manifest-skills-sharia-erp.md) — the authoritative **30-id**
  terminal ordering `<SHARMAN>` is grown to: the same 27 shared ids plus the 3 Stage-C
  Sharia-exclusive ids appended. Terminal boundary: **Dangerous 4** at
  `zakat-and-sharia-compliance-modules`.

Both mirrors carry `arc: immediately-effective` (R8/DD-7), unchanged from plan 17's own mirrors.

---

← Back to the [syllabus index](../README.md)
