# 41 · API Design (By Example, Python †)

**prd row**: Pass 3 · Build for the Real World · By Example · Python † · Learn 141 / Drill 241 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: designing the contract, not just the endpoint — REST vs GraphQL vs gRPC and when
each fits, OpenAPI as the machine-readable contract, versioning, pagination, idempotency, error
envelopes, and rate limiting. The through-line is that an API is a promise to callers you don't
control, so its shape and its failure modes are the design. Builds on the serving mechanics of
[`40-build-your-own-web-framework`](./40-build-your-own-web-framework.md). `†`: Python, fully
type-annotated (DD-39) — every snippet carries type hints in the pyright-clean spirit.

## Why this exists · the big idea

- **The problem before the solution**: an endpoint that works is not an API — the moment a second
  team, a mobile app, or a paying customer depends on it, every field name, status code, and
  pagination quirk becomes a promise you can't quietly break. Ad-hoc APIs turn every change into a
  coordinated migration and every outage into a guessing game about what the response _should_ be.
- **Keep-this-if-you-forget-everything**: design the contract first and design for the caller you'll
  never meet — a stable, versioned, self-describing contract with predictable errors and idempotent
  writes is what lets clients evolve independently of your server.
- **Big ideas touched**: `coupling-vs-cohesion` (a good contract decouples client from server so each
  changes on its own schedule; a leaky one couples every consumer to your internals),
  `consistency-latency-throughput` (pagination, rate limiting, and the REST/GraphQL/gRPC choice are
  all throughput-and-latency decisions dressed as API style).

## Prerequisites

- **Prior topics**: [topic 11 Backend Essentials](./11-backend-essentials.md) (HTTP verbs, status
  codes, routing, JSON handling) and [topic 39 Backend at Scale](./39-backend-at-scale.md)
  (idempotency, auth, and rate limiting as production concerns).
- **Tools & environment**: a macOS/Linux terminal; **Python** at a recent stable release with type
  hints and `pyright`; a web framework you can serve locally; `curl`/an HTTP client; an OpenAPI toolchain
  (spec validator + a mock/codegen); optionally a gRPC/Protobuf and a GraphQL toolchain for the
  contrast tiers; Neovim/VSCode with the Python LSP (DD-17).
- **Assumed knowledge**: serving a CRUD JSON API (topic 11); what idempotency and rate limiting buy
  you (topic 39); reading and writing typed request/response models (topic 04).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: **OpenAPI** remains the dominant REST contract format and **Protocol Buffers /
  gRPC** and the **GraphQL** specification remain the standard non-REST contrasts — all left correctly
  version-unpinned; the RFC 9110 HTTP semantics (methods, status codes) that REST builds on are
  current.
- 2026-07-12 — verified (GAP for plan owner): specific OpenAPI version (3.0 vs 3.1) and the JSON-Schema
  alignment differ between tooling generations — pin the concrete OpenAPI version and validator when
  drafting the examples. Error-envelope guidance is described generically (a stable, documented error
  shape) rather than mandating RFC 9457/Problem Details, which is a defensible-but-optional choice to
  confirm at drafting.

> DD-35 primary-source pass (2026-07-12). Every citation traces to a source the author fetched and
> read; unverifiable specifics flagged `[Needs Verification]`, never guessed. Keep exact when drafting.

- **REST constraints** — Fielding's six: client-server, stateless, cache, uniform interface, layered
  system, code-on-demand (optional). The uniform interface has four sub-constraints, the fourth being
  **HATEOAS** ("hypermedia as the engine of application state"). Source: [Fielding dissertation ch. 5](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm) (2000).
- **Richardson Maturity Model** — L0 POX → L1 resources → L2 HTTP verbs+status → L3 hypermedia; Fielding's
  REST requires L3. Source: [Fowler, Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html) (2010).
