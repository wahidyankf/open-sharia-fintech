# 39 · Backend at Scale (By Example, Python)

**prd row**: Pass 3 · Build for the Real World · By Example · Python · Learn 139 / Drill 239 · Nvim-ready
Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: the deep backend pass — API design (REST/GraphQL/gRPC), persistence patterns, deep
AuthN/Z, reliability (logging/rate-limiting/caching), async/messaging, and applied integration/contract
testing. The usable slice is the prerequisite [`11-backend-essentials`](./11-backend-essentials.md);
system-level scaling is [`44-system-design`](./44-system-design.md).

## Why this exists · the big idea

- **The problem before the solution**: an endpoint that works for one user melts under real load, retries,
  and partial failure — correctness under concurrency and failure is a different problem than correctness
  on the happy path.
- **Keep-this-if-you-forget-everything**: at scale, design for the retry and the failure — idempotency,
  backpressure, and decoupling via queues are what let a service survive load instead of amplifying it.
- **Big ideas touched**: `consistency-latency-throughput` (caching/rate-limiting/pagination are throughput
  management), `taming-state` (idempotency quarantines duplicate-effect state), `coupling-vs-cohesion`
  (async messaging decouples producers from consumers).

## Prerequisites

- **Prior topics**: [topic 11 Backend Essentials](./11-backend-essentials.md) (routing, validation, DB
  access), [topic 10 SQL Essentials](./10-sql-essentials.md), [topic 17 Security Essentials](./17-security-essentials.md)
  (auth to deepen), and [topic 15 Software Testing](./15-software-testing.md) (integration/contract tests).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** with a pinned CVE-clean web framework;
  a local SQL DB + a queue/broker (Valkey/Redis stream fine); `curl`; a contract-test tool (Pact) and
  test-containers concept.
- **Assumed knowledge**: building/serving a CRUD JSON API (topic 11); tokens vs sessions (topic 17);
  writing an integration test (topic 15).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified (CORRECTION/UPDATE): the authoritative OAuth security source is **RFC 9700
  "Best Current Practice for OAuth 2.0 Security"** (IETF, Jan 2025) — deprecates the Implicit Grant and
  ROPC Grant, mandates PKCE for public clients. **OAuth 2.1 is still an IETF draft** (draft-ietf-oauth-v2-1-15,
  March 2026) — NOT a finalized RFC as of July 2026. Cite OAuth 2.0 + RFC 9700 as the settled standard and
  describe OAuth 2.1 as "in-progress consolidation," not a finalized spec. (datatracker.ietf.org/doc/rfc9700)
- 2026-07-12 — verified: gRPC/GraphQL and Pact tooling have no concrete version claim in the body yet —
  re-verify specific tool versions/commands once drafted.

> DD-35 primary-source pass (2026-07-12). Every citation traces to a source the author fetched and
> read; unverifiable specifics flagged `[Needs Verification]`, never guessed. Keep exact in `learning/code/`.

