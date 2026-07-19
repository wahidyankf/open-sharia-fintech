# 69 · Browser Automation with CDP (By Example, Python — CDP client)

**Mapping row** (frozen [tech-docs §Canonical Mapping Table](../tech-docs.md#canonical-mapping-table)):
N=69 · Phase 3 · Deepening (AI & harness engineering, before the harness cluster) · By Example · Python
(CDP client) · folder weight 790 / learn 169 / drill 269. **NEW (Addition 1)** — a harness tool and the
`remotebrowser` substrate (DN-10).

**Scope note**: driving a real browser programmatically over the **Chrome DevTools Protocol (CDP)** —
the low-level protocol beneath higher-level tools like Puppeteer/Playwright. Launch/attach to Chrome,
speak CDP over a WebSocket, navigate, evaluate JavaScript, capture DOM/screenshots/network, and
intercept requests. Placed just before the harness cluster because an agent that can drive a browser is
a powerful tool; reusable beyond agents. Proof-of-transfer target: `remotebrowser` (browser-fleet
orchestration over CDP), not a subject.

## Why this exists · the big idea

- **The problem before the solution**: the web is the largest interface in the world, and much of it has
  no API. Automating a browser lets you drive that interface programmatically — for testing, scraping,
  and (crucially for the harness cluster) giving an agent hands on a real browser. Doing it at the CDP
  level, not just through a wrapper, means you understand what the wrapper is doing and can build your own.
- **Keep-this-if-you-forget-everything**: a browser is a program you can remote-control over a protocol
  — CDP is a request/response + event stream over a WebSocket, and every high-level browser tool is a
  convenience layer over those same CDP messages.
- **Big ideas touched**: `abstraction-and-its-cost` (Playwright hides CDP; going to the protocol shows
  the machinery and its failure modes), `determinism-vs-emergence` (real browsers are asynchronous and
  flaky — you coordinate events, not linear calls).

## Prerequisites

- **Prior topics**: [N=20 Async Python & FastAPI Services](./20-async-python-and-fastapi-services.md)
  (async I/O, WebSocket-shaped concurrency), [N=21 Networking Essentials](./README.md) (HTTP,
  WebSockets), and [N=4 Just Enough Python](./README.md).
- **Tools & environment**: a macOS/Linux terminal; a headless-capable Chrome/Chromium (pinned); a
  Python CDP/WebSocket client library (pinned CVE-clean at authoring); `pytest`; Neovim/VSCode.
- **Assumed knowledge**: async Python, JSON, the request/response + event model, and the browser DOM at
  a basic level.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (DD-28 convention).

- 2026-07-18 — CDP is a **stable, documented** protocol (domains like `Page`, `Runtime`, `DOM`,
  `Network`, `Target`); the transport is a WebSocket carrying JSON messages + events.
- 2026-07-18 — `[Needs Verification]`: exact CVE-clean versions of Chrome/Chromium and the chosen Python
  CDP client library; the CDP domain surface evolves — pin and re-verify at authoring.
- 2026-07-18 — `[Needs Verification]`: whether to demonstrate raw CDP directly vs a thin client library
  — prefer showing the raw protocol once, then a thin client for the rest, and re-verify the library's
  API.

## Concepts

1. **co-01 · what-cdp-is** — the Chrome DevTools Protocol is the JSON-over-WebSocket interface Chrome
   exposes for inspection and automation.
2. **co-02 · launch-and-attach** — Chrome is launched with a remote-debugging port, or attached to an
   existing instance, exposing a CDP endpoint.
3. **co-03 · websocket-transport** — CDP commands and events flow over a WebSocket as JSON messages with
   ids and method names.
4. **co-04 · cdp-domains** — CDP groups capability into domains (`Page`, `Runtime`, `DOM`, `Network`,
   `Target`, `Input`), each with methods and events.
5. **co-05 · commands-and-responses** — a CDP command carries an id + method + params and receives a
   matching id'd response.
6. **co-06 · events-and-subscriptions** — enabling a domain streams asynchronous events (load fired,
   request sent) the client reacts to.
7. **co-07 · targets-and-sessions** — a browser hosts multiple targets (tabs/pages); a session attaches
   the client to one target.
8. **co-08 · navigation** — `Page.navigate` loads a URL; load/lifecycle events signal readiness.
9. **co-09 · waiting-for-readiness** — automation must wait for the right lifecycle/DOM/network signal,
   not a fixed sleep, to avoid flakiness.
10. **co-10 · evaluate-javascript** — `Runtime.evaluate` runs JS in the page and returns a serialized
    result.
11. **co-11 · dom-inspection** — `DOM`/`Runtime` read the document, query nodes, and extract content.
12. **co-12 · input-simulation** — `Input` dispatches synthetic mouse/keyboard events to interact like a
    user.
13. **co-13 · screenshots-and-pdf** — `Page.captureScreenshot`/`printToPDF` capture rendered output.
14. **co-14 · network-observation** — `Network` events expose requests/responses, timings, and bodies.
15. **co-15 · request-interception** — `Fetch`/`Network` interception modifies, blocks, or mocks
    requests in flight.
16. **co-16 · cookies-and-storage** — reading/setting cookies and storage controls session state.
17. **co-17 · headless-vs-headful** — headless runs without a visible window; headful aids debugging;
    behavior can differ subtly.
18. **co-18 · error-and-timeout-handling** — navigations and evaluations fail or hang; robust automation
    bounds them with timeouts and retries.
19. **co-19 · concurrency-and-pooling** — many pages/targets can be driven concurrently; a pool bounds
    resource use (the `remotebrowser` shape).
20. **co-20 · cdp-vs-higher-level-tools** — Playwright/Puppeteer wrap CDP; knowing the protocol explains
    their behavior and limits.
21. **co-21 · automation-ethics-and-robots** — respecting `robots.txt`, rate limits, and terms of
    service is part of responsible automation.
22. **co-22 · exposing-automation-as-a-service** — wrapping browser control behind an API/MCP server
    (the `remotebrowser` pattern) lets other programs — including agents — drive it.

## Tensions & trade-offs — when NOT to reach for this

- **Raw CDP vs a wrapper**: raw CDP is maximally powerful and maximally verbose; Playwright/Puppeteer
  are faster to build with but hide behavior you may need. Learn CDP to understand and to build
  infrastructure; reach for a wrapper for ordinary app-level automation.
- **Automation vs an API**: if a site offers an API, use it — browser automation is slower, flakier, and
  more brittle than a real contract. Automate the browser only when there is no better interface.
- **When NOT to automate**: scraping behind auth or against terms of service, or hammering a site
  without rate limits, is both fragile and unethical — respect `robots.txt` and rate limits.

## Lineage — why it beat the alternative

- Browser automation evolved from brittle screen-scraping and Selenium/WebDriver toward CDP-based tools
  because CDP gives direct, low-latency access to the same machinery Chrome's own DevTools use — precise
  events, network interception, and JS evaluation — instead of a lowest-common-denominator abstraction.
  Understanding CDP is what lets you build a browser-fleet service like `remotebrowser` and expose it to
  agents over MCP. This module feeds [N=71 Agent Tools & MCP](./71-agent-tools-and-mcp.md) (exposing the
  browser as a tool) and the [coding-agent capstone](./74c-capstone-build-your-own-coding-agent.md)'s
  optional browser-driving bonus.

## Worked examples

Colocated under `browser-automation-with-cdp/learning/code/`. Each drives a real (headless) Chrome over
CDP from Python and asserts an observable result. Contiguous `ex-01..ex-50`. Every example cites the
`co-NN` it exercises.

> **Volume-target floor**: this syllabus lists **50** of the required **≥75** (the 75–85 By-Example/
> Primer band, floor not cap — see
> [prd.md §Volume-target bands](../prd.md#volume-target-bands-inherited-from-sibling-dd-34-floor-not-cap-dd-8)).
> The maker adds **≥25** more `ex-NN` entries at authoring time, continuing the numbering and pattern
> taxonomy below, before this topic passes its by-example quality gate.

### Beginner (ex 01–16)

1. **ex-01 · launch-chrome-debug-port** — launch headless Chrome with a remote-debugging port — verify
   the CDP HTTP endpoint lists a target. (co-02)
2. **ex-02 · connect-websocket** — open the CDP WebSocket to a target — verify the socket connects.
   (co-03, co-07)
3. **ex-03 · first-command** — send `Browser.getVersion` and read the response — verify the id matches.
   (co-05)
4. **ex-04 · enable-a-domain** — enable `Page` and subscribe to events — verify events arrive. (co-04,
   co-06)
5. **ex-05 · navigate-a-url** — `Page.navigate` to a page — verify a load lifecycle event fires. (co-08)
6. **ex-06 · wait-for-load** — await the load event, not a fixed sleep — verify readiness before
   proceeding. (co-09)
7. **ex-07 · evaluate-title** — `Runtime.evaluate` `document.title` — verify the returned title. (co-10)
8. **ex-08 · evaluate-expression** — evaluate an arithmetic expression in the page — verify the result.
   (co-10)
9. **ex-09 · read-text-content** — extract an element's text via evaluate — verify the content. (co-11)
10. **ex-10 · query-nodes** — query the DOM for matching nodes — verify the count. (co-11)
11. **ex-11 · screenshot** — `Page.captureScreenshot` to a file — verify a PNG is produced. (co-13)
12. **ex-12 · pdf-print** — `Page.printToPDF` a page — verify a PDF is produced. (co-13)
13. **ex-13 · type-into-input** — dispatch keyboard input into a field — verify the value changed.
    (co-12)
14. **ex-14 · click-a-button** — dispatch a mouse click — verify the resulting DOM change. (co-12)
15. **ex-15 · read-cookies** — read the page's cookies — verify a known cookie appears. (co-16)
16. **ex-16 · headless-vs-headful** — run the same script headless and headful — verify both reach the
    same result. (co-17)

### Intermediate (ex 17–34)

1. **ex-17 · raw-cdp-vs-client** — perform one navigation with raw JSON messages, then with a thin
   client — verify identical results. (co-20, co-03)
2. **ex-18 · lifecycle-events** — subscribe to page lifecycle events and log the sequence — verify the
   expected order. (co-06, co-09)
3. **ex-19 · wait-for-selector** — poll the DOM until a selector appears (event-driven) — verify no
   fixed sleep is used. (co-09, co-11)
4. **ex-20 · fill-and-submit-form** — fill a form and submit it via input events — verify the
   navigation/result. (co-12, co-08)
5. **ex-21 · network-request-log** — enable `Network` and log all requests for a page — verify the
   resource list. (co-14)
6. **ex-22 · capture-response-body** — capture a specific XHR/fetch response body — verify its content.
   (co-14)
7. **ex-23 · block-a-request** — intercept and block image requests — verify they never load. (co-15)
8. **ex-24 · mock-a-response** — intercept a request and return a canned response — verify the page
   renders the mock. (co-15)
9. **ex-25 · set-a-cookie** — set a cookie before navigation to simulate a session — verify the page
   sees it. (co-16)
10. **ex-26 · multiple-tabs** — open two targets and drive both — verify independent state. (co-07,
    co-19)
11. **ex-27 · navigation-timeout** — bound a navigation with a timeout and handle the hang — verify a
    slow page is cut off. (co-18)
12. **ex-28 · retry-flaky-step** — retry a flaky evaluate with backoff — verify eventual success or a
    clean failure. (co-18)
13. **ex-29 · scroll-and-lazy-load** — scroll to trigger lazy content, then read it — verify the loaded
    content. (co-12, co-09)
14. **ex-30 · extract-structured-data** — extract a table into structured JSON via evaluate — verify the
    parsed rows. (co-10, co-11)
15. **ex-31 · full-page-screenshot** — capture a full-page (not just viewport) screenshot — verify the
    height. (co-13)
16. **ex-32 · emulate-device** — set a mobile viewport/user-agent and reload — verify responsive
    rendering. (co-04, co-12)
17. **ex-33 · intercept-and-modify-headers** — add a header to outgoing requests via interception —
    verify it reaches the server. (co-15, co-14)
18. **ex-34 · respect-robots** — check `robots.txt` + apply a rate limit before scraping — verify the
    limiter throttles. (co-21)

### Advanced (ex 35–50)

1. **ex-35 · concurrent-page-pool** — a bounded pool driving N pages concurrently — verify the
   concurrency cap holds. (co-19)
2. **ex-36 · reuse-browser-across-tasks** — reuse one browser instance across many tasks — verify no
   per-task relaunch. (co-19, co-02)
3. **ex-37 · authenticated-session-reuse** — log in once, persist cookies, reuse the session across
   pages — verify no re-login. (co-16, co-07)
4. **ex-38 · network-throttling** — emulate slow network via CDP and observe timings — verify the
   slowdown. (co-14, co-04)
5. **ex-39 · capture-har** — record a HAR-like network trace for a page load — verify entries. (co-14)
6. **ex-40 · js-injection-instrumentation** — inject an instrumentation script on every new document —
   verify it runs before page scripts. (co-10, co-06)
7. **ex-41 · robust-scraper** — a scraper with waits, retries, timeouts, and rate limiting — verify it
   survives a flaky target. (co-09, co-18, co-21)
8. **ex-42 · screenshot-diff-test** — capture + compare screenshots across runs — verify a visual
   regression is detected. (co-13)
9. **ex-43 · drive-a-spa** — automate a client-rendered SPA with event-driven waits — verify a
   multi-step flow. (co-09, co-12)
10. **ex-44 · error-recovery-flow** — recover from a crashed target by reattaching — verify the task
    resumes. (co-07, co-18)
11. **ex-45 · expose-as-http-service** — wrap browser control behind a small async API (a `remotebrowser`
    slice) — verify a client can request a navigation + screenshot. (co-22, co-19)
12. **ex-46 · pooled-service-under-load** — the service above under concurrent clients with a bounded
    pool — verify no resource exhaustion. (co-19, co-22)
13. **ex-47 · compare-with-playwright** — do one task via raw CDP and via a high-level tool, comparing
    code + behavior — verify the results match and note the differences. (co-20)
14. **ex-48 · headless-detection-awareness** — observe how a page can detect headless + discuss ethical
    limits — verify the detection signal. (co-17, co-21)
15. **ex-49 · resilient-fleet-slice** — a small fleet slice: a pool, health checks, and per-task
    timeouts — verify a stuck task is reclaimed. (co-18, co-19)
16. **ex-50 · capstone-browser-service** — a pooled, event-driven browser-automation service exposing
    navigate/evaluate/screenshot/intercept over an API, with waits/timeouts/rate-limits — verify a
    client drives a multi-step authenticated flow end to end. (co-01–co-22)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small **browser-automation service** — a bounded pool of CDP-driven Chrome targets
  exposed behind an async API offering navigate, evaluate, screenshot, and request-interception, with
  event-driven waits, timeouts, retries, and rate limiting — a `remotebrowser`-shaped slice.
- **Concepts exercised**: [ ] launch/attach + WebSocket transport (co-02, co-03) [ ] domains + commands
  - events (co-04–co-06) [ ] navigation + readiness waits (co-08, co-09) [ ] evaluate + DOM + input
    (co-10–co-12) [ ] network observation + interception (co-14, co-15) [ ] timeouts/retries + concurrency
    pool (co-18, co-19) [ ] exposed as a service (co-22).
- **Ordered steps**:
  1. `browser-automation-with-cdp/learning/capstone/code/` — a CDP client + a bounded page pool. Verify
     it drives two pages concurrently.
  2. Add navigate/evaluate/screenshot/intercept operations with event-driven waits + timeouts. Verify a
     multi-step flow with no fixed sleeps.
  3. Expose the operations behind a small async API. Verify a client requests a navigation + screenshot
     and gets a result.
  4. Add rate limiting + retries + a health check. Verify a stuck task is reclaimed and the limiter
     throttles.
- **Acceptance criteria**: a client drives a multi-step (optionally authenticated) browser flow through
  the service, receiving screenshots/extracted data; the pool bounds concurrency; stuck tasks time out
  and are reclaimed; scraping respects rate limits.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

- **Chrome DevTools Protocol documentation** — the authoritative reference for CDP domains, commands,
  and events (pin the domain surface at authoring).
- **Puppeteer / Playwright documentation** — the high-level tools that wrap CDP; useful to compare
  against the raw protocol.

---

← Previous: N=68 `agentic-ai` ([index](./README.md)) · Next:
[N=70 · The Agent Loop](./70-the-agent-loop.md) →
