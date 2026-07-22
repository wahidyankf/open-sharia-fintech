# Syllabus Index — Enterprise Resource Planning

**Custodian**: ayokoding-learning-path-07-skills-erp

Per-course module/topic breakdowns for the 30-course ERP corpus (DD-31 in
[`../tech-docs.md`](../tech-docs.md#syllabus-layer--custody-and-shape-dd-31)). Mirrors the folder
convention `ayokoding-learning-path-02-schema-and-prerequisite-dag` established
(`syllabus/courses/` + `syllabus/paths/`), scoped to this plan's own two ERP paths.

Authored independently from domain reasoning and the
[domain-research grounding](../tech-docs.md#verification-status-carried-forward-a4) **first, with no
external curriculum open** — per programme decision `A12`
([`../../ayokoding-learning-path-programme.md`](../../ayokoding-learning-path-programme.md#a12--how-a-syllabus-may-and-may-not-be-confirmed)),
a published
curriculum may only **corroborate coverage after the fact**; it must never supply the structure being
written. Only **then** does a `web-researcher` confirmation pass run, asking a coverage question only
("is anything missing, is anything included the field would not recognise") against APICS/ASCM CPIM &
CSCP topic outlines (planning/operations content) and the open-source systems' published module
structures, named nominatively only (architecture/module-map content). The pass **never** reproduces a
curriculum's text, module titles, or sequence, and never lifts documentation prose (e.g. ERPNext's own
docs are CC-BY-SA-3.0, share-alike, and cannot be copied from). A finding is actionable only as "add
topic X"; it is never actionable as "reorder to match theirs". See
[delivery.md Phase 1.2a](../delivery.md#12a--web-researcher-confirmation-pass-a12) and
[tech-docs.md §Syllabus confirmation order](../tech-docs.md#syllabus-confirmation-order-a12).

## Stage A — Foundations & Architecture (15 courses, no accounting precondition)

| #   | Course id                                                                                                 | Format            |
| --- | --------------------------------------------------------------------------------------------------------- | ----------------- |
| 1   | [`erp-foundations-and-history`](./courses/erp-foundations-and-history.md)                                 | Annotated-concept |
| 2   | [`erp-conceptual-data-model`](./courses/erp-conceptual-data-model.md)                                     | Annotated-concept |
| 3   | [`erp-module-map-and-architecture`](./courses/erp-module-map-and-architecture.md)                         | Annotated-concept |
| 4   | [`erp-document-lifecycle-and-state-machines`](./courses/erp-document-lifecycle-and-state-machines.md)     | Annotated-concept |
| 5   | [`erp-posting-rules-and-account-determination`](./courses/erp-posting-rules-and-account-determination.md) | By Example        |
| 6   | [`erp-subledger-to-gl-architecture`](./courses/erp-subledger-to-gl-architecture.md)                       | By Example        |
| 7   | [`erp-fiscal-calendar-and-period-close`](./courses/erp-fiscal-calendar-and-period-close.md)               | Annotated-concept |
| 8   | [`erp-numbering-sequences-and-uom-conversion`](./courses/erp-numbering-sequences-and-uom-conversion.md)   | Annotated-concept |
| 9   | [`erp-audit-trail-and-change-tracking`](./courses/erp-audit-trail-and-change-tracking.md)                 | Annotated-concept |
| 10  | [`procure-to-pay-systems`](./courses/procure-to-pay-systems.md)                                           | By Example        |
| 11  | [`order-to-cash-systems`](./courses/order-to-cash-systems.md)                                             | By Example        |
| 12  | [`erp-procurement-and-fulfillment-exceptions`](./courses/erp-procurement-and-fulfillment-exceptions.md)   | By Example        |
| 17  | [`erp-bom-and-routing-architecture`](./courses/erp-bom-and-routing-architecture.md)                       | By Example        |
| 22  | [`erp-extension-and-customization`](./courses/erp-extension-and-customization.md)                         | By Example        |
| 23  | [`erp-integration-patterns`](./courses/erp-integration-patterns.md)                                       | By Example        |

## Stage B — Conventional Enterprise Depth (12 courses, gated on accounting's conventional-accounting boundary)

| #   | Course id                                                                                                 | Format            |
| --- | --------------------------------------------------------------------------------------------------------- | ----------------- |
| 13  | [`record-to-report-systems`](./courses/record-to-report-systems.md)                                       | By Example        |
| 14  | [`inventory-and-warehouse-management`](./courses/inventory-and-warehouse-management.md)                   | By Example        |
| 15  | [`erp-inventory-costing-methods`](./courses/erp-inventory-costing-methods.md)                             | By Example        |
| 16  | [`erp-inventory-integrity-and-concurrency`](./courses/erp-inventory-integrity-and-concurrency.md)         | By Example        |
| 18  | [`production-planning-and-mrp`](./courses/production-planning-and-mrp.md)                                 | By Example        |
| 19  | [`demand-and-supply-planning`](./courses/demand-and-supply-planning.md)                                   | Annotated-concept |
| 20  | [`erp-availability-and-reservations`](./courses/erp-availability-and-reservations.md)                     | By Example        |
| 21  | [`quality-management-and-inspection`](./courses/quality-management-and-inspection.md)                     | By Example        |
| 24  | [`human-capital-management-and-hire-to-retire`](./courses/human-capital-management-and-hire-to-retire.md) | Annotated-concept |
| 25  | [`multi-company-and-multi-currency-erp`](./courses/multi-company-and-multi-currency-erp.md)               | By Example        |
| 26  | [`erp-security-and-controls`](./courses/erp-security-and-controls.md)                                     | Annotated-concept |
| 27  | [`erp-analytics-and-reporting`](./courses/erp-analytics-and-reporting.md)                                 | By Example        |

**Dangerous 3 ⚡ — `conventional-erp` ENDS HERE** (27 courses).

## Stage C — Sharia-Compliant Design (3 courses, `sharia-erp` only, gated on accounting's sharia-accounting boundary)

| #   | Course id                                                                                           | Format            |
| --- | --------------------------------------------------------------------------------------------------- | ----------------- |
| 28  | [`sharia-compliant-erp-design`](./courses/sharia-compliant-erp-design.md)                           | Annotated-concept |
| 29  | [`islamic-contract-based-transaction-flows`](./courses/islamic-contract-based-transaction-flows.md) | By Example        |
| 30  | [`zakat-and-sharia-compliance-modules`](./courses/zakat-and-sharia-compliance-modules.md)           | Annotated-concept |

**Dangerous 4 ⚡ — `sharia-erp` ENDS HERE** (30 courses).

## Path mirrors

- [`paths/manifest-skills-conventional-erp.md`](./paths/manifest-skills-conventional-erp.md) — the
  authoritative 27-id ordering `<CONVMAN>`'s `courseOrder` is transcribed from.
- [`paths/manifest-skills-sharia-erp.md`](./paths/manifest-skills-sharia-erp.md) — the authoritative
  30-id ordering `<SHARMAN>`'s `courseOrder` is transcribed from.

## A6 / A7 stay in force here

No module in any of the 30 syllabus files below asks the reader to build, install, or stand up a
system (A6), and no module smuggles back evaluation, selection, or implementation-methodology content
(A7). Where a module needs to reference how a real system behaves, it describes the behaviour; it
never scaffolds a codebase for the reader to extend.
