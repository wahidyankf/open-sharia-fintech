---
title: "Overview"
date: 2026-07-29T00:00:00+07:00
draft: false
weight: 1
---

## Drills Overview

This page is the spaced-repetition companion to the Backend at Scale course: five fixed drills that force
active recall instead of passive re-reading. Work through them in order -- short-answer recall first, then
scenario judgment, then hands-on repetition against small, genuinely-executed Python fixtures, then a
self-check checklist, then why/why-not prompts that test whether you can explain the reasoning -- including
this topic's cross-cutting big ideas, `consistency-latency-throughput`, `taming-state`, and
`coupling-vs-cohesion` -- not just recite the status codes. Every answer is hidden in a `<details>` block;
try each item yourself before opening it.

## Drill List

### Recall Q&A

Forty short-answer questions, one per concept (`co-01` through `co-40`). Answer from memory, then check.

**Q1 (co-01 -- rest-method-semantics).** Which HTTP methods are idempotent per RFC 9110, and what does
"idempotent" guarantee about calling the same request twice?

<details>
<summary>Answer</summary>

GET, HEAD, PUT, DELETE, OPTIONS, and TRACE are idempotent; POST and PATCH are not (Examples 1-2).
Idempotent means calling the identical request N times produces the SAME end state as calling it once --
two identical PUTs leave the resource identical; two identical POSTs (without an Idempotency-Key) create
two resources.

</details>

**Q2 (co-02 -- http-status-codes).** What is the difference between 401 and 403, and which status signals
"well-formed but semantically invalid"?

<details>
<summary>Answer</summary>

401 = authentication required and has failed or not been provided ("who are you?"); 403 = the server
refuses to authorize a valid identity that lacks permission ("I know you, but no") (Example 6). 422
"Unprocessable Content" (RFC 9110 Sec 15.5.21) signals a well-formed body with a semantically invalid
value (Example 8) -- distinct from 400's malformed shape.

</details>

**Q3 (co-03 -- api-versioning).** Name two versioning strategies and a real API each traces to.

<details>
<summary>Answer</summary>

