# Async Python & FastAPI Services (By Example, Python)

**Course ID**: `async-python-and-fastapi-services` · **Format**: By Example · **Language**: Python.
**NEW** — productivity course; the async-Python / FastAPI stack the `remotebrowser` target codebase is
built on.

**Scope note**: the modern async-Python **service** stack — `async`/`await` and the event loop,
**FastAPI** routing + dependency injection, **Pydantic v2** models/validation, and the current tooling
(`uv` for envs/installs, `ruff` for lint/format, `pyright` for type checking). It builds on
`backend-essentials` (which teaches HTTP backends with persistence generally); this course goes deeper
into async and the FastAPI/Pydantic idiom for **production services**. It keeps `just-enough-python` a
lean interview refresh — the depth lives here, where web/backend productivity lives. Proof-of-transfer
target: `remotebrowser` (async Python + FastAPI + `fastmcp`), not a subject.

## Why this exists · the big idea

- **The problem before the solution**: a synchronous service blocks a whole worker on every slow I/O
  call (a DB query, an HTTP call, a browser command), capping throughput; and untyped, unvalidated
  request handling turns every endpoint into a runtime-error surface. Async concurrency and typed,
  validated contracts are the two levers that make a Python service both fast and safe.
- **Keep-this-if-you-forget-everything**: `async` lets one process interleave thousands of I/O-bound
  waits without threads; FastAPI + Pydantic turn your type hints into the request/response contract,
  validation, and docs — so the types you write are the API you ship.
- **Big ideas touched**: `determinism-vs-emergence` (concurrency without shared mutable state stays
  reasoned; the event loop is cooperative, not preemptive), `abstraction-and-its-cost` (async buys
  I/O throughput but colours your whole call graph `async`).

## Prerequisites

- **Prior topics**: `just-enough-python`, `backend-essentials`
  (HTTP, routing, persistence), and `sql-essentials` for the data layer.
- **Tools & environment**: a macOS/Linux terminal; Python 3.x; `uv`, `ruff`, `pyright`, `FastAPI`,
  `pydantic` (v2), an ASGI server (`uvicorn`), `pytest` + `httpx` for testing — all pinned to exact
  CVE-clean versions at authoring; Neovim/VSCode with a Python LSP.
- **Assumed knowledge**: writing Python functions and classes; HTTP request/response basics; running a
  local server and hitting it with `curl` (topic 19).

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe). This stack moves fast — pin every
> version at authoring.

- 2026-07-18 — `[Needs Verification]`: exact current CVE-clean versions of FastAPI, Pydantic v2,
  Starlette, `uvicorn`, `uv`, `ruff`, `pyright`, `httpx` — pin each before authoring; Pydantic v1 vs v2
  APIs differ substantially, so the module must target v2 explicitly.
- 2026-07-18 — `async`/`await`, the `asyncio` event loop, and ASGI are **stable** Python-language and
  ecosystem concepts.
- 2026-07-18 — `[Needs Verification]`: `uv` command surface (it is evolving quickly) and `ruff`'s
  default rule set — re-verify the exact commands and defaults at authoring.

## Concepts

1. **co-01 · async-await-basics** — `async def` defines a coroutine; `await` yields control while an
   awaitable completes, without blocking the thread.
2. **co-02 · the-event-loop** — a single-threaded event loop schedules coroutines cooperatively,
   interleaving many I/O waits in one process.
3. **co-03 · concurrency-vs-parallelism** — async gives I/O concurrency on one core; CPU-bound work
   still needs processes/threads, not the event loop.
4. **co-04 · awaitables-tasks-gather** — `asyncio.create_task` and `asyncio.gather` run coroutines
   concurrently and collect results.
5. **co-05 · async-context-and-iteration** — `async with` and `async for` manage async resources and
   streams (connections, responses).
6. **co-06 · blocking-call-hazard** — a synchronous blocking call inside a coroutine stalls the whole
   loop; offload it to a thread/executor.
7. **co-07 · uv-environments** — `uv` creates isolated environments and installs pinned dependencies
   fast and reproducibly.
8. **co-08 · ruff-lint-and-format** — `ruff` lints and formats Python in one fast tool, replacing
   several older tools.
9. **co-09 · pyright-static-typing** — `pyright` type-checks Python against its type hints, catching
   contract errors before runtime.
10. **co-10 · fastapi-app-and-routes** — a FastAPI app declares path operations with typed parameters
    and return models.
11. **co-11 · path-query-body-params** — FastAPI derives path, query, and body parameters from the
    function signature and their types.
