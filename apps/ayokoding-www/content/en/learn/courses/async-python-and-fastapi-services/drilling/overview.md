---
title: "Overview"
date: 2026-07-29T00:00:00+07:00
draft: false
weight: 1
---

This page is the active-recall companion to the Async Python & FastAPI Services learning track: five fixed
drills that force retrieval instead of passive re-reading. Work through them in order -- short-answer recall
first, then scenario judgment, then hands-on implementation, then a checklist to confirm real automaticity,
and finally why/why-not prompts that test whether you can explain the reasoning, not just execute the syntax.
Every answer is hidden in a `<details>` block; try each item yourself, out loud or on paper, before opening it.
Every prompt below uses its own mocked, self-contained input -- none of it is copy-pasted from the learning
track's 78 worked examples, so recognizing an answer isn't enough; you have to actually reconstruct the
reasoning.

## Recall Q&A

Twenty-four short-answer questions, one per concept (`co-01` through `co-24`). Answer from memory, then check.

**Q1 (co-01 -- async-await-basics).** What does `async def` define, and what do you get back when you call it
bare?

<details>
<summary>Answer</summary>

`async def` defines a **coroutine function**; calling it does **not** run the body -- it returns a **coroutine
object** that you must schedule (usually by `await`-ing it or handing it to `asyncio.run`). The body only runs
when something drives the coroutine on an event loop.

</details>

**Q2 (co-02 -- the-event-loop).** Is the asyncio event loop preemptive or cooperative, and what does that
imply for a coroutine that refuses to yield?

<details>
<summary>Answer</summary>

Cooperative. The loop runs one ready coroutine until it `await`s, then switches to another -- it never
preempts a running coroutine. So a coroutine that never yields (a blocking call) stalls **every** other
coroutine on the same loop, not just itself.

</details>

**Q3 (co-03 -- concurrency-vs-parallelism).** Does `async` give parallelism for CPU-bound work? If not, what
does it give, and what does CPU-bound work need instead?

<details>
<summary>Answer</summary>

No. `async` gives **I/O concurrency** on one core -- many in-flight waits share one thread. CPU-bound work
still needs processes or threads (or the free-threaded build) to run in parallel; offloading it to a
`ProcessPoolExecutor` is the pattern (ex-47). `async` alone buys nothing for CPU work.

</details>

**Q4 (co-04 -- awaitables-tasks-gather).** What do `create_task` and `gather` each do, and what does `gather`
return?

<details>
<summary>Answer</summary>

`create_task` wraps a coroutine in a `Task` and schedules it to run concurrently immediately. `gather` runs
several awaitables concurrently and returns their results **in submission order** (a list). Both turn "await
one at a time" into "await many at once."

</details>

**Q5 (co-05 -- async-context-and-iteration).** What do `async with` and `async for` manage, and when is each
needed?

<details>
<summary>Answer</summary>

`async with` runs an async resource's `__aenter__`/`__aexit__` (whose acquire/release themselves `await`) --
needed for connections and response bodies. `async for` pulls items from an async generator one at a time,
awaiting between items -- needed for async streams. Both are for resources/streams whose operations are
themselves awaitable.

</details>

**Q6 (co-06 -- blocking-call-hazard).** What happens if a `time.sleep` (or a synchronous DB driver) runs inside
a coroutine, and what are the two fixes?

<details>
<summary>Answer</summary>

It blocks the **entire** loop, not just that coroutine, because the loop cannot switch while the blocking call
runs. Fix one: use an async-native equivalent (`asyncio.sleep`, an async driver). Fix two: offload genuinely
blocking code to an executor via `run_in_executor`.

</details>

**Q7 (co-07 -- uv-environments).** What does `uv` replace, and what one property does a pinned `uv` install
guarantee?

<details>
<summary>Answer</summary>

`uv` replaces the slower `python -m venv` + `pip` pair for creating environments and installing dependencies.
A pinned `uv pip install` (or `uv sync` from a `pyproject.toml`) guarantees a **reproducible** environment --
the same exact versions across machines, CI, and deploys.

</details>

**Q8 (co-08 -- ruff-lint-and-format).** What do `ruff check` and `ruff format` each do, and how do they differ?

<details>
<summary>Answer</summary>

`ruff check` **lints** -- flags likely bugs and smells (unused imports, undefined names) without rewriting.
`ruff format` **formats** -- rewrites code into one deterministic style (spacing, line breaks) without judging
correctness. They are two complementary passes.

</details>

**Q9 (co-09 -- pyright-static-typing).** What does `pyright` check, and why is that especially valuable in a
FastAPI service?

<details>
<summary>Answer</summary>

`pyright` type-checks Python against its type hints, catching contract errors (wrong argument type, `None`
where an `int` is expected) before runtime. In a FastAPI service the type hints **are** the API contract, so
`pyright` checks the contract in the editor before a single request runs.

