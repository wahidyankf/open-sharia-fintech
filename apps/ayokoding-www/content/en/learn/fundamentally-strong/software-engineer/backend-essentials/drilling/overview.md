---
title: "Overview"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 1
---

This page is the active-recall companion to the Backend Essentials learning track: four fixed
drills that force retrieval instead of passive re-reading. Work through them in order -- short-answer
recall first, then scenario judgment, then hands-on implementation, then a checklist to confirm real
automaticity. Every answer is hidden in a `<details>` block; try each item yourself, out loud or on
paper, before opening it. Every prompt below uses its own mocked, self-contained input -- none of it
is copy-pasted from the learning track's 80 worked examples, so recognizing an answer isn't enough;
you have to actually reconstruct the reasoning.

## Recall Q&A

Twenty-four short-answer questions, one per concept (`co-01` through `co-24`). Answer from memory,
then check.

**Q1 (co-01 -- http-request-response).** Describe the shape of an HTTP request and the shape of an
HTTP response, in terms of their parts.

<details>
<summary>Answer</summary>

A request is a method + path + headers + an optional body (for example, `POST /tasks` with a
`Content-Type` header and a JSON body). A response is a status line + headers + an optional body (for
example, `201 Created` with a `Location` header and the created resource as JSON). HTTP is a
request/response protocol: the client always initiates, and the server always replies with exactly
one response per request.

</details>

**Q2 (co-02 -- http-methods).** According to RFC 9110, which HTTP methods are idempotent, and which
of GET/POST/PUT/PATCH/DELETE is explicitly _not_ idempotent?

<details>
<summary>Answer</summary>

The idempotent set is GET, HEAD, PUT, DELETE, OPTIONS, and TRACE -- repeating any of these any number
of times produces the same server state as calling it once. POST is explicitly **not** idempotent
(two identical POSTs can create two separate rows). PATCH is also not idempotent -- RFC 5789 describes
it as "neither safe nor idempotent," since a partial update like "increment by 1" produces a different
result each time it's replayed.

</details>

**Q3 (co-03 -- http-status-codes).** Name the four status-code classes by their leading digit, and
give one status code this topic uses from each class.

<details>
<summary>Answer</summary>

2xx success (e.g. `201 Created`), 3xx redirect, 4xx client error (e.g. `404 Not Found`, `422
Unprocessable Content`), and 5xx server error (e.g. `500`). Notably, 422 is defined natively in RFC
9110 §15.5.21 -- it is not a WebDAV-only extension, contrary to a common misconception. The full set
this topic teaches is 200/201/204/400/401/404/405/422/500.

</details>

**Q4 (co-04 -- http-headers).** What do HTTP headers carry, and name three concrete examples spanning
both request and response.

<details>
<summary>Answer</summary>

Headers carry metadata about the request or response that doesn't belong in the body itself --
content type, authentication, caching hints, tracing ids, and more. Concrete examples: `Content-Type`
(declares the body's media type, sent on requests and responses), `Authorization` (carries a bearer
token or credential on a request), and a custom `X-Request-Id` (a server-generated tracing header
added to a response).

</details>

**Q5 (co-05 -- statelessness).** Why is HTTP deliberately stateless, and what does that force you to
do with data that must persist between requests?

<details>
<summary>Answer</summary>

Each HTTP request is self-contained and shares no server-side memory with any other request -- the
server holds no conversational state about "what happened last time." That forces any data that must
outlive a single request (a user's saved tasks, a session) to live somewhere durable and shared, not
in a worker process's local memory -- typically the database. It's exactly what lets multiple worker
processes serve the same application interchangeably: none of them needs to remember anything about
a specific client between calls.

</details>

**Q6 (co-06 -- raw-stdlib-server).** What does hand-writing a route with Python's `http.server` reveal
that a framework normally hides, and what protocol version does `curl -i` show by default against it?

<details>
<summary>Answer</summary>

Writing directly against `http.server`/`wsgiref` means manually calling `send_response(200)`,
`send_header(...)`, and `end_headers()` -- exactly what a framework like FastAPI automates behind
`@app.get(...)`. `http.server.BaseHTTPRequestHandler` defaults `protocol_version` to `'HTTP/1.0'`, so
`curl -i` against a raw stdlib server shows `HTTP/1.0 200` unless the handler explicitly opts into
`HTTP/1.1`.

</details>

**Q7 (co-07 -- routing).** In one sentence, what does routing do?

<details>
<summary>Answer</summary>

Routing maps a method + path pattern (like `GET /items/{item_id}`) to the specific handler function
responsible for producing a response to that combination -- it's the dispatch table between "what the
client asked for" and "which code runs."

</details>

**Q8 (co-08 -- request-handlers).** What should a request handler do, and what should it ideally
_not_ do?

<details>
<summary>Answer</summary>

A handler receives a parsed request (already-typed path/query params and body) and returns a
response. Ideally it holds no persistence logic of its own -- no raw SQL, no direct database
connection handling -- that responsibility belongs to a repository layer it calls (co-14), which keeps
the request→handler→repository→store layering clean (co-24).

</details>

**Q9 (co-09 -- json-serialization).** What does (de)serialization mean in the context of a JSON API,
and in which two directions does it happen?

<details>
<summary>Answer</summary>

Serialization converts a typed Python object (a dict, dataclass, or Pydantic model) into JSON text for
the outgoing response body; deserialization converts incoming JSON text into a typed Python object the
handler can work with. Both directions happen on nearly every request: the body arrives as JSON text
and is deserialized into a request object, and the return value is serialized back into JSON text for
the response.

</details>

**Q10 (co-10 -- request-validation).** What do typed models like Pydantic check on an incoming
request, and what happens before the handler's own logic ever runs if that check fails?

<details>
<summary>Answer</summary>

Typed models validate the incoming body's shape, field types, and declared constraints (`min_length`,
`gt=0`, and similar). If validation fails -- a missing field, a string where an int is expected, a
value outside a constraint -- the framework rejects the request with a 422 _before_ the handler
function's own code ever executes; the handler only ever sees a body that already satisfies its
declared model.

</details>

**Q11 (co-11 -- structured-errors).** What must every error response share, and what must it never
contain?

<details>
<summary>Answer</summary>

Every error response should share one consistent JSON envelope shape (something like a `code` +
`message` + optional `detail`) paired with the right status code, regardless of which endpoint or
failure path produced it. It must never leak a raw stack trace or internal implementation detail to
the caller -- that's both a poor API experience and a security exposure.

</details>

**Q12 (co-12 -- path-and-query-params).** Distinguish a path param from a query param, with one
example of each.

<details>
<summary>Answer</summary>

A path param is embedded directly in the URL's path template and identifies a specific resource, e.g.
`item_id` in `/items/{item_id}`. A query param appears after `?` as a typed, optional-or-required
input that narrows or modifies the request, e.g. `q` in `/search?q=hello`. Both are parsed from the
URL and typed before reaching the handler.

</details>

**Q13 (co-13 -- request-body-parsing).** What happens to a request body between arriving over the
wire and appearing as a handler argument?

<details>
<summary>Answer</summary>

The raw body bytes are read off the request, parsed as JSON text into a Python value, and -- combined
with request-validation (co-10) -- bound to a typed handler argument. If the body isn't valid JSON, or
isn't shaped as the declared model expects, that parsing/validation failure is what produces the 422
before the handler ever sees it.

</details>

**Q14 (co-14 -- persistence-repository).** What is a repository-style function responsible for, and
what specific SQL practice must it always use?

<details>
<summary>Answer</summary>

A repository is the single place in the codebase that talks to the database -- handlers call it, but
never issue SQL themselves (co-24). It always uses parameterized queries (placeholders like `?` bound
to values by the driver) instead of string-concatenating user input directly into SQL text, which is
exactly what neutralizes SQL-injection attempts: the injected payload stays inert, quoted data instead
of becoming part of the executed SQL syntax.

</details>

**Q15 (co-15 -- migrations).** What does an additive schema migration look like, and why "additive"
specifically?

<details>
<summary>Answer</summary>

An additive migration applies `schema.sql` at startup and evolves it with things like `ALTER TABLE ...
ADD COLUMN` plus a backfill for existing rows, rather than renaming or dropping columns outright.
"Additive" matters because it means already-running application instances (or requests already in
flight) that don't yet know about the new column keep working unchanged -- nothing existing becomes
invalid partway through a deploy.

</details>

**Q16 (co-16 -- middleware).** What is middleware for, and name three concrete cross-cutting behaviors
it commonly adds.

<details>
<summary>Answer</summary>

