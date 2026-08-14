---
title: "Intermediate Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 11
---

Examples 29–56 move from WSGI’s single synchronous call to ASGI events, then build routing, middleware, and safe error boundaries as explicit composable functions.

### Example 29: Hello ASGI

**Brief explanation.** An ASGI application is an async callable that receives a scope plus awaitable receive and send functions. It sends a response as protocol events rather than returning a body iterable.

**Diagram.** `scope → receive() → send(start) → send(body)`.

**Annotated code.** `learning/code/ex-29-hello-asgi/example.py` emits a minimal HTTP event pair.

**Key takeaway.** ASGI is an event protocol with an async application boundary.

**Why it matters.** The event model enables async and long-lived connections while retaining a testable server-to-app seam.

### Example 30: ASGI Scope Read

**Brief explanation.** The ASGI scope holds connection metadata including type, method, and path. It is delivered once before request events arrive.

**Diagram.** `server connection → scope → application`.

**Annotated code.** `learning/code/ex-30-asgi-scope-read/example.py` reads HTTP scope values.

**Key takeaway.** Scope is ASGI’s typed request context.

**Why it matters.** Keeping connection metadata separate from body events avoids conflating setup with streaming input.

### Example 31: ASGI Receive Body

**Brief explanation.** `receive()` returns inbound event dictionaries that can split one HTTP body across chunks. `more_body` determines when assembly is complete.

**Diagram.** `receive chunk → more_body? → receive next | parse`.

**Annotated code.** `learning/code/ex-31-asgi-receive-body/example.py` joins request chunks.

**Key takeaway.** ASGI body reads are event loops, not one assumed read.

**Why it matters.** Correct chunk assembly supports large bodies and prevents truncating client input.

### Example 32: ASGI Send Response

**Brief explanation.** HTTP responses begin with `http.response.start` and then send one or more body events. The order is part of the protocol.

**Diagram.** `response.start → response.body`.

**Annotated code.** `learning/code/ex-32-asgi-send-response/example.py` records the two-event sequence.

**Key takeaway.** Send response metadata before response bytes.

**Why it matters.** Event ordering mistakes surface as broken server integration instead of ordinary handler bugs.

### Example 33: ASGI Bytes Headers

**Brief explanation.** ASGI headers are byte-string pairs, unlike WSGI’s native-string tuples. This is the most common protocol-porting type error.

**Diagram.** `ASGI header = (bytes, bytes)`.

**Annotated code.** `learning/code/ex-33-asgi-bytes-headers/example.py` validates byte headers.

**Key takeaway.** Preserve ASGI’s bytes header contract.

**Why it matters.** Explicit wire types keep encodings and proxy behavior predictable.

### Example 34: ASGI Serve Uvicorn

**Brief explanation.** An ASGI server invokes the application callable and owns sockets and event scheduling. The framework supplies only the callable.

**Diagram.** `ASGI server → application → events`.

**Annotated code.** `learning/code/ex-34-asgi-serve-uvicorn/example.py` documents server invocation.

**Key takeaway.** Deployment and framework responsibilities stay separate.

**Why it matters.** A replaceable server boundary makes development, testing, and production hosting less coupled.

### Example 35: WSGI Vs ASGI Contrast

**Brief explanation.** The same endpoint can be written for WSGI and ASGI while their calling conventions differ. WSGI returns bytes synchronously; ASGI sends async events.

**Diagram.** `WSGI call/return ↔ ASGI receive/send`.

**Annotated code.** `learning/code/ex-35-wsgi-vs-asgi-contrast/example.py` compares equivalent responses.

**Key takeaway.** Choose the adapter for the server contract, not endpoint semantics.

**Why it matters.** Understanding the difference prevents accidental blocking or incorrect response types when migrating stacks.

### Example 36: Router Table

**Brief explanation.** A router maps a method and path pair to a handler. Registration and lookup are separate operations.

**Diagram.** `(method, path) → handler`.

**Annotated code.** `learning/code/ex-36-router-table/example.py` registers and resolves a route.

**Key takeaway.** Routing is a deterministic lookup table.

**Why it matters.** Explicit lookup makes router behavior simple to test and extend.

### Example 37: Route Decorator Impl

**Brief explanation.** A route decorator receives a handler, records it in a router, and returns it. The registration side effect happens at declaration time.

**Diagram.** `@route → register(handler) → handler`.

**Annotated code.** `learning/code/ex-37-route-decorator-impl/example.py` implements registration.