</details>

**Q10 (co-10 -- fastapi-app-and-routes).** What does a FastAPI route declaration drive, beyond just routing?

<details>
<summary>Answer</summary>

The same typed signature drives **validation**, **serialization**, and the **OpenAPI docs** -- one annotation
is simultaneously the validation rule, the response shape, and the schema entry. The route is where the
framework reads the types and turns them into behaviour.

</details>

**Q11 (co-11 -- path-query-body-params).** How does FastAPI infer whether a parameter is a path param, a query
param, or a body param?

<details>
<summary>Answer</summary>

A parameter whose name appears in the route's `{}` placeholder is a **path** param; a Pydantic-model parameter
is the **body**; any other (typically a scalar) is a **query** param. The type annotation on each is the
validation rule.

</details>

**Q12 (co-12 -- pydantic-models).** What does a Pydantic v2 model do on construction, and what role does it
play in a FastAPI handler?

<details>
<summary>Answer</summary>

It validates the incoming data against the declared field types and constraints, raising a `ValidationError`
on a violation (a `422` in a handler). In a handler it is the **boundary** a request must cross before any
handler logic runs, and the shape a response is filtered through on the way out.

</details>

**Q13 (co-13 -- request-validation).** When does request validation run relative to the handler, and what
status does a failure produce?

<details>
<summary>Answer</summary>

Validation runs **before** the handler's own code executes. A failure (missing field, wrong type, violated
constraint) produces a structured **422** naming the offending location -- the handler body only ever sees
already-valid input.

</details>

**Q14 (co-14 -- response-models-and-serialization).** What does a declared `response_model` guarantee about the
response body?

<details>
<summary>Answer</summary>

It filters the return value to exactly the model's fields -- extra fields are stripped. So a field present on
the internal object (a password hash) never reaches the response body if the output model omits it, regardless
of what the handler returns.

</details>

**Q15 (co-15 -- dependency-injection).** What does `Depends` supply, and who resolves it?

<details>
<summary>Answer</summary>

`Depends` supplies a per-request resource (a DB session, a config object, an authenticated user) directly as a
typed handler argument. The **framework** resolves the provider before the handler runs (and tears it down
after), so the handler never knows how the resource was created.

</details>

**Q16 (co-16 -- async-database-access).** Why must an async service use an async DB driver instead of a
synchronous one?

<details>
<summary>Answer</summary>

A synchronous driver blocks the thread on each query, stalling the entire event loop (the co-06 hazard) and
throwing away the concurrency the rest of the service depends on. An async driver (`aiosqlite`, `asyncpg`) lets
each query wait **yield** to the loop, so concurrent requests overlap their query latency.

</details>

**Q17 (co-17 -- error-handling-and-http-exceptions).** What do `HTTPException` and a registered exception
handler each give you?

<details>
<summary>Answer</summary>

`HTTPException(status_code=...)` maps a single failure to a status + body in one call. A registered exception
handler maps a whole **class** of domain errors to a response, so handlers raise plain domain exceptions and
the central mapping decides the status and the consistent envelope shape.

</details>

**Q18 (co-18 -- middleware-and-lifespan).** Distinguish middleware from a lifespan handler -- what does each
run relative to?

<details>
<summary>Answer</summary>

Middleware wraps **every** request/response (cross-cutting behaviour: timing, logging, CORS). A lifespan
handler runs **once** at startup and **once** at shutdown (pooled resources: a connection pool, an HTTP client,
a background worker).

</details>

**Q19 (co-19 -- background-tasks).** When does a `BackgroundTasks` side effect run, and when would you reach
for a lifespan-managed worker instead?

<details>
<summary>Answer</summary>

`BackgroundTasks` runs **after** the response is sent (a one-shot side effect). Reach for a lifespan-managed
worker when the work needs a **long-running** consumer loop (a job processor, a metrics flusher) -- a
`BackgroundTask` is one-shot, not continuous.

</details>

**Q20 (co-20 -- openapi-and-docs).** Where does the OpenAPI schema come from, and what does that imply about
drift?

<details>
<summary>Answer</summary>

It is **generated** from the typed routes -- every path, parameter, model, and status derives from the same
annotations that enforce the contract. So the docs cannot drift from the code: the schema and the
implementation share one source of truth, which is what makes schema-driven client generation safe.

</details>

**Q21 (co-21 -- testing-async-endpoints).** How does an async `httpx` + `pytest` test exercise an endpoint
without a running server?

<details>
<summary>Answer</summary>

Via `ASGITransport(app=app)`: the `AsyncClient` calls the ASGI app **in-process** -- a real request/response
cycle with no socket and no running `uvicorn`. It is fast, deterministic, and part of the same dev loop as
`curl`.

</details>

**Q22 (co-22 -- streaming-responses).** Why stream a response instead of buffering it, and what does an async
generator have to do with it?