Middleware wraps _every_ request/response passing through the app to add behavior that would
otherwise have to be duplicated inside every single handler. Three concrete examples: adding an
`X-Request-Id` header for tracing, logging each request's method + path, and setting an
`X-Process-Time` header to record how long the request took -- none of which is specific to any one
endpoint's own business logic.

</details>

**Q17 (co-17 -- authn-sessions-vs-tokens).** Name the two common authentication mechanisms this topic
covers, and where does each one's "source of truth" about the caller's identity actually live?

<details>
<summary>Answer</summary>

Server-side sessions (identified by a cookie) and stateless bearer tokens. A session's cookie is only
an opaque key -- the actual identity lookup happens against server-side session state (a store the
server maintains). A bearer token, by contrast, is self-contained and stateless: whatever the token
itself encodes or the token's validity check confirms is the identity, with no session store consulted
at all.

</details>

**Q18 (co-18 -- token-check).** What does a bearer-token check do on a protected route, and what
status code guards a missing or invalid token?

<details>
<summary>Answer</summary>

A token check reads the `Authorization` header, confirms it's a well-formed `Bearer <token>` value,
and validates the token itself. A missing header, a malformed value, or a token that doesn't validate
all reject the request with 401 -- typically before the handler's own logic runs. This kind of check
is what commonly guards write operations (POST/PUT/PATCH/DELETE) while leaving reads (GET) open.

</details>

**Q19 (co-19 -- pagination).** What two query params does list pagination typically use, and what
should happen to each when the caller doesn't supply them?

<details>
<summary>Answer</summary>

`limit` and `offset`. `limit` should fall back to a sane default when omitted, and should be clamped
(or rejected with a 422) if the caller asks for more than a configured maximum -- never trusted as-is.
`offset` should default to 0, meaning "start from the beginning." A well-designed list endpoint often
also returns metadata alongside the page -- a `total` count and/or a `next` cursor -- so the caller
knows whether more pages exist.

</details>

**Q20 (co-20 -- filtering).** How do list-endpoint filters typically compose when more than one is
supplied, and what must a filter value always become before it reaches SQL?

<details>
<summary>Answer</summary>

Multiple filters combine with AND semantics -- e.g. `?status=done&priority=high` returns only rows
matching _both_ conditions, not either one. Whatever value the filter carries must become a bound
parameter in a parameterized query, exactly like co-14's persistence rule -- filter values are just as
much untrusted user input as a request body, and string-concatenating them into a `WHERE` clause
reopens the same injection risk.

</details>

**Q21 (co-21 -- content-negotiation).** Does FastAPI's rejection of a JSON body sent with the wrong
`Content-Type` require you to write any code yourself, and does the same framework enforce the
`Accept` header out of the box?

<details>
<summary>Answer</summary>

No hand-written code is required for the `Content-Type` side: FastAPI's `strict_content_type=True`
default (added in FastAPI 0.132.0, still in effect at 0.139.0) natively refuses to parse a body as
JSON unless the request declares an `application/json`-compatible `Content-Type`, so the body fails
its declared Pydantic model and the framework itself returns a 422 -- not a dedicated 415, which
FastAPI does not raise for this case. `Accept`-header enforcement (406) is the opposite story: FastAPI
does **not** enforce it at all by default -- honoring `Accept` requires a hand-written `Header`
dependency or middleware you write yourself.

</details>

**Q22 (co-22 -- local-dev-loop).** What three things make up the local development loop for
exercising a backend service?

<details>
<summary>Answer</summary>

Serving the app with `uvicorn` (or `flask run`), exercising it manually with `curl`, and exercising it
automatically with a `pytest`/`TestClient` suite. Together they let you verify behavior both by hand,
during development, and repeatably, in CI -- without ever needing a browser.

</details>

**Q23 (co-23 -- dependency-injection).** What does FastAPI's `Depends` mechanism supply to a handler,
and who is responsible for resolving it?

<details>
<summary>Answer</summary>

`Depends` supplies a per-request resource -- most commonly a database connection -- directly as a
typed handler argument. The _framework_ resolves the dependency before the handler runs (and can tear
it down afterward), so the handler itself never has to know how the connection was obtained; it only
ever receives an already-ready-to-use resource.

</details>

**Q24 (co-24 -- layering).** Name the four layers in this topic's request-processing pipeline, in
order, and what "clean" means for the boundaries between them.

<details>
<summary>Answer</summary>

Request → handler → repository → store. "Clean" boundaries mean each layer only talks to its
immediate neighbor and holds only its own concern: the handler parses/validates and shapes a response
but issues no SQL; the repository issues SQL (parameterized, per co-14) but knows nothing about HTTP
status codes; the store (the database) just stores data. A handler with an inline SQL query, or a
repository that returns an HTTP status code, is a layering violation -- co-24's whole point.

</details>

## Applied problems

Sixteen scenarios spanning HTTP semantics through auth and list-shaping. Each describes a realistic
engineering situation without naming the concept -- decide which one solves it and why, then check
your reasoning against the worked solution.

**AP1.** Your client library needs to safely retry any failed write on a network timeout, without
risking a duplicate. Which of "create a new order" (a typical POST) and "cancel this specific order"
(a typical DELETE) is safe to blindly retry, and which is not?

<details>
<summary>Worked solution</summary>

DELETE is safe to blindly retry -- it's in RFC 9110's idempotent set, so calling it twice (the first
time succeeding, the retry landing on an already-cancelled order) leaves the same end state as calling
it once. POST is explicitly not idempotent, so blindly retrying "create a new order" risks creating
two separate orders if the first request actually succeeded but the response was lost (co-02, co-01).

</details>

**AP2.** A code reviewer flags that your handler function builds its SQL by f-string-concatenating a
user-supplied `status` filter value directly into a `WHERE` clause. What's the concrete risk, and what
pattern fixes it?

<details>
<summary>Worked solution</summary>

The risk is SQL injection: a value like `done' OR '1'='1` escapes the intended string literal and
changes the query's actual logic, potentially returning every row regardless of status. The fix is a
parameterized query -- `WHERE status = ?` with the value bound separately -- which keeps the payload as
inert, quoted data no matter what it contains, and belongs inside a repository function, not the
handler itself (co-14, co-20, co-24).

</details>

**AP3.** Your API currently returns 500 with a raw Python traceback in the JSON body whenever an
unhandled exception occurs, and a security audit flags it as an information leak. What should the
response look like instead?

<details>
<summary>Worked solution</summary>

A structured error envelope -- a fixed shape like `{"error": {"code", "message"}}` with status 500 --
that names the failure class without exposing internals like file paths, line numbers, or variable
values. Every failure path across the API, not just this one, should emit the same consistent envelope
shape (co-11, co-03).

</details>

**AP4.** A client POSTs a new user record but omits the required `email` field. Your raw stdlib
handler currently crashes with a 500 because it tries to read a missing dict key directly. What should
happen instead, and with which status?

<details>
<summary>Worked solution</summary>

The missing field should be caught by request validation before any business logic runs, and rejected
with a 422 -- a structured error naming exactly which field is missing -- rather than crashing into an
uncaught exception. This is precisely what a typed model (Pydantic) automates: the 422 fires before
the handler function's own code executes at all (co-10, co-11, co-03).

</details>

**AP5.** Two instances of your API run behind a load balancer. A tester reports "sometimes my recent
changes seem to disappear," and it correlates with which instance handled the request.

<details>
<summary>Worked solution</summary>

Some piece of "recent state" is almost certainly being kept in one worker's local, in-process memory
instead of the shared database -- exactly what HTTP's statelessness principle forbids relying on. The
fix is ensuring every durable read/write goes through the shared store, so the response is identical
regardless of which of the two (or more) stateless workers happens to handle any given request
(co-05).

</details>

**AP6.** Ops wants to trace a single request across multiple log lines and downstream calls, even
though several different worker processes might touch it.

<details>
<summary>Worked solution</summary>

