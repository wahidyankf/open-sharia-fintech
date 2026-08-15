---
title: "Beginner Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 10
---

Examples 1-25 establish CDP's JSON command/event model before a real browser is introduced. Each run
uses the annotated, standard-library-only local simulation at `learning/code/cdp_simulation.py`; replace
only that simulator with an authorized local CDP adapter after you can explain every boundary.

### Example 1: Launch Chrome with a Debug Port

_ex-01 · exercises co-02_

**Brief explanation**: A browser exposes CDP only after an explicit remote-debugging endpoint is enabled.
**Code**: `python3 code/cdp_simulation.py launch-chrome-debug-port`
**Expected observation**: JSON reports the scenario and `safe: true`.
**Key takeaway**: launching and attaching are separate responsibilities.
**Why it matters**: an explicit endpoint avoids accidentally automating a user's everyday browser profile.

### Example 2: Connect a WebSocket

_ex-02 · exercises co-03, co-07_

**Brief explanation**: A client attaches to one target over a message transport.
**Code**: `python3 code/cdp_simulation.py connect-websocket`
**Expected observation**: the response correlates to id `1`.
**Key takeaway**: the transport carries both replies and unsolicited events.
**Why it matters**: clients must demultiplex rather than assume one reply per read.

### Example 3: Send a First Command

_ex-03 · exercises co-05_

**Brief explanation**: A command has an id, method, and optional parameters.
**Code**: `python3 code/cdp_simulation.py first-command`
**Expected observation**: the simulated response retains id `1`.
**Key takeaway**: match a response by id, never by arrival order.
**Why it matters**: concurrent commands make arrival order nondeterministic.

### Example 4: Enable a Domain

_ex-04 · exercises co-04, co-06_

**Brief explanation**: CDP groups capability and event subscriptions into domains such as `Page`.
**Code**: `python3 code/cdp_simulation.py enable-a-domain`
**Expected observation**: an acknowledged, local command response.
**Key takeaway**: enable the producer before waiting for its events.
**Why it matters**: otherwise an event can be missed before the client observes it.

### Example 5: Navigate a URL

_ex-05 · exercises co-08_

**Brief explanation**: `Page.navigate` initiates work; it is not a readiness guarantee.
**Code**: `python3 code/cdp_simulation.py navigate-a-url`
**Expected observation**: a deterministic navigation scenario result.
**Key takeaway**: navigate first, then wait for a stated signal.
**Why it matters**: treating command acknowledgement as page completion causes flakes.

### Example 6: Wait for Load

_ex-06 · exercises co-09_

**Brief explanation**: Readiness belongs to an event or observable condition, never a guessed delay.
**Code**: `python3 code/cdp_simulation.py wait-for-load`
**Expected observation**: the coroutine yields and resumes without a blocking sleep.
**Key takeaway**: define readiness before writing automation.
**Why it matters**: the correct signal changes with the user-visible requirement.

### Example 7: Evaluate a Title

_ex-07 · exercises co-10_

**Brief explanation**: `Runtime.evaluate` returns a serialized value from a page execution context.
**Code**: `python3 code/cdp_simulation.py evaluate-title`
**Expected observation**: a response-shaped value, not a live JavaScript object.
**Key takeaway**: evaluation crosses a serialization boundary.
**Why it matters**: return small data rather than leaking page handles into callers.

### Example 8: Evaluate an Expression

_ex-08 · exercises co-10_

**Brief explanation**: A pure expression is the smallest safe evaluation experiment.
**Code**: `python3 code/cdp_simulation.py evaluate-expression`
**Expected observation**: a correlated result with no external effect.
**Key takeaway**: use evaluation deliberately and keep inputs controlled.
**Why it matters**: arbitrary page-side code is a high-authority action.

### Example 9: Read Text Content

_ex-09 · exercises co-11_