<details>
<summary>Answer</summary>

Streaming sends the first byte immediately and keeps peak memory flat (a buffered multi-megabyte response is
slow to first byte and memory-hungry). `StreamingResponse` consumes an **async generator** lazily, flushing
each `yield`ed chunk to the client as it is produced.

</details>

**Q23 (co-23 -- concurrency-safety).** "There are no OS threads, so shared state is safe" -- true or false,
and why?

<details>
<summary>Answer</summary>

False. The read-modify-write window between two `await`s is exactly where a concurrent coroutine can
interleave, so shared mutable state can still lose updates. The fix is an `asyncio.Lock` around the critical
section, or better, avoiding shared state entirely.

</details>

**Q24 (co-24 -- production-config).** Name three things that separate a deployable service from a runnable demo.

<details>
<summary>Answer</summary>

Typed config from environment (`pydantic-settings`) so a missing value fails fast at startup; structured
logging (stable keys, machine-parseable) instead of `print`; and an ASGI server config (host/port, workers,
graceful-timeout) so the process runs behind multiple cores and shuts down cleanly.

</details>

## Applied problems

Twelve scenarios spanning the event loop through production config. Each describes a realistic situation
without naming the concept -- decide which one solves it and why, then check.

**AP1.** A reviewer notices your async handler calls `requests.get(...)` (a synchronous HTTP library) to reach
an upstream. What is the concrete risk, and what is the fix?

<details>
<summary>Worked solution</summary>

`requests.get` is **blocking** -- it stalls the entire event loop for the duration of the call, queuing every
concurrent request behind it (co-06). The fix is an async client (`httpx.AsyncClient`), awaited; if the
blocking library is unavoidable, offload it with `run_in_executor` (co-03, ex-08).

</details>

**AP2.** Your `POST /orders` handler reads a shared in-memory counter with `count += 1` and increments it
twice per request; under load the count drifts below the number of orders created. Why, and what fixes it?

<details>
<summary>Worked solution</summary>

`count += 1` is a read-modify-write; the `await`s around it let another coroutine interleave between the read
and the write, losing updates (co-23). Wrap the critical section in an `asyncio.Lock`, or move the counter into
the database (avoiding shared in-process state entirely).

</details>

**AP3.** A handler needs three independent upstream calls that each take ~100ms. Sequentially it takes ~300ms.
What single change gets it to ~100ms?

<details>
<summary>Worked solution</summary>

Fan out the three calls with `asyncio.gather` so they run concurrently on one loop -- the handler pays the
**slowest** call's latency (~100ms), not the sum (co-04, ex-28). Each upstream call must itself be async.

</details>

**AP4.** Every DB-backed endpoint currently opens its own `aiosqlite.connect` at the top of the handler and
forgets to close it on error. What pattern removes the boilerplate and the leak?

<details>
<summary>Worked solution</summary>

An async-generator `Depends` dependency that `async with`s the connection, `yield`s it, and closes it in the
`finally` (which runs even on error) -- co-15, co-05. Each handler just declares the dependency and receives an
open session.

</details>

**AP5.** A client sends `{"titel": "x"}` (a typo) to your POST route and gets a silent `201` with an empty
title. What model setting would have caught it?

<details>
<summary>Worked solution</summary>

`model_config = ConfigDict(extra="forbid")` on the request model -- the unknown `titel` field becomes a `422`
instead of being silently ignored (co-12, co-13, ex-56). The typo is then rejected loudly at the boundary.

</details>

**AP6.** Your `/users/{id}` route returns the user's `password_hash` in the JSON because the handler returns
the whole internal model. How do you stop the leak without changing the handler's return statement?

<details>
<summary>Worked solution</summary>

Declare a `response_model=UserOut` on the route whose fields **omit** `password_hash` -- `response_model`
filters the output to exactly that shape, stripping the hash regardless of what the handler returns (co-14,
ex-17).

</details>

**AP7.** You need a connection pool opened once at startup and closed once at shutdown, shared by every
request. Where does it live, and how do handlers reach it?

<details>
<summary>Worked solution</summary>

Open it in a `lifespan` handler, stash it on `app.state`, and close it after the `yield` (co-18). Handlers read
it via `request.app.state.pool` (ex-25, ex-43, ex-62). Never open a pool per request -- it throws away pooling.

</details>

**AP8.** A flaky upstream times out intermittently and your handler propagates a 500. You want a bounded retry
with a per-call deadline. What two `asyncio` tools apply?

<details>
<summary>Worked solution</summary>

`asyncio.timeout(deadline)` cuts off a slow call after the deadline (co-06), and a bounded `for` loop retries
on transient failure a fixed number of times. Exhaustion maps to a precise `503` (co-17, ex-44) -- never an
unbounded retry loop.

</details>

