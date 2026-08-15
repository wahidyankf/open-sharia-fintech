---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Goal

Build a minimal typed WSGI JSON framework with a router, an ordered middleware chain, clean error conversion, and per-request dependency injection. The implementation uses only the Python standard library so every protocol and lifecycle boundary remains inspectable.

## Concepts exercised

- [x] WSGI callable, environ, `start_response`, and bytes iterable (`co-01`–`co-04`)
- [x] router and unknown-path response (`co-11`–`co-14`)
- [x] typed request/response and JSON (`co-15`–`co-17`)
- [x] ordered middleware and error-to-response (`co-18`–`co-22`)
- [x] request-scoped DI (`co-23`, `co-24`)

## Steps

1. Run `python3 -m unittest test_app.py` in `code/` to exercise the WSGI entrypoint.
2. Inspect `router.py`: the route table produces a `404` without handler conditionals.
3. Inspect `middleware.py`: logging wraps error conversion, so a handler exception becomes a clean `500`.
4. Inspect `di.py`: the ranked route receives its service explicitly rather than reading a global.

## Acceptance criteria

The test suite proves `/health` and `/ranked` return JSON, an unknown path returns `404`, and `/boom` returns a non-leaking `500`.
