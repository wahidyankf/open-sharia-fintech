---
title: "Rationale"
date: 2026-07-27T00:00:00+07:00
draft: false
weight: 2
---

## Capstone Step 4: per-store CAP/PACELC + license rationale

_exercises co-03, co-04, co-28_

Every store this capstone uses is chosen because its own access pattern demands it -- not because
"NoSQL" is a single interchangeable category. This page states, for each of the three stores
`kv.py`, `doc.py`, and `wide.py` build on, the access pattern that justifies the choice, the
CAP/PACELC position that follows from how the store is actually configured here, and the exact,
checked license -- formalizing the same content Example 80 already drafted and verified in code.

### Valkey (session/cache store, `kv.py`)

**Access pattern**: TTL-bound session tokens, single-key CRUD, disposable by design. `kv.py`'s own
`create_session`/`get_session`/`touch_session`/`delete_session` never read across sessions -- every
operation targets exactly one `session:<id>` key, and a session that is never explicitly deleted
still self-expires via its own TTL (co-20, co-24, co-21).

**CAP/PACELC**: AP/PA/EL. A single-node cache favors availability and low latency over strict
consistency: if this session store were ever replicated, a stale read of "is this session still
valid" for a few milliseconds is a far cheaper mistake than refusing a login because a replica is
momentarily unreachable. There is no cross-key transaction here to protect -- each session round-trips
independently, which is exactly the shape AP/PA/EL is built for (co-03, co-04).

**License**: BSD-3-Clause -- Valkey, the Linux Foundation fork of Redis (the actual store `kv.py`
connects to in this capstone, per Example 25's own citation). A permissive, OSI-approved license with
no source-availability or field-of-use restriction.

### MongoDB (document store, `doc.py`)

**Access pattern**: two NAMED reads -- "fetch a product with its current stock level" and "fetch every
product in a given category, cheapest first" -- both served by indexes chosen specifically to answer
them (co-08, co-17). `doc.py`'s `seed_products` creates exactly the `sku` index and the
`(category, price)` compound index those two patterns need, nothing more.

**CAP/PACELC**: CP/PC/EC. `doc.py`'s own `update_stock` writes a real inventory count -- a value a
reader must never see go backward or read stale after a genuine sale, the kind of correctness a
product catalog's stock level specifically needs. A majority write concern (the production-grade
choice this pattern implies) favors consistency over availability under a partition: better to briefly
refuse a write than let two replicas disagree about how many units are left (co-03, co-04).

**License**: SSPLv1 (Server Side Public License), NOT OSI-approved open source (per Example 26's own
citation). Source-available, but SSPLv1's own terms extend copyleft obligations to any service offered
"as a service" around the software -- a materially different commitment from a permissive or
traditional copyleft license, and one that must be understood before adopting MongoDB behind a
managed-service offering.

### Cassandra (wide-column store, `wide.py`)

**Access pattern**: order history per customer, an append-heavy, partition-scoped feed. `wide.py`'s own
`fetch_order_history` reads exactly one partition (`WHERE customer_id = ?`), already clustering-ordered
newest-first -- and `wide.py`'s own two-customer test proves that partition isolation holds: `cust-2`'s
orders never appear when reading `cust-1`'s history (co-22, co-25).

**CAP/PACELC**: AP/PA/EL at consistency level ONE, or CP/PC/EC at QUORUM -- tunable per query (co-07).
`wide.py`'s own single-node local cluster does not exercise this tuning directly (replication_factor 1
has no quorum to speak of), but the SAME partition-scoped read shape this capstone uses is exactly what
a production Cassandra deployment would read at ONE for availability, or at QUORUM if a customer's own
order history must never show a stale write immediately after checkout.

**License**: Apache License 2.0 -- Cassandra is an Apache Software Foundation top-level project (per
Example 27's own citation). A permissive, OSI-approved license, matching the license tier `wide.py`'s
own driver (`cassandra-driver`, also Apache-2.0) carries.

## Summary table

| Store     | Access pattern (justifies the choice)                      | CAP/PACELC                          | License                            |
| --------- | ---------------------------------------------------------- | ----------------------------------- | ---------------------------------- |
| Valkey    | TTL-bound session CRUD, single-key, disposable             | AP/PA/EL                            | BSD-3-Clause                       |
| MongoDB   | Two named, index-served reads over a product catalog       | CP/PC/EC (majority write concern)   | SSPLv1 (NOT OSI-approved)          |
| Cassandra | Per-customer order history, partition-scoped, append-heavy | AP/PA/EL at ONE, CP/PC/EC at QUORUM | Apache License 2.0 (ASF top-level) |

Every row states three things together, matching Example 80's own discipline: the access pattern that
justifies the choice, the CAP/PACELC position, and the exact, checked license -- a store recommendation
missing any one of the three is an incomplete rationale.

---

&larr; Back to [Overview](./overview.md)
