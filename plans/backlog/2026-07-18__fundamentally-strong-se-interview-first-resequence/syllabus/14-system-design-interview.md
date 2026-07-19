# 14 · System-Design Interview (Annotated-concept, — no code)

**Mapping row** (frozen [tech-docs §Canonical Mapping Table](../tech-docs.md#canonical-mapping-table)):
N=14 · Phase 1 · Interview Preparation · Annotated-concept · — (concept, no code) · folder weight 240 /
learn 114 / drill 214. **NEW (interview module)**.

**Scope note**: the system-design interview **as a format** — the rubric interviewers score, the
structured walkthrough (clarify → estimate → high-level → deep-dive → bottlenecks → trade-offs), and
drills at mid/senior/staff altitude. This is deliberately **NOT** the depth topic
[N=60 `system-design`](./README.md) (which teaches designing real systems for scale) — per design
decision RD-5, "interview format" (Phase 1) and "genuine design depth" (Phase 3) are two separate
topics. This module teaches the _performance and communication_ of the round; it references the depth
topic forward. No runnable code — prose, worked design scenarios, and WCAG-accessible Mermaid diagrams.

## Why this exists · the big idea

- **The problem before the solution**: strong engineers who design real systems daily still stumble in
  the round — they dive into one component without scoping, skip the back-of-envelope estimate, never
  surface a bottleneck, or fail to state a single trade-off out loud. The round scores a _legible design
  conversation_, not a finished architecture.
- **Keep-this-if-you-forget-everything**: drive the round yourself with a repeatable spine — clarify the
  requirements and scale, estimate the numbers, sketch a high-level design, deep-dive one or two
  components the interviewer cares about, then name the bottlenecks and the trade-offs you chose.
- **Big ideas touched**: `correctness-vs-pragmatism` (there is no single right design — defensible
  trade-offs under stated assumptions are the score), `abstraction-and-its-cost` (choosing the right
  altitude to reason at, and dropping down only where it matters).

## Prerequisites

- **Prior topics**: [N=11 OOP Essentials](./README.md), [N=12 OO Design & Patterns](./README.md), and
  [N=13 SQL Essentials](./README.md) for the building blocks; a working mental model of HTTP, caches,
  queues, and databases from earlier Phase 1 exposure.
- **Tools & environment**: a whiteboard or a plain diagramming surface; a timer for drills; no code
  environment required (this is a talking-and-drawing round).
- **Assumed knowledge**: what a load balancer, cache, database index, message queue, and replica are at
  a conceptual level; reading a simple architecture diagram.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (DD-28 convention).

- 2026-07-18 — the round's spine (functional + non-functional requirements, capacity estimation,
  high-level design, data model, API sketch, deep dive, bottleneck + trade-off discussion) and the
  scoring axes (scoping, estimation, breadth, depth, communication, trade-offs) are **stable, vendor-
  independent** practice.
- 2026-07-18 — `[Needs Verification]`: any specific numbers used in capacity estimates (QPS ranges,
  storage-per-record, typical latencies) — present them as illustrative order-of-magnitude figures and
  re-verify representative values at authoring.
- 2026-07-18 — `[Needs Verification]`: named reference systems (URL shortener, news feed, chat, rate
  limiter) are classic prompts; keep any real-company scale claim illustrative, not asserted.

## Concepts

1. **co-01 · what-the-round-scores** — the round scores structured problem-solving, breadth, targeted
   depth, communication, and trade-off reasoning — not a single correct architecture.
2. **co-02 · requirements-clarification** — separating functional (what it does) from non-functional
   (scale, latency, availability, consistency) requirements frames the whole design.
3. **co-03 · scope-negotiation** — narrowing an open-ended prompt to a tractable core within the time
   budget is the first move, not a detour.
4. **co-04 · back-of-envelope-estimation** — order-of-magnitude estimates of QPS, storage, and bandwidth
   size the design and justify later choices.
5. **co-05 · high-level-design-first** — a boxes-and-arrows diagram of the major components before any
   deep dive keeps the conversation legible.
6. **co-06 · api-contract-sketch** — defining the key endpoints/operations pins the interface the design
   must satisfy.
7. **co-07 · data-model-and-storage-choice** — the entities, their access patterns, and the SQL-vs-NoSQL
   choice follow from the requirements, not fashion.
8. **co-08 · scaling-the-web-tier** — statelessness + horizontal scaling behind a load balancer is the
   default path to handling more traffic.
9. **co-09 · load-balancing** — distributing requests across instances (and its health-check + strategy
   choices) removes the single-server bottleneck.
10. **co-10 · caching-strategy** — where to cache (client, CDN, application, database), the invalidation
    approach, and the read/write pattern trade-offs.
11. **co-11 · database-scaling** — replication (read scaling), sharding/partitioning (write scaling), and
    the consistency cost each imposes.
12. **co-12 · consistency-vs-availability** — the CAP-driven choice between strong and eventual
    consistency, framed by what the product actually needs.
13. **co-13 · asynchronous-processing** — message queues and background workers decouple slow work from
    the request path and absorb spikes.
14. **co-14 · rate-limiting-and-backpressure** — protecting a system from overload with limits and
    graceful degradation is a common deep-dive.
15. **co-15 · bottleneck-identification** — naming where the design will break first (the hot shard, the
    single writer, the cache stampede) is a core scored signal.
16. **co-16 · trade-off-articulation** — every choice buys something and costs something; stating both
    sides out loud is what separates a senior answer.
17. **co-17 · reliability-and-failure-modes** — reasoning about what happens when a component fails
    (replicas, retries, idempotency, timeouts) shows production maturity.
18. **co-18 · observability-in-design** — noting how the system would be monitored (metrics, logs,
    alerts) demonstrates operability thinking.
19. **co-19 · non-functional-drivers** — latency, throughput, availability, durability, and cost as the
    axes that actually drive the architecture.
20. **co-20 · altitude-control** — moving fluidly between the whole-system view and one component's
    internals, spending depth where the interviewer signals interest.
21. **co-21 · driving-the-conversation** — leading the round with a stated plan and checkpoints, rather
    than waiting to be interrogated, is a positive senior signal.
22. **co-22 · senior-vs-staff-expectations** — higher levels are scored on ambiguity handling,
    cross-cutting concerns (cost, org, migration), and independent trade-off ownership.

## Tensions & trade-offs — when NOT to reach for this

- **Breadth vs depth under the clock**: covering every component shallowly reads as hand-waving; deep-
  diving one obscure corner while skipping the data model reads as lost. The skill is deliberate
  altitude control — breadth first, then depth where it is scored.
- **Ideal design vs the stated scale**: designing for planet-scale when the prompt implies a modest
  system wastes the round and signals poor judgment. Right-size the design to the estimated numbers.
- **When NOT to reach for a pattern**: bolting on a queue, a cache, or sharding without a requirement
  that demands it adds complexity the interviewer will question — every component must earn its place
  from a stated need.

## Lineage — why it beat the alternative

- The structured round replaced open-ended "design Twitter" chats because unstructured design
  conversations produced noisy, unfair signals: strong designers rambled, weak ones got lucky. A shared
  spine (clarify → estimate → design → deep-dive → trade-offs) made the round legible and gradable, and
  pushed the score toward _reasoning_ over _recall_. This module teaches the spine and the
  communication; the genuine engineering depth lives in [N=58 Software
  Architecture](./README.md), [N=60 System Design](./README.md), and [N=62 Distributed
  Systems](./README.md), which this round draws on but does not replace. It feeds the [Phase 1 mock loop
  capstone](./16c-capstone-interview-loop.md).

## Worked scenarios

No runnable code (Annotated-concept, no-code). Colocated under
`system-design-interview/learning/artifacts/` as design walkthroughs: a prompt, a scored transcript,
and a WCAG-accessible Mermaid architecture diagram per scenario. Grouped by theme. Contiguous
`ex-01..ex-44`. Every scenario cites the `co-NN` it exercises.

### Theme A · The round's spine (ex 01–12)

1. **ex-01 · clarify-functional-vs-nonfunctional** — split a vague prompt into functional and
   non-functional requirements — verify both lists exist and are distinct. (co-02)
2. **ex-02 · negotiate-scope** — narrow "design a social network" to a scored core in the time budget —
   verify a stated, agreed scope. (co-03)
3. **ex-03 · capacity-estimate** — estimate QPS, storage, and bandwidth for the scoped system — verify
   each figure shows its assumption and units. (co-04)
4. **ex-04 · high-level-diagram** — a boxes-and-arrows Mermaid diagram of the major components — verify
   every component has a stated purpose. (co-05)
5. **ex-05 · api-sketch** — the key endpoints/operations with inputs and outputs — verify each maps to a
   functional requirement. (co-06)
6. **ex-06 · data-model** — entities + relationships + primary access patterns — verify the model
   supports the API. (co-07)
7. **ex-07 · storage-choice-justified** — pick SQL or NoSQL from the access patterns — verify the choice
   cites the pattern, not preference. (co-07, co-16)
8. **ex-08 · deep-dive-one-component** — expand one component (e.g. the write path) to internals — verify
   the depth matches interviewer interest. (co-20)
9. **ex-09 · name-the-bottleneck** — identify where the design breaks first at the estimated scale —
   verify the bottleneck ties to a number from ex-03. (co-15)
10. **ex-10 · state-two-tradeoffs** — articulate two design choices with both sides — verify each names a
    benefit and a cost. (co-16)
11. **ex-11 · drive-the-round** — a transcript where the candidate leads with a plan and checkpoints —
    verify the candidate set the agenda, not the interviewer. (co-21)
12. **ex-12 · closing-summary** — a crisp recap of the design, its limits, and next steps — verify it
    names the biggest risk. (co-01, co-15)

### Theme B · Scaling & data (ex 13–26)

1. **ex-13 · stateless-web-tier** — scale the request tier horizontally behind a load balancer — verify
   the design removes server-local state. (co-08)
2. **ex-14 · load-balancer-choices** — pick a balancing strategy + health checks — verify the choice
   fits the traffic shape. (co-09)
3. **ex-15 · read-replica-scaling** — add read replicas for a read-heavy workload — verify the
   replication lag trade-off is stated. (co-11, co-12)
4. **ex-16 · sharding-strategy** — shard a write-heavy table by a key — verify the hot-shard risk is
   named. (co-11, co-15)
5. **ex-17 · cache-placement** — choose where to cache for a hot read path — verify the invalidation
   approach is stated. (co-10)
6. **ex-18 · cache-stampede-mitigation** — prevent a thundering-herd on cache miss — verify a concrete
   mitigation (lock/stale-while-revalidate). (co-10, co-17)
7. **ex-19 · consistency-choice** — pick strong vs eventual consistency for a feature — verify the
   choice cites the product need. (co-12)
8. **ex-20 · async-queue-offload** — move slow work to a queue + workers — verify the request path
   latency drops and the durability of the queue is addressed. (co-13)
9. **ex-21 · idempotency-and-retries** — make a queued operation safe to retry — verify duplicate
   delivery does not double-apply. (co-13, co-17)
10. **ex-22 · rate-limiter-design** — design a rate limiter (token bucket) as a deep dive — verify the
    algorithm and the storage of counters are specified. (co-14)
11. **ex-23 · cdn-for-static-and-media** — offload static/media to a CDN — verify the cache-control and
    origin-shielding are noted. (co-10, co-08)
12. **ex-24 · hot-key-handling** — handle a viral hot key that overwhelms one shard — verify a concrete
    spread strategy. (co-15, co-11)
13. **ex-25 · write-amplification-tradeoff** — a fan-out-on-write vs fan-out-on-read choice (feed
    problem) — verify both costs are stated. (co-16, co-11)
14. **ex-26 · storage-sizing-drives-choice** — let the ex-03 storage estimate drive the DB and
    partitioning choice — verify the number justifies the design. (co-04, co-19)

### Theme C · Reliability, operability & altitude (ex 27–38)

1. **ex-27 · failure-mode-walkthrough** — walk what happens when the primary DB fails — verify failover
   - data-loss window are addressed. (co-17)
2. **ex-28 · timeouts-and-circuit-breakers** — protect a slow downstream dependency — verify the
   degradation behavior is specified. (co-14, co-17)
3. **ex-29 · availability-target-math** — translate a "three nines" target into a redundancy design —
   verify the target drives concrete redundancy. (co-19, co-17)
4. **ex-30 · observability-plan** — name the metrics, logs, and alerts for the design — verify each ties
   to a failure mode. (co-18)
5. **ex-31 · degrade-gracefully** — design a graceful-degradation path under overload — verify the core
   function survives a non-core outage. (co-14, co-17)
6. **ex-32 · altitude-shift-on-cue** — a transcript that drops into a component's internals when the
   interviewer probes, then zooms back out — verify both altitudes appear. (co-20)
7. **ex-33 · cost-as-a-driver** — factor infrastructure cost into a design choice — verify a cheaper
   option is weighed against its downside. (co-19, co-16)
8. **ex-34 · migration-and-rollout** — sketch how the design would be rolled out or migrated to safely —
   verify a reversible plan. (co-22, co-17)
9. **ex-35 · multi-region-consideration** — decide whether the prompt needs multi-region and justify —
   verify the decision cites the requirement. (co-12, co-19)
10. **ex-36 · staff-level-ambiguity** — handle an intentionally ambiguous staff-level prompt — verify the
    candidate frames the ambiguity into decisions. (co-22, co-03)
11. **ex-37 · cross-cutting-concerns** — surface security, privacy, and org/ownership concerns at staff
    altitude — verify at least two cross-cutting concerns are raised. (co-22)
12. **ex-38 · self-score-a-design** — grade a design transcript against the rubric (scoping, estimation,
    breadth, depth, communication, trade-offs) — verify each axis is rated. (co-01, co-22)

### Theme D · Full mock walkthroughs (ex 39–44)

1. **ex-39 · design-a-url-shortener** — full spine walkthrough of a URL shortener — verify every spine
   step and one deep dive appear. (co-01–co-16)
2. **ex-40 · design-a-news-feed** — full walkthrough of a feed with the fan-out trade-off deep-dived —
   verify the write-vs-read choice is justified. (co-01–co-22)
3. **ex-41 · design-a-chat-system** — full walkthrough of a real-time chat (delivery, presence,
   ordering) — verify the consistency + async choices are stated. (co-12, co-13, co-17)
4. **ex-42 · design-a-rate-limited-api-gateway** — full walkthrough centered on rate limiting +
   reliability — verify the limiter deep dive and failure modes. (co-14, co-17)
5. **ex-43 · design-a-typeahead-search** — full walkthrough of an autocomplete service — verify the
   caching + data-structure choice is justified. (co-10, co-07)
6. **ex-44 · capstone-mock-design-round** — a complete timed mock with a self-scored rubric and a final
   diagram — verify the spine, one deep dive, bottlenecks, and trade-offs all appear and are rated.
   (co-01–co-22)

## Capstone spec — intra-topic (concept → design/decision artifact)

- **Goal**: run a complete self-administered, timed system-design round on a fresh prompt, producing a
  scored walkthrough that covers the full spine (clarify → estimate → high-level → deep-dive →
  bottlenecks → trade-offs) with a final architecture diagram and a rubric self-score.
- **Concepts exercised**: [ ] functional/non-functional split + scope (co-02, co-03) [ ] capacity
  estimate (co-04) [ ] high-level design + API + data model (co-05–co-07) [ ] one deep dive with
  altitude control (co-20) [ ] bottleneck + two trade-offs (co-15, co-16) [ ] reliability +
  observability (co-17, co-18) [ ] rubric self-score (co-01, co-22).
- **Ordered steps**:
  1. `system-design-interview/learning/capstone/prompt.md` — a fresh prompt + a timer budget + the
     rubric. Verify the rubric lists all scored axes.
  2. `system-design-interview/learning/capstone/walkthrough.md` + a Mermaid diagram — the full spine
     transcript. Verify every spine step and one deep dive appear.
  3. `system-design-interview/learning/capstone/scoresheet.md` — self-score against the rubric. Verify
     every axis is rated with a justification.
- **Acceptance criteria**: the walkthrough covers the full spine with a legible diagram, names at least
  one bottleneck and two trade-offs, addresses a failure mode, and is self-scored on every rubric axis.
- **Done bar**: produces the stated artifact (scored walkthrough + diagram) + web-verified.

## Read more

- **Designing Data-Intensive Applications** — Martin Kleppmann. The authoritative reference for the
  data, consistency, and scaling reasoning the round draws on.
- **System Design Interview — An Insider's Guide** — Alex Xu. A widely used walkthrough of the round's
  common prompts (treat specific numbers as illustrative).

---

← Previous: N=13 `sql-essentials` ([index](./README.md)) · Next: N=15 `technical-communication`
([index](./README.md)) →
