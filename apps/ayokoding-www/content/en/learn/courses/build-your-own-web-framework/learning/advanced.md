---
title: "Advanced Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 12
---

Examples 57–80 turn the framework core into production-shaped composition: explicit dependency lifecycles, streaming, protocol adapters, sub-app mounting, and end-to-end verification.

### Example 57: DI Registry

**Brief explanation.** A dependency registry maps a declared name to a provider factory. It is the smallest explicit alternative to handlers reaching into globals.

**Diagram.** `dependency name → provider → value`.

**Annotated code.** `learning/code/ex-57-di-registry/example.py` registers and resolves a provider.

**Key takeaway.** Dependencies are framework-owned construction rules.

**Why it matters.** A registry makes resource construction visible, replaceable, and easy to substitute in tests.

### Example 58: DI Inject Handler

**Brief explanation.** A handler declares what it needs and the framework supplies that value before invocation. The handler does not know how the dependency was built.

**Diagram.** `handler declaration → resolver → handler argument`.

**Annotated code.** `learning/code/ex-58-di-inject-handler/example.py` injects a service.

**Key takeaway.** DI separates behavior from resource assembly.

**Why it matters.** Explicit injection reduces hidden coupling and makes handlers easier to reuse.

### Example 59: DI Per Request

**Brief explanation.** A request-scoped provider creates a fresh value for each request. Two requests therefore cannot accidentally share mutable request state.

**Diagram.** `request A → instance A; request B → instance B`.

**Annotated code.** `learning/code/ex-59-di-per-request/example.py` proves distinct instances.

**Key takeaway.** Request scope isolates request state.

**Why it matters.** Isolation prevents cross-request data leakage and concurrency surprises.

### Example 60: DI Singleton

**Brief explanation.** An app-scoped singleton is built once and reused. It is appropriate only for resources designed for shared, safe lifetime.

**Diagram.** `many requests → one singleton`.

**Annotated code.** `learning/code/ex-60-di-singleton/example.py` caches one instance.

**Key takeaway.** Scope is a correctness and lifecycle choice.

**Why it matters.** Choosing singleton deliberately avoids needless setup without accidentally sharing request state.

### Example 61: DI DB Connection

**Brief explanation.** A fake database connection demonstrates a request-scoped dependency passed into a handler. The framework, not the handler, controls construction.

**Diagram.** `request → connection provider → handler`.

**Annotated code.** `learning/code/ex-61-di-db-connection/example.py` injects a fake connection.

**Key takeaway.** Data access is a declared dependency.

**Why it matters.** This seam makes real connection pools testable and replaceable.

### Example 62: Lifespan Startup

**Brief explanation.** ASGI lifespan startup initializes shared resources before requests arrive. The application acknowledges completion through a lifespan event.

**Diagram.** `lifespan.startup → initialize → startup.complete`.

**Annotated code.** `learning/code/ex-62-lifespan-startup/example.py` initializes a resource.

**Key takeaway.** Startup is an explicit protocol phase.

**Why it matters.** Lifecycle events prevent the first user request from racing resource initialization.

### Example 63: Lifespan Shutdown

**Brief explanation.** ASGI lifespan shutdown releases resources before the process exits. Cleanup is the symmetric partner of startup.

**Diagram.** `lifespan.shutdown → close → shutdown.complete`.

**Annotated code.** `learning/code/ex-63-lifespan-shutdown/example.py` closes a resource.

**Key takeaway.** Shared resources need an owned shutdown path.

**Why it matters.** Explicit teardown protects connections, files, and buffered work during deployment changes.

### Example 64: Streaming Response ASGI

**Brief explanation.** ASGI streams a response through several body events while `more_body` remains true. A final event closes the response.

**Diagram.** `start → chunk → chunk → final body`.

**Annotated code.** `learning/code/ex-64-streaming-response-asgi/example.py` sends multiple chunks.

**Key takeaway.** Streaming is ordinary ASGI event sequencing.

