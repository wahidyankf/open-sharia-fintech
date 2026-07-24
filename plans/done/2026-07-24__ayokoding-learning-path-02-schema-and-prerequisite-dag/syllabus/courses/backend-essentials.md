# Backend Essentials (By Example, Python (PostgreSQL))

**Course ID**: `backend-essentials` · **Format**: By Example · **Language**: Python (PostgreSQL).

**Short summary**: HTTP backends with persistence, routing

**Scope note**: the **usable slice** — a real HTTP JSON service wired to a database, run and tested from
the CLI. Scale, deep auth, caching, and messaging are deferred to
[`39-backend-at-scale`](./backend-at-scale.md) (DD-11). HTTP fundamentals are introduced here (they
precede [topic 12 Networking](./networking-essentials.md) in the spiral).

## Why this exists · the big idea

- **The problem before the solution**: many clients need to share and change the same durable state over
  a network — that demands a server mediating access, not a local script.
- **Keep-this-if-you-forget-everything**: a backend is a stateless pipeline — receive, validate, persist,
  respond — with all the real state pushed down into the database.
- **Big ideas touched**: `taming-state` (HTTP is deliberately stateless so the hard state lives in one
  place, the DB); `layering-and-leaks` (request → handler → repository → store is a layering you keep clean).

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./just-enough-python.md) and
  [topic 10 SQL Essentials](./sql-essentials.md) (the service persists to a relational DB).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** in a `venv`; a pinned CVE-clean web
  framework (FastAPI/Flask) + `uvicorn`; **`curl`** to exercise endpoints; SQLite (from topic 10) or a
  local PostgreSQL for the persistence example.
- **Assumed knowledge**: reading/writing Python functions and modules; basic SQL queries and a
  parameterized query from Python (topic 10). No prior web-framework experience required.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28). Re-confirm version pins at authoring.

- 2026-07-12 — verified: **FastAPI 0.139.0**, **uvicorn 0.51.0**, **Flask 3.1.3** — all current/CVE-clean.
  HTTP method/status/statelessness semantics are standards-stable (RFC 9110, unchanged since 2022).
  (pypi.org)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary/authoritative source fetched and read in the retroactive
> grounding sweep (2026-07-12, `web-researcher`; content-negotiation nuance re-verified 2026-07-14).
> Sources: PyPI + NVD (versions/CVE), IETF RFCs, MDN, FastAPI docs, GitHub release notes/source, and
> publisher records. 15/15 claim clusters verified.

