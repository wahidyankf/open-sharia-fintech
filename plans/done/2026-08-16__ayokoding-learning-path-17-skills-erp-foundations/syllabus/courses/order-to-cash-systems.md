# Order to Cash Systems (By Example)

**Course ID**: `order-to-cash-systems` · **Format**: By Example.

**Scope note**: Models customer order, fulfilment, invoice, and collection evidence; it excludes revenue-policy interpretation. License-aware.

## Why this exists · the big idea

- **The problem before the solution**: sales and collections drift when fulfilment lacks a shared trace.
- **Keep-this-if-you-forget-everything**: receivables require traceable order-to-fulfilment evidence.

## Prerequisites

- **Prior courses**: `erp-subledger-to-gl-architecture`.
- **Assumed knowledge**: customer and invoice basics.

## Accuracy notes

- [Repo-grounded, tech-docs.md] Original lifecycle examples, not a revenue standard.

## Concepts

- **co-01 · sales-order** — approved customer commitment.
- **co-02 · allocation** — reserved capacity or quantity for fulfilment.
- **co-03 · shipment-evidence** — proof of operational fulfilment.
- **co-04 · customer-invoice** — accountable claim linked to fulfilment.
- **co-05 · receivable** — customer balance from valid claim.
- **co-06 · collection** — attributable settlement event.
- **co-07 · credit-hold** — policy-based restriction on progression.
- **co-08 · return-flow** — controlled reverse fulfilment evidence.

## Worked examples

### Beginner

- **ex-01 · invoice-after-shipment** — create a claim after evidence arrives — verify source linkage. (co-03, co-04)

### Intermediate

- **ex-02 · credit-hold** — prevent release over policy limit — verify held order remains auditable. (co-07)

### Advanced

- **ex-03 · partial-return** — reverse only returned quantity — verify remaining receivable is explained. (co-08)

## In which paths

- `skills/conventional-erp` — Stage A · operational foundation.
- `skills/sharia-erp` — Stage A · operational foundation.
