# Test Dimensions Checklist (Part 1)

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