**Key takeaway.** Decorators can configure a framework without changing handler identity.

**Why it matters.** This explains the apparent magic of `@app.route` while keeping registration inspectable.

### Example 38: Route Returns Function

**Brief explanation.** A correct route decorator returns the original function object unchanged. The handler remains callable in tests and outside routing.

**Diagram.** `handler → register → same handler`.

**Annotated code.** `learning/code/ex-38-route-returns-function/example.py` asserts identity preservation.

**Key takeaway.** Registration should not destroy handler usability.

**Why it matters.** Preserved identity reduces surprising decorator behavior and simplifies direct unit tests.

### Example 39: Path Param Extract

**Brief explanation.** A parameterized pattern such as `/users/{id}` extracts a named path segment. The router passes the extracted value to the handler.

**Diagram.** `/users/42 → {id: "42"} → handler`.

**Annotated code.** `learning/code/ex-39-path-param-extract/example.py` captures an ID.

**Key takeaway.** Path parameters are route-match output.

**Why it matters.** Extracting once in the router keeps endpoint code focused on domain behavior.

### Example 40: Path Param Typed

**Brief explanation.** A typed parameter pattern converts a matched segment and rejects invalid values. Invalid conversion is a route miss, not a handler crash.

**Diagram.** `/users/x → int conversion fails → 404`.

**Annotated code.** `learning/code/ex-40-path-param-typed/example.py` converts integer IDs.

**Key takeaway.** Type conversion belongs beside route matching.

**Why it matters.** Early conversion protects handlers from malformed path input.

### Example 41: Multiple Params

**Brief explanation.** A route can extract more than one named segment. Parameter names preserve the relationship between URL structure and handler arguments.

**Diagram.** `/users/u/posts/p → {uid, pid}`.

**Annotated code.** `learning/code/ex-41-multiple-params/example.py` resolves two values.

**Key takeaway.** Route matching can produce a typed argument map.

**Why it matters.** Named extraction avoids fragile positional parsing in nested resources.

### Example 42: Route Precedence

**Brief explanation.** Static routes should beat parameter routes on the same prefix. Ordering is therefore a router correctness rule.

**Diagram.** `/users/me → static before /users/{id}`.

**Annotated code.** `learning/code/ex-42-route-precedence/example.py` tests precedence.

**Key takeaway.** More specific routes must win deliberately.

**Why it matters.** Precedence prevents legitimate static endpoints from being swallowed by catch-all patterns.

### Example 43: Unknown Path 404

**Brief explanation.** A router returns a fallback response when no path pattern matches. It keeps absence out of exception control flow.

**Diagram.** `no match → not-found handler`.

**Annotated code.** `learning/code/ex-43-unknown-path-404/example.py` invokes the fallback.

**Key takeaway.** Router misses are expected outcomes.

**Why it matters.** A consistent fallback gives clients and logs a trustworthy contract.

### Example 44: Method Dispatch Router

**Brief explanation.** One path can dispatch to distinct GET and POST handlers. The method is part of the route key.

**Diagram.** `(/items, GET|POST) → distinct handler`.

**Annotated code.** `learning/code/ex-44-method-dispatch-router/example.py` routes both methods.

**Key takeaway.** Method and path together identify an endpoint.

**Why it matters.** This model supports REST semantics without a chain of ad hoc conditionals.

### Example 45: Middleware Single

**Brief explanation.** Middleware accepts a next handler and returns a wrapper. It can observe work before and after the inner call.

**Diagram.** `middleware → handler → middleware`.

**Annotated code.** `learning/code/ex-45-middleware-single/example.py` logs around one handler.

**Key takeaway.** Middleware is higher-order function composition.

**Why it matters.** One reusable wrapper can add cross-cutting behavior without editing endpoints.

### Example 46: Middleware Before After

**Brief explanation.** The before phase executes on the way in and after phase on the way out. This is the foundation of the onion model.

**Diagram.** `before → handler → after`.

**Annotated code.** `learning/code/ex-46-middleware-before-after/example.py` records the sequence.

**Key takeaway.** Response flow reverses request flow.

**Why it matters.** Knowing this order is essential for cleanup, timing, and transaction wrappers.

### Example 47: Middleware Chain Two

**Brief explanation.** Two wrappers nest, so the outer layer’s before code runs first and its after code runs last. Composition order is visible behavior.

**Diagram.** `logging → timing → handler → timing → logging`.

**Annotated code.** `learning/code/ex-47-middleware-chain-two/example.py` shows nesting.