- **HTTP method safety/idempotency** — safe: GET, HEAD, OPTIONS, TRACE; idempotent: GET, HEAD, PUT,
  DELETE, OPTIONS, TRACE. **POST is not idempotent; PATCH is neither safe nor idempotent.** Source:
  [RFC 9110 (HTTP Semantics)](https://www.rfc-editor.org/rfc/rfc9110.html) §9.2.1–9.2.2, IETF, 2022 (STD 97).
- **Status codes** — 401 = "authentication required and has failed or not been provided"; 403 = server
  "refuses to authorize" (valid auth, insufficient permission); 409 = conflict with resource state;
  429 = "too many requests" (rate limiting), may carry `Retry-After`. Source: RFC 9110 §15 + [RFC 6585](https://www.rfc-editor.org/rfc/rfc6585.html) §4 (429).
- **422 rename (correction)** — RFC 9110 §15.5.21 defines **422 "Unprocessable Content"** (renamed from
  RFC 4918's WebDAV-era "Unprocessable Entity"); RFC 9110 does **not** obsolete RFC 4918 — they coexist.
  Teach "Unprocessable Content".
- **API versioning divergence** — path (Google [AIP-185](https://google.aip.dev/185): major version in the
  URI), query `api-version` (Microsoft [Azure REST guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md), "DO NOT include a version in the path"), header (Stripe `Stripe-Version`). Real industry disagreement — present as trade-offs, not one right answer.
- **Cursor vs offset pagination** — OFFSET makes the DB "fetch and discard" all preceding rows (SQL sorts
  then skips); keyset/cursor uses an indexed `WHERE` on the last-seen key, avoiding the scan and the
  duplicate/skip anomaly under concurrent inserts. Sources: [Use The Index, Luke — No Offset](https://use-the-index-luke.com/no-offset) (Markus Winand); [Stripe pagination](https://docs.stripe.com/api/pagination) (`starting_after`/`ending_before`).
- **Idempotency-Key (correction)** — the IETF draft `draft-ietf-httpapi-idempotency-key-header-07` is
  **EXPIRED/archived** (expired 2026-04-18), not an RFC and not currently active. Teach the pattern via
  Stripe prior art ([Idempotent requests](https://docs.stripe.com/api/idempotent_requests): store the first
  result under the key, replay returns it — even 500s; keys expire ~24h) and label the IETF draft "lapsed".
- **Repository / Unit of Work** — Repository: "collection-like interface for accessing domain objects";
  Unit of Work: "maintains a list of objects affected by a business transaction and coordinates writing
  out changes." Source: Martin Fowler, _PoEAA_ catalog ([Repository](https://martinfowler.com/eaaCatalog/repository.html), [Unit of Work](https://martinfowler.com/eaaCatalog/unitOfWork.html)).
- **Dual-write / Transactional Outbox** — "How to atomically update the database and send messages to a
  broker?" Solution: store the message in the DB **as part of the same transaction**, a separate process
  relays it — "sent if and only if the transaction commits." Source: [microservices.io Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html) (Chris Richardson).
- **Auth RFCs** — JWT [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519.html) (2015); OAuth 2.0
  [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749.html) (authorization framework); OIDC = "identity
  layer on top of OAuth 2.0" ([OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)) — so **OAuth2 = authorization, OIDC = authentication**. Security BCP
  [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html) (BCP 240, Jan 2025): Implicit grant "SHOULD NOT"
  be used, ROPC "MUST NOT" be used, public clients "MUST use PKCE" ([RFC 7636](https://www.rfc-editor.org/rfc/rfc7636.html)). **OAuth 2.1 is still an active IETF draft (`-15`, 2026), not an RFC.**
- **Refresh-token rotation (precision)** — RFC 9700 §2.2.2 requires public-client refresh tokens to be
  "sender-constrained **or** use refresh token rotation" — one of two mitigations, not an unconditional
  "rotate on every use" mandate. Don't overstate.
- **RBAC vs ABAC** — RBAC: users → roles → privileges (NIST model, Ferraiolo & Kuhn 1992, INCITS 359);
  ABAC: rule/attribute-based, flexible but harder to manage. Source: [NIST CSRC RBAC](https://csrc.nist.gov/projects/role-based-access-control).
- **Rate-limit algorithms** — token bucket (AWS API Gateway uses it, allows bursts;
  [AWS throttling docs](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)),
  leaky bucket, fixed window (boundary-burst flaw), sliding window (Cloudflare production). Token-bucket
  and sliding-window are `[Verified]` against vendor sources; **leaky-bucket & fixed-window exact
  attribution `[Needs Verification]`** (standard textbook material, aggregator-only sources found).
- **Caching** — cache-aside (lazy load: miss → DB → populate) and write-through (update cache on write)
  from [AWS Redis caching strategies](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html); write-behind wording `[Needs Verification]`. HTTP caching:
  `Cache-Control`, `ETag` + `If-None-Match` → 304, cache invalidation on unsafe methods
  ([RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html), 2022).
- **Observability** — OpenTelemetry = vendor-neutral traces/metrics/logs ([opentelemetry.io](https://opentelemetry.io/docs/what-is-opentelemetry/)); cross-service correlation via W3C
  [Trace Context](https://www.w3.org/TR/trace-context/) `traceparent`/`tracestate` (W3C Rec, 2021).
- **Health probes** — liveness failure → kubelet **restarts** the container; readiness failure → pod
  marked unready, **removed from Service endpoints** but not restarted. Source: [Kubernetes probes docs](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).
- **Idempotent consumer / DLQ** — at-least-once delivery means a consumer "can be invoked repeatedly for
  the same message"; fix by recording processed message IDs and discarding duplicates
  ([microservices.io Idempotent Consumer](https://microservices.io/patterns/communication-style/idempotent-consumer.html)). Dead-letter queue holds messages that fail after `maxReceiveCount`
  ([AWS SQS DLQ](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)).
- **Webhook signing** — GitHub `X-Hub-Signature-256` (HMAC-SHA256, constant-time compare;
  [GitHub validating deliveries](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries)); Stripe `Stripe-Signature` = `t=timestamp` + `v1=` HMAC over `timestamp.payload`, with a
  timestamp tolerance against replay ([Stripe webhooks](https://docs.stripe.com/webhooks)).
- **WebSocket vs SSE** — WebSocket = full-duplex bidirectional over one TCP connection
  ([RFC 6455](https://www.rfc-editor.org/rfc/rfc6455.html), 2011); SSE = one-way server→client push,
  `text/event-stream`, `EventSource`, part of the WHATWG [HTML Living Standard](https://html.spec.whatwg.org/multipage/server-sent-events.html). Broker-backplane scale-out claim (sticky connections need
  pub/sub to broadcast across nodes) is sound distributed-systems reasoning but has no single primary
  citation — flag `[Needs Verification]`, cite a vendor scaling guide when drafted.
- **Contract testing / Testcontainers** — Pact = "code-first consumer-driven contract testing tool"; the
  contract "is generated during the execution of the automated consumer tests" ([pact.io](https://docs.pact.io/)). Testcontainers = "ephemeral, lightweight Docker container instances … for automated testing"
  ([testcontainers.com](https://testcontainers.com/)).
- **Resilience** — circuit breaker: "wrap a protected call … once failures reach a threshold, the breaker
  trips" (closed/open/half-open), popularized by Nygard's _Release It!_ ([Fowler CircuitBreaker](https://martinfowler.com/bliki/CircuitBreaker.html)). Retries: plain exponential backoff clusters retries; use
  **Full Jitter** `sleep = random(0, min(cap, base·2^attempt))` ([AWS "Exponential Backoff and Jitter"](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/), Marc Brooker, 2015). Bulkhead
  attribution to _Release It!_ is `[Needs Verification]` (not directly fetched).
- **N+1 query** — accessing related objects in a loop issues one query per row; fixed with a JOIN /
  batched prefetch (`select_related`/`prefetch_related`). Source: [Django QuerySet docs](https://docs.djangoproject.com/en/stable/ref/models/querysets/#select-related). Connection-pooling concept is standard
  but lacked a strong primary source this pass — `[Needs Verification]` for a citation-grade reference.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject topic). Each example below cites the co-NN it exercises. -->

- **co-01 · rest-method-semantics** — GET/POST/PUT/PATCH/DELETE and which are safe (read-only) vs idempotent (repeatable) per RFC 9110; POST is neither.
- **co-02 · http-status-codes** — choosing the right status: 201 vs 202 vs 204, and 400/401/403/404/409/422/429 distinctions (esp. 401 auth-missing vs 403 forbidden).
- **co-03 · api-versioning** — evolving an API via URI path, header, or query-param versioning and the trade-off each carries.
- **co-04 · offset-pagination** — `offset`/`limit` paging and why the database fetches-and-discards every preceding row.
- **co-05 · cursor-pagination** — keyset/cursor paging on an indexed key that scales and is stable under concurrent inserts.
- **co-06 · idempotency-key** — an `Idempotency-Key` header so a retried POST does not double-apply (store the first result, replay it).
- **co-07 · graphql-vs-rest** — GraphQL's single endpoint + client-specified fields solving over/under-fetching, and its resolver N+1 pitfall.
- **co-08 · grpc-protobuf-http2** — gRPC's protobuf IDL over HTTP/2 with unary and streaming RPCs, for low-latency service-to-service calls.
- **co-09 · repository-pattern** — a collection-like interface mediating between the domain and the data store.
- **co-10 · unit-of-work** — tracking the objects changed in a business transaction and committing them together.
- **co-11 · transactions-acid** — an atomic commit boundary: all writes commit or all roll back.
- **co-12 · dual-write-problem** — writing to a DB and a broker cannot be made atomic; a crash between them loses a message.
- **co-13 · transactional-outbox** — storing the outbound message in the same DB transaction and relaying it separately, so it is sent iff the transaction commits.
- **co-14 · jwt** — a signed, self-contained claims token (RFC 7519) verified without a session lookup.
- **co-15 · oauth2-vs-oidc** — OAuth 2.0 grants **authorization**; OpenID Connect adds an identity layer for **authentication**.
- **co-16 · pkce** — the PKCE code-verifier/challenge that protects public clients from auth-code interception (mandated by the OAuth security BCP).
- **co-17 · rbac-vs-abac** — role-based vs attribute-based access control and when each fits.
- **co-18 · refresh-token-rotation** — short-lived access tokens with rotating refresh tokens, and detecting a reused (stolen) refresh token.
- **co-19 · rate-limit-algorithms** — token bucket, leaky bucket, fixed window, and sliding window, and their burst/accuracy trade-offs.
- **co-20 · rate-limit-429-retry-after** — returning `429 Too Many Requests` with a `Retry-After` hint when a client exceeds its budget.
- **co-21 · cache-aside** — lazy loading: on a miss, read the DB, populate the cache, return the value.
- **co-22 · write-through-cache** — updating the cache synchronously on every write so reads stay fresh.
- **co-23 · cache-ttl-invalidation** — TTL expiry plus explicit invalidation, and the staleness bug a wrong TTL causes.
- **co-24 · http-caching-etag** — `Cache-Control`, `ETag` + `If-None-Match`, and `304 Not Modified` conditional revalidation.
- **co-25 · structured-logging-correlation** — machine-parseable JSON logs carrying a correlation/request id across a request's lifetime.
- **co-26 · distributed-tracing-otel** — OpenTelemetry spans and W3C `traceparent` propagation to follow a request across services.
- **co-27 · health-checks-liveness-readiness** — a liveness probe (restart on failure) vs a readiness probe (drop from traffic while a dependency is down).
- **co-28 · at-least-once-delivery** — a broker redelivers on failure, so a consumer can see the same message more than once.
- **co-29 · idempotent-consumer** — recording processed message ids so a duplicate delivery is detected and its effect applied once.
- **co-30 · dead-letter-queue** — sidelining a message that keeps failing after a max-receive count for later inspection.
- **co-31 · backpressure** — bounding in-flight work (a bounded queue) so a fast producer cannot overwhelm a slow consumer.
- **co-32 · webhook-hmac** — signing outbound webhook payloads with HMAC and verifying them with a constant-time compare.
- **co-33 · websocket-vs-sse** — full-duplex WebSocket vs one-way Server-Sent Events, and when each fits real-time delivery.
- **co-34 · broker-backplane** — connections are sticky to one node, so broadcasting across nodes needs a shared pub/sub backplane.
- **co-35 · contract-testing-pact** — consumer-driven contract tests that verify a provider honours the messages consumers actually send/expect.
- **co-36 · test-containers** — spinning ephemeral real dependencies (DB, broker) in containers for integration tests instead of mocks.
- **co-37 · circuit-breaker** — tripping open after a failure threshold so calls fail fast instead of piling onto a failing dependency.
- **co-38 · retry-backoff-jitter** — retrying with exponential backoff plus full jitter to avoid synchronized retry storms.
- **co-39 · timeout-bulkhead** — bounding how long a call may wait and isolating resource pools so one failure doesn't sink the whole service.
- **co-40 · connection-pool-n-plus-1** — reusing pooled DB connections and eliminating the N+1 query with a join/batched prefetch.

## Tensions & trade-offs — when NOT to reach for this

- **Premature scale**: idempotency keys, queues, caches, and read replicas each add moving parts and new
  failure modes. Adding them before load exists is complexity with no payoff — most services never reach the
  scale that would justify them.
- **Cache invalidation is a correctness problem**: a cache buys latency and charges staleness; the wrong TTL
  serves stale data, and cache-as-source-of-truth is a bug waiting to happen. Cache last, cache only what's
  hot, and make invalidation explicit.
- **When NOT to use it**: a low-traffic internal tool needs no rate limiting, backpressure, or async workers.
  Reach for each pattern when a _measured_ bottleneck demands it, not by default.

## Lineage — why it beat the alternative

- These patterns are the industry's answer to the shift from single-server apps to always-on internet-scale
  services. Idempotency keys came from payments (a retried charge must not double-bill); the outbox/queue
  patterns answered the dual-write problem when one DB transaction couldn't span a broker; OAuth2/OIDC
  replaced ad-hoc session sharing once third-party auth became the norm. The through-line: each pattern makes
  one specific failure — double-charge, lost message, credential sprawl — survivable, so adopt it when its
  failure is on your path. This scales up to systems in [`44-system-design`](./44-system-design.md) and to
  async workflows in [`45-event-driven-architecture`](./45-event-driven-architecture.md).

## Worked examples

Colocated under `backend-at-scale/learning/code/`; each runnable + exercised from the CLI, every Python
snippet fully type-annotated and `pyright`-clean (DD-20/DD-30/DD-34/DD-39). Contiguous `ex-01..ex-80`. Every
example cites the `co-NN` it exercises; every concept above is exercised by ≥ 1 example.

### Beginner

- **ex-01 · rest-crud-endpoints** — GET/POST/PUT/DELETE for one resource — verify each verb takes its path. (co-01)
- **ex-02 · safe-vs-idempotent** — call GET twice, PUT twice, POST twice — verify GET/PUT are repeatable, POST creates duplicates. (co-01)
- **ex-03 · status-201-created** — POST returns `201` + a `Location` header — verify both. (co-02)
- **ex-04 · status-204-delete** — DELETE returns `204` with no body — verify empty body. (co-02)
- **ex-05 · status-400-validation** — a malformed payload returns `400` — verify the error. (co-02)
- **ex-06 · status-401-vs-403** — no token → `401`, wrong role → `403` — verify the distinction. (co-02)
- **ex-07 · status-409-conflict** — a duplicate create returns `409` — verify the conflict. (co-02)
- **ex-08 · status-422-unprocessable** — a semantically invalid body returns `422 Unprocessable Content` — verify the code. (co-02)
- **ex-09 · version-uri-path** — route `/v1/` vs `/v2/` to different handlers — verify each version resolves. (co-03)
- **ex-10 · version-header** — select the version from a request header — verify header-based routing. (co-03)
- **ex-11 · offset-limit-page** — page with `?offset=20&limit=10` — verify the correct slice returns. (co-04)
- **ex-12 · offset-cost-demo** — instrument an offset query — verify it touches all preceding rows. (co-04)
- **ex-13 · cursor-page** — page with a `starting_after` cursor — verify the next page follows the last id. (co-05)
- **ex-14 · cursor-stable-under-insert** — insert a row mid-scan — verify the cursor page is unaffected while offset would drift. (co-05)
- **ex-15 · idempotency-key-store** — store `key → response`, replay the request — verify the same response returns. (co-06)
- **ex-16 · idempotency-key-no-double-apply** — replay a POST charge with the same key — verify it applies once. (co-06)
- **ex-17 · idempotency-key-mismatch** — reuse a key with a different body — verify the request is rejected. (co-06)
- **ex-18 · repository-crud** — a `Repository` over an in-memory store — verify CRUD through the collection interface. (co-09)
- **ex-19 · repository-swap-backend** — swap the repository implementation — verify callers are unchanged. (co-09)
- **ex-20 · unit-of-work-commit** — track changes and commit once — verify all writes land together. (co-10)
- **ex-21 · unit-of-work-rollback** — roll back a unit of work — verify no tracked change persists. (co-10, co-11)
- **ex-22 · transaction-atomic** — two writes in one transaction — verify both commit or both roll back. (co-11)
- **ex-23 · jwt-encode-decode** — sign then verify a JWT with claims — verify the round-trip and signature. (co-14)
- **ex-24 · jwt-expiry** — present an expired JWT — verify it is rejected. (co-14)
- **ex-25 · rbac-role-gate** — a role-restricted route — verify `200` for the right role, `403` for the wrong one. (co-17)
- **ex-26 · abac-attribute-gate** — an owner-only attribute policy — verify a non-owner is denied. (co-17)
- **ex-27 · structured-log-json** — emit a JSON log line with typed fields — verify it parses. (co-25)
- **ex-28 · correlation-id** — thread a request-id through the logs — verify every line carries it. (co-25)

### Intermediate

- **ex-29 · oauth2-authcode-flow** — model the authorization-code grant — verify the code exchanges for a token. (co-15)
- **ex-30 · oidc-id-token** — issue an OIDC `id_token` carrying identity claims — verify the subject. (co-15)
- **ex-31 · pkce-challenge** — generate `code_verifier`/`code_challenge` and verify at exchange — verify a wrong verifier fails. (co-16)
- **ex-32 · refresh-rotate** — expire an access token, rotate the refresh token — verify a new pair issues. (co-18)
- **ex-33 · refresh-reuse-detect** — replay a rotated-out refresh token — verify reuse is detected and the family revoked. (co-18)
- **ex-34 · token-bucket** — a token-bucket limiter allowing bursts — verify tokens refill over time. (co-19)
- **ex-35 · leaky-bucket** — a leaky-bucket limiter draining at a constant rate — verify the smoothed output. (co-19)
- **ex-36 · fixed-window** — a fixed-window counter — verify the boundary-burst flaw (2× at the edge). (co-19)
- **ex-37 · sliding-window** — a sliding-window limiter — verify it avoids the boundary burst. (co-19)
- **ex-38 · rate-limit-429-retry-after** — exceed the limit — verify `429` + a `Retry-After` header. (co-20)
- **ex-39 · cache-aside-read** — miss → DB → populate, then hit — verify the second read comes from cache. (co-21)
- **ex-40 · cache-aside-hit-no-db** — instrument the DB — verify a cached read issues no query. (co-21)
- **ex-41 · write-through** — a write updates cache and DB together — verify both reflect the new value. (co-22)
- **ex-42 · cache-ttl-expiry** — set a TTL — verify the entry expires and re-loads. (co-23)
- **ex-43 · cache-explicit-invalidate** — a mutation invalidates the cached key — verify the next read is fresh. (co-23)
- **ex-44 · cache-stale-bug** — a too-long TTL serves stale data — verify the bug, then the fix. (co-23)
- **ex-45 · etag-304** — return an `ETag`, resend with `If-None-Match` — verify a `304`. (co-24)
- **ex-46 · cache-control-maxage** — set `Cache-Control: max-age` — verify the header is honoured. (co-24)
- **ex-47 · otel-span** — wrap a handler in an OpenTelemetry span — verify the span is recorded. (co-26)
- **ex-48 · traceparent-propagate** — propagate a W3C `traceparent` across a call — verify the trace id is preserved. (co-26)
- **ex-49 · health-liveness** — a `/livez` endpoint — verify it reports healthy. (co-27)
- **ex-50 · health-readiness** — a `/readyz` endpoint — verify it reports unready while a dependency is down. (co-27)
- **ex-51 · graphql-query** — a single GraphQL endpoint where the client picks fields — verify only requested fields return. (co-07)
- **ex-52 · graphql-overfetch-contrast** — the same data via REST vs GraphQL — verify REST over-fetches, GraphQL does not. (co-07)
- **ex-53 · graphql-n-plus-1** — a resolver issuing N+1 queries, then a dataloader batch — verify the query count drops. (co-07, co-40)
- **ex-54 · grpc-unary** — a unary protobuf RPC — verify request/response round-trip. (co-08)
- **ex-55 · grpc-streaming** — a server-streaming RPC — verify multiple messages stream back. (co-08)
- **ex-56 · rest-vs-graphql-vs-grpc** — the same operation three ways — verify each works; note when each fits. (co-07, co-08)

### Advanced

- **ex-57 · queue-produce-consume** — enqueue a job and consume it in a worker — verify the job runs once. (co-28)
- **ex-58 · at-least-once-redeliver** — fail an ack — verify the message is redelivered. (co-28)
- **ex-59 · idempotent-consumer-dedup** — dedup by message id — verify a duplicate delivery is skipped. (co-29)
- **ex-60 · idempotent-consumer-effect-once** — process a duplicated side-effecting message — verify the effect happens once. (co-29)
- **ex-61 · dead-letter-queue** — exceed `maxReceiveCount` on a poison message — verify it lands in the DLQ. (co-30)
- **ex-62 · backpressure-bounded-queue** — a bounded queue with a fast producer — verify the producer blocks when full. (co-31)
- **ex-63 · dual-write-problem-demo** — crash between a DB commit and a broker publish — verify the message is lost. (co-12)
- **ex-64 · transactional-outbox** — write the message in the DB transaction, relay separately — verify it is sent iff the transaction commits. (co-13)
- **ex-65 · outbox-relay-idempotent** — the relay is at-least-once — verify the idempotent consumer keeps effects once. (co-13, co-29)
- **ex-66 · webhook-send-hmac** — send a webhook with an HMAC-SHA256 signature header — verify the signature matches the payload. (co-32)
- **ex-67 · webhook-verify-signature** — verify an incoming webhook signature with a constant-time compare — verify a tampered body is rejected. (co-32)
- **ex-68 · webhook-retry** — retry a failed webhook with backoff — verify successive attempts space out. (co-32, co-38)
- **ex-69 · websocket-echo** — a WebSocket echo endpoint — verify a bidirectional round-trip. (co-33)
- **ex-70 · sse-stream** — an SSE `text/event-stream` push — verify successive server events arrive. (co-33)
- **ex-71 · broker-backplane-fanout** — two app nodes fanning out via a pub/sub backplane — verify a message reaches clients on both nodes. (co-34)
- **ex-72 · circuit-breaker** — trip open after N failures, half-open probe — verify calls fail fast while open. (co-37)
- **ex-73 · retry-exponential-backoff** — retry with exponential backoff — verify the delays double. (co-38)
- **ex-74 · retry-full-jitter** — add full jitter to the backoff — verify retries de-synchronize across clients. (co-38)
- **ex-75 · timeout-guard** — cap a slow call with a timeout — verify it aborts at the deadline. (co-39)
- **ex-76 · bulkhead-isolation** — isolate two resource pools — verify one pool's saturation doesn't starve the other. (co-39)
- **ex-77 · connection-pool** — pool and reuse DB connections — verify connections are reused, not reopened. (co-40)
- **ex-78 · pact-contract** — a consumer-driven Pact contract + provider verification — verify the provider honours the contract. (co-35)
- **ex-79 · testcontainers-integration** — an integration test against a containerized DB — verify the suite runs against a real engine. (co-36)
- **ex-80 · scale-ready-service** — assemble versioned + paginated REST, idempotent writes, RBAC auth, rate limiting, caching, and an idempotent queue consumer behind an integration suite — verify the end-to-end service passes. (co-06, co-17, co-21, co-29)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: evolve the Backend-Essentials service into a scale-ready API: versioned + paginated REST with
  idempotent writes, OAuth2/OIDC + RBAC auth, structured logging + rate limiting + caching, and a
  background-job queue consumer with idempotency — verified by an integration + contract test suite.
- **Concepts exercised**: [ ] versioned/paginated REST + idempotency keys (co-03, co-05, co-06)
  [ ] OAuth2/OIDC + RBAC (co-15, co-17) [ ] repository/unit-of-work persistence (co-09, co-10)
  [ ] structured logging + rate limit + cache (co-25, co-20, co-21) [ ] a queue consumer with idempotent
  processing (co-28, co-29) [ ] integration + contract tests (co-35, co-36).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — versioned REST with pagination + idempotency-key handling. Verify a
     replayed write with the same key does not double-apply (`curl`).
  2. Add OAuth2/OIDC + RBAC. Verify a role-restricted route returns 403 for the wrong role and 200 for the
     right one.
  3. Add structured logging + rate limiting + a cache layer. Verify logs are structured, the rate limit
     returns 429, and a cached read avoids a DB hit.
  4. Add a queue consumer for a background job with a dedup key + an integration/contract test suite.
     Verify duplicate messages process once and the suite passes.
- **Acceptance criteria**: idempotent writes and consumers behave correctly; auth/RBAC gates work; rate
  limit + cache observable; integration + contract tests green.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Designing Data-Intensive Applications** — Martin Kleppmann (2017). The central text on scaling, replication, sharding, and reliability trade-offs for backend systems.
- **Release It!: Design and Deploy Production-Ready Software** — Michael T. Nygard (2007; 2nd ed. 2018). The canonical catalog of stability and resilience patterns — circuit breaker, bulkhead, timeout — for production systems at scale.
- **Site Reliability Engineering: How Google Runs Production Systems** — Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy, eds. (2016). Free, foundational text defining SRE practice for operating services at scale. <https://sre.google/sre-book/table-of-contents/>

**Papers & articles**

- **Fallacies of Distributed Computing** — L. Peter Deutsch, with additions by Bill Joy, Dave Lyon, and James Gosling (1994–1997). The founding list of false assumptions that break distributed backend systems at scale.

---

← Previous: [38 · Search & Information Retrieval](./38-search-and-information-retrieval.md) · Next: [40 · Build Your Own Web Framework](./40-build-your-own-web-framework.md) →
