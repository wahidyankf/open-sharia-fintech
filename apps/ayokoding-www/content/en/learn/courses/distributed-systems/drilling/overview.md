---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

**Q1.** Why does a timeout not prove a peer crashed?

<details>
<summary>Answer</summary>

The network or peer may be slow, partitioned, overloaded, or delayed. A timeout is evidence used by
a policy, which can be wrong; fencing protects resources from a wrongly suspected old authority.

</details>

**Q2.** What does `R + W > N` provide?

<details>
<summary>Answer</summary>

It gives a successful read and successful write at least one overlapping replica. Correct version
selection and replica behavior are still required to return the newest applicable value.

</details>

**Q3.** What is the difference between consensus safety and liveness?

<details>
<summary>Answer</summary>

Safety means never choosing conflicting outcomes. Liveness means eventually deciding under stated
conditions. A safe system can wait when it cannot make progress safely.

</details>

## Scenario judgment

A balance-confirmation write cannot show two confirmed balances, but a product-list page can tolerate
briefly stale information.

<details>
<summary>Reasoned answer</summary>

Use a consistency-preserving path for balance confirmation, accepting an unavailable or pending
result during a partition. A nearby replica may serve the product list if the page states and
operates within its freshness tolerance.

</details>

## Hands-on simulation

Implement a three-replica register with an injected partition. Show one stale read using a
sub-quorum, then change the configuration to intersecting quorums and explain what additional
version-selection rule is still needed.

## Automaticity checklist

- [ ] I can distinguish a timeout from proof of failure.
- [ ] I can state the chosen behavior for an operation during a partition.
- [ ] I can explain why idempotency is needed with retries.
- [ ] I can identify the majority and term evidence a leader needs.
- [ ] I can name a fencing requirement for an externally protected resource.

## Extension challenge

Draw the failure timeline for a leaseholder that pauses, then resumes after another leaseholder has
been elected. Mark the fencing token that rejects the old holder's next write.
