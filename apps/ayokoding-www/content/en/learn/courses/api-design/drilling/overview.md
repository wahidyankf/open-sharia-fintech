---
title: "Overview"
date: 2026-07-29T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the API Design primer: five fixed drills that force
active recall instead of passive re-reading. Work through them in order -- short-answer recall
first, then scenario judgment, then hands-on repetition against small, genuinely-executed Python
fixtures, then a checklist to confirm real automaticity, and finally why/why-not prompts that test
whether you can explain the reasoning -- including this topic's cross-cutting big ideas,
`coupling-vs-cohesion` and `consistency-latency-throughput` -- not just recite the status codes.
Every answer is hidden in a `<details>` block; try each item yourself before opening it.

## Recall Q&A

Thirty-four short-answer questions, one per concept (`co-01` through `co-34`). Answer from memory,
then check.

**Q1 (co-01 -- api-as-contract).** Why does calling an API "a promise to callers you don't control"
change how you think about a field name or a status code compared to an endpoint on a system you
fully own?

<details>
<summary>Answer</summary>

Once a second team, a mobile app, or a paying customer depends on a response's exact shape, every
field name and status code becomes something you can no longer quietly change -- a rename or a
removed field is a breaking change for someone you may never even talk to. Example 72's
spec-conformance test operationalizes this directly: it asserts live responses conform to the
declared contract, treating "the API is a promise" as something checkable, not just a slogan.

</details>

**Q2 (co-02 -- consumer-driven-design).** What does it mean for a client to be a "tolerant reader,"
and what specific server-side change does that tolerance protect the client against?

<details>
<summary>Answer</summary>

A tolerant-reader client reads only the fields it actually needs and does not fail, error, or crash
when a response carries fields it does not recognize (Example 33). This protects the client against
exactly the kind of additive, backward-compatible change Example 32 makes on the server side -- a
new optional field appears in the response, and a tolerant client simply ignores it instead of
treating the unfamiliar shape as invalid.

</details>

**Q3 (co-03 -- rest-constraints).** Name Fielding's six REST constraints, and which one HATEOAS is a
sub-constraint of.

<details>
<summary>Answer</summary>

Client-server, stateless, cache, uniform interface, layered system, and code-on-demand (optional).
HATEOAS -- hypermedia as the engine of application state -- is the fourth of the uniform interface's
own sub-constraints, not a separate, seventh constraint (Example 11). Example 10 demonstrates the
stateless constraint specifically: a request carries all the context it needs, with no server-side
session required to interpret it.

</details>

**Q4 (co-04 -- richardson-maturity).** What distinguishes Richardson Maturity Model level 2 from
level 3, and why does Fielding's own definition of REST require level 3?

<details>
<summary>Answer</summary>

Level 2 uses HTTP verbs and status codes correctly but still hands the client hardcoded URLs it must
already know; level 3 adds hypermedia controls (links) telling the client what it can do next,
without the client needing that knowledge baked in ahead of time (Example 9's classification
exercise). Fielding's own REST definition requires level 3 specifically because HATEOAS -- the
fourth uniform-interface sub-constraint -- is part of what "REST" means in his dissertation; an API
stopping at level 2 is a well-behaved HTTP API, but not REST by Fielding's own stricter definition.

</details>

**Q5 (co-05 -- resource-modeling).** Why does `GET /articles/1` count as more RESTful than
`GET /getArticle?id=1`, even though both return the identical data?

<details>
<summary>Answer</summary>

`/articles/1` names a NOUN -- a specific resource, addressed by its own URI -- while
`/getArticle?id=1` embeds a VERB (`get`) into the path itself, treating the URL as a remote-procedure
call rather than an address (Example 1, Example 2). Resource modeling is about what the URI
structure communicates: `/articles` as a collection and `/articles/{id}` as one member of it lets
the HTTP method (`GET`, `POST`, `DELETE`) carry the verb instead, which is exactly what lets the
uniform interface constraint (co-03) do its job.

</details>

**Q6 (co-06 -- http-method-semantics).** Which HTTP methods are idempotent per RFC 9110, and what
does "idempotent" actually guarantee about calling the same request twice?

<details>
<summary>Answer</summary>

GET, HEAD, PUT, DELETE, OPTIONS, and TRACE are idempotent; POST and PATCH are neither (Example 3).
Idempotent means calling the identical request N times produces the SAME end state as calling it
once -- Example 4 demonstrates this directly: two identical PUTs leave the resource in the same
final state, while two identical POSTs (absent any idempotency-key handling, co-18) each create a
new resource.

</details>

**Q7 (co-07 -- status-code-design).** What is the difference between a `409 Conflict` and a
`422 Unprocessable Content`, and which status code communicates "accepted, but not finished yet"?

<details>
<summary>Answer</summary>

`409` signals the request conflicts with the resource's current state (Example 8) -- the request
itself is well-formed, but applying it right now would produce an inconsistency. `422` signals the
request body is syntactically valid but semantically invalid -- a field fails a business rule, even
though the JSON itself parses fine. `202 Accepted` (Example 6) is the status for "accepted, but not
finished yet" -- a long-running operation that hands back a status URL to poll, distinct from `201`'s
"already fully created" (Example 5) and `204`'s "done, nothing to return" (Example 7).

</details>

**Q8 (co-08 -- problem-details).** Name the five fields RFC 9457's `application/problem+json` defines,
and which ones this course's own error envelope always includes.

<details>
<summary>Answer</summary>

`type`, `title`, `status`, `detail`, and `instance`. Example 12 builds the envelope with `type`,
`title`, `status`, and `detail` populated for every error; `instance` is optional per the RFC and
used when a specific occurrence needs its own identifying URI. Example 14 extends the same envelope
with field-level validation errors for a `422`, without abandoning the base shape.

</details>

**Q9 (co-09 -- openapi-contract).** What are the three top-level pieces of an OpenAPI 3.1 document
this course builds up incrementally, and what does a reusable component schema (`$ref`) buy you?

<details>
<summary>Answer</summary>

`info` (metadata), `paths` (the operations), and `components` (reusable, `$ref`-able schemas) --
Example 15 starts with just `info` + `paths`; Example 16 introduces a component schema referenced by
`$ref`, and Example 18 declares the full set of possible responses (`200`/`404`/`422`) per
operation. A `$ref`'d component schema means a shape like `Article` is defined exactly once and
reused everywhere it appears, instead of being copy-pasted into every operation that returns it --
one definition to update, not N.

</details>

**Q10 (co-10 -- openapi-json-schema).** Why does OpenAPI 3.1's alignment with JSON Schema Draft
2020-12 matter in practice, beyond being a version number?

<details>
<summary>Answer</summary>

Prior OpenAPI versions used a JSON-Schema-LIKE dialect with its own quirks; 3.1 aligns directly with
a real, standard JSON Schema draft, so validators, code generators, and other JSON-Schema-aware
tooling can work against an OpenAPI document's schemas without a translation layer (Example 17). In
practice this means keywords like `oneOf`, `const`, and JSON Schema's own composition rules behave
exactly as JSON Schema tooling elsewhere already expects them to.

