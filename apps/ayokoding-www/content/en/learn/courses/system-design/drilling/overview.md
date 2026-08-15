---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

**Q1.** What is the purpose of a back-of-the-envelope estimate?

<details>
<summary>Answer</summary>

It identifies the first likely bottleneck and the decision it informs. It is a falsifiable
assumption, not a precise forecast.

</details>

**Q2.** What does `R + W > N` provide?

<details>
<summary>Answer</summary>

It gives read and write quorums an overlap after a completed write. It does not by itself solve
concurrent writes, failures, repair, or version conflict resolution.

</details>

**Q3.** Why are cache TTLs a product decision?

<details>
<summary>Answer</summary>

They trade freshness for origin protection. A suitable TTL depends on the harm from a stale answer
and the load created by misses.

</details>

## Calculation practice

A service has 2 million daily active users, each making six reads daily. Estimate the average QPS,
then apply a peak factor of eight. At 2 KB per response, estimate peak egress.

<details>
<summary>Worked answer</summary>

`2,000,000 × 6 ÷ 86,400 ≈ 139 average QPS`; `139 × 8 ≈ 1,112 peak QPS`; at 2 KB each,
peak payload egress is about 2.2 MB/s. State that protocol overhead, cache hits, and geographic
distribution may change the network decision.

</details>

## Scenario judgment

A profile-edit request succeeds at the leader, but the page immediately reads an old value from a
replica. The product team says that this is confusing only to the writer; other users may see a
briefly stale profile.

<details>
<summary>Reasoned answer</summary>

Apply read-your-writes for the editing session: route the next read to the leader or a replica known
to have reached the write position. Keep ordinary viewer reads eligible for replicas. This preserves
the cheaper eventual model where the user expectation permits it.

</details>

## Design exercise

Design a thumbnail-upload service. Write the API, estimate daily storage from an explicit assumed
file size and upload volume, select the direct-upload/object-storage path, and draw the CDN read
path. Then state how the service behaves if thumbnail generation backs up and how clients retry a
failed upload without duplicating metadata.

## Automaticity checklist

- [ ] I can turn DAU, actions/day, and a peak factor into a QPS assumption with units.
- [ ] I can name the cache miss path and the freshness cost of a TTL.
- [ ] I can distinguish partition-time CAP behaviour from normal-operation PACELC latency.
- [ ] I can explain why a queue requires idempotent consumers and bounded backpressure.
- [ ] I can present a design as a coherent API, data model, diagram, estimates, failure response,
      and trade-off rather than a component list.