**AP9.** Tests of your DB-backed handler are slow and order-dependent because they share one database file. How
do you make them fast and isolated?

<details>
<summary>Worked solution</summary>

Drive the app in-process with `httpx.AsyncClient(ASGITransport(app=app))` (co-21) and give each test a FRESH
temp DB file via a `tmp_path` fixture that overrides the config's DB path (ex-49, capstone). No socket, no
shared state, deterministic order.

</details>

**AP10.** You shipped an endpoint that returns a 500 with a raw traceback in the body, and a security audit
flags it. What should every error response share instead?

<details>
<summary>Worked solution</summary>

One consistent JSON error envelope (e.g. `{"error": {"code", "message"}}`) with the right status, never a raw
traceback or internal detail. Register exception handlers so every failure path -- including unhandled ones --
emits that shape (co-17, ex-24, ex-65).

</details>

**AP11.** A frontend at `https://app.example.com` cannot read your API responses in the browser (CORS error).
How do you allow it without opening the API to every origin?

<details>
<summary>Worked solution</summary>

`CORSMiddleware` with an **explicit** `allow_origins=["https://app.example.com"]` -- that origin may call
cross-origin, others are rejected. Never `["*"]` with credentials (co-18, ex-69).

</details>

**AP12.** You want `ruff` and `pyright` to run on every push and block the merge if either reports a finding.
What is the gate, and why both?

<details>
<summary>Worked solution</summary>

A type-and-lint gate: `ruff check` (lint + format check) AND `pyright` (strict) over the application code, run
in CI as a blocking step (co-08, co-09, ex-50). Both, because `ruff` catches the bugs/style `pyright` cannot
and `pyright` catches the contract errors `ruff` cannot.

</details>

## Code katas

Ten hands-on implementation drills, spanning the event loop through production config. Each is a
self-contained, runnable `.py` snippet -- no live HTTP server, no `uvicorn`: implement it yourself first, then
compare against the reference solution and the verified output shown.

### Kata 1 -- Time two awaits sequentially vs. concurrently

**Task.** Implement `measure_sequential` and `measure_concurrent`, each running two ~`d`-second waits, and
prove sequential takes ~`2d` while concurrent takes ~`d`. (co-04)

<details>
<summary>Reference solution</summary>

```python
import asyncio  # => co-04: gather runs the waits concurrently
import time


async def pause(seconds: float) -> None:  # => a unit of async work
    await asyncio.sleep(seconds)  # => yields to the loop (co-01)


async def measure_sequential(d: float) -> float:  # => two awaits IN SEQUENCE -> ~2d
    start = time.perf_counter()  # => baseline
    await pause(d)  # => first wait
    await pause(d)  # => second wait, stacked after the first
    return time.perf_counter() - start  # => ~2d


async def measure_concurrent(d: float) -> float:  # => gather -> ~d
    start = time.perf_counter()  # => baseline
    await asyncio.gather(pause(d), pause(d))  # => both run concurrently on one loop (co-04)
    return time.perf_counter() - start  # => ~d -- the max, not the sum


def main() -> None:  # => drives both measurements
    seq = asyncio.run(measure_sequential(0.10))  # => sequential
    con = asyncio.run(measure_concurrent(0.10))  # => concurrent
    print(f"sequential={seq:.3f}s concurrent={con:.3f}s")  # => sequential ~0.2, concurrent ~0.1
    assert con < seq  # => concurrency is genuinely faster here


if __name__ == "__main__":
    main()
```

**Run**: `python3 kata.py`

**Output**:

```text
sequential=0.201s concurrent=0.101s
```

</details>

### Kata 2 -- Prove a blocking call stalls the loop

**Task.** Implement `run_with_blocker` and `run_fixed`, each gathering a `time.sleep(d)` and an
`asyncio.sleep(d)`; prove the blocking version takes ~`2d` and the fixed one ~`d`. (co-06)

<details>
<summary>Reference solution</summary>

```python
import asyncio  # => co-06: blocking stalls the loop
import time


async def good(d: float) -> None:  # => an async wait
    await asyncio.sleep(d)  # => yields


async def blocker(d: float) -> None:  # => a BLOCKING wait -- the hazard (co-06)
    time.sleep(d)  # => NO await -> freezes the whole loop


async def fixed(d: float) -> None:  # => offloaded blocking -> loop stays responsive (co-06, co-03)
    loop = asyncio.get_running_loop()  # => the running loop
    await loop.run_in_executor(None, time.sleep, d)  # => blocking runs on a thread


async def run_with_blocker(d: float) -> float:  # => gather bad + good -> ~2d (bad froze good)
    start = time.perf_counter()
    await asyncio.gather(blocker(d), good(d))  # => bad blocks good
    return time.perf_counter() - start


async def run_fixed(d: float) -> float:  # => gather fixed + good -> ~d (concurrency restored)
    start = time.perf_counter()
    await asyncio.gather(fixed(d), good(d))  # => both run concurrently again
    return time.perf_counter() - start


def main() -> None:
    stalled = asyncio.run(run_with_blocker(0.10))  # => ~0.2 -- the stall
    ok = asyncio.run(run_fixed(0.10))  # => ~0.1 -- fixed
    print(f"stalled={stalled:.3f}s fixed={ok:.3f}s")
    assert ok < stalled  # => the offload restored concurrency


if __name__ == "__main__":
    main()
```