</details>

**Q11 (co-11 -- openapi-codegen-mock).** What can be generated FROM an OpenAPI spec alone, without
writing a single handler, and why does that matter for a team building against an API that isn't
finished yet?

<details>
<summary>Answer</summary>

Human-readable documentation (Example 79, e.g. Swagger UI / Redoc), a mock server that returns
spec-shaped data (Example 21), and a typed client a consumer can call against (Example 22). A
frontend or mobile team can start building against the mock server's spec-shaped responses the
moment the contract is agreed, in parallel with the backend team building the real handlers -- the
spec, not a finished server, is what unblocks both sides.

</details>

**Q12 (co-12 -- request-validation).** What are the TWO directions a live request/response can be
validated against an OpenAPI schema, and why does validating only one direction leave a gap?

<details>
<summary>Answer</summary>

Inbound: validating an incoming request body against the schema before a handler even runs (Example 19) -- a malformed body is rejected before touching business logic. Outbound: validating a live
RESPONSE against the same schema (Example 20) -- confirming the server itself is honoring the
contract it published. Validating only the request direction leaves a real gap: a handler could
still emit a response that silently drifts from the spec, which is exactly the failure mode Example
72's conformance test exists to catch on the response side.

</details>

**Q13 (co-13 -- versioning-strategies).** Name the three versioning strategies this course covers,
and the real-world API each one traces to.

<details>
<summary>Answer</summary>

