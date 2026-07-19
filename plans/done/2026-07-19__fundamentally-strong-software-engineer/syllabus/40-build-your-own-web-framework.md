# 40 · Build Your Own Web Framework (By Example, Python †)

**prd row**: Pass 3 · Build for the Real World · By Example · Python † · Learn 140 / Drill 240 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: the build-your-own tier for the backend band — a minimal web framework that
demystifies the ones you use (Flask/FastAPI/Django): the WSGI/ASGI contract, a router, a middleware
chain, request/response objects, and lightweight dependency injection. Interleaved after
[`39-backend-at-scale`](./39-backend-at-scale.md), it makes the "magic" of `@app.route` and
middleware concrete. `†`: Python, fully type-annotated (DD-39) — every snippet carries type hints in
the pyright-clean spirit.

## Why this exists · the big idea

- **The problem before the solution**: every framework feels like magic until you've built one — you
  can't reason about a mysterious 500, a middleware ordering bug, or a slow request when the router,
  the request lifecycle, and the server boundary are all opaque. Rebuilding the core turns "the
  framework did something" into "I know exactly what happens between the socket and my handler".
- **Keep-this-if-you-forget-everything**: a web framework is a thin function that turns an incoming
  request (an environ/scope dict) into a response, via a router that picks a handler and a middleware
  chain that wraps it. Everything else is convenience over that one transformation.
- **Big ideas touched**: `abstraction-and-its-cost` (a framework hides the server protocol, routing,
  and lifecycle behind decorators — building it exposes what that convenience costs and where it
  constrains you), `layering-and-leaks` (WSGI/ASGI is the seam between server and app — you'll see
  exactly where the socket, the protocol, and your handler meet, and where each layer bleeds through).

## Prerequisites