**Run**: `python3 kata.py`

**Output**:

```text
stalled=0.201s fixed=0.101s
```

</details>

### Kata 3 -- A Pydantic validator that rejects a bad value

**Task.** Implement an `Email(str)` rule via `field_validator` that rejects a value without `@`, and prove a
violation raises `ValidationError`. (co-12, co-13)

<details>
<summary>Reference solution</summary>

```python
import pydantic  # => to catch ValidationError
from pydantic import BaseModel, field_validator  # => co-12: field_validator is the custom-rule verb


class User(BaseModel):  # => a model with a custom email rule (co-12)
    email: str  # => a plain string at the type level

    @field_validator("email")  # => the custom rule runs during validation (co-13)
    @classmethod
    def must_have_at(cls, value: str) -> str:  # => receives the raw value
        if "@" not in value:  # => the rule
            raise ValueError("email must contain '@'")  # => a violation -> ValidationError/422 (co-13)
        return value  # => accepted value


def main() -> None:
    ok = User(email="a@b.com")  # => accepted
    print(ok.email)  # => Output: a@b.com
    try:
        User(email="bad")  # => no @ -> rejected (co-13)
        raised = False
    except pydantic.ValidationError:
        raised = True
    print(raised)  # => Output: True
    assert raised is True


if __name__ == "__main__":
    main()
```

**Run**: `python3 kata.py`

**Output**:

```text
a@b.com
True
```

</details>

### Kata 4 -- A concurrency-safe counter under simulated concurrent tasks

**Task.** Implement a `Counter` with an `asyncio.Lock`-guarded `inc`, run N concurrent increments, and prove
the final value equals N (no lost updates). (co-23)

<details>
<summary>Reference solution</summary>

```python
import asyncio  # => co-23: Lock guards the critical section


class Counter:  # => a lock-guarded shared counter (co-23)
    def __init__(self) -> None:
        self._value = 0  # => the shared mutable state
        self._lock = asyncio.Lock()  # => only one coroutine in the critical section at a time

    async def inc(self) -> int:  # => a guarded read-modify-write
        async with self._lock:  # => atomic across coroutines (co-23)
            self._value += 1  # => the critical section
            return self._value  # => the new value


async def main() -> None:  # => N concurrent increments
    counter = Counter()  # => the shared counter
    n = 100  # => number of concurrent increments
    await asyncio.gather(*(counter.inc() for _ in range(n)))  # => all run concurrently (co-04)
    print(counter._value)  # => Output: 100 -- no lost updates
    assert counter._value == n  # => the lock made every increment count


if __name__ == "__main__":
    asyncio.run(main())
```

**Run**: `python3 kata.py`

**Output**:

```text
100
```

</details>

### Kata 5 -- A Depends-style provider with teardown

**Task.** Implement `run_with_dependency(provider, handler)` mimicking `Depends`: the provider yields a
resource, the handler uses it, the provider's teardown runs after -- even if the handler raised. (co-15)

<details>
<summary>Reference solution</summary>

```python
from collections.abc import Iterator  # => the shape of a yield-provider (co-15)


class Conn:  # => a stand-in resource
    def __init__(self, name: str) -> None:
        self.name = name
        self.closed = False

    def close(self) -> None:  # => teardown
        self.closed = True


def run_with_dependency(  # => mimics what Depends does per request (co-15)
    provider: Iterator[Conn], handler,
) -> str:
    resource = next(provider)  # => resolve the resource (the part before yield)
    try:
        return handler(resource)  # => the handler just RECEIVES the resource
    finally:
        try:  # => always run teardown, even on error
            next(provider)  # => drive the provider past yield -> runs its teardown
        except StopIteration:  # => the generator finished -- expected after teardown
            pass


def get_conn() -> Iterator[Conn]:  # => a yield-provider (co-15)
    conn = Conn("primary")  # => setup
    yield conn  # => hand it out
    conn.close()  # => teardown -- runs after the handler returns/raises


def use_conn(c: Conn) -> str:  # => a handler that just uses the resource
    return f"used {c.name}"


def main() -> None:
    result = run_with_dependency(get_conn(), use_conn)  # => provider + handler
    print(result)  # => Output: used primary
    assert result == "used primary"


if __name__ == "__main__":
    main()
```

**Run**: `python3 kata.py`