URI-path versioning (`/v1/...`, Example 29, Google AIP-185's convention: "v1, not v1.0"), header
versioning (Example 30, a custom version header), and query-parameter versioning (Example 31,
Microsoft Azure's `api-version=YYYY-MM-DD` convention, where OMITTING the parameter returns a `400
MissingApiVersionParameter`). Each is a genuine trade-off, not a strictly-better option -- co-27
covers when a caller-experience or discoverability concern favors one over another.

</details>

**Q14 (co-14 -- backward-compatible-change).** What makes adding a field "backward-compatible" while
removing one is not, and what test catches the removal case specifically?

<details>
<summary>Answer</summary>

Adding a new, OPTIONAL field never breaks an existing client, because a tolerant reader (co-02)
simply ignores fields it does not recognize (Example 32, Example 33). Removing a field a client
already depends on is a genuine break regardless of how "small" the field seems -- there is no way
for an existing client to keep working if it reads a field that is simply gone. Example 34's consumer
contract test is the specific mechanism that catches this: it asserts a real client's own
expectations against the CURRENT response shape and fails loudly the moment a depended-upon field
disappears.

</details>

**Q15 (co-15 -- deprecation-sunset).** What is the difference between the `Deprecation` header and
the `Sunset` header, and does either one actually stop a request from succeeding?

<details>
<summary>Answer</summary>

`Deprecation` (RFC 9745) signals that an endpoint or feature is deprecated, typically paired with a
`Link` header pointing to migration guidance (Example 35). `Sunset` (RFC 8594) communicates a
specific date after which the endpoint is expected to stop working (Example 36). Neither header
BLOCKS the request -- both are notification-only; the request still succeeds normally, and Example
73's versioned-migration example shows both the old and new version continuing to serve traffic
throughout the deprecation window, right up until the sunset date the caller was warned about.

</details>

**Q16 (co-16 -- offset-pagination).** How does `offset`/`limit` pagination work, and what specific
cost does it pay that a cursor-based approach avoids?

<details>
<summary>Answer</summary>

`offset`/`limit` pagination asks the server to skip `offset` rows and return the next `limit` (Example
23). Its specific cost is fetch-and-discard: to serve `offset=1000`, the underlying query still has
to scan through the first 1000 rows before it can return row 1001 -- work that grows linearly with
how deep into the result set a page sits, and that drifts if rows are inserted or deleted between
page requests. A cursor (co-17) sidesteps both problems by resuming from a stable position marker
instead of a raw count.

</details>

**Q17 (co-17 -- cursor-pagination).** What does a cursor actually encode, and why does that make it
stable under concurrent writes in a way `offset` is not?

<details>
<summary>Answer</summary>

A cursor encodes a position IN THE DATA ITSELF -- typically the last-seen item's own sort key --
rather than a raw count of rows to skip (Example 24). Resuming "after item with id=42" stays correct
even if rows are inserted or deleted elsewhere in the list, because the cursor's meaning does not
depend on how many rows happen to precede it at query time; `offset=1000` has no such anchor and
silently skips or repeats rows if the underlying set shifts between requests. Example 76 applies the
identical idea inside a GraphQL Relay-style connection (`edges`/`cursor`/`pageInfo`), and Example
80's capstone-preview closes the tier by combining cursor pagination with idempotent writes on one
endpoint.

</details>

**Q18 (co-18 -- idempotency-key).** Walk through what happens on a first `POST` with an
`Idempotency-Key`, a REPLAY of that same key, and a REUSE of that key with a different body.

<details>
<summary>Answer</summary>

First call: the server records the key alongside the response it produced and returns normally
(Example 37). A REPLAY -- the identical key AND the identical intended write, typically after a
client-side timeout -- returns the ORIGINAL recorded response instead of creating a second resource
(Example 38); this is Stripe's own prior-art pattern, since the formal IETF draft for this header
lapsed. A REUSE of the same key with a genuinely DIFFERENT body is a client bug, not a safe retry --
Example 39 shows the server rejecting it rather than silently either applying the new body or
returning the stale response for a request that isn't actually the same one.

</details>

**Q19 (co-19 -- rate-limit-429).** What status code communicates a caller has been rate-limited, and
what header tells the caller when it is safe to try again?

<details>
<summary>Answer</summary>

`429 Too Many Requests` (RFC 6585). The `Retry-After` header, when present, tells the caller how many
seconds (or a specific date) to wait before its next attempt is likely to succeed (Example 40).
Example 74 combines this with idempotency on one endpoint and establishes a specific ordering: the
rate-limit check runs BEFORE idempotency bookkeeping, so a rejected `429` call never even reaches the
idempotency-key logic.

</details>

**Q20 (co-20 -- ratelimit-headers).** What do the structured `RateLimit`/`RateLimit-Policy` headers
expose that a bare `429` status code alone does not?

<details>
<summary>Answer</summary>

They expose the CURRENT quota state proactively, on every response, not just once the limit is
already exceeded -- `limit`, `remaining`, and a reset window (Example 41). A caller can watch
`remaining` count down toward zero (Example 42) and slow down voluntarily before ever hitting a
`429`, instead of only discovering the limit reactively after being rejected. These are an ACTIVE
IETF draft (unlike the lapsed Idempotency-Key draft, co-18), standardizing what the older,
non-standard `X-RateLimit-*` convention did informally.

</details>

**Q21 (co-21 -- content-negotiation).** Name the three `Accept*` / `Content-Type` headers this course
covers and what each one negotiates.

<details>
<summary>Answer</summary>

`Content-Type` declares what format the REQUEST body is actually in (Example 26, e.g.
`application/json`, so the server knows how to parse it); `Accept` tells the server what
representation the CLIENT wants back (Example 27, e.g. choosing JSON vs. CSV for the same resource);
`Accept-Language` selects which LANGUAGE a message comes back in (Example 28). All three are
content-negotiation headers, but they negotiate three different axes of the same response: format
in, format out, and language.

</details>

**Q22 (co-22 -- http-caching-etag).** How does `ETag` + `If-None-Match` avoid re-sending an unchanged
resource, and what does `If-Match` protect against instead?

<details>
<summary>Answer</summary>

The server tags a representation with an opaque `ETag`; a client resending `If-None-Match` with that
same tag gets a `304 Not Modified` with no body if the representation is unchanged (Example 43),
saving the bandwidth of re-sending identical data. `Cache-Control: max-age` (Example 44) lets a
client skip asking the server at all, for a bounded window. `If-Match` is the INVERSE use of the same
tag on a WRITE: it protects against a lost update by requiring the client to prove it last read the
CURRENT version before overwriting it -- a stale `If-Match` value gets rejected with `412 Precondition
Failed` (Example 45), rather than silently clobbering a change the client never saw.

</details>

**Q23 (co-23 -- auth-bearer-token).** What is the difference between a bearer token and an API key in
this course's own examples, and what does a "scope" add beyond just "is this token valid"?

<details>
<summary>Answer</summary>

A bearer token (Example 46, `Authorization: Bearer <token>`, RFC 6750) is typically issued through an
OAuth 2.0 flow and identifies a specific authenticated session or client. An API key (Example 47, a
custom `X-API-Key` header) is a simpler, longer-lived credential, often tied directly to one
application or account rather than a session. A SCOPE (Example 48) narrows what an otherwise-valid
token is allowed to DO -- a token can be genuinely valid and still lack the specific scope an
operation requires, which is why a scope check is a separate step from mere token validation,
returning `403` rather than `401` when it fails.

</details>

**Q24 (co-24 -- graphql-schema).** What problem does GraphQL's client-specified field selection solve
that a fixed REST response shape cannot, on its own?

<details>
<summary>Answer</summary>

A REST endpoint's response shape is fixed for every caller -- a caller needing only a `title` still
receives every other field the endpoint returns (over-fetching), and a caller needing MORE than one
endpoint provides has to make several separate round trips (under-fetching). GraphQL's schema
(Example 57) lets each caller specify exactly the fields it wants in the query itself (Example 58),
and Example 59 measures the SAME data fetched both ways to make the over-fetching gap concrete;
Example 62 shows the same selective-shape idea applied to a write via a mutation.

</details>

**Q25 (co-25 -- graphql-resolver-n1).** What is the N+1 problem in a GraphQL resolver, and how does
DataLoader batching fix it?

<details>
<summary>Answer</summary>

A naive resolver that fetches a parent's related items ONE AT A TIME -- once per parent in a list --
issues 1 query for the parent list plus N further queries, one per parent, for their related data
(Example 60 shows a single resolved field; Example 61 shows the N+1 pattern emerging once resolvers
are called across a list). DataLoader batches all N of those individual per-parent lookups within
one execution tick into a SINGLE bulk query, collapsing N+1 calls down to 2 total, regardless of how
large N grows.

</details>

**Q26 (co-26 -- grpc-protobuf).** What is Protocol Buffers' role in a gRPC service, and name the four
RPC kinds gRPC supports.

<details>
<summary>Answer</summary>

Protobuf is BOTH the interface-definition language (`.proto` files declare services and message
types, Example 63) and the wire format messages are serialized into -- a single artifact defines the
contract AND the binary encoding, unlike REST's separation of OpenAPI (contract) from JSON (format).
The four RPC kinds: unary (Example 64, one request/one response), server-streaming (Example 65, one
request/many responses), client-streaming (one request stream/one response, not separately worked in
this course), and bidirectional streaming (Example 66, both sides stream independently).

</details>

**Q27 (co-27 -- style-selection).** What is this course's own position on picking REST vs. GraphQL
vs. gRPC, and name one force that favors each.

<details>
<summary>Answer</summary>

There is no universal winner -- the choice is driven by specific forces, not a general ranking
(Example 69's decision matrix). REST favors cacheability and human-debuggability for a public API
with many unknown clients (Example 67 contrasts REST's `GET`-cacheability against GraphQL riding over
`POST` and gRPC's binary framing). GraphQL favors a client needing to shape a response across several
different screens with different data needs (co-24). gRPC favors typed, high-throughput
internal service-to-service calls where a shared Protobuf schema and streaming matter more than
public cacheability (Example 78 measures a concrete payload-size proxy for the tradeoff); Example
68 additionally contrasts how each style EVOLVES a field over time.

</details>

**Q28 (co-28 -- hateoas-hypermedia).** Name two concrete hypermedia formats this course covers, and
what a client following `_links` gains over one that hardcodes every URL it calls.

<details>
<summary>Answer</summary>

HAL (`_links` required, `_embedded` optional, Example 56) and JSON:API's sparse fieldsets alongside
its own linking convention (Example 51). Example 11 introduces `_links` in isolation; Example 77
builds a client that NAVIGATES purely by following the links a response provides, rather than
constructing URLs from a hardcoded template -- if the server later moves or restructures an endpoint,
a hypermedia-driven client keeps working as long as the LINK RELATIONS stay stable, while a
hardcoded-URL client breaks the moment the server's URL structure changes underneath it.

</details>

**Q29 (co-29 -- pagination-envelope).** What three fields make up this course's consistent pagination
envelope, and why does bundling them together matter more than any one field alone?

<details>
<summary>Answer</summary>

`data` (the actual items on this page), `has_more` (a boolean telling the caller whether a next page
exists), and `next_cursor` (the value to pass to fetch that next page) (Example 25). Bundling them
into ONE envelope, applied the same way on every list endpoint, means a client's paging loop works
identically everywhere -- keep fetching while `has_more` is true, passing `next_cursor` forward each
time -- rather than re-learning a slightly different pagination shape per endpoint. This is the same
uniformity argument co-30 makes for errors, applied to lists instead.

</details>

**Q30 (co-30 -- error-envelope-consistency).** Why does using the SAME error shape across every
endpoint matter more than each endpoint's error being individually well-designed?

<details>
<summary>Answer</summary>

A caller writing error-handling code once, against ONE shape, can apply that same handling logic to
every endpoint in the API -- Example 13 demonstrates three different endpoints returning the
identical `problem+json` shape for their own distinct errors. If each endpoint invented its own error
format, even a well-designed one, a client would need bespoke handling per endpoint, defeating the
whole point of a uniform contract. Example 75 extends the consistency question across API styles:
GraphQL's partial-errors-inside-a-200-response model is a genuinely different error philosophy from
REST's `problem+json`, and naming that difference explicitly is part of what "consistent" has to mean
once more than one style is in play.

</details>

**Q31 (co-31 -- partial-response-field-selection).** How does `?fields=` differ from JSON:API's
sparse fieldsets, and what do both accomplish that GraphQL's field selection (co-24) also
accomplishes, by a different mechanism?

<details>
<summary>Answer</summary>

`?fields=` (Example 50) is a simple, ad-hoc query parameter naming which top-level fields to return.
JSON:API's sparse fieldsets (Example 51) standardize the identical idea (`fields[type]=...`) as part
of a broader specification with its own conventions for relationships and linking. Both let a REST
caller narrow a response's shape WITHOUT switching to GraphQL -- the same over-fetching problem
GraphQL's schema-level field selection solves, solved instead at the query-string level on top of an
otherwise ordinary REST endpoint.

</details>

**Q32 (co-32 -- bulk-batch-endpoints).** What is the difference between `POST /batch` (Example 52)
and a dedicated bulk-create endpoint (Example 53), and why does either matter for round-trip cost?

<details>
<summary>Answer</summary>

`POST /batch` bundles N heterogeneous operations (a mix of creates, updates, deletes across
different resources) into one request, with each sub-operation's own result reported individually in
the response. A dedicated bulk-create endpoint is narrower -- it creates MANY of the SAME resource
type in one call. Both exist to collapse what would otherwise be N separate round trips into one,
which matters directly for `consistency-latency-throughput`: N round trips pay N times the network
latency overhead that one batched round trip pays once.

</details>

**Q33 (co-33 -- webhook-api-surface).** Why is HMAC-signing an outbound webhook payload necessary,
given that the webhook is already being sent over HTTPS?

<details>
<summary>Answer</summary>

HTTPS protects the payload IN TRANSIT from a third party reading or tampering with it, but it says
nothing about who is calling the RECEIVING endpoint -- Example 54 registers a webhook subscription,
and the receiving endpoint has no inherent way to confirm an incoming request genuinely came from the
API provider rather than an attacker who simply found the URL. Example 55's HMAC signature, computed
with a shared secret and verified by the receiver, proves the payload was produced by a party that
knows the secret -- a form of authentication ON TOP OF transport security, not a replacement for it.

</details>

**Q34 (co-34 -- openapi-security-schemes).** Why does declaring `bearer`/`apiKey` security schemes
INSIDE the OpenAPI spec matter, beyond documenting them in prose?

<details>
<summary>Answer</summary>

A security scheme declared in the spec itself (Example 49) is machine-readable -- the same
mock-server, codegen, and doc-rendering tooling that reads `paths`/`components` (co-09, co-11) can
also generate a working "Authorize" button in rendered docs, or a typed client that already knows how
to attach the right header, without a human re-reading a paragraph of prose to figure out how auth
works. Declaring it only in prose means every consumer of the spec has to re-discover the same
information by hand, defeating OpenAPI's whole point as a SINGLE machine-readable source of truth.

</details>

## Applied problems

Fourteen scenarios. Each describes a task without naming the construct -- decide which HTTP
mechanism, OpenAPI feature, or design decision solves it, then check.

**AP1.** A public API's `POST /orders` endpoint is being retried automatically by a client's HTTP
library after a transient network timeout, and the team is seeing duplicate orders show up for a
single genuine purchase attempt.

<details>
<summary>Answer</summary>

An `Idempotency-Key` header on the write, checked server-side before creating anything new (co-18;
Example 37, Example 38). The retry carries the SAME key as the original attempt, so the server
recognizes it as a replay and returns the original response instead of creating a second order.

</details>

**AP2.** A dashboard needs to show whether a resource has changed since the client last fetched it,
without re-downloading the full (large) payload on every poll if nothing actually changed.

<details>
<summary>Answer</summary>

`ETag` + `If-None-Match`, returning `304 Not Modified` with no body when the representation is
unchanged (co-22; Example 43). The client resends the ETag it last saw; a `304` confirms nothing
changed without ever re-sending the payload.

</details>

**AP3.** A mobile client needs to display a resource's `title` and `thumbnail_url` on a list screen,
but the full REST resource returned by the existing endpoint also includes a `body` field that can
be tens of kilobytes of text -- fine for the detail screen, wasteful for the list.

<details>
<summary>Answer</summary>

Either `?fields=title,thumbnail_url` (co-31; Example 50) on the existing REST endpoint, or, if the
data needs of different SCREENS diverge more broadly than one query parameter comfortably expresses,
a GraphQL query that selects exactly those two fields (co-24; Example 58) -- either way, the
mechanism is narrowing the response shape to what THIS caller actually needs, not changing what the
underlying resource contains.

</details>

**AP4.** An API team wants to retire an old endpoint but needs existing integrators to have real
advance notice and a concrete date, rather than the endpoint simply breaking with no warning one day.

<details>
<summary>Answer</summary>

`Deprecation` (signals it is deprecated now, with a `Link` to migration guidance) paired with
`Sunset` (states the specific date it will actually stop working) -- both notification-only headers,
neither blocking the request itself during the window (co-15; Example 35, Example 36, Example 73).

</details>

**AP5.** Two application servers both attempt to update the SAME order resource at nearly the same
instant, each believing it is working from the current, unmodified version -- the team needs to
guarantee the second writer's change does not silently overwrite the first writer's change without
either side knowing a conflict occurred.

<details>
<summary>Answer</summary>

Optimistic concurrency via `If-Match` -- the second write's stale `If-Match` value (computed against
data that has since changed) gets rejected with `412 Precondition Failed` rather than silently
succeeding and clobbering the first writer's change (co-22; Example 45).

</details>

**AP6.** A frontend team keeps needing to make three separate REST calls to assemble one page --
first the article, then its author, then the author's most recent five articles -- and wants that
collapsed into a single round trip driven by exactly what THIS page needs, since a different page
elsewhere needs a different combination of the same underlying data.

<details>
<summary>Answer</summary>

A GraphQL query selecting article, author, and the author's recent articles as one nested query
(co-24; Example 58) -- one round trip, shaped by the caller, rather than a fixed REST response
requiring several separate calls to assemble the equivalent view.

</details>

**AP7.** A public API needs to raise its major version because of a genuinely breaking change, but
the team also wants version selection to work cleanly with existing HTTP caching infrastructure that
keys on the URL alone.

<details>
<summary>Answer</summary>

URI-path versioning (`/v1/...` vs `/v2/...`, co-13; Example 29) -- because the version is baked into
the URL itself, an HTTP cache (or CDN) naturally treats `v1` and `v2` responses as distinct cache
entries with no special configuration; header- or query-param-based versioning (Example 30, Example 31) would need extra cache-key configuration to avoid conflating the two versions' responses under
one cached URL.

</details>

**AP8.** A billing API's write endpoint is being hit by a runaway retry loop from one misbehaving
integrator, and the team needs both to reject the excess calls AND give that integrator's client
library a machine-readable signal of exactly how much quota remains and when to try again.

<details>
<summary>Answer</summary>

`429 Too Many Requests` with a `Retry-After` header for the immediate rejection (co-19; Example 40),
combined with the structured `RateLimit`/`RateLimit-Policy` headers on EVERY response (not just the
rejected one) so the caller can watch its remaining quota proactively and slow down before hitting
`429` again (co-20; Example 41, Example 42).

</details>

**AP9.** A large internal service mesh needs a typed, high-throughput contract between two backend
services that both control, with one endpoint needing to stream a large result set back
incrementally rather than buffering the whole thing before responding.

<details>
<summary>Answer</summary>

gRPC with a server-streaming RPC (co-26; Example 65) -- a typed Protobuf contract for internal
service-to-service calls, with server-streaming specifically for incrementally returning a large
result set instead of buffering it entirely before the first byte goes out.

</details>

**AP10.** A backend team wants a frontend team to start building UI against a not-yet-implemented
endpoint's exact response shape, without waiting for the real handler to be written first.

<details>
<summary>Answer</summary>

Write the OpenAPI spec first (co-09; Example 15, Example 70) and stand up a mock server generated
directly from it (co-11; Example 21) -- the frontend team codes against the mock's spec-shaped
responses immediately, and the real handler is implemented afterward to conform to the SAME already-
agreed contract (Example 71).

</details>

**AP11.** A migration script needs to load 500 new resources in one request rather than issuing 500
separate `POST` calls, and the caller needs to know individually which of the 500 succeeded and which
failed, rather than an all-or-nothing result.

<details>
<summary>Answer</summary>

A bulk-create endpoint (co-32; Example 53) that reports each sub-item's own result individually in
the response body -- collapsing 500 round trips into one, while still surfacing per-item success/
failure rather than a single opaque pass/fail for the whole batch.

</details>

**AP12.** An events system needs to notify a third-party integrator's server the moment an order
ships, and that integrator's receiving endpoint needs a way to confirm an incoming notification
genuinely came from the API provider and was not forged by an attacker who discovered the URL.

<details>
<summary>Answer</summary>

An outbound webhook (co-33; Example 54) with an HMAC signature computed over the payload using a
shared secret (Example 55) -- the receiver recomputes the signature and compares it, proving the
payload's origin, which HTTPS alone (protecting only the transport) does not.

</details>

**AP13.** A GraphQL API's list-of-comments resolver is issuing one extra database query PER COMMENT
to fetch each comment's author, and a query log shows the total query count scaling linearly with
however many comments happen to be on the page.

<details>
<summary>Answer</summary>

DataLoader batching (co-25; Example 61) -- collapsing the N per-comment author lookups within one
execution tick into a single bulk query, fixing the classic GraphQL N+1 pattern regardless of how
many comments the page happens to show.

</details>

**AP14.** A team building a NEW public API is choosing between REST and GraphQL, and one stakeholder
argues GraphQL should win by default because "it is strictly more flexible." Another stakeholder
points out the API needs to be cacheable by a shared CDN in front of many anonymous, unauthenticated
readers.

<details>
<summary>Answer</summary>

REST wins here specifically because of the CDN-cacheability requirement -- GraphQL typically rides
over `POST`, which most HTTP caches and CDNs do not cache by default, while REST's `GET` requests are
naturally cacheable (co-27; Example 67). "Strictly more flexible" is not the deciding force; the
SPECIFIC force this scenario names -- CDN caching for anonymous readers -- is, exactly the kind of
scenario Example 69's decision matrix is built to reason through rather than defaulting to either
style.

</details>

## Code katas

Six hands-on repetition drills against small, self-contained, genuinely-executed Python fixtures --
pure standard library, no external dependency. Each is a before/after `kata.py` file colocated under
`drilling/code/`. Every "before" script is real and misapplies a concept this course teaches -- run
it yourself, diagnose the bug from the observed output, fix it from memory, then compare your fix
against the "after" script and the model solution before checking your work against the shown
output.

### Kata 1 -- Idempotency-Key accepted but never checked

**Task.** `create_article` is meant to make a client retry with the same `Idempotency-Key` safe --
but the key is only ever accepted as a parameter, never looked up. A replayed request creates a
SECOND article instead of returning the original.

**Before** (`drilling/code/kata-01-idempotency-key-not-checked/before/kata.py`)

```python
# pyright: strict
"""Kata 1 (before): POST accepts an Idempotency-Key header but never checks it."""

STORE: dict[int, dict[str, object]] = {}
NEXT_ID = [1]


def create_article(idempotency_key: str, title: str) -> dict[str, object]:
    # THE BUG: idempotency_key is accepted as a parameter but never looked up
    # anywhere -- every call creates a new article, key or no key.
    new_id = NEXT_ID[0]
    article: dict[str, object] = {"id": new_id, "title": title}
    STORE[new_id] = article
    NEXT_ID[0] += 1
    return article


first = create_article("retry-key-1", "Launch Announcement")
print(f"first call: {first}")

replay = create_article("retry-key-1", "Launch Announcement")  # a client retry after a timeout
print(f"replay call (same key): {replay}")

print(f"total articles created: {len(STORE)}")
```

**Observed (buggy) output**:

```text
first call: {'id': 1, 'title': 'Launch Announcement'}
replay call (same key): {'id': 2, 'title': 'Launch Announcement'}
total articles created: 2
```

<details>
<summary>Model solution</summary>

```python
# THE FIX: check IDEMPOTENCY_STORE first -- a known key returns the ORIGINAL
# response instead of creating a second article.
IDEMPOTENCY_STORE: dict[str, dict[str, object]] = {}


def create_article(idempotency_key: str, title: str) -> dict[str, object]:
    if idempotency_key in IDEMPOTENCY_STORE:
        return IDEMPOTENCY_STORE[idempotency_key]
    new_id = NEXT_ID[0]
    article: dict[str, object] = {"id": new_id, "title": title}
    STORE[new_id] = article
    IDEMPOTENCY_STORE[idempotency_key] = article
    NEXT_ID[0] += 1
    return article
```

**Root cause**: the "before" version accepts `idempotency_key` as a parameter purely for show -- it
is never used to look anything up, so the function has no way to recognize a replay from a genuinely
new request (co-18; Example 37, Example 38). Checking `IDEMPOTENCY_STORE` first restores the
guarantee: a known key short-circuits straight to the ORIGINAL response.

**Run**: `python3 kata.py`

**Output**:

```text
first call: {'id': 1, 'title': 'Launch Announcement'}
replay call (same key): {'id': 1, 'title': 'Launch Announcement'}
total articles created: 1
```

</details>

### Kata 2 -- offset pagination's slicing bug

**Task.** `list_articles(offset, limit)` is meant to return the NEXT `limit` articles starting at
`offset`. The version below treats `limit` as an absolute end index instead of a count, so every
page after the first comes back empty.

**Before** (`drilling/code/kata-02-offset-pagination-off-by-one/before/kata.py`)

```python
# pyright: strict
"""Kata 2 (before): a slicing bug shrinks every page as the offset grows."""

ARTICLES: list[str] = [f"Article {i}" for i in range(1, 11)]  # 10 articles, "Article 1".."Article 10"


def list_articles(offset: int, limit: int) -> list[str]:
    # THE BUG: articles[offset:limit] treats `limit` as an ABSOLUTE end index,
    # not a COUNT -- the window shrinks (or vanishes) as offset grows past limit.
    return ARTICLES[offset:limit]


page_1 = list_articles(offset=0, limit=3)
print(f"page 1 (offset=0, limit=3): {page_1}")

page_2 = list_articles(offset=3, limit=3)  # intent: the NEXT 3 articles
print(f"page 2 (offset=3, limit=3): {page_2}")  # BUG: empty -- offset(3) >= limit(3)

page_3 = list_articles(offset=6, limit=3)
print(f"page 3 (offset=6, limit=3): {page_3}")  # BUG: still empty
```

**Observed (buggy) output**:

```text
page 1 (offset=0, limit=3): ['Article 1', 'Article 2', 'Article 3']
page 2 (offset=3, limit=3): []
page 3 (offset=6, limit=3): []
```

<details>
<summary>Model solution</summary>

```python
# THE FIX: the end index is offset + limit -- limit is a COUNT of items to
# return, not an absolute position in the list.
def list_articles(offset: int, limit: int) -> list[str]:
    return ARTICLES[offset : offset + limit]
```

**Root cause**: `offset`/`limit` pagination (co-16; Example 23) means "skip `offset` items, then
return the next `limit` items" -- the slice's end must therefore be `offset + limit`, a COUNT added
to a starting position, not `limit` used on its own as an absolute index. The buggy version's window
shrinks to nothing the instant `offset >= limit`, exactly the off-by-one class of bug that makes
cursor pagination (co-17) attractive for anything beyond a small, fixed dataset.

**Run**: `python3 kata.py`

**Output**:

```text
page 1 (offset=0, limit=3): ['Article 1', 'Article 2', 'Article 3']
page 2 (offset=3, limit=3): ['Article 4', 'Article 5', 'Article 6']
page 3 (offset=6, limit=3): ['Article 7', 'Article 8', 'Article 9']
```

</details>

### Kata 3 -- weak vs. strong ETag comparison

**Task.** `check_not_modified` is meant to return `304` whenever the client's ETag matches the
server's current representation, INCLUDING when an intermediary has tagged the value weak (`W/`
prefix). The version below compares the raw strings directly, so a weak-tagged match is missed.

**Before** (`drilling/code/kata-03-etag-strong-comparison-bug/before/kata.py`)

```python
# pyright: strict
"""Kata 3 (before): comparing a weak ETag against a stored strong ETag never matches."""

STORED_ETAG = '"abc123"'  # the server's own strong validator for the current representation


def check_not_modified(if_none_match: str) -> int:
    # THE BUG: a weak validator ("W/" prefix) is semantically equivalent for a
    # GET's freshness check, but this direct string comparison treats the
    # "W/" prefix as making the values genuinely different.
    if if_none_match == STORED_ETAG:
        return 304
    return 200


weak_client_etag = 'W/"abc123"'  # the SAME representation, tagged weak by an intermediary
status = check_not_modified(weak_client_etag)
print(f"status for weak ETag of the SAME representation: {status}")  # BUG: 200, should be 304
```

**Observed (buggy) output**:

```text
status for weak ETag of the SAME representation: 200
```

<details>
<summary>Model solution</summary>

```python
# THE FIX: strip the "W/" prefix before comparing -- weak comparison only
# needs the OPAQUE TAG to match, not the literal string with its prefix.
def strip_weak_prefix(etag: str) -> str:
    return etag[2:] if etag.startswith("W/") else etag


def check_not_modified(if_none_match: str) -> int:
    if strip_weak_prefix(if_none_match) == strip_weak_prefix(STORED_ETAG):
        return 304
    return 200
```

**Root cause**: co-22's `ETag`/`If-None-Match` mechanism (Example 43) is meant to detect an unchanged
representation, and a WEAK validator (`W/"..."`) is semantically equivalent to its strong counterpart
for exactly this freshness check -- only strict byte-for-byte comparisons (like `If-Match`'s
optimistic-concurrency use, also co-22, Example 45) need to treat weak and strong tags as distinct.
Comparing the raw literal strings conflates the two use cases and produces an unnecessary `200`
where a `304` was correct.

**Run**: `python3 kata.py`

**Output**:

```text
status for weak ETag of the SAME representation: 304
```

</details>

### Kata 4 -- token validity checked, scope never checked

**Task.** `delete_article` is meant to require BOTH a valid token AND the `articles:delete` scope.
The version below checks only that the token is known, so a read-only token can perform a delete.

**Before** (`drilling/code/kata-04-missing-scope-check/before/kata.py`)

```python
# pyright: strict
"""Kata 4 (before): a bearer token is validated, but its SCOPE is never checked."""

VALID_TOKENS: dict[str, list[str]] = {"tok-readonly": ["articles:read"]}


def delete_article(token: str) -> int:
    # THE BUG: presence and validity of the token is checked (401 if missing/unknown),
    # but the token's OWN scopes are never inspected against what this operation needs.
    if token not in VALID_TOKENS:
        return 401
    return 204  # BUG: a read-only token can delete -- no scope gate at all


status = delete_article("tok-readonly")  # a token that can only READ articles
print(f"delete with read-only token: status={status}")  # BUG: 204, should be 403
```

**Observed (buggy) output**:

```text
delete with read-only token: status=204
```

<details>
<summary>Model solution</summary>

```python
# THE FIX: the token's OWN scopes must include what this operation requires.
REQUIRED_SCOPE = "articles:delete"


def delete_article(token: str) -> int:
    if token not in VALID_TOKENS:
        return 401
    if REQUIRED_SCOPE not in VALID_TOKENS[token]:
        return 403
    return 204
```

**Root cause**: co-23 treats "is this token valid" and "does this token have the scope this
operation needs" as two SEPARATE checks (Example 46, Example 48) -- the buggy version only performs
the first. A token can be entirely genuine and still lack the specific permission a write requires,
which is exactly why the correct rejection is `403 Forbidden` (authenticated but not authorized),
not `401 Unauthorized` (not authenticated at all).

**Run**: `python3 kata.py`

**Output**:

```text
delete with read-only token: status=403
```

</details>

### Kata 5 -- GraphQL resolver ignores the field selection

**Task.** `resolve_article` is meant to return ONLY the fields the caller's own query named. The
version below returns the full record regardless of what was requested, defeating the entire
over-fetch-avoidance point of a GraphQL selection set.

**Before** (`drilling/code/kata-05-graphql-resolver-ignores-selection/before/kata.py`)

```python
# pyright: strict
"""Kata 5 (before): the resolver returns the FULL record, ignoring the caller's field selection."""

from typing import Any

ARTICLE: dict[str, object] = {"id": 1, "title": "Hello, GraphQL", "body": "A very long article body..."}


def resolve_article(requested_fields: list[str]) -> dict[str, Any]:
    # THE BUG: `requested_fields` is accepted as a parameter but never used to
    # narrow the response -- the caller always gets EVERY field, defeating the
    # entire over-fetch-avoidance point of a GraphQL selection set.
    return {"data": {"article": ARTICLE}}


narrow_query = resolve_article(["title"])  # the caller asked for ONLY title
print(f"caller asked for ['title'], got: {narrow_query}")  # BUG: id and body leak through too
```

**Observed (buggy) output**:

```text
caller asked for ['title'], got: {'data': {'article': {'id': 1, 'title': 'Hello, GraphQL', 'body': 'A very long article body...'}}}
```

<details>
<summary>Model solution</summary>

```python
# THE FIX: build the response from ONLY the fields the caller's own query named.
def resolve_article(requested_fields: list[str]) -> dict[str, Any]:
    selected = {field: ARTICLE[field] for field in requested_fields if field in ARTICLE}
    return {"data": {"article": selected}}
```

**Root cause**: co-24's whole value proposition is that the CALLER'S query, not the server, decides
the response shape (Example 58) -- the buggy resolver ignores `requested_fields` entirely and always
serializes the full record, which is functionally identical to REST's fixed-shape response (co-27's
own over-fetching problem) despite superficially using GraphQL syntax. Filtering the dict comprehension
down to only the requested keys restores the actual point of field selection.

**Run**: `python3 kata.py`

**Output**:

```text
caller asked for ['title'], got: {'data': {'article': {'title': 'Hello, GraphQL'}}}
```

</details>

### Kata 6 -- RateLimit header reports the WRONG remaining count

**Task.** The `RateLimit` header is meant to report how much budget remains AFTER this call is
counted. The version below builds the header BEFORE decrementing, so it always overstates the
caller's true remaining quota by exactly one.

**Before** (`drilling/code/kata-06-ratelimit-remaining-off-by-one/before/kata.py`)

```python
# pyright: strict
"""Kata 6 (before): the RateLimit header reports remaining BEFORE this call's own cost is deducted."""

BUDGET = [3]


def call_and_report() -> str:
    # THE BUG: the header is built from BUDGET[0] BEFORE decrementing -- the
    # caller is told it has one MORE request left than it actually does, right
    # up until the call that reports remaining=0 and then gets rejected anyway.
    header = f"limit=3, remaining={BUDGET[0]}"
    BUDGET[0] -= 1
    return header


print(f"call 1: {call_and_report()}")  # BUG: claims remaining=3, but THIS call already used 1
print(f"call 2: {call_and_report()}")  # BUG: claims remaining=2, actually 1 left
print(f"call 3: {call_and_report()}")  # BUG: claims remaining=1, actually 0 left -- next call is rejected
```

**Observed (buggy) output**:

```text
call 1: limit=3, remaining=3
call 2: limit=3, remaining=2
call 3: limit=3, remaining=1
```

<details>
<summary>Model solution</summary>

```python
# THE FIX: decrement FIRST, then report -- the header always reflects budget
# genuinely remaining AFTER this call has already been counted.
def call_and_report() -> str:
    BUDGET[0] -= 1
    return f"limit=3, remaining={BUDGET[0]}"
```

**Root cause**: co-20's structured `RateLimit` header exists so a caller can trust `remaining` enough
to slow down BEFORE hitting `429` (Example 41, Example 42) -- a header that overstates the true
remaining budget by one defeats that purpose, since a caller trusting `remaining=1` after call 3
would send a fourth call expecting it to succeed, only to be rejected. Decrementing before building
the header, not after, makes the reported number match the caller's TRUE remaining budget exactly.

**Run**: `python3 kata.py`

**Output**:

```text
call 1: limit=3, remaining=2
call 2: limit=3, remaining=1
call 3: limit=3, remaining=0
```

</details>

## Self-check checklist

Confirm each item without checking the manual first. If you hesitate, that concept needs another
pass.

- [ ] I can explain why "an API is a promise to callers you don't control" changes how I treat a
      field rename. (co-01)
- [ ] I can explain what a tolerant-reader client does, and what server-side change it protects
      against. (co-02)
- [ ] I can name Fielding's six REST constraints and which one HATEOAS is a sub-constraint of.
      (co-03)
- [ ] I can classify an API at a Richardson Maturity Model level and explain why level 3 requires
      hypermedia. (co-04)
- [ ] I can model a resource as a noun-based URI instead of an RPC-style verb-in-the-path endpoint.
      (co-05)
- [ ] I can name which HTTP methods are idempotent per RFC 9110 and demonstrate the difference with
      a repeated call. (co-06)
- [ ] I can choose the correct status code among `201`/`202`/`204`/`409`/`422`/`429` for a given
      scenario. (co-07)
- [ ] I can build an `application/problem+json` error envelope with `type`/`title`/`status`/
      `detail`. (co-08)
- [ ] I can write a minimal OpenAPI 3.1 document with `info`, `paths`, and a `$ref`'d component
      schema. (co-09)
- [ ] I can explain what OpenAPI 3.1's alignment with JSON Schema Draft 2020-12 buys in practice.
      (co-10)
- [ ] I can name what can be generated from an OpenAPI spec alone: docs, a mock server, a typed
      client. (co-11)
- [ ] I can validate both a request body AND a live response against an OpenAPI schema. (co-12)
- [ ] I can implement URI-path, header-based, and query-param versioning, and name a real API each
      traces to. (co-13)
- [ ] I can add a backward-compatible field and explain why removing one is different. (co-14)
- [ ] I can send `Deprecation` and `Sunset` headers and explain that neither blocks the request.
      (co-15)
- [ ] I can implement `offset`/`limit` pagination and explain its fetch-and-discard cost. (co-16)
- [ ] I can implement cursor pagination and explain why it stays stable under concurrent writes.
      (co-17)
- [ ] I can implement Idempotency-Key handling: record, replay, and reject-on-mismatch. (co-18)
- [ ] I can return `429` with `Retry-After` when a caller exceeds its rate limit. (co-19)
- [ ] I can expose structured `RateLimit`/`RateLimit-Policy` headers with a correctly decrementing
      remaining count. (co-20)
- [ ] I can implement `Content-Type`, `Accept`, and `Accept-Language` negotiation. (co-21)
- [ ] I can implement `ETag`/`If-None-Match` (`304`), `Cache-Control`, and `If-Match` optimistic
      concurrency (`412`). (co-22)
- [ ] I can implement bearer-token and API-key auth, plus a scope check returning `403` when scope
      is missing. (co-23)
- [ ] I can define a GraphQL schema and write a resolver that honors the caller's own field
      selection. (co-24)
- [ ] I can identify an N+1 resolver pattern and fix it with DataLoader-style batching. (co-25)
- [ ] I can write a `.proto` service definition and explain gRPC's four RPC kinds. (co-26)
- [ ] I can pick REST, GraphQL, or gRPC for a given scenario and name the SPECIFIC force driving the
      choice, not a general preference. (co-27)
- [ ] I can build a HAL `_links` response and a client that navigates purely by following it. (co-28)
- [ ] I can build a consistent `{data, has_more, next_cursor}` pagination envelope. (co-29)
- [ ] I can explain why the SAME error shape across every endpoint matters more than any one
      endpoint's error design. (co-30)
- [ ] I can implement `?fields=` or JSON:API sparse fieldsets to narrow a REST response. (co-31)
- [ ] I can design a batch endpoint reporting per-item success/failure instead of one opaque
      pass/fail. (co-32)
- [ ] I can register a webhook and HMAC-sign its outbound payload. (co-33)
- [ ] I can declare a `bearer`/`apiKey` security scheme inside an OpenAPI spec itself, not just in
      prose. (co-34)

## Elaborative interrogation & self-explanation

Six why/why-not prompts. Answer each in your own words before opening the model explanation.

**E1.** Why does a stable, versioned, well-documented API contract count as an example of
`coupling-vs-cohesion`, rather than just "good API hygiene"?

<details>
<summary>Model explanation</summary>

`coupling-vs-cohesion` names something structural: a good contract is what lets a client and a
server change on independent schedules, because the contract -- not either side's internals -- is
the only thing either party has to hold constant. A tolerant-reader client (co-02) and a
backward-compatible server change (co-14) are two halves of the SAME decoupling: the server can add
fields freely, and the client can ignore fields it doesn't need, precisely because neither depends
on the other's implementation, only on the shared, published shape. A leaky, undocumented API instead
COUPLES every consumer directly to the server's current internal representation -- any internal
change risks breaking someone, because there was never a stable, independent surface separating
"what the server happens to do today" from "what it promised."

</details>

**E2.** Why do pagination, rate limiting, and the REST/GraphQL/gRPC style choice all count as
`consistency-latency-throughput` decisions, when none of them are explicitly about a database's own
consistency model?

<details>
<summary>Model explanation</summary>

`consistency-latency-throughput` in this course's framing is broader than a database's own CAP-style
guarantees -- it names the general tension between how fast a single call resolves (latency), how
much total load a system can sustain (throughput), and how strictly correct or up-to-date the answer
has to be (consistency). Offset pagination (co-16) trades simplicity for a fetch-and-discard latency
cost that grows with page depth; cursor pagination (co-17) trades a slightly more complex client for
flat latency regardless of depth. Rate limiting (co-19, co-20) is explicitly a throughput decision --
protecting the system's total sustainable load at the cost of an individual caller's latency when
throttled. The REST/GraphQL/gRPC choice (co-27) is the same tension at the API-style level: REST
trades per-caller flexibility for CDN-level throughput via caching; GraphQL trades that
cacheability for per-caller latency efficiency (fewer round trips, exactly the data needed); gRPC
trades human-readability for binary-format throughput and streaming latency. None of the three
concepts requires a literal database underneath to exhibit the same trade-off shape.

</details>

**E3.** Why does `MERGE`-style idempotency (an `Idempotency-Key`) matter specifically for `POST`,
when `PUT` is already idempotent by definition (co-06)?

<details>
<summary>Model explanation</summary>

`PUT`'s idempotency comes from its OWN semantics: "replace this resource with exactly this
representation" naturally produces the same end state no matter how many times it is repeated,
because the request itself fully specifies the target state (Example 4). `POST`'s semantics are
"create a new resource" or "process this action" -- repeating it is supposed to create a SECOND
resource or trigger a SECOND action, which is exactly correct behavior for a genuinely new request,
and exactly wrong behavior for a RETRY of the same request after a timeout, where the client cannot
tell from the outside whether the first attempt actually succeeded before the connection dropped. An
`Idempotency-Key` (co-18) adds an EXPLICIT, out-of-band idempotency guarantee onto an operation whose
own HTTP semantics do not provide one -- it is a deliberate opt-in mechanism, not a property `POST`
gets automatically the way `PUT` does.

</details>

**E4.** Why does this course teach RFC 9457's `problem+json` as the error envelope, given the
syllabus itself notes the underlying research found error-envelope guidance described only
generically, not mandating any one RFC?

<details>
<summary>Model explanation</summary>

The web-verified research explicitly flags this as "a defensible-but-optional choice to confirm at
drafting" -- meaning `problem+json` is not the ONLY defensible answer, but it is A defensible,
standards-track one (RFC 9457, 2023, obsoleting RFC 7807), and picking A SPECIFIC, real, documented
standard is what lets this course's examples show a genuinely consistent shape (co-30) rather than
an invented, ad-hoc one that a reader could not cross-reference against anything outside this
course. The deeper principle this choice illustrates -- pick ONE documented shape and apply it
uniformly across every endpoint -- would hold regardless of which specific standard got chosen; RFC
9457 is this course's concrete instantiation of that principle, not the only structure that could
satisfy it.

</details>

**E5.** Why does checking the rate limit BEFORE idempotency (Example 74's ordering, reused in this
course's own capstone) mean a replay of an already-used idempotency key can still be rejected with
`429`, even though the original request already succeeded?

<details>
<summary>Model explanation</summary>

The rate-limit check and the idempotency check answer two DIFFERENT questions: "is this caller
currently within its allowed request budget" versus "has this specific write already been applied."
Checking rate limiting first means the budget check runs UNCONDITIONALLY, before the server has even
looked at whether the key is a replay -- so once the budget is exhausted, EVERY subsequent call,
replay or not, is rejected before idempotency bookkeeping is ever consulted. This is a genuine,
deliberate trade-off: it keeps the rate limiter simple and unconditional (no special-casing for
"except when it's a replay"), at the cost of a replay attempted after budget exhaustion getting a
`429` instead of the `200` it would have received had it arrived earlier. A different ordering
(idempotency first) would make replays always safe regardless of budget, at the cost of a more
complex rate limiter that has to look inside the request to decide whether to count it at all.

</details>

**E6.** Why does this course explicitly warn that GraphQL and gRPC are "not upgrades" over REST,
rather than presenting them as a strictly more capable evolution of the same idea?

<details>
<summary>Model explanation</summary>

Presenting GraphQL or gRPC as a strict upgrade would obscure the real trade-offs each one makes:
GraphQL's client-shaped queries genuinely solve over/under-fetching (co-24), but at the cost of
losing REST's simple, universal HTTP-cache compatibility and taking on query-complexity and N+1
concerns (co-25) the team now owns directly. gRPC's typed, binary, streaming contract genuinely
outperforms REST for internal service-to-service calls, but trades away human-readability in a
browser and the ability for a public, unknown caller to just use `curl`. Calling either one an
"upgrade" implies REST is simply the worse, earlier version of the same thing -- when in fact all
three are different points on the SAME `consistency-latency-throughput` trade-off surface (E2), each
correct for the specific forces Example 69's decision matrix asks a team to name explicitly, not for
being newer.

</details>

---

← Previous: [Capstone](../learning/capstone/overview.md)
