# Path Manifest — `skills/sharia-erp` (Enterprise Resource Planning, Sharia-Compliant)

The **ordered manifest** for the Sharia-compliant-ERP skills path: a **curated, prerequisite-consistent**
ordered list of **course IDs** over this plan's full 30-course corpus — the same 27 shared courses
`skills/conventional-erp` teaches, **plus** 3 Sharia-exclusive courses interleaved after the shared
corpus. **Covers all the basics** (A10) — a reader entering this path cold gets the full 27-course
foundation; it is never an add-on assuming the conventional path. This is the authoritative reading
order for this path; a course page under `?path=skills/sharia-erp` follows it for prev/next +
breadcrumb.

This file is the **human-readable mirror** of the manifest. The **machine-consumed source of truth** is
the standalone data file `apps/ayokoding-www/src/features/course-paths/manifests/skills/sharia-erp.yaml`.
Per `A11` — cited directly from
[`ayokoding-learning-path-02-schema-and-prerequisite-dag/tech-docs.md:467,474,736`](../../../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/tech-docs.md#design-decisions)
(current as of 2026-07-22; plan 02 is an active, unarchived plan — re-verify via `grep -n` against the
live file before relying on exact line numbers) — every shared id below **references** the same course body `skills/conventional-erp` teaches; **no
body is duplicated**. The manifest carries an explicit `arc: immediately-effective` field (R8). Path
landing served at `/en/learn/paths/skills/sharia-erp`.

## Composition (30 courses, terminal — 27 shared + 3 Sharia-exclusive)

**This list is the reading ramp, in `courseOrder` order.** Per
[tech-docs.md §Authoring stages vs reading ramp](../../tech-docs.md#authoring-stages-vs-reading-ramp-dd-3),
**authoring order is not reading order** — the manifest fixes what a _reader_ walks, while the
delivery checklist fixes what an _author_ writes next. Each entry is annotated with its authoring
stage rather than grouped by it. Positions 1-27 are **identical** to `conventional-erp`'s ramp; only
positions 28-30 differ.

1. `erp-foundations-and-history` — Stage A
2. `erp-conceptual-data-model` — Stage A
3. `erp-module-map-and-architecture` — Stage A
4. `erp-document-lifecycle-and-state-machines` — Stage A
5. `erp-posting-rules-and-account-determination` — Stage A
6. `erp-subledger-to-gl-architecture` — Stage A
7. `erp-fiscal-calendar-and-period-close` — Stage A
8. `erp-numbering-sequences-and-uom-conversion` — Stage A
9. `erp-audit-trail-and-change-tracking` — Stage A — **Dangerous 1 ⚡**
10. `procure-to-pay-systems` — Stage A
11. `order-to-cash-systems` — Stage A
12. `erp-procurement-and-fulfillment-exceptions` — Stage A
13. `record-to-report-systems` — Stage B — the hard accounting edge lands here
14. `inventory-and-warehouse-management` — Stage B
15. `erp-inventory-costing-methods` — Stage B
16. `erp-inventory-integrity-and-concurrency` — Stage B — **Dangerous 2 ⚡**
17. `erp-bom-and-routing-architecture` — Stage A (authored early, read here)
18. `production-planning-and-mrp` — Stage B
19. `demand-and-supply-planning` — Stage B
20. `erp-availability-and-reservations` — Stage B
21. `quality-management-and-inspection` — Stage B
22. `erp-extension-and-customization` — Stage A (authored early, read here)
23. `erp-integration-patterns` — Stage A (authored early, read here)
24. `human-capital-management-and-hire-to-retire` — Stage B
25. `multi-company-and-multi-currency-erp` — Stage B
26. `erp-security-and-controls` — Stage B
27. `erp-analytics-and-reporting` — Stage B — **Dangerous 3 ⚡ — the shared 27-course corpus ends here; `conventional-erp` stops at this id, `sharia-erp` continues**
28. `sharia-compliant-erp-design` — Stage C
29. `islamic-contract-based-transaction-flows` — Stage C
30. `zakat-and-sharia-compliance-modules` — Stage C — **Dangerous 4 ⚡ — path ENDS HERE**

> **Where the two paths diverge.** The shared corpus ends at **position 27**
> (`erp-analytics-and-reporting`), not at `multi-company-and-multi-currency-erp` — both
> `erp-security-and-controls` and `erp-analytics-and-reporting` are shared Stage B ids that
> `conventional-erp` also carries. **Dangerous 3** therefore sits at position 27 in both manifests.
>
> Stage C is **appended, not inserted**. `sharia-compliant-erp-design` prerequisites
> `multi-company-and-multi-currency-erp` only, so it _could_ sit earlier — but placing the
> Sharia-exclusive block last is what makes `zakat-and-sharia-compliance-modules` the terminal course
> and lets **Dangerous 4** mark the end of the path. Inserting the block ahead of
> `erp-security-and-controls` would end `sharia-erp` on two generic shared courses and strand the
> Dangerous 4 boundary mid-ramp.

## Growth history (falsifiable checks)

- **Before Stage B growth**: `courseOrder` has exactly 15 entries; no Stage B or Stage C id is
  present.
- **After Stage B growth**: `courseOrder` has exactly 27 entries (the same 27 shared ids
  `conventional-erp` reaches); no Stage C id is present yet.
- **After Stage C growth**: `courseOrder` has exactly 30 entries; every previously-published id
  retains its relative order; the 3 Sharia-exclusive ids are inserted at the position described
  above.

## Order rationale

See [tech-docs.md §The ERP catalog](../../tech-docs.md#the-erp-catalog-30-courses-settled),
[§Authoring stages vs reading ramp](../../tech-docs.md#authoring-stages-vs-reading-ramp-dd-3), and
[§Two paths, one corpus (A10/A11)](../../tech-docs.md#two-paths-one-corpus-a10--a11).

---

← Back to the [syllabus index](../README.md)
