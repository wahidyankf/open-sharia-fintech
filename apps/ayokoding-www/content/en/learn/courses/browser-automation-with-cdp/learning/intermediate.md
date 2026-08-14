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

**Brief explanation**: A thin client should preserve the raw command/event semantics it simplifies.
**Code**: `python3 code/cdp_simulation.py raw-cdp-vs-client`
**Expected observation**: both modeled paths return the same contract result.
**Key takeaway**: wrappers change ergonomics, not the underlying asynchronous reality.
**Why it matters**: protocol literacy makes wrapper failures diagnosable.

### Example 27: Bound a Navigation Timeout

_ex-27 · exercises co-06, co-09_

**Brief explanation**: Lifecycle ordering reveals which condition actually precedes a step.
**Code**: `python3 code/cdp_simulation.py lifecycle-events`
**Expected observation**: one deterministic event-stream scenario completes.
**Key takeaway**: record the event sequence before choosing a wait.
**Why it matters**: readiness has no universal event.

### Example 28: Retry a Flaky Step

_ex-28 · exercises co-09, co-11_

**Brief explanation**: A selector wait is a bounded predicate, not an unbounded polling loop.
**Code**: `python3 code/cdp_simulation.py wait-for-selector`
**Expected observation**: safe JSON confirms modeled readiness.
**Key takeaway**: use a deadline and report the selector on timeout.
**Why it matters**: diagnostic errors turn flakes into repairable failures.

### Example 29: Scroll and Lazy Load

_ex-29 · exercises co-12, co-08_

**Brief explanation**: A form flow needs field-value and post-submit assertions.
**Code**: `python3 code/cdp_simulation.py fill-and-submit-form`
**Expected observation**: the local flow succeeds without a live account.
**Key takeaway**: assert business-visible state on both sides of the submit.
**Why it matters**: a click can be accepted while validation blocks progress.

### Example 30: Extract Structured Data

_ex-30 · exercises co-14_

**Brief explanation**: Network events expose a page's request graph and timing.
**Code**: `python3 code/cdp_simulation.py network-request-log`
**Expected observation**: a modeled request observation is correlated.
**Key takeaway**: log minimal metadata, not sensitive bodies by default.
**Why it matters**: network traces can contain tokens and personal data.

### Example 31: Capture a Full-Page Screenshot

_ex-31 · exercises co-14_

**Brief explanation**: Capture only an authorized fixture response with an explicit size limit.
**Code**: `python3 code/cdp_simulation.py capture-response-body`
**Expected observation**: no live body is retrieved.
**Key takeaway**: body capture needs a redaction and retention policy.
**Why it matters**: unrestricted capture turns observability into data exfiltration.

### Example 32: Emulate a Device

_ex-32 · exercises co-15_

**Brief explanation**: Interception changes the page's behavior and must be narrowly scoped.
**Code**: `python3 code/cdp_simulation.py block-a-request`
**Expected observation**: the fixture rule is modeled as a controlled decision.
**Key takeaway**: block exact authorized patterns, then log why.
**Why it matters**: broad blocking can hide production defects.

### Example 33: Modify Request Headers

_ex-33 · exercises co-15_

**Brief explanation**: A mock replaces one dependency with a deterministic fixture.
**Code**: `python3 code/cdp_simulation.py mock-a-response`
**Expected observation**: a local canned response scenario returns safely.
**Key takeaway**: test the UI contract, not a third-party system.
**Why it matters**: deterministic mocks make visual and flow tests repeatable.

### Example 34: Respect Robots and Rate Limits

_ex-34 · exercises co-16_

**Brief explanation**: Session setup belongs to a disposable fixture context.
**Code**: `python3 code/cdp_simulation.py set-a-cookie`
**Expected observation**: no credential is created or persisted.
**Key takeaway**: use synthetic, least-privilege fixture sessions.
**Why it matters**: production credentials should never enter course code or logs.

### Example 35: Concurrent Page Pool

_ex-35 · exercises co-07, co-19_

**Brief explanation**: Targets have independent state but share browser resources.
**Code**: `python3 code/cdp_simulation.py multiple-tabs`
**Expected observation**: one modeled multi-target result.
**Key takeaway**: keep session state per target and capacity at the pool.
**Why it matters**: shared mutable page state creates cross-task corruption.

### Example 36: Reuse a Browser Across Tasks

_ex-36 · exercises co-18_

**Brief explanation**: A deadline turns an unbounded navigation into a recoverable failure.
**Code**: `python3 code/cdp_simulation.py navigation-timeout`
**Expected observation**: the simulated operation is bounded.
**Key takeaway**: every browser operation needs an owner and timeout.
**Why it matters**: one stuck tab can otherwise starve the whole pool.

### Example 37: Authenticated Session Reuse

_ex-37 · exercises co-18_

**Brief explanation**: Retry transient, idempotent work with a finite budget and recorded cause.
**Code**: `python3 code/cdp_simulation.py retry-flaky-step`
**Expected observation**: retry policy is modeled without contacting a server.
**Key takeaway**: do not retry authorization failures or unsafe input actions.
**Why it matters**: blind retries can multiply side effects.

### Example 38: Network Throttling

_ex-38 · exercises co-12, co-09_