- **Prior topics**: [topic 11 Backend Essentials](./11-backend-essentials.md) (routing, request
  handling, status codes as a _user_ of a framework) and [topic 39 Backend at Scale](./39-backend-at-scale.md)
  (middleware, auth, and reliability patterns you'll now implement the substrate for).
- **Tools & environment**: a macOS/Linux terminal; **Python** at a recent stable release with type
  hints and `pyright`; a WSGI server (e.g. a reference `gunicorn`/`waitress`) and/or an ASGI server
  (e.g. `uvicorn`); `curl`; Neovim/VSCode with the Python LSP (DD-17). No web framework — that's the
  point.
- **Assumed knowledge**: serving and calling a CRUD JSON endpoint through an existing framework
  (topic 11); what middleware and routing do from the outside (topics 11/39); functions as
  first-class values and decorators (topic 04).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: **WSGI (PEP 3333)** and **ASGI** remain the stable server↔app contracts for
  Python — WSGI for synchronous apps, ASGI for async/streaming/WebSockets. Both are left correctly
  version-unpinned; the `environ`/`start_response` (WSGI) and `scope`/`receive`/`send` (ASGI) shapes
  are unchanged.
- 2026-07-12 — verified (GAP for plan owner): the topic teaches both WSGI and ASGI paths but the
  build-your-own capstone should pick one primary target at drafting time (ASGI is the forward-looking
  default for async handlers); leaving both fully in-scope risks an over-large example. Concrete server
  package + version to be pinned when drafted.

> DD-35 primary-source pass (2026-07-12). Exact signatures and dict-key/type rules the author MUST keep
> verbatim in `learning/code/`; unverifiable specifics flagged `[Needs Verification]`, never guessed.

- **WSGI callable** — `application(environ, start_response)`, two positional args; `environ` **must** be
  a builtin `dict` of CGI-style keys (`REQUEST_METHOD`, `SCRIPT_NAME`, `PATH_INFO`, `QUERY_STRING`,
  `CONTENT_TYPE`, `CONTENT_LENGTH`, `SERVER_NAME/PORT/PROTOCOL`, `HTTP_*`) plus WSGI keys
  (`wsgi.version = (1,0)`, `wsgi.url_scheme`, `wsgi.input`, `wsgi.errors`, `wsgi.multithread`,
  `wsgi.multiprocess`, `wsgi.run_once`). The app returns an **iterable of bytestrings** (`bytes` under
  Py3). Source: [PEP 3333 (WSGI v1.0.1)](https://peps.python.org/pep-3333/), P.J. Eby, 2010 (Final).
- **`start_response`** — `start_response(status, response_headers, exc_info=None)`; `status` is a string
  `"200 OK"` (Status-Code + single space + Reason-Phrase); `response_headers` is a **list** of
  `(name, value)` tuples of **native `str`** (not bytes). Source: PEP 3333.
- **ASGI callable** — `async application(scope, receive, send)`; `scope` is a dict with at least
  `type` (`"http"`/`"websocket"`/`"lifespan"`) and `scope["asgi"]["version"]`. `receive` is an awaitable
  yielding an event dict; `send` is an awaitable taking an event dict. Source: [ASGI spec (`django/asgiref` `specs/asgi.rst`)](https://github.com/django/asgiref/blob/main/specs/asgi.rst) — the version-controlled origin of asgi.readthedocs.io.
- **ASGI HTTP events (exact strings)** — `"http.request"` (`body: bytes = b""`, `more_body: bool = False`),
  `"http.response.start"` (`status: int`, `headers`), `"http.response.body"` (`body: bytes`, `more_body`),
  `"http.disconnect"`. HTTP `scope` keys: `method` (uppercased), `path`, `raw_path` (bytes),
  `query_string` (bytes), `headers` = iterable of `[name, value]` **byte-string** pairs, `root_path`
  (≈ WSGI `SCRIPT_NAME`). Source: [ASGI `specs/www.rst`](https://github.com/django/asgiref/blob/main/specs/www.rst).
- **The type-rule crux (common porting bug)** — WSGI headers are native **`str`**; ASGI headers are
  **`bytes`**; WSGI status is the string `"200 OK"` while ASGI `http.response.start` carries `status` as
  an **`int`**. Keep these straight in the examples. Source: PEP 3333 + ASGI `www.rst`.
- **Why ASGI exists** — WSGI is "a single, synchronous callable that takes a request and returns a
  response; this doesn't allow for long-lived connections, like … long-poll HTTP or WebSocket." ASGI
  adds multiple in/out events + a background coroutine. WWW sub-spec is "deliberately … a superset of
  the WSGI format" for HTTP. Source: [ASGI `docs/introduction.rst`](https://github.com/django/asgiref/blob/main/docs/introduction.rst).
  The spec text names WebSocket/async/long-lived connections as the drivers; an explicit SSE-rationale
  sentence is `[Needs Verification]` (author synthesis, not a literal spec quote).
- **Routing / `@route`** — a decorator binds a function to a URL; path variables `/<name>` (Flask) /
  `/{id}` become handler arguments; Flask converters: `string` (default)/`int`/`float`/`path`/`uuid`.
  A decorator is standard Python: receives the handler, registers it, returns it unchanged. Source:
  [Flask quickstart routing](https://flask.palletsprojects.com/en/stable/quickstart/). Flask's actual
  internal store is a Werkzeug `Map`/`Rule`, not a literal plain dict — teach "routes table" as a
  pedagogical simplification (`[Needs Verification]` at implementation-detail level).
- **Middleware onion** — "each middleware class is a 'layer' that wraps the view … request passes
  top-down, response passes back out in reverse order"; a layer that returns without calling the next
  short-circuits the inner layers. Ordering is a correctness property (e.g. auth must run after
  session). Source: [Django middleware docs](https://docs.djangoproject.com/en/stable/topics/http/middleware/);
  corroborated by PEP 3333 §Middleware.
- **Request/Response wrappers** — `Request(environ)` wraps the environ for ergonomic access; a
  `Response` **is itself a WSGI app** — `return response(environ, start_response)` closes the loop.
  Source: [Werkzeug wrappers](https://github.com/pallets/werkzeug/blob/main/docs/wrappers.rst).
- **Dependency injection** — handlers "declare things they require" and the framework "injects" them;
  a dependency is "a function … you can think of as a path-operation function without the decorator";
  `Depends(fn)` wraps the callable (uncalled), resolved per request. Source:
  [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/).
- **Error → response** — "When there is no error handler registered for an exception, a 500 Internal
  Server Error will be returned" (never a leaked trace); handlers registered by exception class /
  status code, most-specific chosen. FastAPI: `raise HTTPException(status_code=404, detail=…)`;
  `@app.exception_handler(Exc)` maps a type → response. Sources:
  [Flask error handling](https://github.com/pallets/flask/blob/main/docs/errorhandling.rst),
  [FastAPI handling errors](https://fastapi.tiangolo.com/tutorial/handling-errors/).
- **"Built on" lineage** — Flask = Werkzeug (WSGI) + Jinja2; FastAPI = Starlette (web) + Pydantic
  (data). Servers: gunicorn & waitress = WSGI; uvicorn = ASGI (HTTP/1.1 + WebSockets). Sources:
  [Flask README](https://github.com/pallets/flask/blob/main/README.md),
  [FastAPI README](https://github.com/fastapi/fastapi/blob/master/README.md),
  [gunicorn.org](https://gunicorn.org/), [encode/uvicorn README](https://github.com/encode/uvicorn/blob/master/README.md).
  The uvicorn README excerpt did not name Starlette explicitly — that specific pairing is
  `[Needs Verification]` though well established.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject topic). Each example below cites the co-NN it exercises. -->

- **co-01 · wsgi-callable** — the WSGI application signature `application(environ, start_response)`, the synchronous server↔app contract every WSGI framework implements.
- **co-02 · wsgi-environ** — `environ`, a builtin dict of CGI-style keys (`REQUEST_METHOD`, `PATH_INFO`, `QUERY_STRING`, `wsgi.input`, `HTTP_*`) the server hands the app.
- **co-03 · wsgi-start-response** — `start_response(status, headers, exc_info=None)` where `status` is the string `"200 OK"` and `headers` is a list of `(name, value)` native-`str` tuples.
- **co-04 · wsgi-return-iterable** — the app returns an iterable of **bytestrings** (the response body), closing the WSGI contract.
- **co-05 · asgi-callable** — the ASGI signature `async application(scope, receive, send)`, the async server↔app contract for long-lived/streaming/WebSocket connections.
- **co-06 · asgi-scope** — `scope`, a dict keyed by `type` (`"http"`/`"websocket"`/`"lifespan"`) plus `method`/`path`/`headers` the server hands the app once per connection.
- **co-07 · asgi-receive-send** — `receive()` awaits the next inbound event dict; `send()` awaits an outbound event dict — the async message pump.
- **co-08 · asgi-http-events** — the exact event-type strings `"http.request"`, `"http.response.start"` (`status: int`), and `"http.response.body"` that frame an HTTP exchange.
- **co-09 · wsgi-vs-asgi** — WSGI is one-request-per-worker synchronous; ASGI adds async, streaming, and WebSockets — why the async contract exists.
- **co-10 · native-str-vs-bytes** — the porting-bug crux: WSGI headers are native `str` and status is a string; ASGI headers are `bytes` and status is an `int`.
- **co-11 · router** — a routes table mapping a `(method, path)` pair to a handler function, dispatched per request.
- **co-12 · path-parameters** — extracting variable path segments (`/users/{id}`) and passing them to the handler, optionally type-converted.
- **co-13 · route-decorator** — a `@route("/path")` decorator that registers a handler in the routes table and returns the function unchanged.
- **co-14 · route-not-found** — resolving an unknown path/method to a `404` (or `405`) instead of crashing.
- **co-15 · request-object** — parsing the raw `environ`/`scope` into an ergonomic typed `Request` (method, path, query, headers, body).
- **co-16 · response-object** — a typed `Response` (status, headers, body) that serializes back to the protocol (a WSGI `Response` is itself a WSGI app).
- **co-17 · json-codec** — reading a JSON request body and writing a JSON response with `Content-Type: application/json`.
- **co-18 · middleware-onion** — each middleware wraps the next handler, running code before and after the inner call — the onion model.
- **co-19 · middleware-ordering** — the order middleware is applied determines before/after execution order; ordering is a correctness property, not a style choice.
- **co-20 · middleware-short-circuit** — a middleware that returns a response without calling the inner handler (e.g. auth `401`), skipping every inner layer.
- **co-21 · error-to-response** — turning an unhandled exception into a proper `500` response instead of leaking a stack trace to the client.
- **co-22 · exception-handler-registry** — mapping an exception type (or status code) to a response handler, most-specific first.
- **co-23 · dependency-injection** — a provider/registry so handlers declare the dependencies they need instead of reaching for globals.
- **co-24 · di-per-request** — resolving a request-scoped dependency fresh on each request (vs an app-scoped singleton).
- **co-25 · lifespan-events** — ASGI `lifespan` startup/shutdown events that initialize and tear down shared resources.
- **co-26 · query-string-parsing** — parsing `QUERY_STRING` (WSGI) / `scope["query_string"]` bytes (ASGI) into typed parameters.
- **co-27 · header-parsing** — reading request headers (WSGI `HTTP_*` / ASGI byte-pairs) into a case-insensitive typed mapping.
- **co-28 · streaming-response** — sending a body in multiple chunks (ASGI `more_body`, WSGI yielded iterable), the basis of SSE/streaming.
- **co-29 · server-invocation** — a real server (gunicorn/waitress for WSGI, uvicorn for ASGI) invokes the app callable; the framework never binds the socket itself.
- **co-30 · framework-as-transformation** — the whole framework is one function from an incoming request to a response; router, middleware, and DI are convenience over that transformation.

## Worked examples

Colocated under `build-your-own-web-framework/learning/code/`; each runnable behind a real WSGI/ASGI
server and exercised with `curl`, every Python snippet fully type-annotated and `pyright`-clean
(DD-20/DD-30/DD-34/DD-39). Contiguous `ex-01..ex-80`. Every example cites the `co-NN` it exercises; every
concept above is exercised by ≥ 1 example.

### Beginner

- **ex-01 · hello-wsgi** — a minimal WSGI app returning `[b"Hello"]` — verify a server serves it and `curl` gets `200`. (co-01, co-04)
- **ex-02 · environ-dump** — read `REQUEST_METHOD`, `PATH_INFO`, `QUERY_STRING` from `environ` — verify each matches the request. (co-02)
- **ex-03 · start-response-status** — call `start_response("200 OK", headers)` — verify the response status line. (co-03)
- **ex-04 · headers-list-tuples** — return a `Content-Type` header as an `(str, str)` tuple — verify the header reaches the client. (co-03)
- **ex-05 · return-bytes** — return the body as a `bytes` iterable — verify a `str` body raises, `bytes` works. (co-04)
- **ex-06 · method-branch** — branch on `REQUEST_METHOD` (GET vs POST) — verify each method takes its path. (co-02)
- **ex-07 · read-wsgi-input** — read the request body from `environ["wsgi.input"]` — verify the echoed length matches `CONTENT_LENGTH`. (co-02)
- **ex-08 · query-string-parse** — parse `QUERY_STRING` with `urllib.parse` — verify `?a=1&a=2` yields both values. (co-26)
- **ex-09 · http-header-read** — read `HTTP_ACCEPT` from `environ` — verify the sent `Accept` header appears. (co-27)
- **ex-10 · request-object-build** — wrap `environ` into a typed `Request` dataclass — verify `pyright` clean and fields populated. (co-15)
- **ex-11 · response-object-build** — a typed `Response` dataclass with status/headers/body — verify it holds the expected values. (co-16)
- **ex-12 · response-to-wsgi** — `Response.__call__(environ, start_response)` serializes to the protocol — verify the served bytes match. (co-16, co-04)
- **ex-13 · not-found-404** — return `404` for an unknown path — verify the status and body. (co-14)
- **ex-14 · json-response-write** — serialize a dict to a JSON body + `Content-Type: application/json` — verify `curl` parses it. (co-17)
- **ex-15 · json-request-read** — parse a JSON request body into a dict — verify a bad body yields `400`. (co-17)
- **ex-16 · status-string-format** — build a `"201 Created"` status string — verify the reason phrase renders. (co-03)
- **ex-17 · content-length-header** — compute `Content-Length` from the body bytes — verify it equals the byte length. (co-16)
- **ex-18 · native-str-headers** — assert WSGI headers are `str`, not `bytes` — verify a `bytes` header is rejected. (co-10)
- **ex-19 · wsgi-app-class** — a callable class implementing `__call__(environ, start_response)` — verify it serves identically to a function app. (co-01)
- **ex-20 · serve-with-waitress** — serve the app under `waitress` — verify `curl` gets the expected `200`. (co-29)
- **ex-21 · routes-dict-dispatch** — dispatch on `PATH_INFO` to two handlers via a dict — verify each path hits its handler. (co-11)
- **ex-22 · method-not-allowed** — return `405` when the method mismatches the route — verify GET-only route rejects POST. (co-11)
- **ex-23 · request-method-property** — a typed `Request.method` property — verify it returns the uppercased method. (co-15)
- **ex-24 · request-json-body** — a typed `Request.json()` method — verify it returns the parsed dict. (co-15, co-17)
- **ex-25 · echo-endpoint** — a POST echo returning the body as JSON — verify round-trip equality. (co-17)
- **ex-26 · empty-body-204** — return `204 No Content` with an empty body — verify no body is sent. (co-16)
- **ex-27 · redirect-302** — return `302` with a `Location` header — verify `curl -I` shows the redirect. (co-16)
- **ex-28 · framework-as-function** — express the whole app as one `environ → Response` function — verify it composes without hidden state. (co-30)

### Intermediate

- **ex-29 · hello-asgi** — a minimal ASGI app sending `http.response.start` + `http.response.body` — verify `uvicorn` serves it and `curl` gets `200`. (co-05, co-08)
- **ex-30 · asgi-scope-read** — read `scope["method"]`, `scope["path"]`, `scope["type"]` — verify each matches the request. (co-06)
- **ex-31 · asgi-receive-body** — `await receive()` to assemble the `http.request` body across `more_body` — verify a chunked body reassembles. (co-07, co-08)
- **ex-32 · asgi-send-response** — `await send` `http.response.start` then `http.response.body` — verify the two-event sequence. (co-07, co-08)
- **ex-33 · asgi-bytes-headers** — send headers as `(bytes, bytes)` tuples — verify a `str` header is rejected. (co-10)
- **ex-34 · asgi-serve-uvicorn** — serve the ASGI app under `uvicorn` — verify `curl` gets the expected body. (co-29)
- **ex-35 · wsgi-vs-asgi-contrast** — the same endpoint both ways — verify identical responses; note sync vs async. (co-09)
- **ex-36 · router-table** — a `Router` class mapping `(method, path)` → handler — verify registration and lookup. (co-11)
- **ex-37 · route-decorator-impl** — a `@route("/x")` decorator registering into the router — verify the route resolves after decoration. (co-13)
- **ex-38 · route-returns-function** — verify the decorator returns the original function object unchanged (callable elsewhere). (co-13)
- **ex-39 · path-param-extract** — capture `id` from `/users/{id}` — verify the handler receives it. (co-12)
- **ex-40 · path-param-typed** — convert `{id:int}` to an `int` — verify a non-int segment `404`s. (co-12)
- **ex-41 · multiple-params** — resolve `/users/{uid}/posts/{pid}` — verify both params are passed. (co-12)
- **ex-42 · route-precedence** — a static route beats a param route on the same prefix — verify precedence order. (co-11, co-12)
- **ex-43 · unknown-path-404** — the router returns a `404` handler for an unmatched path — verify the fallback fires. (co-14)
- **ex-44 · method-dispatch-router** — the same path with distinct GET and POST handlers — verify each method routes correctly. (co-11)
- **ex-45 · middleware-single** — one logging middleware wrapping the handler — verify the log line brackets the call. (co-18)
- **ex-46 · middleware-before-after** — log before and after the inner handler — verify both fire in order. (co-18)
- **ex-47 · middleware-chain-two** — logging outside, timing inside — verify the before/after nesting order. (co-18, co-19)
- **ex-48 · middleware-order-flip** — swap the two middleware — verify the observed before/after sequence changes. (co-19)
- **ex-49 · middleware-short-circuit** — an auth middleware returning `401` without calling inner — verify the handler never runs. (co-20)
- **ex-50 · middleware-mutate-request** — a middleware attaching a request-id to `Request` — verify the handler sees it. (co-18)
- **ex-51 · middleware-mutate-response** — a middleware adding a header to `Response` — verify the header reaches the client. (co-18)
- **ex-52 · error-middleware** — a middleware catching exceptions → `500` — verify a raised error becomes a clean `500`. (co-21)
- **ex-53 · exception-handler-map** — register a handler for a custom exception type — verify it maps to its response. (co-22)
- **ex-54 · http-exception-raise** — `raise HTTPException(404)` → `404` response — verify the detail body. (co-21, co-22)
- **ex-55 · leaked-trace-vs-clean** — an unhandled exception yields a clean `500`, not a stack trace — verify no traceback in the body. (co-21)
- **ex-56 · query-parse-asgi** — parse `scope["query_string"]` bytes into params — verify decoded values. (co-26)

### Advanced

- **ex-57 · di-registry** — a provider registry mapping a name → factory — verify a registered provider resolves. (co-23)
- **ex-58 · di-inject-handler** — a handler declaring a dependency the framework injects — verify the handler receives it. (co-23)
- **ex-59 · di-per-request** — a request-scoped dependency resolved fresh each request — verify two requests get distinct instances. (co-24)
- **ex-60 · di-singleton** — an app-scoped singleton dependency reused across requests — verify the same instance returns. (co-23)
- **ex-61 · di-db-connection** — inject a (fake) DB connection into a handler — verify it is the request-scoped one. (co-23, co-24)
- **ex-62 · lifespan-startup** — an ASGI `lifespan` startup event initializing a resource — verify the resource exists before the first request. (co-25)
- **ex-63 · lifespan-shutdown** — a `lifespan` shutdown event closing the resource — verify cleanup runs on shutdown. (co-25)
- **ex-64 · streaming-response-asgi** — send the body in multiple `http.response.body` chunks (`more_body=True`) — verify the client receives the full stream. (co-28)
- **ex-65 · streaming-response-wsgi** — yield the body in chunks from the WSGI iterable — verify chunked delivery. (co-28, co-04)
- **ex-66 · sse-endpoint** — a `text/event-stream` SSE endpoint via ASGI streaming — verify `curl` receives successive events. (co-28)
- **ex-67 · middleware-stack-three** — a logging → auth → timing three-layer onion — verify the full nesting order. (co-18, co-19)
- **ex-68 · full-request-lifecycle** — trace `socket → environ → router → middleware → handler → response` — verify each stage runs once in order. (co-30)
- **ex-69 · typed-request-response-full** — a fully typed `Request`/`Response` pair — verify `pyright` (strict mode) is clean. (co-15, co-16)
- **ex-70 · content-negotiation** — an `Accept` header choosing JSON vs plain text — verify the right `Content-Type` returns. (co-17, co-27)
- **ex-71 · header-case-insensitive** — a case-insensitive `Request.headers` lookup — verify `content-type` and `Content-Type` match. (co-27)
- **ex-72 · port-flask-handler** — port a Flask handler onto the framework — verify identical response bytes. (co-30)
- **ex-73 · port-fastapi-handler** — port a FastAPI-style handler with a `Depends`-like dependency — verify the injected value. (co-23, co-30)
- **ex-74 · wsgi-middleware-wrap** — a WSGI middleware wrapping the whole app callable — verify it intercepts every request. (co-18)
- **ex-75 · asgi-middleware-wrap** — an ASGI middleware wrapping `scope`/`receive`/`send` — verify it wraps the event pump. (co-18)
- **ex-76 · error-in-middleware** — an exception raised inside a middleware still becomes a `500` — verify the outer error handler catches it. (co-21)
- **ex-77 · mount-subapp** — mount a sub-app under a path prefix — verify prefixed routes resolve to the sub-app. (co-11)
- **ex-78 · static-file-handler** — serve a static file with the correct `Content-Type` — verify bytes and header. (co-16, co-17)
- **ex-79 · integration-test-suite** — a test client hitting routes end-to-end — verify the suite passes. (co-30)
- **ex-80 · mini-framework** — assemble a WSGI/ASGI entrypoint + router + middleware + DI into one framework serving a JSON API — verify an end-to-end request returns the expected ranked response. (co-01, co-05, co-11, co-18, co-23)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a minimal but real typed web framework — WSGI/ASGI entrypoint, router with path
  params, an ordered middleware chain, typed request/response objects, and lightweight DI — that
  serves a small JSON API behind a standard server and passes an integration test suite driven by
  `curl`/a client.
- **Concepts exercised**: [ ] WSGI/ASGI entrypoint (co-01, co-05) [ ] router + path params (co-11,
  co-12) [ ] typed request/response (co-15, co-16) [ ] ordered middleware chain (co-18, co-19)
  [ ] lightweight DI (co-23) [ ] error-to-response handling (co-21).
- **Ordered steps**:
  1. `.../learning/capstone/code/app.py` — a WSGI/ASGI callable that builds a typed `Request` and
     returns a typed `Response`. Verify a standard server serves it and `curl` gets a 200 with the
     expected body; `pyright` clean.
  2. `.../learning/capstone/code/router.py` — a router + `@route` decorator with a path parameter.
     Verify a parameterized route resolves and an unknown path returns 404.
  3. `.../learning/capstone/code/middleware.py` — a logging + error-handling middleware chain. Verify
     ordering (logging wraps errors) and that a raised exception becomes a 500 response, not a leaked
     trace.
  4. `.../learning/capstone/code/di.py` — a provider registry injecting a dependency into a handler,
     plus an integration test suite. Verify handlers receive their declared dependency and the suite
     passes.
- **Acceptance criteria**: the framework serves a JSON API behind a real server; routing, middleware
  ordering, DI, and error-to-response all behave; the integration suite is green; all Python is
  type-annotated and `pyright`-clean.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Papers & articles**

- **Let's Build A Web Server (Parts 1–3)** — Ruslan Spivak (2015). Widely cited free tutorial series
  building an HTTP server and a WSGI-compatible framework from raw sockets upward.
  <https://ruslanspivak.com/lsbaws-part1/>
- **PEP 3333 – Python Web Server Gateway Interface (WSGI) v1.0.1** — Phillip J. Eby / Python Software
  Foundation (2010). The standard request/response contract between Python web servers and the
  frameworks built on top of them. <https://peps.python.org/pep-3333/>
- **ASGI (Asynchronous Server Gateway Interface) Specification** — ASGI Team (continually maintained).
  The async successor to WSGI defining the routing, middleware, and lifecycle contract for modern
  Python frameworks. <https://asgi.readthedocs.io/en/latest/specs/main.html>
- **Rack Specification (SPEC.rdoc)** — Rack Core Team (continually maintained). The Ruby middleware and
  request-lifecycle contract underlying Sinatra, Rails, and minimal Ruby frameworks — a useful
  cross-language mirror of WSGI/ASGI. <https://github.com/rack/rack/blob/main/SPEC.rdoc>

---

← Previous: [39 · Backend at Scale](./39-backend-at-scale.md) · Next: [41 · API Design](./41-api-design.md) →