**Brief explanation**: Extract only the text needed for the next decision.
**Code**: `python3 code/cdp_simulation.py read-text-content`
**Expected observation**: one local extraction scenario completes.
**Key takeaway**: DOM reads should have an explicit selector and expected shape.
**Why it matters**: broad page dumps are brittle and can expose unnecessary data.

### Example 10: Query Nodes

_ex-10 · exercises co-11_

**Brief explanation**: Querying returns a collection whose cardinality is an assertion opportunity.
**Code**: `python3 code/cdp_simulation.py query-nodes`
**Expected observation**: a deterministic success result.
**Key takeaway**: assert a useful count or identity, not merely that a command returned.
**Why it matters**: selectors can keep matching while the page behavior regresses.

### Example 11: Capture a Screenshot

_ex-11 · exercises co-13_

**Brief explanation**: Screenshot bytes are an artifact; they need a named storage and comparison policy.
**Code**: `python3 code/cdp_simulation.py screenshot`
**Expected observation**: the safe simulator reports completion instead of writing a file.
**Key takeaway**: capture is distinct from artifact retention.
**Why it matters**: uncontrolled image output can exhaust storage or leak page content.

### Example 12: Print a PDF

_ex-12 · exercises co-13_

**Brief explanation**: PDF generation is another rendered-output command with different layout limits.
**Code**: `python3 code/cdp_simulation.py pdf-print`
**Expected observation**: local response JSON.
**Key takeaway**: rendered artifacts require explicit validation criteria.
**Why it matters**: a successful command does not prove that pagination is correct.

### Example 13: Type into an Input

_ex-13 · exercises co-12_

**Brief explanation**: Input dispatch changes user-visible state and therefore needs a before/after check.
**Code**: `python3 code/cdp_simulation.py type-into-input`
**Expected observation**: a side-effect-free modeled input action.
**Key takeaway**: verify the resulting field value, not just the dispatched key.
**Why it matters**: focus and client-side validation can make input disappear.

### Example 14: Click a Button

_ex-14 · exercises co-12_

**Brief explanation**: A click is coordinates or a target-relative interaction plus an expected outcome.
**Code**: `python3 code/cdp_simulation.py click-a-button`
**Expected observation**: a deterministic simulated click result.
**Key takeaway**: interact through a stable, authorized fixture and assert the DOM change.
**Why it matters**: coordinate-only automation breaks with viewport and layout changes.

### Example 15: Read Cookies

_ex-15 · exercises co-16_

**Brief explanation**: Cookies are sensitive session state and must be scoped narrowly.
**Code**: `python3 code/cdp_simulation.py read-cookies`
**Expected observation**: the scenario completes without handling a real credential.
**Key takeaway**: inspect only a known fixture cookie and redact values in logs.
**Why it matters**: browser cookies can grant account access.

### Example 16: Compare Headless and Headful

_ex-16 · exercises co-17_

**Brief explanation**: Rendering mode can expose different timing and graphics behavior.
**Code**: `python3 code/cdp_simulation.py headless-vs-headful`
**Expected observation**: both modeled modes produce the same contract result.
**Key takeaway**: compare behavior, not a claim that both modes are identical.
**Why it matters**: a visible browser remains valuable for diagnosing fixture failures.

### Example 17: Raw CDP vs. a Thin Client

_ex-17 · exercises co-02, co-05_

**Brief explanation**: Raw CDP makes the command envelope explicit; a thin client should preserve the
same method-and-parameter contract while hiding serialization details.
**Code**: `python3 code/ex-17-raw-cdp-vs-client/example.py`
**Expected observation**: the raw `Page.navigate` command and thin-client tuple describe the same URL.
**Key takeaway**: choose a wrapper for ergonomics, but keep the underlying CDP contract legible.
**Why it matters**: when a wrapper fails, protocol literacy reveals whether the defect is in its
translation or in the browser interaction itself.

### Example 18: Log Lifecycle Events

_ex-18 · exercises co-03, co-05_

