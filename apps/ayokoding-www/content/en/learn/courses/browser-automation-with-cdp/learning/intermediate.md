---
title: "Intermediate Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 20
---

Examples 26-50 connect page interaction to the failure, authorization, and observation boundaries
that make browser automation reliable. Run every snippet with `python3 code/cdp_simulation.py <scenario>`.

### Example 26: Drive Multiple Tabs

_ex-26 · exercises co-20, co-03_

**Brief explanation**: A browser can host several targets; each tab must retain independent state while
sharing the browser process responsibly.
**Code**: `python3 code/ex-26-multiple-tabs/example.py`
**Expected observation**: the two fixture targets retain different titles.
**Key takeaway**: scope state and sessions to a target, then manage capacity above them.
**Why it matters**: cross-target state leaks make concurrent browser work corrupt and nondeterministic.

### Example 27: Bound a Navigation Timeout

_ex-27 · exercises co-06, co-09_

**Brief explanation**: A navigation needs a deadline so a stuck page becomes a recoverable outcome
rather than a permanently occupied browser target.
**Code**: `python3 code/ex-27-navigation-timeout/example.py`
**Expected observation**: the fixture navigation completes within its `asyncio` deadline.
**Key takeaway**: pair every awaited browser operation with an explicit timeout.
**Why it matters**: one hung navigation can otherwise starve a shared page pool.

### Example 28: Retry a Flaky Step

_ex-28 · exercises co-09, co-11_

**Brief explanation**: Retry only a transient, safe fixture operation with a finite attempt budget.
**Code**: `python3 code/ex-28-retry-flaky-step/example.py`
**Expected observation**: the local read-like step succeeds on its second bounded attempt.
**Key takeaway**: retries need an operation-specific policy and a recorded limit.
**Why it matters**: blind retries can multiply side effects or hide persistent failures.

### Example 29: Scroll and Lazy Load

_ex-29 · exercises co-12, co-08_

**Brief explanation**: A scroll action is useful only when it produces the lazy content required by the
next extraction step.
**Code**: `python3 code/ex-29-scroll-and-lazy-load/example.py`
**Expected observation**: `lazy-item` becomes visible in the local fixture after the modeled scroll.
**Key takeaway**: assert the content change, not just the dispatched scroll input.
**Why it matters**: viewport movement alone does not prove that lazy loading succeeded.

### Example 30: Extract Structured Data

_ex-30 · exercises co-14_

**Brief explanation**: Extract selected DOM rows into a named structured shape before application logic
consumes them.
**Code**: `python3 code/ex-30-extract-structured-data/example.py`
**Expected observation**: the fixture rows become dictionaries with `name` and `role` fields.
**Key takeaway**: validate structure at the page boundary rather than passing positional text onward.
**Why it matters**: markup changes otherwise become silent data-quality regressions.

### Example 31: Capture a Full-Page Screenshot

_ex-31 · exercises co-14_

**Brief explanation**: Full-page screenshots need explicit rendered dimensions so a visual artifact has
reproducible context.
**Code**: `python3 code/ex-31-full-page-screenshot/example.py`
**Expected observation**: the fixture image is taller than the viewport and carries PNG bytes.
**Key takeaway**: record viewport and page dimensions with every full-page artifact.
**Why it matters**: visual diffs are not meaningful when rendering conditions are implicit.

### Example 32: Emulate a Device

_ex-32 · exercises co-15_

**Brief explanation**: Device emulation pins the width, height, and mobile behavior a responsive test
claims to cover.
**Code**: `python3 code/ex-32-emulate-device/example.py`
**Expected observation**: the 390px fixture profile renders the compact layout.
**Key takeaway**: put the device profile in the test contract, not in undocumented machine defaults.
**Why it matters**: responsive failures often depend on an omitted viewport condition.

### Example 33: Modify Request Headers

_ex-33 · exercises co-15_

**Brief explanation**: Header mutation is an interception capability that must be restricted to known,
non-secret fixture headers.
**Code**: `python3 code/ex-33-intercept-and-modify-headers/example.py`
**Expected observation**: the fixture request contains `x-fixture-mode: test`.
**Key takeaway**: allowlist mutated header names and never echo sensitive values in logs.
**Why it matters**: a header can change identity, authorization, caching, or routing behavior.

### Example 34: Respect Robots and Rate Limits

_ex-34 · exercises co-16_