Request-id middleware: a piece of cross-cutting logic that wraps every request/response and stamps an
`X-Request-Id` header (generated if the client didn't already send one) that every log line and
downstream call can reference. It's a textbook cross-cutting concern -- exactly what middleware exists
for, instead of adding tracing logic inside every individual handler (co-16, co-04).

</details>

**AP7.** You need "list tasks" to remain publicly readable, but "delete task" must only work for an
authenticated caller.

<details>
<summary>Worked solution</summary>

A token-check guard applied selectively: GET stays open, while POST/PUT/PATCH/DELETE require a valid
bearer token, rejecting a missing or invalid one with 401. The split maps directly onto method
semantics -- reads are safe (co-02), writes are the operations worth protecting (co-18, co-02).

</details>

**AP8.** A frontend developer complains that `GET /tasks` returns all 50,000 rows from the table in a
single JSON response, causing the browser to hang.

<details>
<summary>Worked solution</summary>

Pagination via `limit`/`offset`, with a sane default and a bounded maximum on `limit` so a caller can't
demand the whole table at once. Returning `total`/`next` metadata alongside the page also lets the
frontend know how many more pages exist without loading them all up front (co-19).

</details>

**AP9.** Product wants users to narrow the task list down to just `status=done` items owned by a
specific user, without loading the entire list client-side and filtering it in the browser.

<details>
<summary>Worked solution</summary>

Query-param filtering, mapped to a parameterized `WHERE` clause combining conditions with AND
semantics -- `?status=done&owner=alice` returns only rows matching both. This keeps the filtering work
on the server (and the database index), rather than shipping the whole table over the wire just to
throw most of it away in the browser (co-20, co-14).

</details>

**AP10.** Your `/items/{item_id}` handler currently declares `item_id` as a plain string. A request
for `/items/abc` reaches deep into a database call expecting an integer primary key and crashes there
instead of failing cleanly at the boundary.

<details>
<summary>Worked solution</summary>

Declare `item_id: int` as a typed path parameter instead of a bare string. With a typed param, a
non-numeric path segment like `abc` fails validation and returns a 422 immediately -- at the routing
boundary -- instead of propagating a wrong-typed value deep into a database call where the failure is
harder to diagnose and further from the actual mistake (co-12, co-10).

</details>

**AP11.** A client sends a POST with a JSON-shaped body but forgets to set `Content-Type:
application/json` -- it sends `text/plain` instead. Against your pinned FastAPI version, what happens,
and did anyone on your team have to write code to make it happen?

<details>
<summary>Worked solution</summary>

The request is rejected with a 422 -- FastAPI's `strict_content_type=True` default (in effect since
0.132.0, still active at the pinned 0.139.0) refuses to parse the body as JSON without a
`Content-Type` FastAPI recognizes as JSON-compatible, so the body fails the declared model and the
framework itself returns the 422. Nobody had to write that check by hand -- it's a framework default,
not application code, and notably it is a 422, not a dedicated 415 (co-21).

</details>

**AP12.** During a live deploy, you need to add a nullable `archived_at` column to the `tasks` table
without breaking requests from an already-running, not-yet-redeployed instance of the app.

<details>
<summary>Worked solution</summary>

An additive migration: an `ALTER TABLE ... ADD COLUMN` plus a backfill for existing rows, never a
rename or a drop. Because the change only adds, an older running instance that has no idea the new
column exists keeps working exactly as before -- nothing it already relies on changed shape (co-15).

</details>

**AP13.** A new hire's pull request adds a raw `SELECT` statement directly inside a request handler
function, right alongside the response-formatting logic, and a senior engineer requests a refactor
before merging.

<details>
<summary>Worked solution</summary>

Move the SQL into a repository-style function -- the one place in the codebase permitted to talk to
the database -- and have the handler call it instead of issuing SQL itself. That keeps the
request→handler→repository→store layering clean: the handler shapes a response, the repository owns
persistence, and each concern stays testable and swappable in isolation (co-24, co-14).

</details>

**AP14.** Every DB-backed endpoint currently opens its own SQLite connection by hand at the top of the
function body, causing duplicated boilerplate and connection leaks across tests.

<details>
<summary>Worked solution</summary>

A FastAPI `Depends`-based dependency that supplies the database connection as a typed handler
argument, resolved (and torn down) once per request by the framework. Each handler stops managing its
own connection lifecycle entirely -- it just declares the dependency and receives an already-ready
connection (co-23, co-14).

</details>

**AP15.** QA wants an automated test suite that exercises your API's endpoints without starting a real
`uvicorn` process or opening a real network socket.

<details>
<summary>Worked solution</summary>

A `pytest` suite driven through a `TestClient` (or equivalent in-process test client), which calls the
app directly in-process rather than over a real socket -- fast, deterministic, and part of the same
local dev loop as manually exercising the API with `curl` (co-22).

</details>

**AP16.** A login endpoint issues some kind of credential after checking a username and password, and
a completely separate, stateless downstream service must later verify the caller's identity from that
credential _alone_, without querying any shared session store.

<details>
<summary>Worked solution</summary>

A bearer token, not a session cookie. A session cookie is only meaningful together with server-side
session state that the issuing service maintains -- a different, stateless service has nothing to look
it up against. A bearer token is self-contained: whatever it encodes (or however its validity is
checked) is enough on its own, with no shared store required (co-17, co-18).

</details>

## Code katas

Nineteen hands-on implementation drills, spanning HTTP fundamentals through composing pagination,
filtering, and sorting together. Each is a self-contained, runnable `.py` snippet -- no live HTTP
server, no `uvicorn`, no `curl`: implement the task yourself first, then compare against the reference
solution and the actually-verified output shown.

### Kata 1 -- Parse a raw HTTP request line

**Task.** Implement `parse_request_line(line: str) -> tuple[str, str, str]`, returning `(method, path,
version)` from a raw request-line string like `"GET /items/5 HTTP/1.1"`, raising `ValueError` on a
malformed line. (co-01)

<details>
<summary>Reference solution</summary>

```python
def parse_request_line(line: str) -> tuple[str, str, str]:  # => co-01: request = method + path + version
    parts = line.strip().split(" ")  # => splits "GET /items/5 HTTP/1.1" into 3 whitespace-separated fields
    if len(parts) != 3:  # => a well-formed request line always has exactly 3 space-separated tokens
        raise ValueError(f"malformed request line: {line!r}")  # => not a shape a server should ever accept
    method, path, version = parts  # => unpack in RFC 9110's canonical order: method, target, version
    return method, path, version  # => the caller gets the three parts a handler dispatches on


line = "GET /items/5 HTTP/1.1"  # => a mocked raw request line, never touching a socket
method, path, version = parse_request_line(line)
print(method, path, version)  # => Output: GET /items/5 HTTP/1.1

assert method == "GET"  # => the verb that carries "read" semantics (co-02)
assert path == "/items/5"  # => the resource being addressed, with a path param baked in (co-12)
assert version == "HTTP/1.1"

try:
    parse_request_line("not a valid line")  # => only 3 tokens are required; this has 4
    raised = False
except ValueError:  # => malformed input is rejected loudly, not silently mis-parsed
    raised = True
print(raised)  # => Output: True

assert raised is True
print("kata-01 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
GET /items/5 HTTP/1.1
True
kata-01 OK
```

</details>

### Kata 2 -- Classify a status code into its response class

**Task.** Implement `classify_status(code: int) -> str`, mapping any code in 200/201/204/301/
400/401/404/405/422/500 to `"success"`, `"redirect"`, `"client-error"`, or `"server-error"`. (co-03)

<details>
<summary>Reference solution</summary>

```python
def classify_status(code: int) -> str:  # => co-03: RFC 9110 groups status codes into five classes
    if 200 <= code < 300:  # => 2xx: the request succeeded
        return "success"
    if 300 <= code < 400:  # => 3xx: further action (redirect) needed
        return "redirect"
    if 400 <= code < 500:  # => 4xx: the CLIENT made a mistake (bad body, missing auth, wrong path)
        return "client-error"
    if 500 <= code < 600:  # => 5xx: the SERVER failed to fulfil a valid request
        return "server-error"
    raise ValueError(f"not a valid HTTP status code: {code}")  # => outside 200-599 isn't a status class at all


codes = [200, 201, 204, 301, 400, 401, 404, 405, 422, 500]  # => the exact status set this topic teaches
classes = [classify_status(c) for c in codes]  # => one class label per code, same order
print(classes)  # => Output: ['success', 'success', 'success', 'redirect', 'client-error', 'client-error', 'client-error', 'client-error', 'client-error', 'server-error']

assert classify_status(201) == "success"  # => 201 Created -- a successful POST (co-02)
assert classify_status(422) == "client-error"  # => Unprocessable Content, native to RFC 9110 (co-10/co-11)
assert classify_status(500) == "server-error"  # => an unhandled exception, never a stack trace (co-11)
print("kata-02 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
['success', 'success', 'success', 'redirect', 'client-error', 'client-error', 'client-error', 'client-error', 'client-error', 'server-error']
kata-02 OK
```

</details>

### Kata 3 -- Validate required fields into a 422 error envelope

**Task.** Implement `validate_required(body: dict[str, object], required: list[str]) -> dict[str,
object] | None`, returning `None` when nothing's missing, or a 422-shaped error envelope naming the
missing field(s). (co-10, co-11)

<details>
<summary>Reference solution</summary>