**Output**:

```text
used primary
```

</details>

### Kata 6 -- Map a domain exception to an HTTP-like response

**Task.** Implement `dispatch(handler, exc_map)` that runs a handler and, if it raises a mapped domain
exception, returns the mapped `(status, body)` instead of propagating. (co-17)

<details>
<summary>Reference solution</summary>

```python
class NotFound(Exception):  # => a domain error (co-17)
    pass


class Conflict(Exception):  # => another domain error
    pass


def dispatch(handler, exc_map: dict[type[Exception], tuple[int, str]]):  # => runs handler, maps failures (co-17)
    try:
        return 200, handler()  # => the success path
    except Exception as exc:  # => a domain error raised by the handler
        for exc_type, mapping in exc_map.items():  # => find the mapped class
            if isinstance(exc, exc_type):
                return mapping  # => the mapped (status, body)
        raise  # => unmapped -> re-raise (co-17)


def read_missing():  # => raises NotFound
    raise NotFound()


def create_conflict():  # => raises Conflict
    raise Conflict()


def main() -> None:
    mapping = {NotFound: (404, "not found"), Conflict: (409, "conflict")}  # => the central mapping (co-17)
    print(dispatch(read_missing, mapping))  # => Output: (404, 'not found')
    print(dispatch(create_conflict, mapping))  # => Output: (409, 'conflict')
    assert dispatch(read_missing, mapping) == (404, "not found")


if __name__ == "__main__":
    main()
```

**Run**: `python3 kata.py`

**Output**:

```text
(404, 'not found')
(409, 'conflict')
```

</details>

### Kata 7 -- Compose pagination + filter on an in-memory list

**Task.** Implement `list_page(rows, status, limit, offset)` returning a page plus `total`/`next`, where
`total` reflects the filtered count. (co-11)

<details>
<summary>Reference solution</summary>

```python
from typing import TypedDict


class Row(TypedDict):  # => a typed row
    id: int
    status: str


class Page(TypedDict):  # => the paginated envelope (co-11)
    items: list[Row]
    total: int  # => the FILTERED count
    next: int | None  # => None at the end


def list_page(rows: list[Row], status: str | None, limit: int, offset: int) -> Page:  # => co-11
    filtered = [r for r in rows if status is None or r["status"] == status]  # => filter step
    total = len(filtered)  # => the filtered count, not the whole list (co-11)
    page = filtered[offset : offset + limit]  # => pagination step over the filtered set
    nxt = offset + limit  # => the next page's offset
    return {"items": page, "total": total, "next": nxt if nxt < total else None}  # => None at end


def main() -> None:
    rows: list[Row] = [  # => 4 rows: 2 done, 2 todo
        {"id": 1, "status": "done"},
        {"id": 2, "status": "todo"},
        {"id": 3, "status": "done"},
        {"id": 4, "status": "todo"},
    ]
    p = list_page(rows, status="done", limit=1, offset=0)  # => first page of done-only
    print([r["id"] for r in p["items"]], p["total"], p["next"])  # => [1] 2 1 -- total is the FILTERED count
    assert [r["id"] for r in p["items"]] == [1]
    assert p["total"] == 2  # => 2 done rows total, even though only 1 is on this page


if __name__ == "__main__":
    main()
```

**Run**: `python3 kata.py`

**Output**:

```text
[1] 2 1
```

</details>

### Kata 8 -- A response_model that strips a secret field

**Task.** Given an input dict with `name` and `secret`, implement `filter_output(input_dict)` that returns only
`name` -- mimicking what `response_model` does to the output. (co-14)

<details>
<summary>Reference solution</summary>

```python
ALLOWED_OUT_FIELDS = {"name"}  # => the output model's allowed fields (co-14)


def filter_output(input_dict: dict[str, object]) -> dict[str, object]:  # => mimics response_model filtering
    return {k: v for k, v in input_dict.items() if k in ALLOWED_OUT_FIELDS}  # => keep only allowed fields (co-14)


def main() -> None:
    internal = {"name": "widget", "secret": "cost-is-3.50"}  # => the internal object has a secret
    out = filter_output(internal)  # => the output model strips it
    print(out)  # => Output: {'name': 'widget'}
    assert out == {"name": "widget"}  # => secret never reaches the output (co-14)
    assert "secret" not in out


if __name__ == "__main__":
    main()
```

**Run**: `python3 kata.py`

**Output**:

```text
{'name': 'widget'}
```

</details>

### Kata 9 -- A bounded retry with a timeout around a flaky call

**Task.** Implement `call_with_retry(func, attempts, timeout)` that retries a flaky `func` up to `attempts`
times, each under `asyncio.timeout(timeout)`, returning the result or raising after exhaustion. (co-06, co-17)

<details>
<summary>Reference solution</summary>