**Brief explanation**: Responsible extraction checks robots policy and a rate budget before it processes a
fixture path.
**Code**: `python3 code/ex-34-respect-robots/example.py`
**Expected observation**: the permitted local path has one remaining request token.
**Key takeaway**: technical access is not permission; origin policy and rate limits come first.
**Why it matters**: respectful automation protects people, services, and the reliability of the tool.

### Example 35: Concurrent Page Pool

_ex-35 · exercises co-07, co-19_

**Brief explanation**: A bounded pool drives several page tasks concurrently without allowing resource
ownership to exceed its configured capacity.
**Code**: `python3 code/ex-35-concurrent-page-pool/example.py`
**Expected observation**: three local jobs observe a maximum of two active page slots.
**Key takeaway**: pool scarce browser targets with a semaphore and assert the observed cap.
**Why it matters**: unbounded tab creation turns traffic spikes into browser memory exhaustion.

### Example 36: Reuse a Browser Across Tasks

_ex-36 · exercises co-18_

**Brief explanation**: Browser startup is expensive, so independent tasks should borrow one pool-owned
browser instead of launching a new process for every request.
**Code**: `python3 code/ex-36-reuse-browser-across-tasks/example.py`
**Expected observation**: two tasks share `browser-1` while the launch count remains one.
**Key takeaway**: reuse the browser process while keeping target state isolated per task.
**Why it matters**: per-task browser launches waste time, memory, and OS resources.

### Example 37: Authenticated Session Reuse

_ex-37 · exercises co-18_

**Brief explanation**: A synthetic session can be reused across authorized fixture pages without exposing
a real login flow or credential.
**Code**: `python3 code/ex-37-authenticated-session-reuse/example.py`
**Expected observation**: both pages use the same fixture session and login count stays one.
**Key takeaway**: persist only least-privilege test session state inside a disposable context.
**Why it matters**: repeated logins are slow, flaky, and unsafe when they involve real accounts.

### Example 38: Network Throttling

_ex-38 · exercises co-12, co-09_

**Brief explanation**: A network profile makes latency and bandwidth constraints explicit before the
automation observes a slower fixture response.
**Code**: `python3 code/ex-38-network-throttling/example.py`
**Expected observation**: the modeled transfer duration exceeds its profile latency.
**Key takeaway**: test slow-network behavior with a stated profile, not ambient machine conditions.
**Why it matters**: a flow that works locally can fail when a user has constrained connectivity.

### Example 39: Capture a HAR-like Trace

_ex-39 · exercises co-10, co-11_

**Brief explanation**: A HAR-like trace captures request timing and status for diagnosis while omitting
unbounded response bodies.
**Code**: `python3 code/ex-39-capture-har/example.py`
**Expected observation**: one local page-load entry has status `200` and a bounded duration.
**Key takeaway**: collect the smallest trace that proves the network behavior under test.
**Why it matters**: full network capture can retain sensitive data without improving a diagnosis.

### Example 40: Inject JavaScript Instrumentation

_ex-40 · exercises co-13_

**Brief explanation**: Document-start instrumentation registers before page scripts so later observations
can explain what the fixture executed.
**Code**: `python3 code/ex-40-js-injection-instrumentation/example.py`
**Expected observation**: instrumentation registration precedes the modeled page script.
**Key takeaway**: setup order is part of the instrumentation contract.
**Why it matters**: late instrumentation misses the very page behavior it is meant to observe.

### Example 41: Build a Robust Scraper

_ex-41 · exercises co-04, co-12_

**Brief explanation**: A robust scraper combines origin authorization, bounded retry, and structured
fixture extraction rather than assuming a single page response will work.
**Code**: `python3 code/ex-41-robust-scraper/example.py`
**Expected observation**: the authorized fixture yields one item on its second bounded attempt.
**Key takeaway**: compose waits, retries, and policy checks around a narrow extraction goal.
**Why it matters**: real-world pages fail transiently and must not trigger unbounded or unauthorized work.

### Example 42: Run a Screenshot Diff Test

_ex-42 · exercises co-15, co-14_

**Brief explanation**: A visual regression test compares normalized fixture artifacts and reports a
meaningful difference when their bytes change.
**Code**: `python3 code/ex-42-screenshot-diff-test/example.py`
**Expected observation**: the blue baseline and orange candidate produce a detected regression.
**Key takeaway**: compare a defined visual artifact, not an unspecified browser screenshot.
**Why it matters**: deterministic visual checks catch rendering changes that DOM assertions can miss.