**Key takeaway.** Middleware forms an onion, not a flat list.

**Why it matters.** Teams can reason about interacting cross-cutting concerns by reading composition order.

### Example 48: Middleware Order Flip

**Brief explanation.** Swapping middleware changes before/after execution. The same layers therefore can produce different correct or incorrect behavior.

**Diagram.** `A(B(handler)) ≠ B(A(handler))`.

**Annotated code.** `learning/code/ex-48-middleware-order-flip/example.py` compares orders.

**Key takeaway.** Middleware order is a correctness decision.

**Why it matters.** Authentication, caching, and error conversion can become unsafe when composed in the wrong order.

### Example 49: Middleware Short Circuit

**Brief explanation.** A middleware may return a response without calling the next handler. Authentication uses this to reject an unauthorized request.

**Diagram.** `auth failure → 401 → skip inner layers`.

**Annotated code.** `learning/code/ex-49-middleware-short-circuit/example.py` verifies the handler is not called.

**Key takeaway.** Short-circuiting is a deliberate control-flow boundary.

**Why it matters.** It prevents unauthorized work and makes policy enforcement centralized.

### Example 50: Middleware Mutate Request

**Brief explanation.** A wrapper can attach derived request context before calling the handler. The mutation must be scoped to one request.

**Diagram.** `middleware adds request ID → handler reads ID`.

**Annotated code.** `learning/code/ex-50-middleware-mutate-request/example.py` attaches a request ID.

**Key takeaway.** Request context flows inward through middleware.

**Why it matters.** Scoped metadata supports tracing without mutable process-global state.

### Example 51: Middleware Mutate Response

**Brief explanation.** A wrapper can add a response header after the handler returns. This is a safe location for common response policy.

**Diagram.** `handler response → middleware adds header → client`.

**Annotated code.** `learning/code/ex-51-middleware-mutate-response/example.py` adds a header.

**Key takeaway.** Response policy flows outward through middleware.

**Why it matters.** Central header policies reduce duplication and inconsistent endpoint behavior.

### Example 52: Error Middleware

**Brief explanation.** An outer middleware catches unexpected handler exceptions and maps them to a clean `500` response. It never returns a traceback to the caller.

**Diagram.** `exception → error middleware → 500 response`.

**Annotated code.** `learning/code/ex-52-error-middleware/example.py` contains an exception.

**Key takeaway.** Exceptions cross one controlled error boundary.

**Why it matters.** Clean errors protect internals while preserving a stable client contract.

### Example 53: Exception Handler Map

**Brief explanation.** An exception registry maps a known exception type to a response handler. Specific domain failures can therefore produce precise client responses.

**Diagram.** `exception type → registered handler → response`.

**Annotated code.** `learning/code/ex-53-exception-handler-map/example.py` resolves a custom exception.

**Key takeaway.** Error policy can be declarative data.

**Why it matters.** A registry avoids scattering exception translation across endpoints.

### Example 54: HTTP Exception Raise

**Brief explanation.** A typed HTTP exception carries status and detail while normal control flow remains readable. The outer error layer translates it.

**Diagram.** `raise HTTPException(404) → error handler → 404`.

**Annotated code.** `learning/code/ex-54-http-exception-raise/example.py` maps a raised not-found error.

**Key takeaway.** Intentional HTTP failures are data-rich exceptions.

**Why it matters.** Handlers can stop immediately without manually constructing every failure response.

### Example 55: Leaked Trace Vs Clean

**Brief explanation.** An unhandled failure must become a safe generic response. A stack trace belongs in logs, never in a client body.

**Diagram.** `unexpected error → logged detail + clean 500`.

**Annotated code.** `learning/code/ex-55-leaked-trace-vs-clean/example.py` asserts no traceback leaks.

**Key takeaway.** Error observability and client disclosure have different audiences.

**Why it matters.** Avoiding trace leakage protects implementation details and reduces security exposure.

### Example 56: Query Parse ASGI

**Brief explanation.** ASGI gives query strings as bytes in the scope. Decode and parse them before handlers consume parameters.

**Diagram.** `scope query_string bytes → decode → parse_qs`.

**Annotated code.** `learning/code/ex-56-query-parse-asgi/example.py` parses ASGI query bytes.

**Key takeaway.** ASGI query parsing is a bytes-to-values codec boundary.

**Why it matters.** Explicit decoding makes Unicode and repeated query values predictable across endpoints.
