# Procure to Pay Systems (By Example)

**Course ID**: `procure-to-pay-systems` · **Format**: By Example.

**Scope note**: Models request, order, receipt, invoice, and payment evidence; it excludes purchasing strategy. License-aware.

## Why this exists · the big idea

- **The problem before the solution**: ordering and payment lose control when their evidence is disconnected.
- **Keep-this-if-you-forget-everything**: pay only against traceable request, commitment, receipt, and invoice facts.

## Prerequisites

- **Prior courses**: `erp-subledger-to-gl-architecture`.
- **Assumed knowledge**: vendor and invoice basics.

## Accuracy notes

- [Repo-grounded, tech-docs.md] Examples are original process models.

## Concepts

- **co-01 · purchase-requisition** — accountable internal request.
- **co-02 · purchase-order** — approved external commitment.
- **co-03 · goods-receipt** — evidence of accepted delivery.
- **co-04 · invoice-match** — comparison of commitment, receipt, and claim.
- **co-05 · payable** — obligation recorded from valid evidence.
- **co-06 · payment-run** — controlled settlement proposal.
- **co-07 · tolerance** — permitted bounded mismatch.
- **co-08 · exception-workflow** — accountable handling of mismatch.

## Worked examples

### Beginner

- **ex-01 · three-way-match** — compare order, receipt, and invoice — verify unmatched quantity is held. (co-02–co-04)

### Intermediate

- **ex-02 · approval-limit** — route an order above authority — verify no commitment precedes approval. (co-01, co-02)

### Advanced

- **ex-03 · duplicate-invoice** — reject a repeated supplier claim — verify a single payable remains. (co-05, co-08)

## In which paths

- `skills/conventional-erp` — Stage A · operational foundation.
- `skills/sharia-erp` — Stage A · operational foundation.