### Example 43: Drive a Single-Page Application

_ex-43 · exercises co-21_

**Brief explanation**: A client-rendered application becomes ready when its route and rendered state
change, not merely after the initial document load.
**Code**: `python3 code/ex-43-drive-a-spa/example.py`
**Expected observation**: the fixture route changes to `/report` and heading becomes `Report`.
**Key takeaway**: wait for the post-interaction SPA state your next step requires.
**Why it matters**: client-side navigation is asynchronous even when the original page stays open.

### Example 44: Recover from a Crashed Target

_ex-44 · exercises co-16_

**Brief explanation**: Target loss is an ordinary browser failure; recovery needs a new attachment before
the task resumes.
**Code**: `python3 code/ex-44-error-recovery-flow/example.py`
**Expected observation**: an unavailable target is replaced by the live `target-new` fixture.
**Key takeaway**: reattach explicitly and discard stale target/session identifiers.
**Why it matters**: continuing with a crashed target turns a recoverable error into a stuck workflow.

### Example 45: Expose Browser Control as an HTTP Service

_ex-45 · exercises co-08, co-14_

**Brief explanation**: A browser-control service should expose narrow, typed operations and return plain
data rather than handing a browser object to callers.
**Code**: `python3 code/ex-45-expose-as-http-service/example.py`
**Expected observation**: the authorized fixture navigation returns status `200` and a title.
**Key takeaway**: keep browser ownership behind the service boundary.
**Why it matters**: a narrow API makes authorization, capacity, and audit policy enforceable.

### Example 46: Run a Pooled Service Under Load

_ex-46 · exercises co-10, co-18_

**Brief explanation**: A service under concurrent demand must hold clients to its page-pool capacity
instead of creating targets without a limit.
**Code**: `python3 code/ex-46-pooled-service-under-load/example.py`
**Expected observation**: three fixture clients observe a peak service concurrency of two.
**Key takeaway**: enforce resource limits at the shared service boundary.
**Why it matters**: an unbounded client surge can exhaust the browser before any request completes.

### Example 47: Compare Raw CDP with Playwright

_ex-47 · exercises co-18_

**Brief explanation**: Raw CDP and a high-level wrapper can be compared through the user-visible result
they promise rather than through identical internals.
**Code**: `python3 code/ex-47-compare-with-playwright/example.py`
**Expected observation**: both local forms return `Fixture title`.
**Key takeaway**: use a wrapper when its contract meets the need, while retaining protocol awareness.
**Why it matters**: abstraction removes boilerplate but not browser lifecycle and readiness failures.

### Example 48: Recognize Headless Detection Signals

_ex-48 · exercises co-05, co-18_

**Brief explanation**: A page can expose a headless signal; recognizing it is legitimate, but evading it
is outside this course's responsible-automation boundary.
**Code**: `python3 code/ex-48-headless-detection-awareness/example.py`
**Expected observation**: the fixture reports that a WebDriver signal was observed.
**Key takeaway**: record detection signals transparently; do not add stealth behavior.
**Why it matters**: automation must respect site policy and avoid deceptive browser manipulation.

### Example 49: Build a Resilient Fleet Slice

_ex-49 · exercises co-09, co-14_

**Brief explanation**: A small browser fleet needs health checks and replacement before a failed worker
is allowed to hold future tasks.
**Code**: `python3 code/ex-49-resilient-fleet-slice/example.py`
**Expected observation**: the unhealthy fixture worker is replaced by the healthy worker.
**Key takeaway**: make health, reclamation, and assignment distinct fleet responsibilities.
**Why it matters**: a stuck worker quietly reduces throughput until every caller queues behind it.

### Example 50: Capstone Browser Service

_ex-50 · exercises co-21, co-22_

**Brief explanation**: The capstone combines an authorized navigation request, a bounded service result,
and a screenshot artifact without handing browser ownership to the caller.
**Code**: `python3 code/ex-50-capstone-browser-service/example.py`
**Expected observation**: the fixture checkout returns status `200`, title `Checkout`, and PNG bytes.
**Key takeaway**: reliable browser automation is a service contract with policy, capacity, and evidence.
**Why it matters**: this is the reusable shape behind a safe browser-automation tool boundary.
