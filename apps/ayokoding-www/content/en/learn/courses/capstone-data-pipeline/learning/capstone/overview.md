---
title: "Governed Path"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

1. Ingest immutable raw fixture records into bronze with batch identifiers.
2. Normalize to silver; reject duplicate keys, invalid types, and failed reconciliation checks.
3. Publish a gold star schema and prove a serving query against hand-computed totals.
4. Serve a cited answer that names the gold rows used; return "insufficient evidence" when none exist.
5. Re-run the batch and demonstrate idempotency, freshness reporting, and reproducible answer evaluation.

```sql
SELECT
  customer_id,
  SUM(net_amount) AS net_amount
FROM
  fact_order
GROUP BY
  customer_id;
```

The RAG layer retrieves and cites governed records; it must not invent a value absent from gold.
