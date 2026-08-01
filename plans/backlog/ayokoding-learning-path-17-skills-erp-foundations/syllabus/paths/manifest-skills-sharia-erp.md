# Path Manifest — `skills/sharia-erp` (Stage A publication)

The **ordered manifest** for the sharia-ERP skills path, at this plan's own Stage A checkpoint —
**identical** to `manifest-skills-conventional-erp.md` at this checkpoint (DD-10): both hold the same
15 course ids. The two paths diverge only once the successor plan grows `<SHARMAN>` past 27 ids with
the 3 Sharia-exclusive courses in its own Stage C.

The **machine-consumed source of truth** is the standalone data file
`apps/ayokoding-www/src/features/course-paths/manifests/skills/sharia-erp.yaml`. Path landing served
at `/en/learn/paths/skills/sharia-erp`.

## Composition (15 courses at this checkpoint — 30 terminal, grown by the successor plan)

1. `erp-foundations-and-history`
2. `erp-conceptual-data-model`
3. `erp-module-map-and-architecture`
4. `erp-document-lifecycle-and-state-machines`
5. `erp-posting-rules-and-account-determination`
6. `erp-subledger-to-gl-architecture`
7. `erp-fiscal-calendar-and-period-close`
8. `erp-numbering-sequences-and-uom-conversion`
9. `erp-audit-trail-and-change-tracking` — **Dangerous 1 ⚡**
10. `procure-to-pay-systems`
11. `order-to-cash-systems`
12. `erp-procurement-and-fulfillment-exceptions`
13. `erp-bom-and-routing-architecture`
14. `erp-extension-and-customization`
15. `erp-integration-patterns`

## Growth notice

The successor plan grows this array to 27 ids identically to `<CONVMAN>`'s own Stage B growth, then
**appends** the 3 Sharia-exclusive ids (`sharia-compliant-erp-design`,
`islamic-contract-based-transaction-flows`, `zakat-and-sharia-compliance-modules`) after the complete
27-id shared corpus, occupying positions 28-30 — see
[tech-docs.md §courseOrder arrays at each growth boundary](../../../ayokoding-learning-path-18-skills-erp-enterprise-depth/tech-docs.md#courseorder-arrays-at-each-growth-boundary)
in the successor plan. No id already published above is ever reordered.