```python
def validate_required(body: dict[str, object], required: list[str]) -> dict[str, object] | None:  # => co-10/co-11: reject bad shapes with a 422 BEFORE handler logic runs
    missing = [field for field in required if field not in body]  # => every required field not present
    if not missing:  # => nothing missing -- the body is shaped correctly, no error to return
        return None
    return {  # => co-11: a consistent JSON error envelope, never a bare stack trace
        "status": 422,  # => co-03: 422 Unprocessable Content, defined natively in RFC 9110 Section 15.5.21
        "error": {
            "code": "validation_error",
            "message": "missing required field(s)",
            "detail": missing,  # => names EXACTLY which fields were missing, for the caller to fix
        },
    }


good_body: dict[str, object] = {"title": "Ship report", "owner": "alice"}
bad_body: dict[str, object] = {"title": "Ship report"}  # => "owner" is missing
required_fields = ["title", "owner"]

good_result = validate_required(good_body, required_fields)  # => nothing missing
bad_result = validate_required(bad_body, required_fields)  # => "owner" missing
print(good_result)  # => Output: None
print(bad_result)  # => Output: {'status': 422, 'error': {'code': 'validation_error', 'message': 'missing required field(s)', 'detail': ['owner']}}

assert good_result is None  # => a fully-shaped body produces no error envelope at all
assert bad_result is not None
assert bad_result["status"] == 422
error = bad_result["error"]
assert isinstance(error, dict) and error["detail"] == ["owner"]  # => names the exact missing field
print("kata-03 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
None
{'status': 422, 'error': {'code': 'validation_error', 'message': 'missing required field(s)', 'detail': ['owner']}}
kata-03 OK
```

</details>

### Kata 4 -- Parse and bounds-check `limit`/`offset` query params

**Task.** Implement `parse_pagination(params: dict[str, str]) -> tuple[int, int]`, defaulting and
clamping `limit`, defaulting `offset`, and rejecting negative values. (co-19)

<details>
<summary>Reference solution</summary>

```python
DEFAULT_LIMIT = 10  # => co-19: list endpoints page results with a DEFAULTED limit
MAX_LIMIT = 100  # => co-19: and a BOUNDED limit -- callers can't demand the whole table at once


def parse_pagination(params: dict[str, str]) -> tuple[int, int]:  # => returns (limit, offset)
    raw_limit = params.get("limit")  # => absent when the caller sends no ?limit= at all
    raw_offset = params.get("offset")  # => absent when the caller sends no ?offset= at all

    limit = int(raw_limit) if raw_limit is not None else DEFAULT_LIMIT  # => fall back to the default
    offset = int(raw_offset) if raw_offset is not None else 0  # => a page always starts at 0 by default

    if limit < 0 or offset < 0:  # => negative values make no sense as a window into a list
        raise ValueError("limit and offset must be non-negative")
    limit = min(limit, MAX_LIMIT)  # => co-19: clamp an over-large request instead of scanning everything

    return limit, offset


defaults = parse_pagination({})  # => neither param supplied
explicit = parse_pagination({"limit": "25", "offset": "50"})  # => a normal page request
clamped = parse_pagination({"limit": "9999", "offset": "0"})  # => an abusive over-large limit

print(defaults)  # => Output: (10, 0)
print(explicit)  # => Output: (25, 50)
print(clamped)  # => Output: (100, 0) -- clamped down to MAX_LIMIT, never trusted as-is

assert defaults == (10, 0)
assert explicit == (25, 50)
assert clamped == (100, 0)

try:
    parse_pagination({"limit": "-5"})  # => a negative limit is rejected outright
    raised = False
except ValueError:
    raised = True
print(raised)  # => Output: True
assert raised is True
print("kata-04 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
(10, 0)
(25, 50)
(100, 0)
True
kata-04 OK
```

</details>

### Kata 5 -- Detect a string-concatenated SQL injection vs a parameterized query

**Task.** Implement `build_unsafe_query`, `build_safe_query`, and `is_injection_attempt`, then prove a
malicious `status` value corrupts the unsafe query's structure but not the safe one's. (co-14, co-20)

<details>
<summary>Reference solution</summary>

```python
def build_unsafe_query(status: str) -> str:  # => co-14/co-20: string-concatenated -- the INJECTION-UNSAFE way
    return f"SELECT * FROM tasks WHERE status = '{status}'"  # => user input lands DIRECTLY in the SQL text


def build_safe_query(status: str) -> tuple[str, tuple[str, ...]]:  # => co-14: parameterized -- the SAFE way
    return "SELECT * FROM tasks WHERE status = ?", (status,)  # => the driver binds params, never concatenates


def is_injection_attempt(user_input: str) -> bool:  # => a crude but effective mocked detector for this kata
    suspicious = ["'", "--", ";", " OR ", " or "]  # => classic single-quote breakout + comment + stacking
    return any(token in user_input for token in suspicious)


malicious_input = "done' OR '1'='1"  # => a classic SQL-injection payload targeting the status filter

unsafe_sql = build_unsafe_query(malicious_input)  # => the payload becomes part of the SQL TEXT itself
safe_sql, safe_params = build_safe_query(malicious_input)  # => the payload stays DATA, never SQL syntax

print(unsafe_sql)  # => Output: SELECT * FROM tasks WHERE status = 'done' OR '1'='1'
print(safe_sql, safe_params)  # => Output: SELECT * FROM tasks WHERE status = ? ("done' OR '1'='1",)

# => the unsafe query's WHERE clause now ALWAYS matches every row -- the injection succeeded structurally
assert "OR '1'='1'" in unsafe_sql  # => the payload escaped the intended string literal boundary
# => the safe query's placeholder never changes shape -- the payload is inert, quoted DATA, not code
assert safe_sql == "SELECT * FROM tasks WHERE status = ?"  # => structurally IDENTICAL regardless of input
assert safe_params == (malicious_input,)  # => the whole payload is just one opaque bound parameter

assert is_injection_attempt(malicious_input) is True  # => flags the suspicious payload
assert is_injection_attempt("done") is False  # => a normal, benign filter value passes through clean
print("kata-05 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
SELECT * FROM tasks WHERE status = 'done' OR '1'='1'
SELECT * FROM tasks WHERE status = ? ("done' OR '1'='1",)
kata-05 OK
```

</details>

### Kata 6 -- Authenticate via session cookie vs bearer token

**Task.** Implement `check_session` (looks a cookie up in a mock server-side store) and
`check_bearer_token` (self-validates against a mock token store), and show what each requires vs. does
not. (co-17, co-18)

<details>
<summary>Reference solution</summary>

```python
def check_session(  # => co-17: server-side session -- the STORE, not the cookie, is the source of truth
    session_id: str | None, sessions: dict[str, str]
) -> str | None:
    if session_id is None:  # => no cookie sent at all
        return None
    return sessions.get(session_id)  # => O(1) lookup: cookie is only an opaque KEY into server-side state


def check_bearer_token(  # => co-18: a stateless bearer token -- the token itself carries the identity
    authorization: str | None, valid_tokens: dict[str, str]
) -> tuple[int, str | None]:  # => returns (status, caller) -- no session store consulted at all
    if authorization is None or not authorization.startswith("Bearer "):  # => co-18: missing/malformed
        return 401, None  # => reject BEFORE ever touching valid_tokens
    token = authorization.removeprefix("Bearer ")  # => strip the scheme, keep the opaque token value
    caller = valid_tokens.get(token)  # => co-18: reads Authorization, validates it against known tokens
    if caller is None:  # => the token doesn't match any known-valid entry
        return 401, None
    return 200, caller  # => a good token identifies the caller with no server-side session lookup


sessions: dict[str, str] = {"sess-abc123": "alice"}  # => co-17: session store -- state lives on the SERVER
tokens: dict[str, str] = {"tok-xyz789": "bob"}  # => co-17/co-18: token store -- state lives IN the token

session_hit = check_session("sess-abc123", sessions)  # => cookie resolves via the server-side store
session_miss = check_session("sess-nope", sessions)  # => an unknown/expired session id
print(session_hit, session_miss)  # => Output: alice None

status_ok, caller_ok = check_bearer_token("Bearer tok-xyz789", tokens)  # => a valid bearer token
status_missing, caller_missing = check_bearer_token(None, tokens)  # => co-18: no Authorization header at all
status_bad, caller_bad = check_bearer_token("Bearer tok-wrong", tokens)  # => co-18: a malformed/unknown token
print(status_ok, caller_ok)  # => Output: 200 bob
print(status_missing, caller_missing)  # => Output: 401 None
print(status_bad, caller_bad)  # => Output: 401 None

assert session_hit == "alice" and session_miss is None  # => the cookie alone means nothing without the store
assert (status_ok, caller_ok) == (200, "bob")  # => the token alone is enough -- no store lookup needed
assert status_missing == 401 and status_bad == 401  # => co-18: both reject with 401, not a crash
print("kata-06 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
alice None
200 bob
401 None
401 None
kata-06 OK
```