- **HTTP semantics = RFC 9110 (not 7231)** — RFC 9110 (2022, STD 97) is the current spec and obsoletes
  RFC 7231; teach methods/status from 9110. Safe: GET/HEAD/OPTIONS/TRACE. Idempotent: GET/HEAD/PUT/
  DELETE/OPTIONS/TRACE; POST and PATCH neither. **422 = "Unprocessable Content"** (§15.5.21, renamed from
  RFC 4918's "Unprocessable Entity"). **429 lives in [RFC 6585](https://www.rfc-editor.org/rfc/rfc6585.html), not 9110**, with an optional `Retry-After`. Source: [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html).
- **Problem Details** — [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) (2023) **obsoletes RFC 7807**; media type `application/problem+json`; fields `type`/`title`/`status`/`detail`/`instance`. Use it for the error envelope.
- **OpenAPI** — 3.1.0 (2021) defines Paths/Operation/Schema/Components; **3.1 aligns with JSON Schema Draft
  2020-12** (verbatim from the spec). Source: [OpenAPI Specification 3.1.0](https://spec.openapis.org/oas/v3.1.0.html). Confirm the latest 3.1.x patch at drafting.
- **Versioning divergence** — path (Google [AIP-185](https://google.aip.dev/185): major version in the URI,
  "v1 not v1.0"), query `api-version=YYYY-MM-DD` (Microsoft [Azure guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md), omission → 400 `MissingApiVersionParameter`), header `Stripe-Version` ([Stripe](https://docs.stripe.com/api/versioning)). Present as trade-offs.
- **Pagination** — cursor (`starting_after`/`ending_before`, `has_more`, no total; [Stripe](https://docs.stripe.com/api/pagination)) beats OFFSET because OFFSET fetches-and-discards preceding rows and drifts under concurrent inserts ([Use The Index, Luke — No Offset](https://use-the-index-luke.com/no-offset)).
- **Idempotency-Key (correction)** — the IETF draft `draft-ietf-httpapi-idempotency-key-header-07` is
  **EXPIRED** (2026-04-18), not an RFC. Teach via Stripe prior art ([Idempotent requests](https://docs.stripe.com/api/idempotent_requests)); label the draft "lapsed."
- **Rate-limit headers (status split)** — `429` is [RFC 6585](https://www.rfc-editor.org/rfc/rfc6585.html);
  the structured `RateLimit`/`RateLimit-Policy` header fields are an **active** IETF draft
  (`draft-ietf-httpapi-ratelimit-headers-11`, expires 2026-11-24) — standardizing the non-standard
  `X-RateLimit-*` convention. Note this draft is active, unlike the expired Idempotency-Key one.
- **Auth RFCs** — OAuth 2.0 [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749.html); **bearer token syntax
  `Authorization: Bearer <token>` = [RFC 6750](https://www.rfc-editor.org/rfc/rfc6750.html)**; JWT [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519.html); scopes are space-delimited case-sensitive strings.
- **Deprecation/Sunset (precise RFCs)** — `Deprecation` response header = **[RFC 9745](https://www.rfc-editor.org/rfc/rfc9745.html) (2025, Standards Track)**; `Sunset` header = **[RFC 8594](https://www.rfc-editor.org/rfc/rfc8594.html) (2019, Informational)** — different statuses, both notification-only.
- **gRPC** — protobuf as IDL + message format; HTTP/2 transport; four RPC kinds: unary, server-streaming,
  client-streaming, bidirectional. Source: [grpc.io core concepts](https://grpc.io/docs/what-is-grpc/core-concepts/).
- **GraphQL** — single endpoint, client-specified fields, over/under-fetch solution; resolver **N+1** fixed
  by DataLoader batching + per-request cache ([graphql/dataloader](https://github.com/graphql/dataloader)).
  graphql.org/spec.graphql.org were fetch-blocked (403) — the "no over/under-fetch" tagline is
  `[Needs Verification]` by direct fetch (well-corroborated by secondary sources).
- **Hypermedia formats** — JSON:API v1.1 (`application/vnd.api+json`, [jsonapi.org](https://jsonapi.org/));
  HAL (`_links` required, `_embedded` optional, `application/hal+json`, Mike Kelly Internet-Draft, never an
  RFC). Siret/Siren `[Needs Verification]` (no formal spec; GitHub repo only).
- **REST-vs-GraphQL-vs-gRPC positioning** — no single primary source states the three-way comparison; it
  is synthesized from each project's stated design goals (REST = cacheable/ubiquitous via RFC 9111,
  GraphQL = client-shaped queries, gRPC = typed internal service-to-service/streaming). Present as
  synthesized guidance, `[Needs Verification]` for a single-source citation.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject topic). Each example below cites the co-NN it exercises. -->

- **co-01 · api-as-contract** — an API is a promise to callers you don't control; its shape and failure modes are the design.
- **co-02 · consumer-driven-design** — designing for the caller you'll never meet, and reading responses tolerantly.
- **co-03 · rest-constraints** — Fielding's six constraints (client-server, stateless, cache, uniform interface, layered, code-on-demand) and HATEOAS as the fourth uniform-interface sub-constraint.
- **co-04 · richardson-maturity** — the RMM ladder: L0 POX → L1 resources → L2 HTTP verbs+status → L3 hypermedia.
- **co-05 · resource-modeling** — modeling nouns not verbs, plural collections, and resource URIs over RPC-style endpoints.
- **co-06 · http-method-semantics** — GET/POST/PUT/PATCH/DELETE and which are safe/idempotent (RFC 9110).
- **co-07 · status-code-design** — choosing the right status: 201/202/204, and 400/401/403/404/409/422/429.
- **co-08 · problem-details** — RFC 9457 `application/problem+json` (`type`/`title`/`status`/`detail`/`instance`) as the error envelope.
- **co-09 · openapi-contract** — OpenAPI 3.1 describing paths, operations, schemas, and reusable components as the source of truth.
- **co-10 · openapi-json-schema** — OpenAPI 3.1 schemas aligning with JSON Schema Draft 2020-12.
- **co-11 · openapi-codegen-mock** — generating human docs, typed clients, and mock servers from the spec.
- **co-12 · request-validation** — validating live requests and responses against the OpenAPI schema.
- **co-13 · versioning-strategies** — URI-path vs header vs query-param versioning and the trade-off each carries.
- **co-14 · backward-compatible-change** — additive, non-breaking evolution and the tolerant-reader rule that enables it.
- **co-15 · deprecation-sunset** — signalling retirement with the `Deprecation` (RFC 9745) and `Sunset` (RFC 8594) headers.
- **co-16 · offset-pagination** — `offset`/`limit` paging and its fetch-and-discard cost.
- **co-17 · cursor-pagination** — keyset/cursor paging that scales and stays stable under concurrent writes.
- **co-18 · idempotency-key** — an `Idempotency-Key` header so a retried write applies once (Stripe prior art; the IETF draft is lapsed).
- **co-19 · rate-limit-429** — communicating limits with `429 Too Many Requests` + `Retry-After`.
- **co-20 · ratelimit-headers** — the structured `RateLimit`/`RateLimit-Policy` header fields exposing remaining quota.
- **co-21 · content-negotiation** — `Accept`/`Content-Type`/`Accept-Language` choosing representation and language.
- **co-22 · http-caching-etag** — `Cache-Control`, `ETag` + `If-None-Match` → `304`, and `If-Match` optimistic concurrency.
- **co-23 · auth-bearer-token** — API keys, OAuth 2.0 bearer tokens (`Authorization: Bearer`, RFC 6750), and scopes.
- **co-24 · graphql-schema** — GraphQL's type system, single endpoint, and client-specified field selection.
- **co-25 · graphql-resolver-n1** — resolvers and the N+1 problem, fixed with DataLoader batching.
- **co-26 · grpc-protobuf** — gRPC's protobuf IDL over HTTP/2 with unary and streaming RPCs.
- **co-27 · style-selection** — the forces that pick REST vs GraphQL vs gRPC — caching, over/under-fetching, and evolution — not a winner.
- **co-28 · hateoas-hypermedia** — hypermedia formats (HAL `_links`, JSON:API) that let clients follow links instead of hardcoding URLs.
- **co-29 · pagination-envelope** — a consistent list envelope (`data` + `has_more` + `next_cursor`) across endpoints.
- **co-30 · error-envelope-consistency** — one documented error shape used uniformly across every endpoint.
- **co-31 · partial-response-field-selection** — sparse fieldsets / field filtering so callers fetch only what they need.
- **co-32 · bulk-batch-endpoints** — batch/bulk operation design for applying many changes in one request.
- **co-33 · webhook-api-surface** — outbound webhook events (with HMAC signing) as a first-class part of the API.
- **co-34 · openapi-security-schemes** — declaring auth (bearer / apiKey) in the OpenAPI contract itself.

## Tensions & trade-offs — when NOT to reach for this

- **GraphQL/gRPC are not upgrades**: GraphQL's client-shaped queries trade a simple cacheable surface
  for query-complexity, N+1, and caching problems you now own; gRPC trades human-readable, browser-
  native calls for typed performance and a Protobuf toolchain. A public, cacheable, human-debuggable
  API is usually still REST — reach for the alternatives only when their specific force applies.
- **Over-versioning is its own tax**: a new version per change forces callers to migrate constantly
  and multiplies the surface you maintain. Most changes should be additive and backward-compatible;
  a new version is for the rare truly-breaking change, not for every field.
- **Idempotency and rate limiting cost complexity**: idempotency keys need storage and dedup logic;
  rate limiting needs counters and a fairness policy. On a low-traffic internal API with trusted
  callers, both can be premature — add each when a real retry-storm or abuse pattern demands it.

## Lineage — why it beat the alternative

- API design consolidated as web services replaced hand-rolled RPC and SOAP: Fielding's REST
  dissertation gave resource-orientation and HTTP-native semantics a theory, the Richardson Maturity
  Model gave teams a ladder to judge how RESTful an API really was, and OpenAPI (from Swagger) turned
  the contract into a machine-readable artifact that generates docs, clients, and mocks. GraphQL and
  gRPC then carved out the cases REST fits worst — client-shaped aggregation and typed internal
  streaming. The durable lesson is contract-first design: the contract, not the code, is the product.
  This hands stable interfaces up to [topic 42 Software Architecture](./42-software-architecture.md)
  and its scaling/failure concerns back to [topic 39 Backend at Scale](./39-backend-at-scale.md).

## Worked examples

Colocated under `api-design/learning/code/`; each runnable and exercised with `curl`/a client, every
Python snippet fully type-annotated and `pyright`-clean (DD-20/DD-30/DD-34/DD-39). Contiguous `ex-01..ex-80`.
Every example cites the `co-NN` it exercises; every concept above is exercised by ≥ 1 example.

### Beginner

- **ex-01 · resource-noun-uri** — model an `/articles` collection + `/articles/{id}` item — verify the URIs name nouns, not actions. (co-05)
- **ex-02 · rpc-vs-resource-contrast** — contrast `/getArticle?id=1` with `GET /articles/1` — verify the resource form is verb-free. (co-05)
- **ex-03 · method-semantics-map** — map CRUD onto GET/POST/PUT/PATCH/DELETE — verify each verb's intent. (co-06)
- **ex-04 · idempotent-put-vs-post** — call PUT twice and POST twice — verify PUT is repeatable, POST is not. (co-06)
- **ex-05 · status-201-location** — POST returns `201` + a `Location` header — verify both. (co-07)
- **ex-06 · status-202-async** — a long-running op returns `202 Accepted` + a status URL — verify the async contract. (co-07)
- **ex-07 · status-204-delete** — DELETE returns `204` with no body — verify empty body. (co-07)
- **ex-08 · status-409-vs-422** — a conflict returns `409`, a semantically-invalid body `422` — verify the distinction. (co-07)
- **ex-09 · richardson-level-classify** — classify three sample APIs at RMM levels 0–3 — verify each classification. (co-04)
- **ex-10 · rest-constraint-stateless** — show a request carries all its own context — verify no server session is needed. (co-03)
- **ex-11 · hateoas-links** — a response includes `_links` to next actions — verify a client can follow them. (co-03, co-28)
- **ex-12 · problem-details-envelope** — return `application/problem+json` with `type`/`title`/`status`/`detail`/`instance` — verify the shape. (co-08)
- **ex-13 · error-envelope-consistency** — the same error shape across three endpoints — verify uniformity. (co-30)
- **ex-14 · validation-error-422** — a validation failure returns field errors in `problem+json` — verify the `422`. (co-08)
- **ex-15 · openapi-skeleton** — write a minimal OpenAPI 3.1 doc (`info` + `paths`) — verify it validates. (co-09)
- **ex-16 · openapi-schema-component** — a reusable component schema with `$ref` — verify the reference resolves. (co-09)
- **ex-17 · openapi-json-schema-2020** — a schema using JSON Schema 2020-12 keywords — verify validation applies them. (co-10)
- **ex-18 · openapi-operation-responses** — declare `200`/`404`/`422` per operation — verify each response is documented. (co-09)
- **ex-19 · openapi-validate-request** — validate a request body against the schema — verify a bad body is rejected. (co-12)
- **ex-20 · openapi-validate-response** — validate a live response against the spec — verify conformance. (co-12)
- **ex-21 · openapi-mock-server** — serve a mock from the spec — verify the mock returns spec-shaped data. (co-11)
- **ex-22 · openapi-client-codegen** — generate a typed client from the spec — verify a generated call type-checks. (co-11)
- **ex-23 · offset-page-endpoint** — an `?offset=&limit=` list endpoint — verify the correct slice returns. (co-16)
- **ex-24 · cursor-page-endpoint** — a cursor list returning a `next_cursor` — verify the next page follows it. (co-17)
- **ex-25 · pagination-envelope** — a `{data, has_more, next_cursor}` envelope — verify the envelope shape. (co-29)
- **ex-26 · content-type-json** — set `Content-Type: application/json` — verify the client parses it. (co-21)
- **ex-27 · accept-negotiation** — `Accept` chooses JSON vs CSV — verify the right representation returns. (co-21)
- **ex-28 · accept-language** — `Accept-Language` selects a localized message — verify the language. (co-21)

### Intermediate

- **ex-29 · version-uri-path** — route `/v1` vs `/v2` — verify each version resolves to its handler. (co-13)
- **ex-30 · version-header** — select the version from a request header — verify header-based routing. (co-13)
- **ex-31 · version-query** — select the version from `?api-version=` — verify query-based routing. (co-13)
- **ex-32 · additive-change-compatible** — add an optional field — verify old clients keep working. (co-14)
- **ex-33 · tolerant-reader** — a client that ignores unknown fields — verify it survives a server addition. (co-14, co-02)
- **ex-34 · breaking-change-detect** — remove a field and catch the break — verify a consumer test fails. (co-14)
- **ex-35 · deprecation-header** — send a `Deprecation` header + `Link` — verify the client sees the notice. (co-15)
- **ex-36 · sunset-header** — send a `Sunset` header with a date — verify the retirement date is communicated. (co-15)
- **ex-37 · idempotency-key-write** — an `Idempotency-Key` on POST — verify the key is recorded. (co-18)
- **ex-38 · idempotency-replay** — replay the request — verify the stored response returns. (co-18)
- **ex-39 · idempotency-key-mismatch** — reuse a key with a different body — verify rejection. (co-18)
- **ex-40 · rate-limit-429** — exceed the limit — verify `429` + a `Retry-After` header. (co-19)
- **ex-41 · ratelimit-headers** — expose `RateLimit`/`RateLimit-Policy` structured headers — verify they parse. (co-20)
- **ex-42 · quota-remaining** — the remaining counter decrements per call — verify it reaches zero. (co-20)
- **ex-43 · etag-304** — return an `ETag`, resend with `If-None-Match` — verify a `304`. (co-22)
- **ex-44 · cache-control-header** — set `Cache-Control: max-age` — verify the directive. (co-22)
- **ex-45 · conditional-put-if-match** — `If-Match` optimistic concurrency — verify a stale write returns `412`. (co-22)
- **ex-46 · bearer-token-auth** — `Authorization: Bearer <token>` — verify a missing token returns `401`. (co-23)
- **ex-47 · api-key-auth** — an `X-API-Key` header — verify an invalid key is rejected. (co-23)
- **ex-48 · scope-check** — a token scope gates an operation — verify an out-of-scope call returns `403`. (co-23)
- **ex-49 · openapi-security-scheme** — declare bearer/apiKey in the spec — verify the scheme is documented. (co-34)
- **ex-50 · partial-response-fields** — `?fields=` selects returned fields — verify only those return. (co-31)
- **ex-51 · sparse-fieldset-jsonapi** — JSON:API sparse fieldsets — verify the sparse representation. (co-31, co-28)
- **ex-52 · batch-endpoint** — `POST /batch` applies N operations — verify each sub-result. (co-32)
- **ex-53 · bulk-create** — create many resources in one request — verify all are created. (co-32)
- **ex-54 · webhook-subscribe** — register a webhook endpoint — verify the subscription is stored. (co-33)
- **ex-55 · webhook-hmac-sign** — sign the outbound webhook payload with HMAC — verify the signature matches. (co-33)
- **ex-56 · hal-links** — a HAL `_links`/`_embedded` response — verify the hypermedia shape. (co-28)

### Advanced

- **ex-57 · graphql-schema-def** — define a GraphQL schema and types — verify the SDL parses. (co-24)
- **ex-58 · graphql-query-fields** — a client selects exactly the fields it needs — verify only those return. (co-24)
- **ex-59 · graphql-overfetch-contrast** — the same data via REST vs GraphQL — verify REST over-fetches, GraphQL does not. (co-24)
- **ex-60 · graphql-resolver** — a resolver resolving a field — verify the resolved value. (co-25)
- **ex-61 · graphql-n1-dataloader** — an N+1 resolver, then a DataLoader batch — verify the query count drops. (co-25)
- **ex-62 · graphql-mutation** — a mutation writes data — verify the write and its return. (co-24)
- **ex-63 · grpc-proto-define** — write a `.proto` service + messages — verify it compiles. (co-26)
- **ex-64 · grpc-unary** — a unary RPC — verify the request/response round-trip. (co-26)
- **ex-65 · grpc-server-streaming** — a server-streaming RPC — verify multiple messages stream back. (co-26)
- **ex-66 · grpc-bidi-streaming** — a bidirectional-streaming RPC — verify interleaved read/write. (co-26)
- **ex-67 · style-caching-contrast** — contrast REST (cacheable) vs GraphQL (POST) vs gRPC (binary) on caching — verify the observation. (co-27)
- **ex-68 · style-evolution-contrast** — how each style evolves a field — verify each evolution path. (co-27)
- **ex-69 · style-selection-matrix** — pick a style per scenario with a rationale — verify each choice is justified. (co-27)
- **ex-70 · contract-first-openapi** — write the OpenAPI spec before any code — verify the spec drives the design. (co-09, co-14)
- **ex-71 · spec-driven-server** — implement handlers from the spec — verify responses match the schema. (co-12)
- **ex-72 · spec-conformance-test** — assert live responses conform to the spec — verify the contract holds (the API is a promise). (co-12, co-01)
- **ex-73 · versioned-migration** — evolve `v1 → v2` with a deprecation window — verify both versions serve during the window. (co-13, co-15)
- **ex-74 · idempotent-rate-limited-write** — combine idempotency + rate limiting on one endpoint — verify both behave. (co-18, co-19)
- **ex-75 · error-envelope-graphql** — contrast GraphQL partial errors with REST `problem+json` — verify each error model. (co-30, co-08)
- **ex-76 · pagination-graphql-connections** — Relay-style cursor connections in GraphQL — verify the `edges`/`pageInfo` shape. (co-17, co-24)
- **ex-77 · hateoas-driven-client** — a client that follows links instead of hardcoded URLs — verify it navigates by hypermedia. (co-28)
- **ex-78 · grpc-vs-rest-latency** — measure gRPC vs REST round-trip — verify the latency contrast. (co-27)
- **ex-79 · openapi-full-docs** — generate human docs (Swagger UI / Redoc) from the spec — verify the docs render the operations. (co-11)
- **ex-80 · contract-first-api** — assemble a versioned REST API from an OpenAPI spec with cursor pagination, idempotent writes, a consistent error envelope, rate limiting, and a GraphQL/gRPC facade — verify end-to-end conformance. (co-09, co-17, co-18, co-30, co-27)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: design and serve a versioned REST API for one resource, contract-first from an OpenAPI
  spec — with cursor pagination, idempotent writes, a consistent error envelope, and rate limiting —
  then add a GraphQL or gRPC facade over the same data and document when each contract wins.
- **Concepts exercised**: [ ] OpenAPI contract-first (co-09) [ ] versioning + backward-compatible change
  (co-13, co-14) [ ] cursor pagination (co-17) [ ] idempotency keys (co-18) [ ] error envelope (co-08,
  co-30) [ ] rate limiting (429 + headers) (co-19, co-20).
- **Ordered steps**:
  1. `.../learning/capstone/openapi.yaml` — the contract for a versioned resource with pagination and
     the error envelope. Verify the spec validates and a mock server serves it.
  2. `.../learning/capstone/code/rest.py` — implement the spec; add idempotency-key handling. Verify a
     replayed write with the same key does not double-apply (`curl`) and responses match the spec.
  3. `.../learning/capstone/code/limits.py` — add rate limiting. Verify an over-limit caller gets 429
     with correct limit/remaining headers and a compliant caller succeeds.
  4. `.../learning/capstone/code/facade/` — expose the same data via GraphQL or gRPC and write a short
     contrast note. Verify the facade returns equivalent data and the note names when each style wins.
- **Acceptance criteria**: live responses conform to the OpenAPI contract; idempotent writes and rate
  limiting behave; the second-style facade returns equivalent data; the contrast note is concrete; all
  Python is type-annotated and `pyright`-clean.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **RESTful Web APIs** — Leonard Richardson, Mike Amundsen, Sam Ruby (2013). The standard reference
  for hypermedia-driven, resource-oriented API design.
- **Designing Web APIs** — Brenda Jin, Saurabh Sahni, Amir Shevat (2018). Widely used, product-oriented
  guide to API design decisions (versioning, pagination, developer experience).
- **REST in Practice** — Jim Webber, Savas Parastatidis, Ian Robinson (2010). Connects REST theory to
  hypermedia controls and enterprise integration patterns.
- **gRPC: Up and Running** — Kasun Indrasiri, Danesh Kuruppu (2020). The standard introductory book for
  gRPC service design and Protocol Buffers contracts.

**Papers & articles**

- **Architectural Styles and the Design of Network-based Software Architectures** — Roy T. Fielding
  (2000). The doctoral dissertation that defines REST, the theoretical basis of nearly all modern HTTP
  API design. <https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm>
- **Richardson Maturity Model** — Martin Fowler, with Leonard Richardson (2010). The canonical
  explanation of the four-level model used to gauge how "RESTful" an API actually is.
  <https://martinfowler.com/articles/richardsonMaturityModel.html>
- **HTTP Semantics (RFC 9110)** — R. Fielding, M. Nottingham, J. Reschke, eds. (2022). The current
  normative IETF specification (STD 97) defining HTTP methods, status codes, and content negotiation
  that all REST APIs build on; obsoletes RFC 7231. <https://www.rfc-editor.org/rfc/rfc9110>
- **GraphQL Specification** — GraphQL Working Group, Joint Development Foundation (ongoing). The
  official language and execution specification behind GraphQL API design. <https://spec.graphql.org/>

---

← Previous: [40 · Build Your Own Web Framework](./40-build-your-own-web-framework.md) · Next: [42 · Software Architecture](./42-software-architecture.md) →
