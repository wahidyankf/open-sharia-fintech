# Path Manifest — `skills/conventional-erp` (Stage A publication)

The **ordered manifest** for the conventional-ERP skills path, at this plan's own Stage A checkpoint:
a **curated, prerequisite-consistent** ordered list of 15 **course IDs** — this plan's full slice of
the eventual 30-course corpus. This is the authoritative reading order for the path at this
checkpoint; a course page under `?path=skills/conventional-erp` follows it for prev/next +
breadcrumb.

This file is the **human-readable mirror** of the manifest. The **machine-consumed source of truth**
is the standalone data file
`apps/ayokoding-www/src/features/course-paths/manifests/skills/conventional-erp.json`. The manifest
also carries an explicit `arc: immediately-effective` field (R8). Path landing served at
`/en/learn/paths/skills/conventional-erp`.

## Composition (15 courses at this checkpoint — 27 terminal, grown by the successor plan)

**This list is the reading ramp, in `courseOrder` order.** Authoring order is not reading order; see
[tech-docs.md §Design Decisions, DD-3](../../tech-docs.md#design-decisions)
for why course 17 sits at reading position 13 despite being authored 13th in this plan's own
authoring sequence (its position among these 15 happens to match, since Stage A's authoring order and
reading order coincide for this slice — the divergence only becomes visible once Stage B's courses
interleave in the successor plan).

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

The successor plan grows this array to 27 ids by **inserting** four Stage-B ids after position 12
(`erp-procurement-and-fulfillment-exceptions`), four more after position 13
(`erp-bom-and-routing-architecture`), and **appending** four more at the end — see
[tech-docs.md §courseOrder arrays at each growth boundary](../../../ayokoding-learning-path-18-skills-erp-enterprise-depth/tech-docs.md#courseorder-arrays-at-each-growth-boundary)
in the successor plan. No id already published above is ever reordered.