**Why it matters.** Chunking supports long outputs without materializing the entire response in memory.

### Example 65: Streaming Response WSGI

**Brief explanation.** WSGI streams by yielding multiple byte chunks from its returned iterable. The server consumes the iterable as data becomes available.

**Diagram.** `generator yields bytes → server writes chunks`.

**Annotated code.** `learning/code/ex-65-streaming-response-wsgi/example.py` yields body chunks.

**Key takeaway.** WSGI streaming uses its iterable return value.

**Why it matters.** Lazy responses support efficient downloads and progressive generation in synchronous deployments.

### Example 66: SSE Endpoint

**Brief explanation.** Server-sent events are a streaming text response whose frames use the `data:` format. The framework must set the event-stream content type and keep the stream open.

**Diagram.** `event generator → text/event-stream → client`.

**Annotated code.** `learning/code/ex-66-sse-endpoint/example.py` emits successive event frames.

**Key takeaway.** SSE is streaming HTTP with a defined text framing.

**Why it matters.** It enables simple server-to-browser updates without a bespoke WebSocket protocol.

### Example 67: Middleware Stack Three

**Brief explanation.** Logging, authentication, and timing form a three-layer onion. Their nesting determines both observability and which work unauthorized requests perform.

**Diagram.** `logging → auth → timing → handler → timing → auth → logging`.

**Annotated code.** `learning/code/ex-67-middleware-stack-three/example.py` verifies full ordering.

**Key takeaway.** Middleware interactions scale by composition, not by special cases.

**Why it matters.** A visible stack lets teams review security and cost consequences of ordering.

### Example 68: Full Request Lifecycle

**Brief explanation.** One trace follows a request from server boundary through request construction, router, middleware, handler, and response serialization. It unifies the framework model.

**Diagram.** `socket → environ → router → middleware → handler → response`.

**Annotated code.** `learning/code/ex-68-full-request-lifecycle/example.py` records each stage once.

**Key takeaway.** A framework is a chain of explicit transformations.

**Why it matters.** End-to-end traces make performance and failure investigation systematic.

### Example 69: Typed Request Response Full

**Brief explanation.** Fully typed request and response values clarify ownership of headers, query, body, and status. Static checking catches contract drift before server execution.

**Diagram.** `typed Request → typed Response`.

**Annotated code.** `learning/code/ex-69-typed-request-response-full/example.py` uses complete typed values.

**Key takeaway.** Types make protocol assumptions executable documentation.

**Why it matters.** Strong boundaries lower the chance of wrong header, status, or body handling in extensions.

### Example 70: Content Negotiation

**Brief explanation.** An `Accept` header lets a client state which representation it prefers. A handler chooses JSON or text and sets the matching response content type.

**Diagram.** `Accept → representation choice → Content-Type`.

**Annotated code.** `learning/code/ex-70-content-negotiation/example.py` selects JSON or text.

**Key takeaway.** Representation selection is request-driven response policy.

**Why it matters.** Negotiation lets one resource serve multiple interoperable clients without ambiguous payloads.

### Example 71: Header Case Insensitive

**Brief explanation.** HTTP header names are case-insensitive even when a concrete request representation preserves a spelling. A request wrapper should normalize lookup.

**Diagram.** `content-type = Content-Type`.

**Annotated code.** `learning/code/ex-71-header-case-insensitive/example.py` normalizes header keys.

**Key takeaway.** Header semantics differ from dictionary-key semantics.

**Why it matters.** Case-insensitive access avoids client-specific failures and duplicate policy logic.

### Example 72: Port Flask Handler

**Brief explanation.** A simple Flask-shaped handler can be ported by expressing its request input and response output through the small framework core. The endpoint’s semantics need not depend on Flask internals.

**Diagram.** `Flask-shaped handler → framework Request/Response`.

**Annotated code.** `learning/code/ex-72-port-flask-handler/example.py` preserves response bytes.

**Key takeaway.** Framework convenience can be separated from endpoint behavior.