**Brief explanation**: Lifecycle events provide evidence for readiness: DOM content is available before
the later full-load event in this local fixture.
**Code**: `python3 code/ex-18-lifecycle-events/example.py`
**Expected observation**: `Page.domContentEventFired` appears before `Page.loadEventFired`.
**Key takeaway**: select the weakest event that proves the next step is safe to run.
**Why it matters**: a full-load wait can be slower or never finish when unrelated page resources remain
active.

### Example 19: Wait for a Selector

_ex-19 · exercises co-05, co-06_

**Brief explanation**: Selector presence is a concrete, event-driven readiness condition; it replaces a
fixed sleep with an observable DOM predicate.
**Code**: `python3 code/ex-19-wait-for-selector/example.py`
**Expected observation**: the fixture advances from an empty snapshot to one containing `#ready`.
**Key takeaway**: make the selector and deadline part of the automation contract.
**Why it matters**: a timing guess either flakes on slow runs or wastes time on fast ones.

### Example 20: Fill and Submit a Form

_ex-20 · exercises co-07_

**Brief explanation**: A form flow is complete only when the typed field produces the expected
post-submit state, not when an input event has merely been dispatched.
**Code**: `python3 code/ex-20-fill-and-submit-form/example.py`
**Expected observation**: the local email fixture is present and the form becomes submitted.
**Key takeaway**: assert the visible state before and after a user action.
**Why it matters**: focus, validation, and client-side handlers can accept a click without advancing the
workflow.

### Example 21: Log Network Requests

_ex-21 · exercises co-07_

**Brief explanation**: Network observation records the minimum metadata needed to explain a page load
without retaining live response bodies or credentials.
**Code**: `python3 code/ex-21-network-request-log/example.py`
**Expected observation**: the local trace contains one `GET` request with status `200`.
**Key takeaway**: log method, status, and authorized URL metadata before considering body capture.
**Why it matters**: raw network traces can unintentionally retain personal data and tokens.

### Example 22: Capture a Response Body

_ex-22 · exercises co-06, co-09_

**Brief explanation**: Response-body capture needs a named fixture, byte limit, and retention policy;
unbounded capture is not ordinary request logging.
**Code**: `python3 code/ex-22-capture-response-body/example.py`
**Expected observation**: the synthetic JSON body stays within the configured 64-byte limit.
**Key takeaway**: capture only authorized, bounded data and validate its size before decoding.
**Why it matters**: response bodies can be large or sensitive even when their request metadata is safe.

### Example 23: Block a Request

_ex-23 · exercises co-04, co-12_

**Brief explanation**: Request interception is a privileged action, so this fixture blocks one exact
image path instead of broadly changing page traffic.
**Code**: `python3 code/ex-23-block-a-request/example.py`
**Expected observation**: only the local `/ads/banner.png` fixture matches the blocking rule.
**Key takeaway**: make interception rules narrow, authorized, and observable.
**Why it matters**: broad blocking can conceal application defects or unexpectedly change behavior.

### Example 24: Mock a Response

_ex-24 · exercises co-21_

**Brief explanation**: A mocked response replaces one authorized dependency with a deterministic local
contract so the page behavior can be asserted without an external service.
**Code**: `python3 code/ex-24-mock-a-response/example.py`
**Expected observation**: the fixture endpoint returns a `200` response containing `hello`.
**Key takeaway**: mock the narrow dependency contract that the test actually needs.
**Why it matters**: deterministic fixtures keep a UI test from inheriting a third party's outages.

### Example 25: Set a Cookie

_ex-25 · exercises co-05, co-06_

**Brief explanation**: A synthetic fixture cookie establishes local session state before navigation,
without using a real credential or persisting it beyond the test context.
**Code**: `python3 code/ex-25-set-a-cookie/example.py`
**Expected observation**: the session cookie can be read at the `fixture.test` origin.
**Key takeaway**: isolate and redact fixture session state; never place production cookies in examples.
**Why it matters**: browser cookies can confer account access and must be treated as sensitive data.