</details>

### Kata 7 -- Determine method idempotency from a dispatch table

**Task.** Implement `is_idempotent(method: str) -> bool` against RFC 9110's idempotent set, and a
`safe_to_blind_retry` wrapper a client library would actually call. (co-02)

<details>
<summary>Reference solution</summary>

```python
# => co-02: RFC 9110's idempotent set -- repeating the same call any number of times has the SAME effect
IDEMPOTENT_METHODS: frozenset[str] = frozenset({"GET", "HEAD", "PUT", "DELETE", "OPTIONS", "TRACE"})


def is_idempotent(method: str) -> bool:  # => O(1) average membership test against the frozen set
    return method.upper() in IDEMPOTENT_METHODS  # => normalize case -- HTTP methods are conventionally upper


def safe_to_blind_retry(method: str) -> bool:  # => the practical consequence a client relies on
    return is_idempotent(method)  # => co-02: only idempotent methods are safe to retry without side effects


methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]  # => the five methods this topic teaches
results = {m: is_idempotent(m) for m in methods}  # => one idempotency verdict per method
print(results)  # => Output: {'GET': True, 'POST': False, 'PUT': True, 'PATCH': False, 'DELETE': True}

assert results["POST"] is False  # => co-02: POST is explicitly NOT idempotent -- two POSTs can create two rows
assert results["PATCH"] is False  # => RFC 5789: PATCH is "neither safe nor idempotent"
assert results["PUT"] is True  # => PUT "created or replaced" -- repeating it converges to the same state
assert safe_to_blind_retry("GET") is True  # => reads are always safe to retry blindly
assert safe_to_blind_retry("POST") is False  # => a client library must NOT blindly retry a bare POST
print("kata-07 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
{'GET': True, 'POST': False, 'PUT': True, 'PATCH': False, 'DELETE': True}
kata-07 OK
```

</details>

### Kata 8 -- A reusable error-envelope constructor

**Task.** Implement `error_envelope(status, code, message, detail=None)` returning a typed envelope,
and prove three different failures all share the exact same top-level shape. (co-11)

<details>
<summary>Reference solution</summary>

```python
from typing import TypedDict


class ErrorBody(TypedDict):  # => co-11: one FIXED shape every error path returns, never a bare string
    code: str
    message: str
    detail: object | None


class ErrorEnvelope(TypedDict):  # => the full response body wrapping ErrorBody
    status: int
    error: ErrorBody


def error_envelope(status: int, code: str, message: str, detail: object | None = None) -> ErrorEnvelope:
    # => co-11: a single constructor every failure path calls -- guarantees UNIFORM shape (co-24: ex-77's idea)
    return {"status": status, "error": {"code": code, "message": message, "detail": detail}}


not_found = error_envelope(404, "not_found", "task 42 does not exist")  # => co-03: a missing resource
unauthorized = error_envelope(401, "unauthorized", "missing or invalid bearer token")  # => co-18's failure
server_fault = error_envelope(500, "internal_error", "unexpected failure")  # => co-11: NEVER a stack trace

print(not_found)  # => Output: {'status': 404, 'error': {'code': 'not_found', 'message': 'task 42 does not exist', 'detail': None}}
print(unauthorized)  # => Output: {'status': 401, 'error': {'code': 'unauthorized', 'message': 'missing or invalid bearer token', 'detail': None}}
print(server_fault)  # => Output: {'status': 500, 'error': {'code': 'internal_error', 'message': 'unexpected failure', 'detail': None}}

# => every envelope this function produces shares the EXACT same top-level keys, regardless of status
assert set(not_found.keys()) == set(unauthorized.keys()) == set(server_fault.keys()) == {"status", "error"}
assert not_found["status"] == 404
assert unauthorized["error"]["code"] == "unauthorized"
print("kata-08 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
{'status': 404, 'error': {'code': 'not_found', 'message': 'task 42 does not exist', 'detail': None}}
{'status': 401, 'error': {'code': 'unauthorized', 'message': 'missing or invalid bearer token', 'detail': None}}
{'status': 500, 'error': {'code': 'internal_error', 'message': 'unexpected failure', 'detail': None}}
kata-08 OK
```

</details>

### Kata 9 -- A minimal router with typed path params

**Task.** Implement a `Router` class with `add(method, pattern, handler)` and `dispatch(method, path)`,
supporting `{name}`-style path segments, and route `GET /items/{id}` to a handler. (co-07, co-12)

<details>
<summary>Reference solution</summary>

```python
from collections.abc import Callable

Handler = Callable[[dict[str, str]], str]  # => co-08: a handler takes parsed params, returns a body


class Router:  # => co-07: maps a method + path PATTERN to a handler function
    def __init__(self) -> None:
        self._routes: list[tuple[str, list[str], Handler]] = []  # => (method, pattern segments, handler)

    def add(self, method: str, pattern: str, handler: Handler) -> None:  # => co-07: register one route
        segments = pattern.strip("/").split("/")  # => "/items/{id}" -> ["items", "{id}"]
        self._routes.append((method.upper(), segments, handler))

    def dispatch(self, method: str, path: str) -> str:  # => co-07/co-12: match method + path, extract params
        path_segments = path.strip("/").split("/")  # => the ACTUAL incoming path, same segment shape
        for route_method, pattern_segments, handler in self._routes:
            if route_method != method.upper():  # => wrong verb -- this route can't handle this call
                continue
            if len(pattern_segments) != len(path_segments):  # => different segment counts can't match
                continue
            params: dict[str, str] = {}  # => co-12: path params extracted from this specific request
            matched = True
            for pattern_seg, path_seg in zip(pattern_segments, path_segments):  # => compare segment by segment
                if pattern_seg.startswith("{") and pattern_seg.endswith("}"):  # => a PARAM slot, e.g. {id}
                    params[pattern_seg[1:-1]] = path_seg  # => bind the literal path text to its param name
                elif pattern_seg != path_seg:  # => a literal segment that doesn't match -- not this route
                    matched = False
                    break
            if matched:
                return handler(params)  # => co-08: hand the extracted params to the matched handler
        raise LookupError(f"no route for {method} {path}")  # => co-03: caller should map this to a 404


def get_item(params: dict[str, str]) -> str:  # => a tiny handler -- holds no routing logic itself
    return f"item {params['id']}"


router = Router()
router.add("GET", "/items/{id}", get_item)  # => co-07: registers the pattern once

result = router.dispatch("GET", "/items/42")  # => co-12: "42" is extracted and bound to params["id"]
print(result)  # => Output: item 42

assert result == "item 42"
try:
    router.dispatch("GET", "/items/42/extra")  # => co-03: segment count mismatch -- no route matches
    raised = False
except LookupError:
    raised = True
print(raised)  # => Output: True
assert raised is True
print("kata-09 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
item 42
True
kata-09 OK
```

</details>

### Kata 10 -- Parse a raw JSON request body, handling malformed input

**Task.** Implement `parse_json_body(raw_body: str) -> tuple[dict[str, object] | None, str | None]`,
returning a caller-facing error string for malformed JSON or a non-object body, never a crash. (co-09,
co-13)

<details>
<summary>Reference solution</summary>

```python
import json
from typing import cast


def parse_json_body(raw_body: str) -> tuple[dict[str, object] | None, str | None]:
    # => co-09/co-13: (de)serialize the raw request body into a typed Python object for the handler
    try:
        parsed = json.loads(raw_body)  # => co-09: JSON text -> Python value (json.loads returns Any)
    except json.JSONDecodeError as exc:  # => co-13: malformed body -- must NOT crash the handler
        return None, f"invalid JSON: {exc.msg}"  # => a caller-facing reason, not a raw traceback (co-11)
    if not isinstance(parsed, dict):  # => co-13: the handler expects an OBJECT body, not a bare list/number
        return None, "request body must be a JSON object"
    return cast(dict[str, object], parsed), None  # => JSON objects always have str keys -- safe to narrow


good_raw = '{"title": "Ship report", "done": false}'  # => a well-formed JSON object body
malformed_raw = '{"title": "Ship report",}'  # => a trailing comma -- invalid JSON syntax
wrong_shape_raw = "[1, 2, 3]"  # => valid JSON, but not an OBJECT -- still not usable as a request body

good_parsed, good_error = parse_json_body(good_raw)
malformed_parsed, malformed_error = parse_json_body(malformed_raw)
wrong_shape_parsed, wrong_shape_error = parse_json_body(wrong_shape_raw)

print(good_parsed, good_error)  # => Output: {'title': 'Ship report', 'done': False} None
print(malformed_parsed, malformed_error is not None)  # => Output: None True
print(wrong_shape_parsed, wrong_shape_error)  # => Output: None request body must be a JSON object

assert good_parsed == {"title": "Ship report", "done": False} and good_error is None
assert malformed_parsed is None and malformed_error is not None  # => rejected, not silently truncated
assert wrong_shape_parsed is None and wrong_shape_error == "request body must be a JSON object"
print("kata-10 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
{'title': 'Ship report', 'done': False} None
None True
None request body must be a JSON object
kata-10 OK
```