```python
import asyncio  # => co-06: asyncio.timeout enforces a deadline


async def call_with_retry(func, attempts: int, timeout: float):  # => bounded retry + per-call deadline
    last_error: Exception = RuntimeError("no attempts made")  # => remembers the last failure
    for _ in range(attempts):  # => a BOUNDED number of attempts (co-06)
        try:
            async with asyncio.timeout(timeout):  # => cut off a slow call after `timeout` (co-06)
                return await func()  # => success -> return immediately
        except (RuntimeError, TimeoutError) as exc:  # => transient failure or timeout -> retry
            last_error = exc  # => record and retry
    raise last_error  # => exhausted -> re-raise (a handler maps this to 503, co-17)


attempts_made = 0  # => a mutable counter for the mock


async def flaky():  # => fails twice, then succeeds
    global attempts_made
    attempts_made += 1
    await asyncio.sleep(0.01)  # => simulate latency (co-02)
    if attempts_made < 3:  # => fail the first two
        raise RuntimeError("transient")
    return "ok"  # => succeed on the third


async def main() -> None:
    result = await call_with_retry(flaky, attempts=5, timeout=1.0)  # => succeeds on attempt 3
    print(result)  # => Output: ok
    assert result == "ok"


if __name__ == "__main__":
    asyncio.run(main())
```

**Run**: `python3 kata.py`

**Output**:

```text
ok
```

</details>

### Kata 10 -- Load typed config from a dict (mimicking pydantic-settings)

**Task.** Implement `load_settings(raw, defaults)` returning a typed dict with defaults filled in, raising
`ValueError` if a present value has the wrong type. (co-24)

<details>
<summary>Reference solution</summary>

```python
DEFAULTS: dict[str, object] = {"env": "dev", "port": 8000}  # => co-24: typed defaults
TYPES: dict[str, type] = {"env": str, "port": int}  # => the expected type per field


def load_settings(raw: dict[str, object]) -> dict[str, object]:  # => mimics pydantic-settings (co-24)
    out: dict[str, object] = dict(DEFAULTS)  # => start from defaults
    for key, value in raw.items():  # => apply overrides
        if key in TYPES and not isinstance(value, TYPES[key]):  # => wrong type -> fail fast (co-24)
            raise ValueError(f"{key} must be {TYPES[key].__name__}, got {type(value).__name__}")
        out[key] = value  # => accepted override
    return out  # => resolved config


def main() -> None:
    ok = load_settings({"port": 9000})  # => override applies, env stays default
    print(ok)  # => Output: {'env': 'dev', 'port': 9000}
    assert ok["port"] == 9000
    raised = False
    try:
        load_settings({"port": "not-an-int"})  # => wrong type -> ValueError (co-24)
    except ValueError:
        raised = True
    print(raised)  # => Output: True
    assert raised is True


if __name__ == "__main__":
    main()
```

**Run**: `python3 kata.py`

**Output**:

```text
{'env': 'dev', 'port': 9000}
True
```

</details>

## Self-check checklist

Confirm each item without checking the learning track first. If you hesitate, that concept needs another pass.

- [ ] I can explain what `async def` defines and that calling it returns a coroutine object, not a result.
      (co-01)
- [ ] I can state that the event loop is cooperative and what that implies for a non-yielding coroutine.
      (co-02)
- [ ] I can distinguish async I/O concurrency from CPU parallelism and say what CPU-bound work needs instead.
      (co-03)
- [ ] I can describe `create_task` and `gather` and that `gather` returns results in submission order. (co-04)
- [ ] I can explain when `async with` and `async for` are needed (resources/streams whose ops await). (co-05)
- [ ] I can describe the blocking-call hazard and its two fixes. (co-06)
- [ ] I can state what `uv` replaces and what a pinned install guarantees. (co-07)
- [ ] I can distinguish `ruff check` from `ruff format`. (co-08)
- [ ] I can explain what `pyright` checks and why that is especially valuable with FastAPI. (co-09)
- [ ] I can state what a route declaration drives beyond routing. (co-10)
- [ ] I can explain how FastAPI infers path vs. query vs. body params. (co-11)
- [ ] I can describe what a Pydantic model does on construction and its role in a handler. (co-12)
- [ ] I can state when request validation runs and the status a failure produces. (co-13)
- [ ] I can explain what a `response_model` guarantees about the response body. (co-14)
- [ ] I can describe what `Depends` supplies and who resolves it. (co-15)
- [ ] I can explain why an async service must use an async DB driver. (co-16)
- [ ] I can distinguish `HTTPException` from a registered exception handler. (co-17)
- [ ] I can distinguish middleware from a lifespan handler. (co-18)
- [ ] I can state when a `BackgroundTasks` side effect runs and when a worker is the better choice. (co-19)
- [ ] I can explain where the OpenAPI schema comes from and what that implies about drift. (co-20)
- [ ] I can explain how an async `httpx` test exercises an endpoint without a running server. (co-21)
- [ ] I can explain why you stream a response and what an async generator does for it. (co-22)
- [ ] I can refute "no threads means shared state is safe" and name the fix. (co-23)
- [ ] I can name three things that separate a deployable service from a runnable demo. (co-24)
- [ ] I can explain, in one sentence, what `determinism-vs-emergence` means for this topic -- why a cooperative
      loop's fairness is a discipline every author maintains. (`determinism-vs-emergence`)
