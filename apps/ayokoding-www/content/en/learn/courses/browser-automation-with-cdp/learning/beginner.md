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

**Brief explanation**: Version metadata identifies the browser/protocol pair an adapter supports.
**Code**: `python3 code/cdp_simulation.py inspect-version-endpoint`
**Expected observation**: a stable local protocol result.
**Key takeaway**: record versions with failures.
**Why it matters**: CDP domains evolve with Chrome.

### Example 18: Log Lifecycle Events

_ex-18 · exercises co-03, co-05_

**Brief explanation**: One envelope makes command construction testable without transport I/O.
**Code**: `python3 code/cdp_simulation.py create-command-envelope`
**Expected observation**: JSON with id, method, and parameters.
**Key takeaway**: serialize at the transport edge.
**Why it matters**: pure command construction is easy to unit-test.

### Example 19: Wait for a Selector

_ex-19 · exercises co-05, co-06_

**Brief explanation**: Events and replies may arrive in either order.
**Code**: `python3 code/cdp_simulation.py correlate-out-of-order-response`
**Expected observation**: the id invariant still holds.
**Key takeaway**: keep pending futures keyed by command id.
**Why it matters**: arrival-order assumptions fail under concurrent work.

### Example 20: Fill and Submit a Form

_ex-20 · exercises co-07_

**Brief explanation**: A browser can host many pages, workers, and other targets.
**Code**: `python3 code/cdp_simulation.py list-targets`
**Expected observation**: a local target-discovery result.
**Key takeaway**: select target type and ownership deliberately.
**Why it matters**: attaching to the wrong target can automate the wrong page.

### Example 21: Log Network Requests

_ex-21 · exercises co-07_

**Brief explanation**: A session scopes commands to one target attachment.
**Code**: `python3 code/cdp_simulation.py attach-session`
**Expected observation**: one safe attachment scenario.
**Key takeaway**: retain and dispose the session explicitly.
**Why it matters**: leaked sessions confuse event routing and resource cleanup.

### Example 22: Capture a Response Body

_ex-22 · exercises co-06, co-09_

**Brief explanation**: `DOMContentLoaded` can be the right signal before querying static document content.
**Code**: `python3 code/cdp_simulation.py observe-dom-content-loaded`
**Expected observation**: event-shaped completion without timing guesses.
**Key takeaway**: choose the weakest readiness event that proves your precondition.
**Why it matters**: waiting for full load can waste time or hang on unrelated assets.

### Example 23: Block a Request

_ex-23 · exercises co-04, co-12_

**Brief explanation**: Emulation changes the rendering contract before a page is loaded.
**Code**: `python3 code/cdp_simulation.py set-viewport`
**Expected observation**: a deterministic emulation scenario.
**Key takeaway**: pin viewport, scale, and user agent in visual tests.
**Why it matters**: an unspecified viewport makes screenshots incomparable.

### Example 24: Mock a Response

_ex-24 · exercises co-21_

**Brief explanation**: Authorization belongs before navigation and before resource allocation.
**Code**: `python3 code/cdp_simulation.py build-allowlist`
**Expected observation**: only a fixture origin is accepted by the model.
**Key takeaway**: deny unknown origins by default.
**Why it matters**: a browser service has more reach than a normal HTTP client.

### Example 25: Set a Cookie

_ex-25 · exercises co-05, co-06_

**Brief explanation**: A trace ties command ids, methods, durations, and errors together.
**Code**: `python3 code/cdp_simulation.py emit-structured-trace`
**Expected observation**: deterministic JSON suitable for a test assertion.
**Key takeaway**: observability begins at the protocol boundary.
**Why it matters**: a screenshot alone cannot explain a failed automation step.