</details>

### Kata 11 -- An in-memory repository keeping a handler free of SQL

**Task.** Implement a `TaskRepository` with `create`/`get`/`update_done`/`delete`, and a handler
function that calls it without touching persistence itself. (co-14, co-24)

<details>
<summary>Reference solution</summary>

```python
from typing import TypedDict


class Task(TypedDict):  # => co-14: the repo returns a TYPED shape, not a loose dict-of-anything
    id: int
    title: str
    done: bool


class TaskRepository:  # => co-14/co-24: the ONLY place that touches the "store" -- a mocked in-memory table
    def __init__(self) -> None:
        self._rows: dict[int, Task] = {}  # => stands in for a real DB table for this pure kata
        self._next_id = 1  # => stands in for an auto-increment primary key

    def create(self, title: str) -> Task:  # => co-14: INSERT-equivalent
        task: Task = {"id": self._next_id, "title": title, "done": False}
        self._rows[self._next_id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task | None:  # => co-14: SELECT-by-id-equivalent
        return self._rows.get(task_id)  # => None if absent -- the CALLER decides how to map that to a 404

    def update_done(self, task_id: int, done: bool) -> Task | None:  # => co-14: UPDATE-equivalent
        task = self._rows.get(task_id)
        if task is None:  # => co-14: nothing to update -- signal absence, don't raise a generic error
            return None
        task["done"] = done  # => in a real repo this would be a parameterized UPDATE ... WHERE id = ?
        return task

    def delete(self, task_id: int) -> bool:  # => co-14: DELETE-equivalent
        return self._rows.pop(task_id, None) is not None  # => True only if a row actually existed


def complete_task_handler(repo: TaskRepository, task_id: int) -> dict[str, object]:
    # => co-24: the HANDLER holds zero persistence logic -- it only calls the repo and shapes a response
    task = repo.update_done(task_id, True)  # => all the "how do we store this" detail lives in the repo
    if task is None:
        return {"status": 404, "body": {"error": "task not found"}}  # => co-11: a structured 404
    return {"status": 200, "body": task}


repo = TaskRepository()
created = repo.create("Write the report")  # => co-14: id=1 assigned by the repo, not the handler
print(created)  # => Output: {'id': 1, 'title': 'Write the report', 'done': False}
assert created == {"id": 1, "title": "Write the report", "done": False}

response = complete_task_handler(repo, created["id"])  # => the handler never sees a single line of SQL
missing_response = complete_task_handler(repo, 999)  # => a task id that was never created

print(response)  # => Output: {'status': 200, 'body': {'id': 1, 'title': 'Write the report', 'done': True}}
print(missing_response)  # => Output: {'status': 404, 'body': {'error': 'task not found'}}

assert response["status"] == 200
body = response["body"]
assert isinstance(body, dict) and body["done"] is True  # => the repo's update actually persisted
assert missing_response["status"] == 404  # => co-14/co-11: a clean 404, not a KeyError leaking upward
print("kata-11 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
{'id': 1, 'title': 'Write the report', 'done': False}
{'status': 200, 'body': {'id': 1, 'title': 'Write the report', 'done': True}}
{'status': 404, 'body': {'error': 'task not found'}}
kata-11 OK
```

</details>

### Kata 12 -- Simulate two stateless workers sharing only a common store

**Task.** Model two `Worker` instances that each keep their own local cache but must route all durable
state through one shared dict, and prove the shared value stays consistent while local caches diverge.
(co-05)

<details>
<summary>Reference solution</summary>

```python
class Worker:  # => co-05: models one server PROCESS -- its own local memory, no memory shared with peers
    def __init__(self, name: str) -> None:
        self.name = name
        self._local_cache: dict[str, int] = {}  # => in-process state -- this is what statelessness FORBIDS relying on

    def handle_request(self, shared_db: dict[str, int], key: str, increment: int) -> int:
        # => co-05: the ONLY state this handler is allowed to depend on is the SHARED store, not local memory
        self._local_cache[key] = self._local_cache.get(key, 0) + 1  # => a LOCAL counter -- diverges per worker
        shared_db[key] = shared_db.get(key, 0) + increment  # => co-05: durable state lives in ONE shared place
        return shared_db[key]  # => every worker reads/writes the SAME shared value, regardless of which handled it

    def local_count(self, key: str) -> int:  # => a PUBLIC accessor -- for this kata's inspection only
        return self._local_cache.get(key, 0)


shared_db: dict[str, int] = {}  # => co-05: stands in for "the database" -- the one place real state lives
worker_a = Worker("worker-a")  # => co-05: two independent workers, as if behind a load balancer
worker_b = Worker("worker-b")

result1 = worker_a.handle_request(shared_db, "views", 1)  # => request 1 happens to land on worker A
result2 = worker_b.handle_request(shared_db, "views", 1)  # => request 2 happens to land on worker B
result3 = worker_a.handle_request(shared_db, "views", 1)  # => request 3 lands back on worker A

print(result1, result2, result3)  # => Output: 1 2 3
print(worker_a.local_count("views"), worker_b.local_count("views"))  # => Output: 2 1

# => co-05: each worker's LOCAL count only reflects requests IT happened to handle -- they diverge
assert worker_a.local_count("views") == 2 and worker_b.local_count("views") == 1
# => but the SHARED db is consistent regardless of which worker handled which request -- that's the point
assert shared_db["views"] == 3 == result3
print("kata-12 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
1 2 3
2 1
kata-12 OK
```

</details>

### Kata 13 -- Compose a request-id + timing middleware chain

**Task.** Implement `request_id_middleware` and `timing_middleware` as functions that wrap a handler
and each add one response header, then compose both around a bare handler. (co-16, co-04)

<details>
<summary>Reference solution</summary>

```python
from collections.abc import Callable
from typing import TypedDict


class Response(TypedDict):  # => co-04: a typed shape, so `headers` is always known to be dict[str, str]
    status: int
    body: str
    headers: dict[str, str]


Handler = Callable[[dict[str, str]], Response]  # => co-08: a plain handler -- knows nothing about middleware
Middleware = Callable[[Handler], Handler]  # => co-16: wraps a handler, returns a NEW handler


def request_id_middleware(counter: list[int]) -> Middleware:  # => co-16/co-04: adds X-Request-Id
    def wrap(handler: Handler) -> Handler:
        def wrapped(headers: dict[str, str]) -> Response:
            counter[0] += 1  # => a mocked id generator -- a real one might use uuid4()
            response = handler(headers)  # => call the INNER handler first
            response["headers"]["X-Request-Id"] = str(counter[0])  # => co-04: mutate the typed headers dict
            return response

        return wrapped

    return wrap


def timing_middleware(clock: Callable[[], float]) -> Middleware:  # => co-16: adds X-Process-Time
    def wrap(handler: Handler) -> Handler:
        def wrapped(headers: dict[str, str]) -> Response:
            start = clock()  # => mocked clock -- avoids real-time flakiness in this kata
            response = handler(headers)
            elapsed = clock() - start  # => wall-clock cost of the WRAPPED handler only
            response["headers"]["X-Process-Time"] = f"{elapsed:.3f}"  # => co-04/co-16
            return response

        return wrapped

    return wrap


def base_handler(headers: dict[str, str]) -> Response:  # => co-08: the actual endpoint logic, middleware-free
    return {"status": 200, "body": "ok", "headers": {}}


ticks = iter([0.0, 0.25])  # => mocked clock readings: start=0.0, end=0.25 -- deterministic, no real sleep
request_counter = [0]

wrapped_handler = timing_middleware(lambda: next(ticks))(  # => co-16: compose middlewares around base_handler
    request_id_middleware(request_counter)(base_handler)
)
response = wrapped_handler({})

print(response)  # => Output: {'status': 200, 'body': 'ok', 'headers': {'X-Request-Id': '1', 'X-Process-Time': '0.250'}}

headers = response["headers"]
assert headers["X-Request-Id"] == "1"  # => co-16/co-04: every response now carries a traceable id
assert headers["X-Process-Time"] == "0.250"  # => co-16: cross-cutting behavior added WITHOUT touching base_handler
print("kata-13 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
{'status': 200, 'body': 'ok', 'headers': {'X-Request-Id': '1', 'X-Process-Time': '0.250'}}
kata-13 OK
```