- [ ] I can explain, in one sentence, what `abstraction-and-its-cost` means for this topic -- that `async`
      colours the whole call graph, so reach for it only when the workload is I/O-bound. (`abstraction-and-its-cost`)

## Elaborative interrogation & self-explanation

Eight why/why-not prompts that test whether you can explain the reasoning, not just execute the syntax. Answer
each in 2-4 sentences, then check.

**EI1.** Why does `asyncio.gather(pause(0.1), pause(0.1))` take ~0.1s and not ~0.2s, given there is only one
thread?

<details>
<summary>Answer</summary>

Because the two waits **overlap** on the single event loop: when the first coroutine `await`s, the loop
switches to the second, so both waits are in flight simultaneously. The loop interleaves the waits rather than
running them one after another, so the total time is the **max** (~0.1s), not the sum. There is still only one
thread -- concurrency is about interleaving waits, not parallel execution.

</details>

**EI2.** Why is replacing `asyncio.sleep` with `time.sleep` inside a coroutine a bug, even though both "sleep
for 0.1s"?

<details>
<summary>Answer</summary>

`asyncio.sleep` **yields** to the loop, letting other coroutines run during the wait; `time.sleep` **blocks**
the thread, so the loop cannot switch to anything else for the whole 0.1s. On a busy server that means every
concurrent request queues behind the blocking call. The two look identical in isolation and differ catastrophically under load.

</details>

**EI3.** Why declare separate `ItemIn` and `ItemOut` models instead of one model with an optional `secret_note`?

<details>
<summary>Answer</summary>

Because `response_model=ItemOut` **guarantees** the secret never leaves the server: the output filter strips
any field not on `ItemOut`, regardless of what the handler returns. A single model with an optional field
relies on handler discipline (don't return the secret) -- one refactor that accidentally returns the whole
object leaks it. Two models make the leak structurally impossible.

</details>

**EI4.** Why is an async service with a synchronous DB driver no faster (in concurrency) than a synchronous
service?

<details>
<summary>Answer</summary>

Because the synchronous driver blocks the thread on every query, stalling the event loop exactly like
`time.sleep` (co-06). The handler is `async def`, but it `await`s nothing useful during the query -- the loop
is frozen. So every concurrent request queues behind each blocking query, and the async machinery buys
nothing. The async driver is what closes the gap.

</details>

**EI5.** Why does a `Depends`-injected async session close cleanly even when the handler raises an exception?

<details>
<summary>Answer</summary>

Because the dependency is an async generator: the `yield` hands the session to the handler, and the code after
the `yield` (the `await conn.close()`) runs in the dependency's teardown phase, which FastAPI runs whether the
handler returned normally **or** raised. The `finally`/post-yield cleanup is guaranteed, so the connection is
never leaked.

</details>

**EI6.** Why does `response.status_code == 422` (not 400) indicate a validation failure in FastAPI?

<details>
<summary>Answer</summary>

Because FastAPI uses `422 Unprocessable Content` (defined natively in RFC 9110) for request-validation
failures specifically, distinguishing "the request was well-formed JSON but its content failed the declared
schema" (422) from "the request was malformed" (400). The 422 carries a `detail` array naming each offending
location, which is more useful to a client than a generic 400.

</details>

**EI7.** Why put a pooled HTTP client in a lifespan (on `app.state`) instead of constructing one per request?

<details>
<summary>Answer</summary>

Because a pooled client reuses TCP connections across requests -- constructing one per request pays a fresh
handshake (and a fresh pool) every call, throwing away the pooling benefit and increasing latency and
resource use. The lifespan opens the pool once at startup and closes it once at shutdown, so every request
shares it; per-request construction defeats the entire purpose of pooling.

</details>

**EI8.** Why is the `read-modify-write` on a shared counter unsafe in async even though "there are no threads"?

<details>
<summary>Answer</summary>

Because the loop can switch coroutines between the read and the write: coroutine A reads `count=5`, then
`await`s; the loop runs coroutine B which also reads `5` and writes `6`; A resumes and writes `6` -- one
increment is lost. There are no OS threads, but there **is** interleaving at `await` points, and that
interleaving is enough to lose updates. An `asyncio.Lock` makes the read-modify-write atomic across those
interleavings.

</details>

---

← Previous: [Capstone](../learning/capstone/overview.md)