**Why it matters.** This distinction makes migration and framework evaluation less risky.

### Example 73: Port FastAPI Handler

**Brief explanation.** A FastAPI-shaped dependency can be represented as a provider resolved before a handler call. The useful design is declared input, not a particular library API.

**Diagram.** `Depends-like provider → handler value`.

**Annotated code.** `learning/code/ex-73-port-fastapi-handler/example.py` injects a declared value.

**Key takeaway.** DI patterns are portable across frameworks.

**Why it matters.** Understanding the underlying mechanism reduces lock-in and clarifies test seams.

### Example 74: WSGI Middleware Wrap

**Brief explanation.** WSGI middleware wraps the whole application callable and sees every request before the inner app. It preserves the same two-argument callable shape.

**Diagram.** `server → middleware(app) → app`.

**Annotated code.** `learning/code/ex-74-wsgi-middleware-wrap/example.py` intercepts a request.

**Key takeaway.** WSGI middleware is callable composition.

**Why it matters.** Global policy can be added without modifying route handlers or server configuration.

### Example 75: ASGI Middleware Wrap

**Brief explanation.** ASGI middleware wraps an async application and can observe scope, receive, and send. It therefore wraps the entire event pump.

**Diagram.** `scope/receive/send → middleware → application`.

**Annotated code.** `learning/code/ex-75-asgi-middleware-wrap/example.py` wraps events.

**Key takeaway.** ASGI middleware composes at the event boundary.

**Why it matters.** The wrapper can implement consistent policy for HTTP, WebSocket, and lifespan scopes.

### Example 76: Error In Middleware

**Brief explanation.** Middleware can fail too, so the outer error boundary must wrap every inner layer. Error handling is only reliable when composition is intentional.

**Diagram.** `outer errors → failing middleware → clean 500`.

**Annotated code.** `learning/code/ex-76-error-in-middleware/example.py` contains a middleware failure.

**Key takeaway.** Error conversion must be outermost.

**Why it matters.** A contained failure protects clients even when cross-cutting code is defective.

### Example 77: Mount Subapp

**Brief explanation.** A parent router can delegate a path prefix to a sub-application. The mount boundary preserves the child’s routing responsibility.

**Diagram.** `/admin/* → subapp router`.

**Annotated code.** `learning/code/ex-77-mount-subapp/example.py` resolves a prefixed route.

**Key takeaway.** Mounting composes applications by path.

**Why it matters.** It enables modular ownership without one monolithic route table.

### Example 78: Static File Handler

**Brief explanation.** A static handler reads bytes and chooses an appropriate content type. It must not decode arbitrary file data as text.

**Diagram.** `path → file bytes + Content-Type → response`.

**Annotated code.** `learning/code/ex-78-static-file-handler/example.py` serves a typed file response.

**Key takeaway.** Static delivery is response serialization with file input.

**Why it matters.** Correct byte and type handling avoids broken assets and accidental content sniffing.

### Example 79: Integration Test Suite

**Brief explanation.** A small test client invokes the complete request-to-response pipeline instead of testing only isolated helpers. It verifies composition contracts.

**Diagram.** `test client → app pipeline → asserted response`.

**Annotated code.** `learning/code/ex-79-integration-test-suite/example.py` tests routes end to end.

**Key takeaway.** Integration tests prove framework pieces work together.

**Why it matters.** They catch wrong ordering and adapter mismatches invisible to unit tests.

### Example 80: Mini Framework

**Brief explanation.** The final assembly combines entrypoint, router, middleware, request/response values, and DI into a small JSON API. Each component remains individually visible.

**Diagram.** `server → adapter → router → middleware → DI handler → JSON response`.

**Annotated code.** `learning/code/ex-80-mini-framework/example.py` serves the ranked response end to end.

**Key takeaway.** Frameworks are conveniences over one explicit transformation.

**Why it matters.** A small coherent core gives you the mental model needed to use larger frameworks safely and diagnose their behavior.
