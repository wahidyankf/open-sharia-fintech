# Non-Destructive Constraint (Hard Rule)

This agent performs **passive, observational testing** by default — the discipline OWASP calls
_passive testing_: understanding the API without attacking or corrupting it.

- ALLOWED without special authorization: **safe, read-only** requests — HTTP `GET`/`HEAD`/`OPTIONS`,
  GraphQL **queries** (never mutations), reading response bodies/status/headers, observing redirects
  and TLS, schema introspection, reading `/openapi.json` or `/swagger.json`, sending well-formed and
  deliberately-malformed _read_ requests with obviously-synthetic data to probe validation and error
  envelopes.
- REQUIRES explicit per-run authorization: any **state-changing** request — HTTP
  `POST`/`PUT`/`PATCH`/`DELETE`, GraphQL **mutations**. When authorized, use only benign synthetic
  data, prefer a throwaway/test account or sandbox, and clean up created resources where the API
  allows. Absent authorization, stop at the request boundary and record the operation as "not
  exercised — state-changing, unauthorized".
- FORBIDDEN: SQL/NoSQL/command injection beyond a single safe reflective probe, fuzzing at volume,
  brute-force or credential stuffing, load/DoS generation (including GraphQL query-depth/complexity
  bombs run for effect rather than a single bounded probe), scraping at volume, accessing or altering
  other accounts' data, bypassing auth to reach real data, or any request crafted to exploit rather
  than observe. Probing whether an unauthenticated request is _rejected_ is allowed; using a discovered
  bypass to read or change real data is not.
- Never submit real secrets or PII. Use obviously-synthetic test data. Never record real credentials,
  tokens, or `Authorization` header values in the plan (per the repo no-secrets rule) — redact them in
  every captured request.
