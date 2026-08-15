---
title: "Beginner Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–28 make the synchronous WSGI contract concrete before introducing the convenience layers of a framework. Each example is deliberately self-contained when its companion artifact is added under `learning/code/`.

### Example 1: Hello WSGI

**Brief explanation.** A WSGI application is a synchronous callable that receives an environ dictionary and a `start_response` callback. This smallest app establishes the server-to-framework boundary every later example relies on.

**Diagram.** `server → application(environ, start_response) → [bytes]`.

**Annotated code.** `learning/code/ex-01-hello-wsgi/example.py` returns `[b"Hello"]` after sending `200 OK`.

**Key takeaway.** WSGI is an explicit function contract, not a web server.

**Why it matters.** Once this seam is visible, framework behavior becomes traceable: the server owns sockets while the application owns the request-to-response transformation.

### Example 2: Environ Dump

**Brief explanation.** The WSGI environ is a built-in dictionary of CGI-style request facts. Reading method, path, and query values directly shows what a request wrapper will later improve.

**Diagram.** `HTTP request → environ keys → application decision`.

**Annotated code.** `learning/code/ex-02-environ-dump/example.py` reads `REQUEST_METHOD`, `PATH_INFO`, and `QUERY_STRING`.

**Key takeaway.** WSGI request metadata arrives through named environ keys.

**Why it matters.** Correctly locating raw request data prevents routers and middleware from inventing incompatible request representations.

### Example 3: Start Response Status

**Brief explanation.** `start_response` accepts a status string before the application yields body bytes. The required WSGI spelling is a code, one space, and a reason phrase.

**Diagram.** `application → start_response("200 OK", headers) → server`.

**Annotated code.** `learning/code/ex-03-start-response-status/example.py` sends `"200 OK"` before returning its body.

**Key takeaway.** WSGI status is a native string, not an integer.

**Why it matters.** Confusing WSGI status with ASGI status creates protocol adapters that fail only when a real server invokes them.

### Example 4: Headers List Tuples

**Brief explanation.** WSGI response headers are a list of `(str, str)` tuples. A content type is therefore protocol data, not an optional formatting hint.

**Diagram.** `Response metadata → list[(name, value)] → client header`.

**Annotated code.** `learning/code/ex-04-headers-list-tuples/example.py` sends a `Content-Type` tuple.

**Key takeaway.** Header names and values are native strings in WSGI.

**Why it matters.** Keeping header types exact avoids subtle proxy, encoding, and test-client failures.

### Example 5: Return Bytes

**Brief explanation.** A WSGI application returns an iterable of bytestrings, even for a one-chunk response. Returning text instead crosses the protocol boundary with the wrong type.

**Diagram.** `text → UTF-8 encode → iterable[bytes] → server`.

**Annotated code.** `learning/code/ex-05-return-bytes/example.py` encodes text before returning `[body]`.

**Key takeaway.** Encode response text before it reaches WSGI.

**Why it matters.** An explicit bytes boundary makes character encoding, content length, and streaming behavior predictable.

### Example 6: Method Branch

**Brief explanation.** A first router can branch on `REQUEST_METHOD` before any route table exists. This demonstrates that HTTP method dispatch is ordinary data-driven control flow.

**Diagram.** `REQUEST_METHOD → GET branch | POST branch`.

**Annotated code.** `learning/code/ex-06-method-branch/example.py` returns a distinct response for GET and POST.

**Key takeaway.** Method selection belongs at the request boundary.

**Why it matters.** Separating method behavior early makes later `405 Method Not Allowed` handling precise instead of accidental.

### Example 7: Read WSGI Input

**Brief explanation.** WSGI gives the request body through `wsgi.input`, with `CONTENT_LENGTH` describing how many bytes to read. The application must treat body data as bytes until it chooses a codec.

**Diagram.** `wsgi.input → read(length) → bytes body`.

**Annotated code.** `learning/code/ex-07-read-wsgi-input/example.py` reads and echoes the declared byte length.

**Key takeaway.** Request-body framing precedes JSON or form parsing.

**Why it matters.** Correct length-aware reads prevent stalled requests and corrupted payload handling.

### Example 8: Query String Parse

**Brief explanation.** `QUERY_STRING` holds the raw query portion without the question mark. `urllib.parse` preserves repeated keys such as `a=1&a=2` without framework magic.

**Diagram.** `QUERY_STRING → parse_qs → list-valued parameters`.

**Annotated code.** `learning/code/ex-08-query-string-parse/example.py` parses repeated query values.

**Key takeaway.** Query parsing is a codec step, not route matching.

**Why it matters.** Keeping repeated values intact avoids silently changing caller intent in filters and search endpoints.

### Example 9: HTTP Header Read

**Brief explanation.** WSGI represents inbound headers as environ keys such as `HTTP_ACCEPT`. This shows why a framework usually supplies a normalized header mapping.

**Diagram.** `Accept header → HTTP_ACCEPT → Request.headers`.