</details>

### Kata 14 -- Filter and sort mock records from query-param-like input

**Task.** Implement `filter_and_sort(tasks, filters, sort_key)` applying AND-combined filters, then an
optional sort, against a small in-memory list. (co-20)

<details>
<summary>Reference solution</summary>

```python
from collections.abc import Callable
from typing import TypedDict


class Task(TypedDict):
    id: int
    status: str
    priority: str


FILTER_KEYS: dict[str, Callable[[Task], str]] = {  # => co-20: an allowlist -- never eval() a raw field name
    "status": lambda t: t["status"],
    "priority": lambda t: t["priority"],
}
SORT_KEYS: dict[str, Callable[[Task], str]] = FILTER_KEYS  # => same typed accessors double as sort keys


def filter_and_sort(tasks: list[Task], filters: dict[str, str], sort_key: str | None) -> list[Task]:  # => co-20: query-param-like filters narrow the list, an optional sort orders it
    result = [  # => co-20: AND semantics -- a row must match EVERY supplied filter, not just one
        task for task in tasks if all(FILTER_KEYS[field](task) == value for field, value in filters.items())
    ]
    if sort_key is not None:  # => co-20: sort is optional -- absent means "keep insertion order"
        result = sorted(result, key=SORT_KEYS[sort_key])  # => Timsort: stable, O(n log n)
    return result


tasks: list[Task] = [
    {"id": 1, "status": "open", "priority": "high"},
    {"id": 2, "status": "done", "priority": "low"},
    {"id": 3, "status": "done", "priority": "high"},
    {"id": 4, "status": "open", "priority": "low"},
]

done_only = filter_and_sort(tasks, {"status": "done"}, None)  # => single filter, no sort
done_high = filter_and_sort(tasks, {"status": "done", "priority": "high"}, None)  # => co-20: two filters, AND'd
sorted_by_priority = filter_and_sort(tasks, {}, "priority")  # => no filter at all, just a sort

print([t["id"] for t in done_only])  # => Output: [2, 3]
print([t["id"] for t in done_high])  # => Output: [3]
print([t["id"] for t in sorted_by_priority])  # => Output: [1, 3, 2, 4] -- alphabetical: high, high, low, low

assert [t["id"] for t in done_only] == [2, 3]
assert [t["id"] for t in done_high] == [3]  # => id 2 is done but low priority -- excluded by the AND
assert [t["id"] for t in sorted_by_priority] == [1, 3, 2, 4]
print("kata-14 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
[2, 3]
[3]
[1, 3, 2, 4]
kata-14 OK
```

</details>

### Kata 15 -- Validate field constraints without a framework

**Task.** Implement `validate_constraints(body)` mimicking `min_length`/`gt=0`-style Pydantic
constraints in plain Python, collecting _every_ violation rather than stopping at the first. (co-10)

<details>
<summary>Reference solution</summary>

```python
def validate_constraints(body: dict[str, object]) -> list[str]:  # => co-10: mimics Pydantic-style field rules
    errors: list[str] = []  # => co-11: collect ALL violations, not just the first -- one 422 lists them all
    title = body.get("title")
    if not isinstance(title, str) or len(title) < 3:  # => co-10: min_length=3 equivalent
        errors.append("title: must be a string with min_length 3")
    quantity = body.get("quantity")
    if not isinstance(quantity, int) or quantity <= 0:  # => co-10: gt=0 equivalent
        errors.append("quantity: must be an integer greater than 0")
    return errors  # => empty list means the body satisfies every constraint


valid_body: dict[str, object] = {"title": "Ship it", "quantity": 3}
short_title_body: dict[str, object] = {"title": "Hi", "quantity": 3}  # => violates min_length
bad_quantity_body: dict[str, object] = {"title": "Ship it", "quantity": 0}  # => violates gt=0
both_bad_body: dict[str, object] = {"title": "Hi", "quantity": -1}  # => violates BOTH constraints

print(validate_constraints(valid_body))  # => Output: []
print(validate_constraints(short_title_body))  # => Output: ['title: must be a string with min_length 3']
print(validate_constraints(bad_quantity_body))  # => Output: ['quantity: must be an integer greater than 0']
print(validate_constraints(both_bad_body))  # => Output: ['title: must be a string with min_length 3', 'quantity: must be an integer greater than 0']

assert validate_constraints(valid_body) == []  # => co-10: nothing to reject -- the body is valid
assert len(validate_constraints(short_title_body)) == 1
assert len(validate_constraints(both_bad_body)) == 2  # => co-11: BOTH violations reported in one 422, not just the first
print("kata-15 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
[]
['title: must be a string with min_length 3']
['quantity: must be an integer greater than 0']
['title: must be a string with min_length 3', 'quantity: must be an integer greater than 0']
kata-15 OK
```

</details>

### Kata 16 -- Apply an additive schema migration with backfill

**Task.** Implement `migrate_add_archived(rows)`, adding a new `archived` column defaulted to `False`
for every existing row, without dropping or renaming anything. (co-15)

<details>
<summary>Reference solution</summary>

```python
from typing import TypedDict


class TaskV1(TypedDict):  # => co-15: the SHAPE before the migration -- what existing rows already look like
    id: int
    title: str


class TaskV2(TypedDict):  # => co-15: the SHAPE after the migration -- one new nullable-with-default column
    id: int
    title: str
    archived: bool  # => the new column -- an ADDITIVE change, nothing removed or renamed


def migrate_add_archived(rows: list[TaskV1]) -> list[TaskV2]:  # => co-15: ALTER TABLE ... ADD COLUMN + backfill
    return [
        {"id": row["id"], "title": row["title"], "archived": False}  # => co-15: backfill every existing row
        for row in rows  # => a real migration would run one UPDATE, not a Python loop -- same idea though
    ]


existing_rows: list[TaskV1] = [  # => co-15: rows that existed BEFORE the migration ran
    {"id": 1, "title": "Write the report"},
    {"id": 2, "title": "Ship the release"},
]

migrated_rows = migrate_add_archived(existing_rows)
print(migrated_rows)  # => Output: [{'id': 1, 'title': 'Write the report', 'archived': False}, {'id': 2, 'title': 'Ship the release', 'archived': False}]

# => co-15: EVERY pre-existing row gained the new column with a safe default -- nothing became invalid
assert all(row["archived"] is False for row in migrated_rows)
assert [row["id"] for row in migrated_rows] == [1, 2]  # => co-15: identity and order fully preserved
assert len(migrated_rows) == len(existing_rows)  # => co-15: additive means no row is dropped or merged
print("kata-16 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
[{'id': 1, 'title': 'Write the report', 'archived': False}, {'id': 2, 'title': 'Ship the release', 'archived': False}]
kata-16 OK
```

</details>

### Kata 17 -- Decide JSON-vs-reject from a `Content-Type` header

**Task.** Implement `accepts_json_body(content_type: str | None) -> tuple[bool, int]`, mirroring
FastAPI's `strict_content_type` default: accept only an `application/json`-compatible type, else
reject with 422 (never a dedicated 415). (co-21)

<details>
<summary>Reference solution</summary>

```python
def accepts_json_body(content_type: str | None) -> tuple[bool, int]:  # => returns (should_parse, status)
    # => co-21: mirrors FastAPI's strict_content_type=True default (since 0.132.0) -- reject non-JSON bodies
    if content_type is None:  # => no Content-Type header sent at all
        return False, 422  # => co-21: still 422 -- FastAPI parses this as "body didn't match the model"
    media_type = content_type.split(";")[0].strip().lower()  # => strip a "; charset=utf-8" suffix if present
    if media_type == "application/json":  # => co-21: the only media type this endpoint accepts as JSON
        return True, 200
    return False, 422  # => co-21: NOT a 415 -- FastAPI's default has no dedicated 415 for this case


json_ct = "application/json"  # => the well-formed, expected case
json_ct_with_charset = "application/json; charset=utf-8"  # => co-21: a charset suffix must not break matching
plain_text_ct = "text/plain"  # => co-21: JSON body sent with the wrong declared Content-Type
missing_ct = None  # => co-21: no Content-Type header at all

for label, ct in [
    ("json", json_ct),
    ("json+charset", json_ct_with_charset),
    ("plain-text", plain_text_ct),
    ("missing", missing_ct),
]:
    accepted, status = accepts_json_body(ct)
    print(label, accepted, status)
    # => Output rows: json True 200 / json+charset True 200 / plain-text False 422 / missing False 422

assert accepts_json_body(json_ct) == (True, 200)
assert accepts_json_body(json_ct_with_charset) == (True, 200)  # => co-21: charset suffix tolerated
assert accepts_json_body(plain_text_ct) == (False, 422)  # => co-21: rejected -- a framework default, not hand-written
assert accepts_json_body(missing_ct) == (False, 422)
print("kata-17 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
json True 200
json+charset True 200
plain-text False 422
missing False 422
kata-17 OK
```

