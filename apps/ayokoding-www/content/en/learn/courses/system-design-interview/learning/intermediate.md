---
title: "Scale and Reliability Scenarios"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

These scenarios focus on choosing and explaining a mechanism under a stated constraint. They do not
teach the mechanisms from zero; use [System Design](../../system-design/overview.md) for depth.

## ex-13 · stateless-web-tier

**Concepts**: co-08.

**Scenario**: Scale a request tier for a profile lookup workload.

**Observable check**: Show that request state is not stored on an individual application instance.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-14 · load-balancer-choices

**Concepts**: co-09.

**Scenario**: Choose a traffic-balancing policy and health signal.

**Observable check**: Explain why the policy fits the traffic shape and how unhealthy nodes leave rotation.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-15 · read-replica-scaling

**Concepts**: co-11, co-12.

**Scenario**: Handle a read-heavy catalog workload.

**Observable check**: State the replication-lag consequence and the product behavior it permits.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-16 · sharding-strategy

**Concepts**: co-11, co-15.

**Scenario**: Partition a write-heavy event table.

**Observable check**: Name the partition key, hot-partition risk, and an observation that would detect it.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-17 · cache-placement

**Concepts**: co-10.

**Scenario**: Choose cache placement for a hot public read.

**Observable check**: State miss behavior, freshness rule, and invalidation ownership.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-18 · cache-stampede-mitigation

**Concepts**: co-10, co-17.

**Scenario**: Prevent many concurrent misses from overloading an origin.

**Observable check**: Specify one coordination or stale-response approach and its failure behavior.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-19 · consistency-choice

**Concepts**: co-12.

**Scenario**: Choose consistency behavior for a reservation confirmation.

**Observable check**: State the harm of a stale or conflicting result and let that harm drive the choice.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-20 · async-queue-offload

**Concepts**: co-13.

**Scenario**: Move a slow export from the request path.

**Observable check**: Show durable handoff, worker responsibility, and the changed user-visible response.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-21 · idempotency-and-retries

**Concepts**: co-13, co-17.

**Scenario**: Make a delivery attempt safe when a worker retries.

**Observable check**: Define an idempotency key and show why duplicate delivery does not double-apply.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-22 · rate-limiter-design

**Concepts**: co-14.

**Scenario**: Deep-dive a token-bucket API limit.

**Observable check**: Name the identity being limited, refill rule, counter location, and rejection response.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-23 · cdn-for-static-and-media

**Concepts**: co-10, co-08.

**Scenario**: Offload fictional media reads.

**Observable check**: State cache-control intent and the origin path after a miss.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-24 · hot-key-handling

**Concepts**: co-15, co-11.

**Scenario**: Handle a viral item that overloads one partition.

**Observable check**: Describe a spread or precompute strategy and its cost.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-25 · write-amplification-tradeoff

**Concepts**: co-16, co-11.

**Scenario**: Choose fan-out-on-write or fan-out-on-read for a feed.

**Observable check**: State both write and read costs, then select against the named workload.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-26 · storage-sizing-drives-choice

**Concepts**: co-04, co-19.

**Scenario**: Use a storage estimate to revisit a retention decision.

**Observable check**: Show the number, its assumptions, and the product or cost consequence.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-27 · failure-mode-walkthrough

**Concepts**: co-17.

**Scenario**: Walk the primary database failure path.

**Observable check**: Name detection, failover behavior, client consequence, and possible data-loss window.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-28 · timeouts-and-circuit-breakers

**Concepts**: co-14, co-17.

**Scenario**: Protect a slow dependency in a checkout-adjacent flow.

**Observable check**: State timeout, bounded retry, fallback, and what the caller sees.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-29 · availability-target-math

**Concepts**: co-19, co-17.

**Scenario**: Translate an illustrative availability target into a resilience requirement.

**Observable check**: Explain the target’s effect on redundancy without presenting it as a vendor guarantee.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-30 · observability-plan

**Concepts**: co-18.

**Scenario**: Add observability to a delayed reminder design.

**Observable check**: Name a metric, log or trace, and alert; tie each to a question or failure mode.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-31 · degrade-gracefully

**Concepts**: co-14, co-17.

**Scenario**: Keep a core action usable while a non-core dependency fails.

**Observable check**: Identify the preserved core, the omitted enhancement, and the recovery signal.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-32 · altitude-shift-on-cue

**Concepts**: co-20.

**Scenario**: Answer a probe on one component then resume the whole-system explanation.

**Observable check**: Show both altitudes and a spoken transition between them.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-33 · cost-as-a-driver

**Concepts**: co-19, co-16.

**Scenario**: Compare a lower-cost and higher-cost storage path.

**Observable check**: State what each saves or spends and the service-level cost of the cheaper option.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-34 · migration-and-rollout

**Concepts**: co-22, co-17.

**Scenario**: Describe a reversible change to a fictional delivery workflow.

**Observable check**: Include compatibility, observation, rollback trigger, and ownership.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-35 · multi-region-consideration

**Concepts**: co-12, co-19.

**Scenario**: Decide whether a prompt requires multiple regions.

**Observable check**: Ask for recovery and locality requirements, then state the conditional choice.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-36 · staff-level-ambiguity

**Concepts**: co-22, co-03.

**Scenario**: Turn a deliberately ambiguous staff prompt into decisions.

**Observable check**: Make assumptions explicit, rank open questions, and state a first slice.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-37 · cross-cutting-concerns

**Concepts**: co-22.

**Scenario**: Surface staff-level cross-cutting concerns.

**Observable check**: Name at least two of security, privacy, cost, migration, accessibility, or ownership and their decision impact.

**Interview move**: Connect the choice back to an explicit requirement or estimate.

## ex-38 · self-score-a-design

**Concepts**: co-01, co-22.

**Scenario**: Grade a short design transcript.

**Observable check**: Rate scope, estimation, breadth, depth, communication, and trade-offs with evidence.

**Interview move**: Connect the choice back to an explicit requirement or estimate.