- **Version pins** — FastAPI **0.139.0** (2026-07-01), uvicorn **0.51.0** (2026-07-08), Flask **3.1.3**
  (2026-02-19) all confirmed latest on [PyPI](https://pypi.org/project/fastapi/#history); Flask 3.1.3 is
  the fix for [CVE-2026-27205](https://nvd.nist.gov/vuln/detail/CVE-2026-27205) (substantiates "CVE-clean").
- **HTTP semantics (co-02/03, ex-09/75)** — [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
  (Fielding/Nottingham/Reschke eds., 2022): idempotent set = GET/HEAD/PUT/DELETE/OPTIONS/TRACE (POST **not**
  idempotent); PUT "created or replaced"; PATCH "neither safe nor idempotent" ([RFC 5789](https://www.rfc-editor.org/rfc/rfc5789));
  **422 Unprocessable Content is defined natively in RFC 9110 §15.5.21** (not WebDAV-only); 405 "MUST
  generate an Allow header" (§15.5.6). Status set 200/201/204/400/401/404/405/422/500 confirmed vs
  [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status). "POST creates" is pedagogical
  shorthand (RFC defines POST as generic resource-specific processing).
- **stdlib + FastAPI behavior (ex-02/53)** — `http.server` default `protocol_version='HTTP/1.0'`
  ([Python docs](https://docs.python.org/3/library/http.server.html)) → `curl -i` shows `HTTP/1.0 200`;
  FastAPI default 422 body `{"detail":[{"loc","msg","type"}]}`
  ([Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)).
- **Content-negotiation nuance (co-21, ex-27/54)** `2026-07-14 — verified` — FastAPI's
  `strict_content_type=True` default, added in
  [FastAPI 0.132.0](https://github.com/fastapi/fastapi/releases/tag/0.132.0) (2026-02-23) and still
  in effect at the pinned 0.139.0, natively rejects a JSON body sent without an
  `application/json`-compatible `Content-Type`: the body is not parsed as JSON, so it fails the
  declared Pydantic model and returns a native **422** — confirmed in
  [`fastapi/routing.py`](https://github.com/fastapi/fastapi/blob/master/fastapi/routing.py) and the
  [Strict Content-Type Checking docs](https://fastapi.tiangolo.com/advanced/strict-content-type/).
  ex-27's 422 half is therefore a framework default, not hand-written code. FastAPI still does
  **not** raise a dedicated **415** for that same case (no such status appears in `routing.py`), and
  still does **not** enforce `Accept` (406) at all (ex-54) — both still require hand-written
  validation (a `Header` dependency or middleware), unchanged per
  [FastAPI discussion #9371](https://github.com/fastapi/fastapi/discussions/9371) and
  [#11157](https://github.com/fastapi/fastapi/discussions/11157). co-21's "honors" phrasing is now
  literally accurate for Content-Type (a framework default) and remains accurate as deliberate
  implementation for Accept.
- **Read more** — Fielding's dissertation (2000, UC Irvine,
  [roy.gbiv.com](https://roy.gbiv.com/pubs/dissertation/top.htm)); RFC 9110 (2022); _RESTful Web APIs_
  (Richardson/Amundsen/Ruby, O'Reilly 2013); _Building Microservices_ 2nd ed. (Newman, O'Reilly 2021);
  _Release It!_ 2nd ed. (Nygard, Pragmatic 2018) — all author/edition/year confirmed.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By Example band). Each example below cites the co-NN it exercises. -->

- **co-01 · http-request-response** — HTTP is a request/response protocol: a client sends a method + path +
  headers + optional body, the server returns a status line + headers + optional body.
- **co-02 · http-methods** — Methods carry semantics: GET reads, POST creates, PUT replaces (idempotent),
  PATCH partially updates, DELETE removes; safe/idempotent properties matter.
- **co-03 · http-status-codes** — Status codes signal outcome class: 2xx success, 3xx redirect, 4xx client
  error, 5xx server error (200/201/204/400/401/404/405/422/500).
- **co-04 · http-headers** — Headers carry metadata (`Content-Type`, `Authorization`, custom `X-*`) on both
  the request and the response.
- **co-05 · statelessness** — HTTP is stateless: each request is self-contained and shares no server memory,
  so durable state lives in the database and workers scale horizontally.
- **co-06 · raw-stdlib-server** — Python's `http.server`/`wsgiref` serve a route by hand-writing the status
  line and headers, revealing what a framework automates.
- **co-07 · routing** — Routing maps a method + path pattern to a handler function.
- **co-08 · request-handlers** — A handler receives a parsed request and returns a response, ideally holding
  no persistence logic itself.
- **co-09 · json-serialization** — Request and response bodies are (de)serialized between JSON text and
  typed Python objects.
- **co-10 · request-validation** — Typed models (e.g. Pydantic) validate incoming data, rejecting bad
  shapes/types/constraints with a 422 before handler logic runs.
- **co-11 · structured-errors** — Errors return a consistent JSON envelope (code + message + detail) with
  the right status, never a stack trace.
- **co-12 · path-and-query-params** — Path params (`/items/{id}`) and query params (`?q=`) are typed inputs
  parsed from the URL.
- **co-13 · request-body-parsing** — The request body is read and parsed (JSON) into a handler argument.
- **co-14 · persistence-repository** — A repository-style function is the only place that talks to the DB,
  using parameterized queries, keeping SQL out of handlers.
- **co-15 · migrations** — Schema migrations (apply `schema.sql`, additive `ALTER TABLE` + backfill) evolve
  the persistence layer safely.
- **co-16 · middleware** — Middleware wraps every request/response to add cross-cutting behavior
  (request-id, logging, timing, auth, CORS).
- **co-17 · authn-sessions-vs-tokens** — Authentication identifies the caller; server-side sessions (cookie)
  and stateless bearer tokens are the two common mechanisms.
- **co-18 · token-check** — A bearer-token check reads `Authorization`, validates it, and rejects
  missing/invalid tokens with 401, typically guarding writes.
- **co-19 · pagination** — List endpoints page results with `limit`/`offset` (bounded and defaulted) and
  often return total/next metadata.
- **co-20 · filtering** — List endpoints narrow results by query-param filters (and sort), mapped to
  parameterized SQL.
- **co-21 · content-negotiation** — The server honors `Content-Type`/`Accept`, requiring JSON on input and
  returning JSON, rejecting mismatches.
- **co-22 · local-dev-loop** — The dev loop serves the app via `uvicorn` (or `flask run`) and exercises it
  with `curl` and a `pytest`/`TestClient` suite.
- **co-23 · dependency-injection** — Framework dependency injection (FastAPI `Depends`) supplies per-request
  resources (a DB connection) to handlers.
- **co-24 · layering** — The request→handler→repository→store layering keeps each concern isolated and its
  boundaries clean.

## Worked examples

Colocated under `backend-essentials/learning/code/`; each served via `uvicorn` (or the stdlib server) and
exercised with `curl` and `pytest`, with static type hints throughout (DD-20/DD-30/DD-34/DD-39). Each cites the
`co-NN` it exercises. Contiguous `ex-01..ex-80`.

### Beginner

- **ex-01 · raw-server-hello** — a `http.server.BaseHTTPRequestHandler` writing a status line + headers by
  hand for `GET /` — verify `curl localhost:8000/` returns `hello`. (co-06, co-01)
- **ex-02 · raw-status-line** — call `send_response(200)` then `end_headers()` — verify `curl -i` shows
  `HTTP/1.0 200`. (co-06, co-03)
- **ex-03 · raw-set-header** — `send_header("Content-Type", "text/plain")` — verify the header appears in
  `curl -i` output. (co-06, co-04)
- **ex-04 · raw-read-path** — branch on `self.path` — verify `/a` and `/b` return different bodies. (co-06,
  co-12)
- **ex-05 · raw-json-response** — `json.dumps({...})` with `Content-Type: application/json` — verify `curl`
  receives parseable JSON. (co-06, co-09)
- **ex-06 · raw-404** — return 404 for an unknown path — verify `curl -o /dev/null -w '%{http_code}'` prints 404. (co-06, co-03)
- **ex-07 · wsgiref-app** — a typed WSGI callable served by `wsgiref.simple_server` — verify `curl` returns 200. (co-06)
- **ex-08 · handle-get-only** — the raw handler implements only `do_GET` — verify GET succeeds. (co-02)
- **ex-09 · method-405-raw** — POST to a GET-only handler returns 405 with an `Allow` header — verify via
  `curl -i -X POST`. (co-02, co-03)
- **ex-10 · install-framework** — install pinned `fastapi`/`uvicorn`, print `fastapi.__version__` — verify
  the pinned CVE-clean version. (co-22)
- **ex-11 · fastapi-hello** — `@app.get("/")` returns a dict — verify `uvicorn` serves JSON `{"msg":...}`.
  (co-07, co-08)
- **ex-12 · run-via-uvicorn** — `uvicorn app:app --port 8000` — verify `curl localhost:8000/` responds.
  (co-22)
- **ex-13 · health-endpoint** — `GET /health` returns `{"status":"ok"}` with 200 — verify `curl`. (co-08,
  co-03)
- **ex-14 · typed-path-param** — `/items/{item_id}` with `item_id: int` — verify `curl /items/5` echoes 5.
  (co-12)
- **ex-15 · typed-query-param** — `q: str` query param — verify `?q=hi` is parsed into the handler. (co-12)
- **ex-16 · optional-query-default** — `limit: int = 10` — verify omitting it uses the default. (co-12)
- **ex-17 · json-request-body** — POST a body parsed into a typed model — verify the fields echo back.
  (co-13, co-10)
- **ex-18 · response-model** — declare a `response_model` — verify the response shape matches the model.
  (co-09, co-10)
- **ex-19 · status-201-created** — POST returns 201 — verify `curl -i` shows 201. (co-03)
- **ex-20 · status-204-no-content** — DELETE returns 204 with an empty body — verify no body in `curl -i`.
  (co-03)
- **ex-21 · read-request-header** — read `X-Request-Id` from the request — verify it is echoed in the
  response. (co-04)
- **ex-22 · set-response-header** — set a custom `X-App-Version` response header — verify it in `curl -i`.
  (co-04)
- **ex-23 · flask-hello** — the same hello route in Flask via `flask run` — verify `curl` returns 200
  (framework-agnostic). (co-07, co-08)
- **ex-24 · put-idempotent** — `PUT /items/{id}` replaces the resource — verify two identical PUTs yield the
  same state. (co-02)
- **ex-25 · patch-partial** — `PATCH /items/{id}` updates one field — verify only that field changed.
  (co-02)
- **ex-26 · statelessness-demo** — two sequential requests share no in-process state — verify each is
  independent. (co-05)
- **ex-27 · require-json-content-type** — POST without `Content-Type: application/json` — verify a 415/422
  rejection. (co-21, co-11)
- **ex-28 · curl-post-json** — `curl -X POST -H 'Content-Type: application/json' -d '{...}'` — verify the
  JSON round-trips. (co-22, co-13)

### Intermediate

- **ex-29 · validation-required-field** — omit a required body field — verify a 422 with a structured
  detail. (co-10, co-11)
- **ex-30 · validation-wrong-type** — send a string where an int is required — verify a 422 type error.
  (co-10, co-11)
- **ex-31 · validation-constraints** — field constraints (`min_length`, `gt=0`) — verify out-of-range input
  is rejected. (co-10)
- **ex-32 · error-envelope** — a custom `{"error": {"code", "message"}}` envelope — verify its shape on a
  failure. (co-11)
- **ex-33 · exception-handler** — an app exception handler mapping a domain error to a 4xx JSON body —
  verify the mapped response. (co-11)
- **ex-34 · not-found-404-json** — a missing resource returns a 404 error envelope — verify status + body.
  (co-11, co-03)
- **ex-35 · repository-connect** — a repository module that opens the SQLite DB and runs a query — verify it
  returns rows. (co-14, co-24)
- **ex-36 · repository-parameterized** — the repo uses `?` placeholders — verify an injection attempt is
  neutralized. (co-14, co-20)
- **ex-37 · crud-create** — `POST /tasks` inserts a row via the repo — verify 201 and the row persists.
  (co-14, co-08)
- **ex-38 · crud-read-one** — `GET /tasks/{id}` reads via the repo — verify the row is returned. (co-14,
  co-12)
- **ex-39 · crud-read-list** — `GET /tasks` returns all rows — verify a JSON array. (co-14)
- **ex-40 · crud-update** — `PUT /tasks/{id}` updates via the repo — verify the change persists. (co-14,
  co-02)
- **ex-41 · crud-delete** — `DELETE /tasks/{id}` removes the row — verify 204 and the row is gone. (co-14)
- **ex-42 · crud-missing-404** — update/delete a nonexistent id — verify a 404 envelope. (co-14, co-11)
- **ex-43 · migration-apply-schema** — apply `schema.sql` at startup — verify the table exists before
  serving. (co-15)
- **ex-44 · migration-add-column** — an additive `ALTER TABLE` + backfill migration — verify existing rows
  stay valid. (co-15)
- **ex-45 · repository-typed-return** — the repo returns a typed `TypedDict`/dataclass — verify the handler
  consumes typed rows. (co-14, co-24)
- **ex-46 · layering-no-sql-in-handler** — the handler calls the repo and holds no SQL — verify the clean
  layering by inspection/test. (co-24)
- **ex-47 · dependency-injection-db** — a FastAPI `Depends` supplies the DB connection per request — verify
  the injected connection is used. (co-23, co-14)
- **ex-48 · request-id-middleware** — middleware adds `X-Request-Id` to every response — verify the header
  is present. (co-16, co-04)
- **ex-49 · logging-middleware** — middleware logs method + path per request — verify the log line appears.
  (co-16)
- **ex-50 · timing-middleware** — middleware sets `X-Process-Time` — verify the timing header. (co-16)
- **ex-51 · cors-header** — middleware sets `Access-Control-Allow-Origin` — verify the CORS header in the
  response. (co-16, co-04)
- **ex-52 · error-500-envelope** — an unhandled exception maps to a 500 envelope (no stack trace) — verify
  the sanitized body. (co-11, co-03)
- **ex-53 · validation-error-detail** — a 422 body lists the offending field and message — verify the detail
  array. (co-10, co-11)
- **ex-54 · accept-json-negotiation** — honor `Accept: application/json` (else 406) — verify negotiation.
  (co-21)
- **ex-55 · create-then-read-roundtrip** — POST a task then GET it back — verify the persisted round-trip.
  (co-14, co-02)
- **ex-56 · pytest-testclient** — a `TestClient` test exercising an endpoint — verify the assertions pass.
  (co-22)

### Advanced

- **ex-57 · sessions-vs-tokens** — one route authenticated by a session cookie, another by a bearer token —
  verify both identify the caller. (co-17)
- **ex-58 · issue-token** — `POST /login` returns a token — verify the response contains a token string.
  (co-17, co-18)
- **ex-59 · token-check-middleware** — middleware validating a `Bearer` token on protected routes — verify a
  valid token reaches the handler. (co-18, co-16)
- **ex-60 · missing-token-401** — a protected route with no `Authorization` header — verify a 401 envelope.
  (co-18, co-11)
- **ex-61 · invalid-token-401** — a protected route with a malformed token — verify a 401. (co-18)
- **ex-62 · valid-token-200** — a protected route with a good token — verify a 200. (co-18)
- **ex-63 · protect-writes-only** — GET open, but POST/PUT/DELETE require a token — verify the read/write
  split. (co-18, co-02)
- **ex-64 · session-cookie-auth** — set a session cookie on login, read it on the next request — verify the
  session persists. (co-17)
- **ex-65 · pagination-limit-offset** — `GET /tasks?limit=&offset=` slices the list — verify the page
  window. (co-19)
- **ex-66 · pagination-default** — a default limit when the param is absent — verify a bounded page. (co-19)
- **ex-67 · pagination-metadata** — the response includes `total` and `next` — verify the envelope. (co-19,
  co-09)
- **ex-68 · pagination-bounds** — a `limit` over the maximum is clamped or 422'd — verify the guard. (co-19,
  co-10)
- **ex-69 · filter-by-field** — `?status=done` filters the list — verify the subset. (co-20)
- **ex-70 · filter-multiple** — combine `?status=done&priority=high` — verify AND semantics. (co-20)
- **ex-71 · filter-parameterized-sql** — filters map to a parameterized `WHERE` — verify injection safety.
  (co-20, co-14)
- **ex-72 · sort-param** — `?sort=created_at` orders the list — verify the ordering. (co-20)
- **ex-73 · combined-list-query** — pagination + filter + sort together — verify all three compose. (co-19,
  co-20)
- **ex-74 · idempotent-put-verified** — PUT the same body twice — verify the second call is idempotent (no
  duplicate). (co-02)
- **ex-75 · method-not-allowed-405** — call a route with an unsupported method — verify a 405 with an
  `Allow` header. (co-02, co-03)
- **ex-76 · health-vs-readiness** — `/health` (liveness) vs `/ready` (pings the DB) — verify readiness fails
  when the DB is down. (co-08, co-14)
- **ex-77 · error-envelope-consistency** — every error path shares one envelope shape — verify uniformity
  across 400/401/404/422/500. (co-11)
- **ex-78 · curl-crud-auth-script** — a documented `curl` script exercising CRUD + auth end-to-end — verify
  every step passes. (co-22, co-18)
- **ex-79 · pytest-full-integration** — a `pytest` suite covering CRUD + token + pagination — verify green.
  (co-14, co-18, co-19)
- **ex-80 · stateless-two-workers** — run two `uvicorn` workers sharing the DB (not memory) — verify
  consistent responses across workers. (co-05, co-24)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small HTTP JSON API (a task or notes service) with full CRUD backed by the SQL DB,
  request validation, structured errors, a token-check middleware, and pagination — runnable via
  `uvicorn` and fully exercisable with `curl`.
- **Concepts exercised**: [ ] routing + handlers [ ] JSON in/out + validation [ ] structured error
  envelope [ ] repository-style DB access (parameterized) [ ] token-check middleware [ ] pagination +
  filtering.
- **Ordered steps**:
  1. `.../learning/capstone/code/app/` — the framework app + a `GET /health`. Verify
     `uvicorn app.main:app` serves and `curl localhost:8000/health` returns 200 JSON.
  2. CRUD endpoints backed by the DB with parameterized queries + validation. Verify `curl` create → read
     → update → delete round-trips and invalid bodies return a structured 4xx.
  3. A token-check middleware protecting writes. Verify a missing/invalid token returns 401.
  4. Pagination + filtering on the list endpoint. Verify `?limit=&offset=&filter=` behaves.
- **Acceptance criteria**: every endpoint returns correct status codes; writes require a valid token;
  invalid input yields structured errors; a `pytest` suite (or a documented `curl` script) passes.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **RESTful Web APIs** — Richardson, Amundsen, Ruby (2013). Definitive successor to "RESTful Web Services": resource design, hypermedia, API-description formats.
- **Building Microservices** — Sam Newman (2nd ed., 2021). Standard reference for decomposing backends into independently deployable, well-bounded services.
- **Release It!** — Michael Nygard (2nd ed., 2018). Canonical catalog of production-readiness patterns (circuit breaker, bulkhead, timeout).

**Papers & articles**

- **Architectural Styles and the Design of Network-based Software Architectures** — Roy T. Fielding (2000, dissertation). Introduces REST. <https://roy.gbiv.com/pubs/dissertation/top.htm>
- **RFC 9110: HTTP Semantics** — Fielding, Nottingham, Reschke, eds. (2022). Current IETF standard for HTTP methods, status codes, headers. <https://www.rfc-editor.org/rfc/rfc9110>

## In which paths

- `interview-ready/software-engineer` — Phase 1 · Interview preparation (through senior).
- `immediately-effective/software-engineer` — Stage 2 · One language end-to-end, then BUILD A REAL APP FIRST.
- `fundamentally-strong/software-engineer` — Stage 5 · Web foundations (the minimal application slice the depth courses build on).

> _Content originated in the now-closed FS-SE plan (topic 11); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