**Annotated code.** `learning/code/ex-09-http-header-read/example.py` reads the incoming accept value.

**Key takeaway.** WSGI header names are transformed before handlers see them.

**Why it matters.** A wrapper can hide the transformation while preserving case-insensitive HTTP semantics.

### Example 10: Request Object Build

**Brief explanation.** A typed `Request` dataclass gathers method, path, query, headers, and body behind one ergonomic value. It replaces repeated untyped environ lookups without changing the wire contract.

**Diagram.** `environ → Request → handler`.

**Annotated code.** `learning/code/ex-10-request-object-build/example.py` constructs a typed request wrapper.

**Key takeaway.** Request objects improve ergonomics while keeping raw protocol data at one edge.

**Why it matters.** One parsing boundary prevents each handler from interpreting the same request differently.

### Example 11: Response Object Build

**Brief explanation.** A typed `Response` makes status, headers, and body explicit before serialization. It separates application decisions from WSGI mechanics.

**Diagram.** `handler result → Response value → protocol adapter`.

**Annotated code.** `learning/code/ex-11-response-object-build/example.py` defines a typed response dataclass.

**Key takeaway.** A response is data until the protocol edge serializes it.

**Why it matters.** Value responses are easy to test, transform in middleware, and reuse across server adapters.

### Example 12: Response To WSGI

**Brief explanation.** A response object can implement `__call__` and become a WSGI application itself. This closes the loop from typed response data back to the exact server contract.

**Diagram.** `Response.__call__ → start_response → iterable[bytes]`.

**Annotated code.** `learning/code/ex-12-response-to-wsgi/example.py` serializes a response through WSGI.

**Key takeaway.** Serialization belongs in one reusable response adapter.

**Why it matters.** Centralizing serialization avoids inconsistent headers and status formatting across endpoints.

### Example 13: Not Found 404

**Brief explanation.** An unmatched path should produce a deliberate `404 Not Found` response instead of an exception. This is the first correctness promise made by a router.

**Diagram.** `unmatched path → 404 response`.

**Annotated code.** `learning/code/ex-13-not-found-404/example.py` returns a clean not-found body.

**Key takeaway.** Missing routes are normal control flow.

**Why it matters.** Treating expected absence as a response keeps error monitoring focused on genuine server failures.

### Example 14: JSON Response Write

**Brief explanation.** A JSON response requires both serialization and an `application/json` content type. The response body remains bytes at the WSGI boundary.

**Diagram.** `dict → json.dumps → UTF-8 bytes + Content-Type`.

**Annotated code.** `learning/code/ex-14-json-response-write/example.py` writes a JSON response.

**Key takeaway.** JSON is a codec layered over a bytes response.

**Why it matters.** Explicit encoding prevents clients from guessing a representation or misreading an error body.

### Example 15: JSON Request Read

**Brief explanation.** A JSON request is parsed only after the application has safely read body bytes. Invalid JSON becomes a client `400`, not an uncaught decoder traceback.

**Diagram.** `wsgi.input → bytes → json.loads → value | 400`.

**Annotated code.** `learning/code/ex-15-json-request-read/example.py` maps malformed input to `400 Bad Request`.

**Key takeaway.** Codecs turn bad client data into precise responses.

**Why it matters.** Boundary validation keeps malformed payloads from contaminating handler logic or leaking internal errors.

### Example 16: Status String Format

**Brief explanation.** A helper can build the WSGI status string for a code and reason phrase. This keeps status formatting consistent while still exposing the underlying protocol rule.

**Diagram.** `201 + Created → "201 Created"`.

**Annotated code.** `learning/code/ex-16-status-string-format/example.py` formats a creation response.

**Key takeaway.** WSGI status formatting is exact protocol data.

**Why it matters.** Centralizing this rule prevents malformed responses when new status codes are introduced.

### Example 17: Content Length Header

**Brief explanation.** `Content-Length` describes the length of encoded bytes, not the number of Python characters. Compute it after encoding the final response body.

**Diagram.** `body bytes → len(body) → Content-Length`.

**Annotated code.** `learning/code/ex-17-content-length-header/example.py` derives the header from bytes.

**Key takeaway.** Measure transport bytes, not source text.

**Why it matters.** Correct framing prevents truncated reads and persistent-connection protocol confusion.

### Example 18: Native Str Headers

**Brief explanation.** WSGI requires native-string response headers; byte headers belong to ASGI instead. The example rejects the tempting but incorrect cross-protocol port.

**Diagram.** `WSGI: str headers ≠ ASGI: bytes headers`.

**Annotated code.** `learning/code/ex-18-native-str-headers/example.py` validates WSGI header types.

**Key takeaway.** Protocol adapters must preserve their own type rules.

**Why it matters.** Type checks at the edge catch interoperability errors before a server emits a broken response.

### Example 19: WSGI App Class

