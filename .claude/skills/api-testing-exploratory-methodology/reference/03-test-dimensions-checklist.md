# Test Dimensions Checklist

Apply the dimensions relevant to the goal; record which were covered and which were not.

- **Contract conformance (always probe)** — every response matches the authoritative contract: the
  **status code**, the **response body shape** (every documented field present and correctly typed; no
  undocumented fields leaking; nullability honoured), the **declared content-type**, and the
  **headers** the contract promises. For REST, test against the OpenAPI 3.x spec; for GraphQL, against
  the SDL (every selected field resolves to its declared type; non-null fields are never `null` without
  an accompanying `errors` entry). A response that diverges from the contract is a finding whose
  "expected" cites the contract by file + path/operation.
- **Status-code correctness** — the right code for the right condition: `200/201/204` on success,
  `400` on malformed input, `401` vs `403` used correctly (unauthenticated vs unauthorized), `404` on
  missing resource, `405` on wrong method, `409` on conflict, `422` on semantic validation failure,
  `429` on rate-limit. A `200` wrapping an error, or a `500` where `400` belongs, is a finding.
- **Error-envelope consistency** — every error response shares one documented shape (e.g. a consistent
  `{ error: { code, message, details } }` or RFC 9457 `application/problem+json`); messages are
  descriptive and leak no stack traces, SQL, file paths, or internal hostnames. Enumerate error
  responses across endpoints and assert the envelope is uniform.
- **Edge cases & boundary conditions (always probe — find at least one, or state explicitly that a
  genuine attempt surfaced none)** — deliberately push past the happy path. Exercise:
  boundary/extreme values (min/max, zero, negative, very large, numeric overflow, off-by-one on
  limits/pages); empty / null / missing / whitespace-only fields; very long strings and large payloads;
  special characters, Unicode, emoji, RTL text; malformed bodies (truncated JSON, wrong content-type,
  array where object expected); the **empty / zero-result** response of every list/collection endpoint;
  pagination edges (page 0, page beyond last, negative/huge page size, invalid cursor); and temporal
  edges (expired token mid-sequence, out-of-order writes, concurrent update of one resource). A _wrong_
  behaviour at an edge is a finding; a _correct_ edge behaviour the contract/`specs/**` does not
  describe is a prime **spec-gap** candidate. This dimension is mandatory for every run — edge coverage
  is never "not applicable", only "attempted and none found" with that stated.
- **Auth & authorization** — protected operations reject missing/invalid/expired credentials with the
  correct code (`401`); a valid-but-unauthorized credential is refused (`403`) and cannot reach another
  principal's data (probe for Broken Object Level Authorization — OWASP API1 — by requesting an object
  ID the test principal should not own, and assert refusal **without** reading the data); no operation
  that should require auth is silently public. Observation only — never use a real bypass to read or
  mutate real data.
- **Behavioural consistency** — the API must not contradict itself even where no single contract clause
  is violated; an internal contradiction _is_ a defect whose "expected" cites the conflicting instance.
  Probe two axes:
  - **Within one endpoint** — the same request returns the same result on repeat (or documents why
    not); identical inputs validate identically; the formatting of dates / numbers / currency / IDs is
    uniform across fields.
  - **Across related endpoints** — the same resource representation agrees wherever it appears (the
    object returned by `GET /x/{id}` matches the element in `GET /x`); shared conventions (pagination
    params, sort syntax, timestamp format, error envelope) are uniform across the whole API; the same
    datum exposed by two operations agrees.
- **Pagination, filtering & sorting** — documented params are honoured (a filter actually filters; an
  unknown filter is rejected or ignored per contract, consistently); pagination is stable (no
  duplicate/missing items across pages); total/has-more metadata is accurate; sort order is correct and
  stable.
- **Idempotency & side effects** — `GET`/`HEAD`/`OPTIONS` cause no state change; `PUT`/`DELETE` are
  idempotent (a repeat yields the same final state, not a new error); a replayed `POST` does not
  silently double-create when the contract implies an idempotency key.
- **Content negotiation & versioning** — the API honours `Accept`/`Content-Type`, rejects unsupported
  media types with `415`, and the version mechanism (path, header, or media-type) behaves as
  documented.
- **GraphQL-specific (when protocol = graphql)** — introspection exposure is intentional (often
  disabled in production — flag if leaking a private schema); **partial errors** are correct (a
  resolver failure returns `null` for that field **and** a matching `errors[]` entry; a non-null field
  that fails nulls out its nearest nullable parent per the spec); **nullability** is honoured
  everywhere; **query depth / complexity limits** exist and reject an abusive (single, bounded) deep
  query with a clear error rather than hanging; **N+1 / over-fetch** smells are noted from latency or
  visible downstream fan-out; **aliases, fragments, and variables** behave (variable type coercion,
  default values, required variables); unknown fields are rejected with a useful validation error;
  mutations are not reachable via `GET`.
- **Performance (latency & payload)** — capture per-request `time_total` and response size; flag
  operations far slower than their siblings, unbounded list responses with no pagination, and
  obvious N+1 latency scaling. Single bounded probes only — never load-test.
- **Safe security surface (passive, per OWASP API Security Top 10 & WSTG)** — HTTP→HTTPS and valid
  TLS; presence of security headers where relevant (`Strict-Transport-Security`,
  `X-Content-Type-Options`, and CORS `Access-Control-Allow-Origin` not blanket-`*` for credentialed
  APIs); no version/stack over-disclosure (`Server`, `X-Powered-By`); error responses do not leak stack
  traces/SQL/paths; no sensitive data in URLs/query strings; rate-limiting present on auth endpoints
  (observed via `429`, not generated by flooding); object-level and function-level authorization
  enforced (API1/API5). Observation only — never exploit.
