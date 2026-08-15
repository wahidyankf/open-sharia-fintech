---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

This fixed drilling sequence turns the worked examples into active recall. Answer before opening an answer or running a kata; the purpose is to reconstruct the request lifecycle rather than recognize familiar syntax.

## Recall Q&A

**Q1.** What are the exact WSGI application inputs and output?

<details>
<summary>Answer</summary>

`application(environ, start_response)` receives a CGI-style dictionary and a callback, then returns an iterable of bytestrings. WSGI status and headers are native strings.

</details>

**Q2.** Which ASGI values are bytes, and which status representation is used?

<details>
<summary>Answer</summary>

ASGI HTTP headers are byte pairs, request body chunks are bytes, and `http.response.start` carries an integer status. The application uses `scope`, `receive`, and `send`.

</details>

**Q3.** Why can middleware short-circuit?

<details>
<summary>Answer</summary>

Middleware owns whether it calls the next handler. Authentication can return `401` immediately, deliberately skipping inner middleware and the endpoint.

</details>

## Scenario Judgment

1. A WSGI response uses `(b"Content-Type", b"text/plain")`. Identify the protocol type error and correct it.
2. An ASGI response starts with a body event. Explain the required event ordering.
3. A path exists but receives an unsupported method. Choose `404` or `405` and justify the choice.
4. Error middleware is inside logging middleware. Trace which layer sees a raised handler exception.
5. A handler reads a mutable module global connection. Replace it with a request-scoped provider.

## Hands-on Implementation

1. Implement a WSGI JSON response and test it with a fake `start_response`.
2. Write a route decorator that registers and returns the original function.
3. Compose logging, auth, and error middleware; assert the before/after order.
4. Reassemble an ASGI body from two `http.request` events using `more_body`.
5. Add a per-request dependency and prove two requests get distinct instances.

## Automaticity Checklist

- [ ] I can state the WSGI and ASGI callable contracts from memory.
- [ ] I can distinguish WSGI native strings from ASGI byte headers.
- [ ] I can explain `404`, `405`, and safe `500` conversion.
- [ ] I can predict middleware onion order and a short-circuit.
- [ ] I can describe request, application, and singleton dependency scopes.
- [ ] I can trace a request from server protocol to response bytes.

## Extension challenge

Add one route with path parameters and one request-level concern to your framework. Explain why the
route matcher and the concern run in that order.