**Brief explanation**: Scroll changes state; wait for the new content signal before extracting.
**Code**: `python3 code/cdp_simulation.py scroll-and-lazy-load`
**Expected observation**: a local lazy-load scenario completes.
**Key takeaway**: tie an interaction to the observable state it should create.
**Why it matters**: scroll position alone proves nothing about loaded content.

### Example 39: Capture a HAR-like Trace

_ex-39 · exercises co-10, co-11_

**Brief explanation**: Convert selected DOM rows into a small typed data shape at the page boundary.
**Code**: `python3 code/cdp_simulation.py extract-structured-data`
**Expected observation**: an authorized simulated extraction result.
**Key takeaway**: validate structure before handing data to application logic.
**Why it matters**: markup changes otherwise become silent data-quality errors.

### Example 40: Inject JavaScript Instrumentation

_ex-40 · exercises co-13_

**Brief explanation**: Full-page capture requires documented dimensions and artifact limits.
**Code**: `python3 code/cdp_simulation.py full-page-screenshot`
**Expected observation**: a deterministic artifact scenario.
**Key takeaway**: record viewport and page dimensions with visual artifacts.
**Why it matters**: visual diffs are meaningless without rendering context.

### Example 41: Build a Robust Scraper

_ex-41 · exercises co-04, co-12_

**Brief explanation**: Device emulation controls the rendering conditions a test claims to cover.
**Code**: `python3 code/cdp_simulation.py emulate-device`
**Expected observation**: one stable modeled device profile.
**Key takeaway**: make emulation part of the test name and trace.
**Why it matters**: responsive bugs often depend on an omitted condition.

### Example 42: Run a Screenshot Diff Test

_ex-42 · exercises co-15, co-14_

**Brief explanation**: Header changes are privileged request mutation, not ordinary logging.
**Code**: `python3 code/cdp_simulation.py intercept-and-modify-headers`
**Expected observation**: a local policy decision only.
**Key takeaway**: allowlist header names and never log secrets.
**Why it matters**: header interception can change identity and authorization.

### Example 43: Drive a Single-Page Application

_ex-43 · exercises co-21_

**Brief explanation**: Automation is responsible even when a technical route exists.
**Code**: `python3 code/cdp_simulation.py respect-robots`
**Expected observation**: the fixture limiter models throttling.
**Key takeaway**: permission, terms, and a rate budget precede extraction.
**Why it matters**: responsible automation protects people and services.

### Example 44: Recover from a Crashed Target

_ex-44 · exercises co-16_

**Brief explanation**: Test isolation means clearing cookies and storage after every fixture run.
**Code**: `python3 code/cdp_simulation.py clear-storage-between-tests`
**Expected observation**: modeled storage cleanup succeeds.
**Key takeaway**: start and finish each test from a known state.
**Why it matters**: leaked storage causes order-dependent tests.

### Example 45: Expose Browser Control as an HTTP Service

_ex-45 · exercises co-08, co-14_

**Brief explanation**: Navigation may produce multiple network hops before its final page.
**Code**: `python3 code/cdp_simulation.py detect-redirect-chain`
**Expected observation**: a safe chain model is returned.
**Key takeaway**: assert the final authorized origin as well as status.
**Why it matters**: redirects can cross a trust boundary.

### Example 46: Run a Pooled Service Under Load

_ex-46 · exercises co-10, co-18_

**Brief explanation**: Evaluation errors are protocol data that need a typed failure path.
**Code**: `python3 code/cdp_simulation.py handle-javascript-exception`
**Expected observation**: the modeled failure stays correlated to its command.
**Key takeaway**: surface exception details without exposing page secrets.
**Why it matters**: swallowing evaluation failures creates false passes.

### Example 47: Compare Raw CDP with Playwright

_ex-47 · exercises co-18_

**Brief explanation**: Cancellation must release the target and discard stale responses safely.
**Code**: `python3 code/cdp_simulation.py cancel-in-flight-command`
**Expected observation**: a cancellable local coroutine result.
**Key takeaway**: cancellation is normal control flow, not an ignored exception.
**Why it matters**: callers and pools need prompt resource reclamation.

### Example 48: Recognize Headless Detection Signals

_ex-48 · exercises co-05, co-18_

**Brief explanation**: Measure every boundary crossing with a monotonic clock.
**Code**: `python3 code/cdp_simulation.py record-command-duration`
**Expected observation**: a deterministic trace-shaped response.
**Key takeaway**: timeout and latency are separate signals.
**Why it matters**: p95 latency reveals contention before total failure.

### Example 49: Build a Resilient Fleet Slice

_ex-49 · exercises co-09, co-14_

**Brief explanation**: Network idle is a policy with a precise definition, not a magical browser state.
**Code**: `python3 code/cdp_simulation.py assert-network-idle-policy`
**Expected observation**: one modeled policy check.
**Key takeaway**: document which requests count and the quiet window.
**Why it matters**: long-polling pages may never reach generic network idle.

### Example 50: Capstone Browser Service

_ex-50 · exercises co-21, co-22_

**Brief explanation**: A service must validate a caller's requested origin before it opens a target.
**Code**: `python3 code/cdp_simulation.py validate-authorized-fixture-origin`
**Expected observation**: only `example.test`-shaped work is modeled.
**Key takeaway**: authorization is a service policy, not a caller promise.
**Why it matters**: this is the boundary that makes tool exposure safer.