**Brief explanation.** A class implementing `__call__` satisfies the same WSGI callable contract as a function. It can hold configured immutable dependencies while remaining server-compatible.

**Diagram.** `server → App.__call__ → iterable[bytes]`.

**Annotated code.** `learning/code/ex-19-wsgi-app-class/example.py` serves a callable application object.

**Key takeaway.** WSGI depends on callability, not a particular declaration style.

**Why it matters.** Callable classes offer structured composition without changing deployment semantics.

### Example 20: Serve With Waitress

**Brief explanation.** A WSGI server invokes the framework callable; the framework does not bind the socket. This deployment boundary remains true whether the server is Waitress, Gunicorn, or the standard-library reference server.

**Diagram.** `WSGI server → application callable → HTTP response`.

**Annotated code.** `learning/code/ex-20-serve-with-waitress/example.py` documents the server invocation seam.

**Key takeaway.** Servers transport requests; frameworks transform them.

**Why it matters.** Keeping these responsibilities separate makes servers replaceable and tests runnable without a listening socket.

### Example 21: Routes Dict Dispatch

**Brief explanation.** A dictionary can map fixed paths to handler functions. This is the smallest useful router and makes dispatch data visible.

**Diagram.** `PATH_INFO → routes[path] → handler`.

**Annotated code.** `learning/code/ex-21-routes-dict-dispatch/example.py` dispatches two paths.

**Key takeaway.** A router is a lookup table plus a fallback.

**Why it matters.** Starting with an explicit table makes later parameter matching and precedence rules understandable.

### Example 22: Method Not Allowed

**Brief explanation.** A known path with an unsupported method should return `405 Method Not Allowed`. It differs from `404`, which says no route exists for the resource path.

**Diagram.** `known path + wrong method → 405`.

**Annotated code.** `learning/code/ex-22-method-not-allowed/example.py` rejects POST on a GET-only route.

**Key takeaway.** Method mismatch and path absence communicate different facts.

**Why it matters.** Accurate status codes let clients correct requests and let operators diagnose routing behavior.

### Example 23: Request Method Property

**Brief explanation.** A request wrapper can normalize method access through a typed property. Handlers then avoid scattered environ lookup and normalization logic.

**Diagram.** `environ method → Request.method`.

**Annotated code.** `learning/code/ex-23-request-method-property/example.py` exposes an uppercase method property.

**Key takeaway.** Normalization belongs in request construction.

**Why it matters.** Consistent request values reduce surprising route and authorization mismatches.

### Example 24: Request JSON Body

**Brief explanation.** `Request.json()` makes a JSON codec a method of the typed request, while preserving the error boundary. It should return parsed data only after valid decoding.

**Diagram.** `Request.body → json() → typed JSON value`.

**Annotated code.** `learning/code/ex-24-request-json-body/example.py` adds a typed JSON reader.

**Key takeaway.** Request helpers should centralize codecs, not hide errors.

**Why it matters.** One JSON implementation gives every handler the same validation and failure semantics.

### Example 25: Echo Endpoint

**Brief explanation.** An echo endpoint reads a JSON request and returns the same JSON response. It tests both codec directions in one deliberately small endpoint.

**Diagram.** `JSON request → parse → JSON response`.

**Annotated code.** `learning/code/ex-25-echo-endpoint/example.py` verifies round-trip equality.

**Key takeaway.** Request and response codecs must agree on the boundary representation.

**Why it matters.** A round trip exposes encoding, content-type, and body-handling defects before domain behavior complicates them.

### Example 26: Empty Body 204

**Brief explanation.** `204 No Content` communicates successful work with no response body. The framework must not invent JSON or text when the HTTP contract says the body is empty.

**Diagram.** `successful operation → 204 → empty bytes`.

**Annotated code.** `learning/code/ex-26-empty-body-204/example.py` sends an empty response.

**Key takeaway.** Status code semantics determine whether a body is valid.

**Why it matters.** Correct empty responses make client behavior and caches predictable.

### Example 27: Redirect 302

**Brief explanation.** A redirect combines a redirect status with a `Location` header. The framework supplies the protocol shape; clients decide whether and how to follow it.

**Diagram.** `302 + Location → client follows target`.

**Annotated code.** `learning/code/ex-27-redirect-302/example.py` builds a redirect response.

**Key takeaway.** Redirects are ordinary responses with required metadata.

**Why it matters.** A typed response helper prevents redirect endpoints from omitting the destination header.

### Example 28: Framework As Function

**Brief explanation.** The complete beginner model is a function from raw request data to a response value. Router, middleware, and DI are later conveniences over that transformation.

**Diagram.** `environ → Request → handler → Response → WSGI bytes`.

**Annotated code.** `learning/code/ex-28-framework-as-function/example.py` expresses the transformation without hidden state.

**Key takeaway.** A framework core stays understandable when it is composed from explicit functions.

**Why it matters.** This model gives teams a reliable way to trace failures, test behavior, and resist unnecessary framework complexity.
