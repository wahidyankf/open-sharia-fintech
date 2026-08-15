# Path Manifest — `skills/sharia-erp` (terminal, 30 ids)

The **ordered manifest** for the sharia-ERP skills path at its terminal state: the same 27 shared ids
as `manifest-skills-conventional-erp.md` plus 3 Sharia-exclusive ids appended. `sharia-erp` is not an
add-on assuming the conventional path — a reader entering it cold gets full grounding, because its
`courseOrder` **includes** all 27 shared ids ahead of the Sharia-exclusive 3 (A10/A11).

The **machine-consumed source of truth** is the standalone data file
`apps/ayokoding-www/src/features/course-paths/manifests/skills/sharia-erp.json` (created by plan 17
at 15 ids, grown to 27 by this plan's Stage B alongside `<CONVMAN>`, then to this terminal 30-id state
by this plan's own Stage C). Path landing served at `/en/learn/paths/skills/sharia-erp`.

## Composition (30 courses, terminal — no further growth)

Positions 1-15 are [plan 17's own corpus](../../../../in-progress/ayokoding-learning-path-17-skills-erp-foundations/syllabus/courses/README.md);
positions 16-27 are this plan's own 12 Stage-B courses (identical to `<CONVMAN>`'s own positions
16-27); positions 28-30 are this plan's own 3 Stage-C, Sharia-exclusive courses.

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
13. `record-to-report-systems` — this plan (Stage B)
14. `inventory-and-warehouse-management` — this plan (Stage B)
15. `erp-inventory-costing-methods` — this plan (Stage B)
16. `erp-inventory-integrity-and-concurrency` — this plan (Stage B) — **Dangerous 2 ⚡**
17. `erp-bom-and-routing-architecture` — plan 17
18. `production-planning-and-mrp` — this plan (Stage B)
19. `demand-and-supply-planning` — this plan (Stage B)
20. `erp-availability-and-reservations` — this plan (Stage B)
21. `quality-management-and-inspection` — this plan (Stage B)
22. `erp-extension-and-customization` — plan 17
23. `erp-integration-patterns` — plan 17
24. `human-capital-management-and-hire-to-retire` — this plan (Stage B)
25. `multi-company-and-multi-currency-erp` — this plan (Stage B)
26. `erp-security-and-controls` — this plan (Stage B)
27. `erp-analytics-and-reporting` — this plan (Stage B) — shared corpus complete here
28. `sharia-compliant-erp-design` — this plan (Stage C) — appended after position 27
29. `islamic-contract-based-transaction-flows` — this plan (Stage C)
30. `zakat-and-sharia-compliance-modules` — this plan (Stage C) — **Dangerous 4 ⚡ — ENDS HERE**

## Growth history

1. Plan 17 published positions 1-15 — Stage A, Dangerous 1 (identical to `<CONVMAN>` at this point).
2. This plan grew to 27 ids identically to `<CONVMAN>`'s own Stage B growth — Dangerous 2.
3. This plan **appended** 3 Sharia-exclusive ids after the complete 27-id shared corpus — Stage C,
   27 → 30, Dangerous 4. Appending (never inserting mid-corpus) is what makes
   `zakat-and-sharia-compliance-modules` the terminal id.

No id already published is ever reordered. `<CONVMAN>` is verified **unchanged** at 27 ids throughout
this plan's own Stage C growth of `<SHARMAN>`.