URI-path versioning (`/v1/...`, Example 9, Google AIP-185) and header versioning (Example 10, Stripe's
`Stripe-Version`). A third is query-param versioning (Microsoft Azure's `api-version`). Each is a genuine
trade-off in cache compatibility and discoverability, not a strictly-better option.

</details>

**Q4 (co-04 -- offset-pagination).** What cost does `offset`/`limit` pagination pay that cursor pagination
avoids?

<details>
<summary>Answer</summary>

OFFSET fetches-and-discards every preceding row: to serve `offset=5000,limit=10` it walks past 5000 rows
before returning 10 (Example 12). The cost grows linearly with page depth and drifts under concurrent
inserts. A cursor (co-05) resumes from a position in the data and avoids both.

</details>

**Q5 (co-05 -- cursor-pagination).** Why is a cursor stable under concurrent inserts when an offset is not?

<details>
<summary>Answer</summary>

A cursor anchors to a position IN THE DATA (the last-seen id, `WHERE id > cursor`), so a row inserted
elsewhere does not shift it (Example 14). An offset is a raw position count, so a new row near the front
shifts every later position -- the offset page skips or repeats a row.

</details>

**Q6 (co-06 -- idempotency-key).** Walk through what happens on a first POST with an Idempotency-Key, a
REPLAY, and a REUSE with a different body.

<details>
<summary>Answer</summary>

First call: the server records key -> response and returns normally (Example 15). A REPLAY of the same
key returns the ORIGINAL recorded response (200), creating nothing new (Example 16). A REUSE of the same
key with a DIFFERENT body is a client bug and is REJECTED, not silently applied (Example 17). This follows
Stripe prior art; the IETF draft for the header is lapsed.

</details>

**Q7 (co-07 -- graphql-vs-rest).** What problem does GraphQL's client-specified field selection solve, and
what pitfall comes with it?

<details>
<summary>Answer</summary>

It solves REST's over/under-fetching: the caller's query names exactly which fields to return (Examples
51-52). The pitfall is the resolver N+1 -- a naive resolver issues one query per item across a list,
fixed by DataLoader-style batching (Example 53, co-40).

</details>

**Q8 (co-08 -- grpc-protobuf-http2).** What is Protobuf's dual role in gRPC, and name two RPC kinds.

<details>
<summary>Answer</summary>

Protobuf is BOTH the interface-definition language (`.proto`) AND the wire format -- one artifact defines
the contract and the binary encoding (unlike REST's separation of OpenAPI from JSON). RPC kinds include
unary (Example 54) and server-streaming (Example 55); also client-streaming and bidirectional.

</details>

**Q9 (co-09 -- repository-pattern).** What does a Repository mediate, and why?

<details>
<summary>Answer</summary>

A Repository mediates between the domain and the data store with a collection-like interface (add/get/
all/remove), so the domain never touches the storage mechanism (Examples 18-19, Fowler PoEAA). This lets
the backend be swapped without touching domain logic.

</details>

**Q10 (co-10 -- unit-of-work).** What does a Unit of Work coordinate, and when does it write out?

<details>
<summary>Answer</summary>

A UoW maintains a list of objects affected by a business transaction and coordinates writing them out ALL
at once on `commit()` (Example 20) -- or discarding them all on `rollback()` (Example 21, Fowler PoEAA).

</details>

**Q11 (co-11 -- transactions-acid).** What does atomicity guarantee for a multi-write transaction?

<details>
<summary>Answer</summary>

All writes commit together, or all roll back -- never half-applied (Example 22). A debit and a credit
commit atomically, or the books stay balanced.

</details>

**Q12 (co-12 -- dual-write-problem).** Why can writing to a DB and a broker not be made atomic, and what
is lost?

<details>
<summary>Answer</summary>

The two writes are to different systems with no shared transaction; a crash between them leaves the DB
write committed but the message LOST (Example 63). The lost message is the specific failure mode the
outbox solves.

</details>

**Q13 (co-13 -- transactional-outbox).** How does the transactional outbox make "update the DB and send a
message" atomic?

<details>
<summary>Answer</summary>

The message is written INTO the DB as part of the same transaction, then a separate relay publishes it --
so it is "sent if and only if the transaction commits" (Examples 64-65, microservices.io). A rollback
discards the message; a commit guarantees it will be published.

</details>

**Q14 (co-14 -- jwt).** How is a JWT verified without a session lookup, and how is expiry enforced?

<details>
<summary>Answer</summary>

A JWT is signed (HMAC-SHA256 over header.payload); the receiver recomputes the signature to verify it --
stateless, no session store (Example 23). An `exp` claim lets the receiver reject any token whose expiry
is in the past (Example 24).

</details>

**Q15 (co-15 -- oauth2-vs-oidc).** What does OAuth 2.0 grant, and what does OpenID Connect add?

<details>
<summary>Answer</summary>

OAuth 2.0 grants AUTHORIZATION (what you may do, RFC 6749, Example 29). OpenID Connect adds an IDENTITY
layer for AUTHENTICATION -- an id_token (a JWT) whose claims say WHO you are (Example 30). OAuth 2.1 is
still an IETF draft, not a finalized RFC.

</details>

**Q16 (co-16 -- pkce).** What attack does PKCE prevent, and for which clients is it mandated?

<details>
<summary>Answer</summary>

PKCE prevents authorization-code interception: the client sends a derived challenge and redeems the code
with the secret verifier, so an interceptor with the code but not the verifier is blocked (Example 31).
RFC 9700 MANDATES PKCE for public clients (SPAs, mobile apps).

</details>

**Q17 (co-17 -- rbac-vs-abac).** Contrast RBAC and ABAC, and name when each fits.

<details>
<summary>Answer</summary>

RBAC maps users -> roles -> privileges (Example 25, NIST model): auditable but coarse. ABAC decides from
rules over attributes (Example 26): flexible but harder to manage. RBAC fits stable role hierarchies;
ABAC fits dynamic policies like "only the owner."

</details>

**Q18 (co-18 -- refresh-token-rotation).** What does rotation do, and what does reuse detection do?

<details>
<summary>Answer</summary>

Rotation issues a NEW single-use refresh token on every use, so the old one is immediately invalid
(Example 32). Reuse detection revokes the ENTIRE token family when an already-rotated token reappears,
signaling theft (Example 33). RFC 9700 requires sender-constraint OR rotation for public clients.

</details>

**Q19 (co-19 -- rate-limit-algorithms).** Which algorithm allows bursts, and which one has a boundary-burst
flaw?

<details>
<summary>Answer</summary>

The token bucket allows bursts up to capacity (Example 34, AWS API Gateway). The fixed window has a
boundary-burst flaw -- 2x the limit across a window edge (Example 36). The sliding window avoids that
flaw (Example 37, Cloudflare).

</details>

**Q20 (co-20 -- rate-limit-429-retry-after).** What status and header communicate a throttle, and what
does the header tell the caller?

<details>
<summary>Answer</summary>

429 Too Many Requests with a Retry-After header (Example 38, RFC 6585). Retry-After tells the caller how
many seconds (or a date) to wait before retrying -- actionable guidance, not a bare rejection.

</details>

**Q21 (co-21 -- cache-aside).** Describe the cache-aside read path and what it avoids on a hit.

<details>
<summary>Answer</summary>

On a MISS, read the DB, populate the cache, return; on a HIT, return straight from the cache (Examples
39-40). A hit issues ZERO DB queries -- the cache absorbs the DB load.

</details>

**Q22 (co-22 -- write-through-cache).** How does write-through keep reads fresh?

<details>
<summary>Answer</summary>

Write-through updates the cache SYNCHRONOUSLY on every write (Example 41), so reads are always fresh
without waiting for a TTL or a lazy reload.

</details>

**Q23 (co-23 -- cache-ttl-invalidation).** Why is a too-long TTL a correctness bug?

<details>
<summary>Answer</summary>

A TTL longer than the data's real freshness window serves STALE data: the DB changes but the cache keeps
returning the old value until the over-long TTL expires (Example 44). The fix is a correct TTL PLUS
explicit invalidation on writes (Examples 42-43).

</details>

**Q24 (co-24 -- http-caching-etag).** How does ETag + If-None-Match avoid re-sending an unchanged resource?

<details>
<summary>Answer</summary>

The server tags a representation with an opaque ETag; a client resending If-None-Match with the SAME tag
gets 304 with no body when unchanged (Example 45). Cache-Control: max-age lets a cache skip asking the
origin entirely for a bounded window (Example 46).

</details>

**Q25 (co-25 -- structured-logging-correlation).** Why thread a correlation id through every log line?

<details>
<summary>Answer</summary>

A correlation (request) id minted at the request boundary and carried on EVERY structured JSON log line
groups all of a request's lines together in an aggregator, across functions and services (Examples 27-28).

</details>

**Q26 (co-26 -- distributed-tracing-otel).** What does a traceparent propagate, and why?

<details>
<summary>Answer</summary>

A W3C traceparent (version-traceid-spanid-flags) carries the trace identity across a service-to-service
call, so a request can be followed across services (Example 48). OpenTelemetry spans (Example 47) record
each unit of work; the traceparent ties them into one trace.

</details>

**Q27 (co-27 -- health-checks-liveness-readiness).** What is the difference between a liveness failure
and a readiness failure?

<details>
<summary>Answer</summary>

A liveness failure causes the orchestrator to RESTART the container (Example 49). A readiness failure
removes the pod from the Service's endpoints WITHOUT restarting it -- it stops getting traffic while a
dependency is down (Example 50).

</details>

**Q28 (co-28 -- at-least-once-delivery).** Why can an at-least-once consumer see the same message twice?

<details>
<summary>Answer</summary>

The broker redelivers a message if the consumer does not ack -- so a crash before acking means the same
message is handed over again (Example 58). This is why an idempotent consumer (co-29) is mandatory.

</details>

**Q29 (co-29 -- idempotent-consumer).** How does an idempotent consumer keep a duplicate delivery harmless?

<details>
<summary>Answer</summary>

It records every processed message id and DISCARDS duplicates, so a redelivery has no effect (Example 59)
-- the side effect happens exactly once (Example 60). Dedup by message id, never by payload.

</details>

**Q30 (co-30 -- dead-letter-queue).** When does a message land in a DLQ?

<details>
<summary>Answer</summary>

When a poison message exceeds maxReceiveCount (it keeps failing), the broker moves it to a dead-letter
queue for later inspection instead of redelivering it forever (Example 61, AWS SQS DLQ).

</details>

**Q31 (co-31 -- backpressure).** How does a bounded queue protect a slow consumer?

<details>
<summary>Answer</summary>

A bounded queue caps in-flight work; when it is FULL, the producer is rejected (or blocks) rather than
piling up unbounded work (Example 62). Backpressure bounds load at the source.

</details>

**Q32 (co-32 -- webhook-hmac).** Why sign a webhook with HMAC when it is already sent over HTTPS?

<details>
<summary>Answer</summary>

HTTPS protects the payload in transit; it says nothing about WHO called the receiving endpoint. An HMAC
signature (verified in constant time) authenticates the sender (Examples 66-67). A tampered body produces
a different digest and is rejected.

</details>

**Q33 (co-33 -- websocket-vs-sse).** Contrast WebSocket and SSE, and when each fits.

<details>
<summary>Answer</summary>

WebSocket is full-duplex bidirectional over one TCP connection (Example 69, RFC 6455) -- fits when the
client also pushes. SSE is one-way server->client push over plain HTTP (Example 70, WHATWG HTML) --
simpler when the client only listens.

</details>

**Q34 (co-34 -- broker-backplane).** Why do multi-node real-time deployments need a pub/sub backplane?

<details>
<summary>Answer</summary>

Connections are sticky to one node; a broadcast from one node only reaches its own clients. A shared
pub/sub backplane fans the message out so clients on EVERY node receive it (Example 71).

</details>

**Q35 (co-35 -- contract-testing-pact).** What does a consumer-driven contract test verify?

<details>
<summary>Answer</summary>

The consumer declares the request it sends and the response it expects, generating a contract; provider
verification checks the provider HONOURS it (Example 78, pact.io). It catches provider drift that would
break a consumer without a full integration environment.

</details>

**Q36 (co-36 -- test-containers).** Why spin up a containerized dependency instead of a mock?

<details>
<summary>Answer</summary>

A containerized dependency is a REAL engine, not a mock that drifts from production behavior (Example 79,
testcontainers.com). Each test gets a fresh, isolated, ephemeral instance, then tears it down.

</details>

**Q37 (co-37 -- circuit-breaker).** What are the three breaker states, and what does "fail fast" mean?

<details>
<summary>Answer</summary>

Closed (calls go through), open (calls fail FAST without hitting the dependency), and half-open (one probe
trial) (Example 72). "Fail fast" means while open, a call returns immediately instead of waiting on a
failing dependency -- stopping cascading failure.

</details>

**Q38 (co-38 -- retry-backoff-jitter).** Why add full jitter to exponential backoff?

<details>
<summary>Answer</summary>

Plain exponential backoff CLUSTERS retries -- many clients failing at once retry at base*2^n together,
a synchronized storm. Full jitter (`sleep = random(0, min(cap, base*2^attempt))`) de-synchronizes them
(Examples 73-74, AWS Brooker 2015).

</details>

**Q39 (co-39 -- timeout-bulkhead).** What do a timeout and a bulkhead each protect against?

<details>
<summary>Answer</summary>

A timeout caps how long a call may wait, aborting at the deadline so a slow dependency does not hang a
request thread (Example 75). A bulkhead isolates resource pools so saturation in one does not starve the
others (Example 76).

</details>

**Q40 (co-40 -- connection-pool-n-plus-1).** What is the N+1 query, and what are the two fixes?

<details>
<summary>Answer</summary>

Accessing related objects in a loop issues one query per row (1 + N). Fix it with a JOIN / batched
prefetch (Example 53's DataLoader batch) AND reuse pooled connections to avoid reopen cost (Example 77).

</details>

### Applied problems

Scenarios. Each describes a task without naming the construct -- decide which pattern solves it, then
check.

**AP1.** A client's HTTP library auto-retries a `POST /orders` after a network timeout, and you are seeing
duplicate orders.

<details>
<summary>Answer</summary>

An Idempotency-Key header on the write, checked server-side before creating anything new (co-06; Examples
15-16). The retry carries the SAME key, so the server returns the original response instead of a second
order.

</details>

**AP2.** A list endpoint gets slower the deeper you page, and rows sometimes repeat or vanish under load.

<details>
<summary>Answer</summary>

Switch from offset/limit to cursor (keyset) pagination (co-05; Examples 13-14). A cursor resumes from a
position in the data, avoiding the fetch-and-discard cost (co-04) and staying stable under concurrent
inserts.

</details>

**AP3.** You update the database but the cache keeps serving the old value until a 10-minute TTL expires.

<details>
<summary>Answer</summary>

Explicitly invalidate the cached key on every mutation, and set a TTL that matches the data's real
freshness window (co-23; Examples 43-44). The wrong TTL is a correctness bug.

</details>

**AP4.** A misbehaving integrator's runaway retry loop is hammering your write endpoint.

<details>
<summary>Answer</summary>

Rate-limit with a token bucket (or sliding window) returning 429 + Retry-After (co-19/co-20; Examples
34-38). Retry-After tells the client exactly how long to back off.

</details>

**AP5.** A background worker crashes after debiting a wallet but before acking, and you see double-debits.

<details>
<summary>Answer</summary>

Make the consumer idempotent: record processed message ids and dedup (co-29; Examples 59-60). At-least-
once delivery (co-28) means redeliveries are expected; idempotency keeps the effect once.

</details>

**AP6.** You commit an order to the DB and then publish an event to a broker, but sometimes the event is
lost when the process restarts.

<details>
<summary>Answer</summary>

Use the transactional outbox: write the event into the DB in the same transaction, then relay it
separately (co-13; Examples 64-65). Sent iff the transaction commits; the dual-write problem (co-12) is
solved.

</details>

**AP7.** A downstream service is failing, and every request to your service hangs on it until your own
threads are exhausted.

<details>
<summary>Answer</summary>

Add a circuit breaker (fail fast while the dependency is down, co-37; Example 72), a timeout so calls
abort at a deadline (co-39; Example 75), and bulkheads to isolate pools (co-39; Example 76).

</details>

**AP8.** You need to test against a real database engine but mocks keep drifting from production behavior.

<details>
<summary>Answer</summary>

Use testcontainers to spin up an ephemeral, real containerized DB per test (co-36; Example 79), and a
Pact consumer-driven contract to catch provider drift (co-35; Example 78).

</details>

### Code katas

Six hands-on repetition drills against small, self-contained, genuinely-executed Python fixtures -- pure
standard library, no external dependency. Each is a before/after `kata.py` file colocated under
`drilling/code/`. Every "before" script misapplies a concept this course teaches -- run it, diagnose the
bug from the observed output, fix it from memory, then compare against the "after" script.

#### Kata 1 -- A 429 without a Retry-After hint

The over-limit path returns 429 but omits `Retry-After`, so a client has no machine-readable wait hint.
**Before**: `drilling/code/kata-01-rate-limit-returns-429-without-retry-after/before/kata.py`. **Fix**:
include `Retry-After` (the "after" file). **Root cause**: co-20 (Example 38) -- Retry-After turns a bare
rejection into actionable guidance.

#### Kata 2 -- Cursor treated as an offset

The "cursor" is sliced as `ROWS[cursor:cursor+limit]` instead of `WHERE id > cursor`, so paging breaks on
non-contiguous ids. **Before**: `drilling/code/kata-02-cursor-page-resumes-after-wrong-key/before/kata.py`.
**Fix**: resume with `id > cursor`. **Root cause**: co-05 (Examples 13-14) -- a cursor is a key, not a row
offset.

#### Kata 3 -- Cache-aside never populates on a miss

On a miss the DB is queried but the value is returned WITHOUT writing it to the cache, so every read
misses again. **Before**: `drilling/code/kata-03-cache-aside-never-populates-on-miss/before/kata.py`.
**Fix**: `CACHE[key] = value` on a miss. **Root cause**: co-21 (Examples 39-40) -- lazy loading populates
on miss so the next read hits.

#### Kata 4 -- Dedup by payload instead of by message id

Two genuinely different messages with the same body are conflated, and the same body under different ids
is wrongly skipped. **Before**: `drilling/code/kata-04-idempotent-consumer-dedups-by-payload-not-id/before/kata.py`.
**Fix**: dedup on `msg.id`. **Root cause**: co-29 (Examples 59-60) -- the dedup key is the message id,
never the payload.

#### Kata 5 -- Outbox message written outside the transaction

The DB write and the outbox write are not atomic, so a crash between them loses the event (the dual-write
problem). **Before**: `drilling/code/kata-05-outbox-message-not-in-same-transaction/before/kata.py`.
**Fix**: stage both writes, commit together. **Root cause**: co-12/co-13 (Examples 63-64) -- the message
must be in the same transaction.

#### Kata 6 -- Circuit breaker stuck half-open

A half-open probe never closes on success and never re-opens on failure, so recovery never completes.
**Before**: `drilling/code/kata-06-circuit-breaker-never-half-opens/before/kata.py`. **Fix**: close on a
successful probe, re-open on a failed one. **Root cause**: co-37 (Example 72) -- half-open is a single
trial that transitions either way.

### Self-check checklist

Confirm each item without the manual first. If you hesitate, that concept needs another pass.

- [ ] I can name which HTTP methods are idempotent and demonstrate it with a repeated call. (co-01)
- [ ] I can choose the right status among 201/204/400/401/403/409/422 for a scenario. (co-02)
- [ ] I can implement URI-path and header versioning and name a trade-off of each. (co-03)
- [ ] I can explain offset's fetch-and-discard cost. (co-04)
- [ ] I can implement cursor pagination and explain its stability under inserts. (co-05)
- [ ] I can implement Idempotency-Key record/replay/reject-on-mismatch. (co-06)
- [ ] I can explain GraphQL's field selection and the N+1 pitfall. (co-07)
- [ ] I can describe gRPC's Protobuf IDL+wire and two RPC kinds. (co-08)
- [ ] I can build a repository and swap its backend with callers unchanged. (co-09)
- [ ] I can build a unit of work that commits or rolls back all changes. (co-10)
- [ ] I can explain transaction atomicity (all-or-nothing). (co-11)
- [ ] I can describe the dual-write problem and what it loses. (co-12)
- [ ] I can implement the transactional outbox (sent iff committed). (co-13)
- [ ] I can hand-roll a JWT encode/verify and enforce expiry. (co-14)
- [ ] I can explain OAuth2 (authorization) vs OIDC (authentication). (co-15)
- [ ] I can generate a PKCE challenge and reject a wrong verifier. (co-16)
- [ ] I can build an RBAC gate and an ABAC owner policy. (co-17)
- [ ] I can implement refresh-token rotation and reuse detection. (co-18)
- [ ] I can implement the four rate-limit algorithms and name the boundary flaw. (co-19)
- [ ] I can return 429 + Retry-After. (co-20)
- [ ] I can implement cache-aside and prove a hit issues no DB query. (co-21)
- [ ] I can implement write-through. (co-22)
- [ ] I can explain TTL expiry, explicit invalidation, and the stale-TTL bug. (co-23)
- [ ] I can implement ETag/If-None-Match (304) and Cache-Control. (co-24)
- [ ] I can emit structured JSON logs with a correlation id. (co-25)
- [ ] I can record an OTel span and propagate a traceparent. (co-26)
- [ ] I can distinguish liveness (restart) from readiness (drop traffic). (co-27)
- [ ] I can explain at-least-once redelivery. (co-28)
- [ ] I can build an idempotent consumer that applies an effect once. (co-29)
- [ ] I can move a poison message to a DLQ after maxReceiveCount. (co-30)
- [ ] I can bound a queue to apply backpressure. (co-31)
- [ ] I can HMAC-sign a webhook and verify it in constant time. (co-32)
- [ ] I can contrast WebSocket (full-duplex) and SSE (one-way). (co-33)
- [ ] I can explain why multi-node fanout needs a pub/sub backplane. (co-34)
- [ ] I can describe a consumer-driven Pact contract. (co-35)
- [ ] I can describe testcontainers vs mocks. (co-36)
- [ ] I can implement a circuit breaker (closed/open/half-open). (co-37)
- [ ] I can add full jitter to exponential backoff and say why. (co-38)
- [ ] I can implement a timeout guard and a bulkhead. (co-39)
- [ ] I can pool connections and fix an N+1 with a batch. (co-40)

### Elaborative interrogation & self-explanation

Answer each in your own words before opening the model explanation.

**E1.** Why do caching, rate limiting, and pagination all count as `consistency-latency-throughput`
decisions, when none is explicitly about a database's consistency model?

<details>
<summary>Model explanation</summary>

Each trades latency, throughput, or correctness. Pagination trades simplicity for a fetch-and-discard
latency cost (offset) vs flat latency (cursor). Rate limiting is a throughput decision -- protecting total
sustainable load at the cost of a throttled caller's latency. Caching trades a staleness (consistency)
budget for latency and throughput. None requires a literal database, but each sits on the same trade-off
surface.

</details>

**E2.** Why does an Idempotency-Key matter specifically for POST, when PUT is already idempotent?

<details>
<summary>Model explanation</summary>

PUT's idempotency comes from its own semantics (replace this exact representation) -- repeating it
naturally produces the same end state. POST's semantics are "create new" or "process this" -- repeating
correctly creates a second resource, which is wrong for a RETRY the client can't distinguish from a new
request. The Idempotency-Key adds an explicit, opt-in idempotency guarantee onto an operation whose HTTP
semantics don't provide one.

</details>

**E3.** Why is at-least-once delivery not a bug, and why does it make an idempotent consumer mandatory?

<details>
<summary>Model explanation</summary>

At-least-once is a deliberate reliability choice: redeliver on a failed ack so a crash never silently
drops a message. The cost is that a consumer may see the same message twice. That cost is acceptable ONLY
if the consumer is idempotent -- dedup by id and apply the effect once -- otherwise the reliability
guarantee becomes a correctness bug.

</details>

**E4.** Why does the transactional outbox write the message INTO the database, instead of just retrying the
broker publish?

<details>
<summary>Model explanation</summary>

Retrying the broker publish doesn't make it atomic with the DB write -- a crash can still leave the DB
committed and the message lost (the dual-write problem). Writing the message into the DB as part of the
same transaction means the message's existence is guaranteed by the same atomic commit as the business
write; a separate relay then publishes it. "Sent iff the transaction commits" is only achievable when the
message and the business write share one commit boundary.

</details>

## Difficulty Progression

The drills escalate in three bands. The **Recall Q&A** is pure retrieval -- name the concept from memory.
The **Applied problems** add a layer of recognition -- read a scenario and pick the right construct without
it being named. The **Code katas** add execution -- diagnose a real bug from observed output and fix it
from memory. The **Self-check checklist** is automaticity -- you should answer without hesitation. The
**Elaborative interrogation** is the deepest -- explain WHY, including the cross-cutting big ideas. Work
the bands in order; if you can do the katas but stumble on the elaborative prompts, the "why" layer needs
another pass.

## Evaluation Criteria

You are ready to move on when: (1) you can answer all 40 recall questions without the manual; (2) you
correctly match every applied problem to its construct; (3) you can fix all six katas from memory and
explain each root cause by its `co-NN`; (4) every self-check item is an unhesitating "yes"; and (5) you
can give the model explanation for each elaborative prompt in your own words. The capstone is the final
check: if you can build its four steps from the patterns alone, the drilling has done its job.

## Capstone Integration

Every capstone step exercises a drilled concept directly. **Step 1** (rest.py) combines co-03 (versioning),
co-05 (cursor pagination), and co-06 (idempotency) -- drilled in Recall Q3/Q5/Q6 and Katas 1-2. **Step 2**
(auth.py) combines co-15 (OAuth2/OIDC) and co-17 (RBAC) -- drilled in Recall Q15/Q17. **Step 3**
(resilience.py) combines co-20 (429), co-21 (cache-aside), and co-25 (structured logging) -- drilled in
Recall Q20/Q21/Q25 and Kata 3. **Step 4** (queue.py) combines co-28 (at-least-once), co-29 (idempotent
consumer), and co-35 (contract testing) -- drilled in Recall Q28/Q29/Q35 and Katas 4-5. The capstone's
acceptance criteria are the evaluation criteria made runnable: if the four steps pass end to end, the
drilled concepts compose correctly under one roof.

---

← Previous: [Capstone](../learning/capstone/overview.md)