12. **co-12 · pydantic-models** — Pydantic v2 models declare typed, validated data shapes used as
    request and response schemas.
13. **co-13 · request-validation** — invalid input is rejected automatically with a structured 422
    before the handler runs.
14. **co-14 · response-models-and-serialization** — a declared `response_model` shapes and validates
    what the endpoint returns.
15. **co-15 · dependency-injection** — FastAPI's `Depends` supplies shared resources (DB sessions,
    auth) to handlers declaratively.
16. **co-16 · async-database-access** — an async DB driver/session lets query waits yield to the loop
    instead of blocking.
17. **co-17 · error-handling-and-http-exceptions** — raising `HTTPException` (or exception handlers)
    maps failures to correct status codes and bodies.
18. **co-18 · middleware-and-lifespan** — middleware wraps every request; a lifespan handler manages
    startup/shutdown resources (pools, clients).
19. **co-19 · background-tasks** — `BackgroundTasks` defers non-critical work past the response without
    a full queue.
20. **co-20 · openapi-and-docs** — FastAPI generates an OpenAPI schema and interactive docs from the
    typed routes automatically.
21. **co-21 · testing-async-endpoints** — `httpx` + `pytest` (async) exercise endpoints in-process with
    real request/response cycles.
22. **co-22 · streaming-responses** — streaming/SSE responses push data incrementally for long or
    real-time payloads.
23. **co-23 · concurrency-safety** — shared mutable state across coroutines needs care (locks, or
    avoiding shared state) even without OS threads.
24. **co-24 · production-config** — settings via environment/`pydantic-settings`, structured logging,
    and an ASGI server config make a service deployable.

## Tensions & trade-offs — when NOT to reach for this

- **Async everywhere vs where it pays**: async colours the whole call graph and adds cognitive cost; a
  CPU-bound or low-concurrency service gains nothing and pays the complexity. Reach for async when the
  workload is I/O-bound and concurrent (many simultaneous slow calls) — exactly `remotebrowser`'s shape.
- **Framework magic vs explicitness**: FastAPI's dependency injection and validation are convenient but
  implicit; over-nesting `Depends` or hiding logic in validators can obscure the request path. Keep the
  handler's behavior legible.
- **When NOT to block**: the single most common failure is a synchronous library call inside a
  coroutine silently stalling the loop — if a dependency is not async, isolate it in an executor rather
  than pretending the endpoint is non-blocking.

## Lineage — why it beat the alternative

- Python services moved from synchronous WSGI (one worker per concurrent request) to ASGI + async
  because I/O-bound web work — waiting on databases, upstream APIs, and, for `remotebrowser`, remote
  browsers — is dominated by waiting, and async interleaves those waits in one process cheaply. FastAPI
  won mindshare by making the type hints the contract: one declaration drives validation, serialization,
  and OpenAPI docs, collapsing boilerplate. The tooling consolidated too — `uv` and `ruff` replaced a
  stack of slower tools. This module deepens `backend-essentials` toward production
  services and feeds `browser-automation-with-cdp` and the
  harness cluster.

## Worked examples

Colocated under `async-python-and-fastapi-services/learning/code/`. Each is a runnable module or a
FastAPI app exercised by `httpx`, run under `uv`, lint-clean under `ruff`, type-clean under `pyright`.
Contiguous `ex-01..ex-54`. Every example cites the `co-NN` it exercises; every concept is exercised by
≥ 1 example.