</details>

### Kata 18 -- A tiny per-call dependency-injection factory

**Task.** Implement `run_with_dependency(provider, handler)`, mimicking what FastAPI's `Depends` does:
resolve a connection, hand it to the handler, then close it -- without the handler wiring any of that
itself. (co-23)

<details>
<summary>Reference solution</summary>

```python
from collections.abc import Callable


class Connection:  # => stands in for a real DB connection object
    def __init__(self, name: str) -> None:
        self.name = name
        self.closed = False

    def close(self) -> None:
        self.closed = True


def get_connection(pool: list[Connection]) -> Connection:  # => co-23: a FastAPI-Depends-style PROVIDER
    return pool.pop()  # => hands out ONE connection per call, taking it out of the shared pool


def run_with_dependency(  # => co-23: mimics what FastAPI does with `Depends(get_connection)` per request
    provider: Callable[[], Connection], handler: Callable[[Connection], str]
) -> str:
    connection = provider()  # => co-23: the FRAMEWORK resolves the dependency -- the handler never calls it
    try:
        return handler(connection)  # => co-23: the handler just RECEIVES a ready-to-use resource
    finally:
        connection.close()  # => co-23: the framework is responsible for teardown too, not the handler


def list_tasks_handler(connection: Connection) -> str:  # => co-08: a thin handler -- no wiring logic itself
    return f"tasks from {connection.name}"


pool = [Connection("conn-a"), Connection("conn-b")]  # => co-23: a mocked connection pool
provider = lambda: get_connection(pool)  # => co-23: bound once, reused per simulated "request"

result = run_with_dependency(provider, list_tasks_handler)  # => request 1: injected with conn-b (last popped)
print(result)  # => Output: tasks from conn-b
print(len(pool))  # => Output: 1 -- whatever's left in the pool after one injection

assert result == "tasks from conn-b"
assert len(pool) == 1  # => co-23: exactly one connection was handed out and consumed
print("kata-18 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
tasks from conn-b
1
kata-18 OK
```

</details>

### Kata 19 -- Compose pagination, filter, and sort together

**Task.** Implement `list_tasks(tasks, status, sort_by, limit, offset)`, combining a filter step, an
optional sort step, and a pagination step -- in that order -- against one in-memory dataset, returning
a page plus `total`/`next_offset` metadata. (co-19, co-20)

<details>
<summary>Reference solution</summary>

```python
from collections.abc import Callable
from typing import TypedDict


class Task(TypedDict):
    id: int
    status: str
    priority: int


class Page(TypedDict):  # => co-19: a typed pagination envelope -- items, total, and a next-page cursor
    items: list[Task]
    total: int
    next_offset: int | None


# => co-20: a small allowlist of sortable fields, each with an explicit typed accessor (never eval()'d)
SORT_KEYS: dict[str, Callable[[Task], int]] = {"priority": lambda t: t["priority"]}


def list_tasks(  # => co-19/co-20: pagination + filter + sort composed in ONE query-shaping function
    tasks: list[Task],
    status: str | None,
    sort_by: str | None,
    limit: int,
    offset: int,
) -> Page:
    filtered = [t for t in tasks if status is None or t["status"] == status]  # => co-20: filter step first
    if sort_by is not None:  # => co-20: sort step second, over the ALREADY-filtered set
        filtered = sorted(filtered, key=SORT_KEYS[sort_by])
    page = filtered[offset : offset + limit]  # => co-19: pagination step LAST, over the filtered+sorted set
    return {  # => co-19: pagination metadata alongside the page itself
        "items": page,
        "total": len(filtered),  # => co-19: total reflects the FILTERED count, not the whole table
        "next_offset": offset + limit if offset + limit < len(filtered) else None,
    }


tasks: list[Task] = [
    {"id": 1, "status": "open", "priority": 3},
    {"id": 2, "status": "open", "priority": 1},
    {"id": 3, "status": "done", "priority": 2},
    {"id": 4, "status": "open", "priority": 2},
]

page1 = list_tasks(tasks, status="open", sort_by="priority", limit=2, offset=0)  # => co-19/co-20: all 3 combine
page2 = list_tasks(tasks, status="open", sort_by="priority", limit=2, offset=2)  # => the SECOND page

print([t["id"] for t in page1["items"]], page1["total"], page1["next_offset"])  # => Output: [2, 4] 3 2
print([t["id"] for t in page2["items"]], page2["total"], page2["next_offset"])  # => Output: [1] 3 None

assert [t["id"] for t in page1["items"]] == [2, 4]  # => sorted by priority (1, 2) among "open" tasks
assert page1["total"] == 3  # => co-19: 3 total open tasks, even though only 2 are on this page
assert page1["next_offset"] == 2  # => co-19: a next page exists
assert page2["next_offset"] is None  # => co-19: this page reaches the end of the filtered set
print("kata-19 OK")
```

**Run**: `python3 kata.py`

**Output**:

```text
[2, 4] 3 2
[1] 3 None
kata-19 OK
```

</details>

## Self-check checklist

Confirm each item without checking the learning track first. If you hesitate, that concept needs
another pass.

- [ ] I can describe the shape of an HTTP request and an HTTP response, part by part, without
      notes. (co-01)
- [ ] I can name RFC 9110's idempotent method set and state that POST is explicitly not idempotent.
      (co-02)
- [ ] I can name the four status-code classes and give a concrete code this topic uses from each.
      (co-03)
- [ ] I can name three concrete HTTP headers and what each one carries. (co-04)
- [ ] I can explain why HTTP is deliberately stateless and where durable state must live instead.
      (co-05)
- [ ] I can explain what hand-writing a route with `http.server` reveals that a framework
      automates, and its default protocol version. (co-06)
- [ ] I can state, in one sentence, what routing does. (co-07)
- [ ] I can describe what a request handler should do and what it should ideally not do. (co-08)
- [ ] I can explain (de)serialization and identify both directions it happens in a JSON API. (co-09)
- [ ] I can explain what request validation checks and when it runs relative to the handler's own
      logic. (co-10)
- [ ] I can state what every error response must share and what it must never contain. (co-11)
- [ ] I can distinguish a path param from a query param with one example of each. (co-12)
- [ ] I can trace what happens to a request body between arriving over the wire and reaching a
      typed handler argument. (co-13)
- [ ] I can explain what a repository function is responsible for and the SQL practice it must
      always use. (co-14)
- [ ] I can describe an additive schema migration and explain why "additive" matters during a live
      deploy. (co-15)
- [ ] I can explain what middleware is for and name three concrete cross-cutting behaviors it
      commonly adds. (co-16)
- [ ] I can name the two common authentication mechanisms this topic covers and where each one's
      identity source of truth lives. (co-17)
- [ ] I can describe what a bearer-token check does and the status code that guards a
      missing/invalid token. (co-18)
- [ ] I can name the two params list pagination typically uses and the default/bound behavior for
      each. (co-19)
- [ ] I can explain how multiple list filters combine and what a filter value must become before it
      reaches SQL. (co-20)
- [ ] I can explain FastAPI's default behavior for a mismatched `Content-Type` and for the `Accept`
      header, and which one requires hand-written code. (co-21)
- [ ] I can name the three pieces of a local development loop for exercising a backend service.
      (co-22)
- [ ] I can explain what FastAPI's `Depends` supplies to a handler and who resolves it. (co-23)
- [ ] I can name the four layers of this topic's request-processing pipeline, in order, and explain
      what "clean" boundaries mean between them. (co-24)
- [ ] I can explain, in one sentence, what `taming-state` means for this topic -- why HTTP is
      deliberately stateless and where the hard state actually lives instead. (`taming-state`)
- [ ] I can explain, in one sentence, what `layering-and-leaks` means for this topic -- name one
      concrete layering violation (like SQL inside a handler) and the layer it should have lived in
      instead. (`layering-and-leaks`)

---

← Previous: [Capstone](../learning/capstone/overview.md)
