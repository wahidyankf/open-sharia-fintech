# Path Manifest — `skills/conventional-erp` (terminal, 27 ids)

The **ordered manifest** for the conventional-ERP skills path at its terminal state: a **curated,
prerequisite-consistent** ordered list of 27 **course IDs** over the full ERP corpus. This is the
authoritative reading order for the path; a course page under `?path=skills/conventional-erp` follows
it for prev/next + breadcrumb.

The **machine-consumed source of truth** is the standalone data file
`apps/ayokoding-www/src/features/course-paths/manifests/skills/conventional-erp.yaml` (created by
plan 17 at 15 ids, grown to this terminal 27-id state by this plan). Path landing served at
`/en/learn/paths/skills/conventional-erp`.

## Composition (27 courses, terminal — no further growth)

Positions 1-15 are [plan 17's own corpus](../../../ayokoding-learning-path-17-skills-erp-foundations/syllabus/courses/README.md)
(referenced by id, never copied); positions 16-27 are this plan's own 12 Stage-B courses. **This list
is the reading ramp, in `courseOrder` order** — authoring order is not reading order (see
[tech-docs.md §Authoring stages vs reading ramp](../../tech-docs.md#the-erp-catalog-this-plans-15-course-slice)).

1. `erp-foundations-and-history` — plan 17
2. `erp-conceptual-data-model` — plan 17
3. `erp-module-map-and-architecture` — plan 17
4. `erp-document-lifecycle-and-state-machines` — plan 17
5. `erp-posting-rules-and-account-determination` — plan 17
6. `erp-subledger-to-gl-architecture` — plan 17
7. `erp-fiscal-calendar-and-period-close` — plan 17
8. `erp-numbering-sequences-and-uom-conversion` — plan 17
9. `erp-audit-trail-and-change-tracking` — plan 17 — **Dangerous 1 ⚡**
10. `procure-to-pay-systems` — plan 17
11. `order-to-cash-systems` — plan 17
12. `erp-procurement-and-fulfillment-exceptions` — plan 17
13. `record-to-report-systems` — this plan (Stage B) — inserted after position 12
14. `inventory-and-warehouse-management` — this plan (Stage B)
15. `erp-inventory-costing-methods` — this plan (Stage B)
16. `erp-inventory-integrity-and-concurrency` — this plan (Stage B) — **Dangerous 2 ⚡**
17. `erp-bom-and-routing-architecture` — plan 17
18. `production-planning-and-mrp` — this plan (Stage B) — inserted after position 17
19. `demand-and-supply-planning` — this plan (Stage B)
20. `erp-availability-and-reservations` — this plan (Stage B)
21. `quality-management-and-inspection` — this plan (Stage B)
22. `erp-extension-and-customization` — plan 17
23. `erp-integration-patterns` — plan 17
24. `human-capital-management-and-hire-to-retire` — this plan (Stage B) — appended
25. `multi-company-and-multi-currency-erp` — this plan (Stage B)
26. `erp-security-and-controls` — this plan (Stage B)
27. `erp-analytics-and-reporting` — this plan (Stage B) — **Dangerous 3 ⚡ — ENDS HERE**

## Growth history

1. Plan 17 published positions 1-9, 10-12, 13 (`erp-bom-and-routing-architecture`), 14-15
   (`erp-extension-and-customization`, `erp-integration-patterns`) at 15 ids total — Stage A,
   Dangerous 1.
2. This plan inserted 4 ids after `erp-procurement-and-fulfillment-exceptions`, 4 more after
   `erp-bom-and-routing-architecture`, and appended 4 more at the end — Stage B, 15 → 27,
   Dangerous 2 and Dangerous 3.

No id already published by plan 17 is ever reordered.