> **Volume-target floor**: this syllabus lists **54** of the required **≥75** (the 75–85 By-Example/
> Primer band, floor not cap — see
> [prd.md §Volume-target bands](../prd.md#new-course--capstone-specifications)).
> The maker adds **≥21** more `ex-NN` entries at authoring time, continuing the numbering and pattern
> taxonomy below, before this topic passes its by-example quality gate.

### Beginner (ex 01–18)

1. **ex-01 · first-coroutine** — an `async def` awaited via `asyncio.run` — verify it prints after an
   `await asyncio.sleep`. (co-01)
2. **ex-02 · await-sequential** — two awaits in sequence — verify total time ≈ the sum. (co-01, co-02)
3. **ex-03 · gather-concurrent** — the same two awaits via `gather` — verify total time ≈ the max, not
   the sum. (co-04)
4. **ex-04 · create-task** — schedule a background task and await it — verify both complete. (co-04)
5. **ex-05 · async-with-resource** — `async with` over an async context manager — verify setup/teardown
   order. (co-05)
6. **ex-06 · async-for-stream** — `async for` over an async generator — verify each item arrives. (co-05)
7. **ex-07 · blocking-call-stalls-loop** — a `time.sleep` inside a coroutine — verify it blocks
   concurrency, then fix with `asyncio.sleep`. (co-06)
8. **ex-08 · offload-to-executor** — run a blocking function via `run_in_executor` — verify the loop
   stays responsive. (co-06, co-03)
9. **ex-09 · uv-init-env** — `uv` create env + install a pinned dep — verify a locked, reproducible
   install. (co-07)
10. **ex-10 · ruff-lint-clean** — run `ruff check` + `ruff format` — verify zero findings. (co-08)
11. **ex-11 · pyright-clean** — type-check a typed module with `pyright` — verify zero errors. (co-09)
12. **ex-12 · fastapi-hello** — a one-route FastAPI app — verify `GET /` returns JSON via `httpx`.
    (co-10)
13. **ex-13 · path-param** — a typed path parameter route — verify the type is coerced + validated.
    (co-11)
14. **ex-14 · query-param** — a typed optional query parameter — verify default + override. (co-11)
15. **ex-15 · pydantic-model-body** — a POST accepting a Pydantic model body — verify a valid body is
    parsed. (co-12, co-11)
16. **ex-16 · validation-422** — post an invalid body — verify a structured 422 before the handler runs.
    (co-13)
17. **ex-17 · response-model** — declare a `response_model` — verify extra fields are stripped. (co-14)
18. **ex-18 · openapi-docs** — inspect the generated OpenAPI schema — verify every route + model
    appears. (co-20)

### Intermediate (ex 19–38)

1. **ex-19 · depends-shared-resource** — inject a config object via `Depends` — verify handlers share
   it. (co-15)
2. **ex-20 · depends-db-session** — inject a DB session per request via `Depends` — verify it opens +
   closes per request. (co-15, co-16)
3. **ex-21 · async-sqlite-query** — an async DB query in a handler — verify the query yields to the
   loop. (co-16)
4. **ex-22 · crud-create-read** — POST + GET round-trip against the DB — verify persistence. (co-16,
   co-12)
5. **ex-23 · http-exception** — raise `HTTPException(404)` for a missing resource — verify the status +
   body. (co-17)
6. **ex-24 · custom-exception-handler** — map a domain error to a JSON response — verify the mapping.
   (co-17)
7. **ex-25 · lifespan-pool** — open a connection pool in a lifespan handler — verify it is created once
   at startup. (co-18)
8. **ex-26 · middleware-timing** — a middleware adding a timing header — verify it wraps every request.
   (co-18)
9. **ex-27 · background-task** — send a deferred side effect via `BackgroundTasks` — verify the
   response returns before it completes. (co-19)
10. **ex-28 · concurrent-upstream-calls** — a handler fanning out to two upstreams via `gather` — verify
    combined latency ≈ the slower one. (co-04, co-16)
11. **ex-29 · pydantic-validator** — a Pydantic field validator enforcing a rule — verify a violating
    value is rejected. (co-12, co-13)
12. **ex-30 · nested-models** — a response with nested Pydantic models — verify serialization. (co-12,
    co-14)
13. **ex-31 · settings-from-env** — `pydantic-settings` loading config from env — verify an env override
    applies. (co-24)
14. **ex-32 · structured-logging** — structured request logging middleware — verify one log line per
    request with fields. (co-24, co-18)
15. **ex-33 · test-endpoint-httpx** — an async `httpx` + `pytest` test of an endpoint — verify status +
    body. (co-21)
16. **ex-34 · test-validation-path** — a test asserting a 422 on bad input — verify red→green after the
    model tightens. (co-21, co-13)
17. **ex-35 · dependency-override-in-tests** — override a `Depends` with a fake in tests — verify the
    handler uses the fake DB. (co-15, co-21)
18. **ex-36 · streaming-response** — a `StreamingResponse` chunking a payload — verify chunks arrive
    incrementally. (co-22)
19. **ex-37 · sse-endpoint** — a server-sent-events endpoint — verify a client receives a stream of
    events. (co-22)
20. **ex-38 · concurrency-safe-counter** — a shared counter guarded across coroutines — verify no lost
    updates under concurrent requests. (co-23)

### Advanced (ex 39–54)

1. **ex-39 · full-crud-service** — a complete typed async CRUD service over a DB with DI, validation,
   and error mapping — verify every endpoint round-trips. (co-10–co-17)
2. **ex-40 · pagination-and-filtering** — list endpoints with async pagination + filters — verify page
   boundaries. (co-11, co-16)
3. **ex-41 · auth-dependency** — an auth `Depends` gating protected routes — verify unauthenticated
   calls are rejected. (co-15, co-17)
4. **ex-42 · rate-limit-middleware** — a simple in-process rate limiter as middleware — verify excess
   requests are throttled. (co-18, co-23)
5. **ex-43 · async-http-client-service** — a service calling an upstream API via async `httpx` with a
   pooled client — verify the client is reused. (co-16, co-18)
6. **ex-44 · timeout-and-retry** — an upstream call with a timeout + bounded retry — verify a slow
   upstream is cut off. (co-17, co-06)
7. **ex-45 · background-worker-pattern** — a lifespan-managed background worker draining a queue —
   verify it processes items without blocking requests. (co-19, co-18)
8. **ex-46 · websocket-endpoint** — a FastAPI WebSocket echo — verify a bidirectional message. (co-22,
   co-05)
9. **ex-47 · executor-for-cpu-work** — offload a CPU-bound step to a process/thread pool — verify the
   loop stays responsive under load. (co-03, co-06)
10. **ex-48 · openapi-driven-client** — generate a typed client from the OpenAPI schema and call the
    service — verify contract parity. (co-20)
11. **ex-49 · integration-test-suite** — a full async integration test suite (DB + endpoints + errors) —
    verify all green with a seeded DB. (co-21, co-16, co-17)
12. **ex-50 · type-and-lint-gate** — a `ruff` + `pyright` gate over the whole service — verify both are
    clean. (co-08, co-09)
13. **ex-51 · graceful-shutdown** — a lifespan shutdown draining in-flight work — verify no request is
    dropped on stop. (co-18, co-24)
14. **ex-52 · observability-metrics** — request-count + latency metrics exposed on an endpoint — verify
    the metrics update. (co-24, co-18)
15. **ex-53 · remotebrowser-shaped-fanout** — a service that fans out concurrent long I/O calls
    (illustrating a browser-fleet-shaped workload) and aggregates — verify concurrency + aggregation.
    (co-04, co-16, co-22)
16. **ex-54 · capstone-production-service** — a production-shaped async service: DI, async DB, auth,
    error mapping, streaming, config, logging, tests, and a clean `ruff`/`pyright` gate — verify it runs
    and every gate passes. (co-01–co-24)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small but production-shaped async FastAPI service — typed routes, Pydantic v2
  models, dependency-injected async DB access, error mapping, one streaming endpoint, env config, and
  structured logging — installed and gated under `uv` + `ruff` + `pyright`, tested with async `httpx`.
- **Concepts exercised**: [ ] async + event loop + `gather` (co-01–co-04) [ ] FastAPI routes + params +
  models (co-10–co-12) [ ] validation + response models (co-13, co-14) [ ] DI + async DB (co-15, co-16)
  [ ] error handling + lifespan + config + logging (co-17, co-18, co-24) [ ] streaming (co-22) [ ] async
  tests + `ruff`/`pyright` gate (co-21, co-08, co-09).
- **Ordered steps**:
  1. `async-python-and-fastapi-services/learning/capstone/code/` — the service under `uv` with pinned
     deps. Verify `uv run uvicorn ...` boots and `httpx`/`curl /health` returns 200.
  2. Add typed CRUD over an async DB with DI + validation + error mapping. Verify round-trips and 422s.
  3. Add one streaming endpoint + env config + structured logging + a lifespan-managed resource. Verify
     streaming works and config loads from env.
  4. Add the async test suite and run `ruff` + `pyright`. Verify tests green and both gates clean.
- **Acceptance criteria**: the service boots from a clean `uv` install, every endpoint round-trips,
  invalid input yields a 422, the streaming endpoint streams, tests pass, and `ruff` + `pyright` report
  no findings.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

- **FastAPI documentation** — the authoritative reference for routing, dependency injection, and
  Pydantic integration (pin the version at authoring).
- **Using Asyncio in Python** — Caleb Hattingh. A clear treatment of the event loop and async patterns.
- **Pydantic v2 documentation** — the authoritative reference for models and validation (v2 differs
  materially from v1).

## In which paths

- `job-seeking-software-engineer` — Phase 2 · Multi-Platform Productivity (web → cloud → mobile →
  desktop) — Web sub-phase.
- `software-engineer` — Stage 2 · One language end-to-end, then BUILD A REAL APP FIRST (the
  "immediately effective" payoff).

---

← Back to [README.md — course library catalog](./README.md)
