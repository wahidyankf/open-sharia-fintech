---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

This by-example route has 75 contiguous local, runnable CDP-shaped examples. The first fifty preserve
the settled syllabus sequence; Examples 51-75 add bounded-service, safety, and observability practice.
All use Python's standard library and the local simulator, so direct browser actions are optional
adaptations rather than a requirement.

## Concepts

The route covers launch/attach, WebSocket JSON messages, CDP domains, commands/responses/events,
targets/sessions, navigation/readiness, evaluation/DOM/input, artifacts, network/interception/storage,
headless behavior, errors/timeouts, pooling, wrappers, responsible automation, and service boundaries.

## Course route

### Beginner (Examples 1–25)

Examples 1–16 are launch Chrome with a debug port, connect WebSocket, first command, enable a domain,
navigate a URL, wait for load, evaluate title/expression, read text/query nodes, screenshot/PDF, type,
click, read cookies, and headless vs headful. Examples 17–25 are raw CDP vs client, lifecycle events,
wait for selector, form submit, request log, response body, block/mock request, and set cookie.

### Intermediate (Examples 26–50)

Examples 26–34 are multiple tabs, navigation timeout, retry, lazy load, structured extraction,
full-page screenshot, device emulation, header interception, and robots/rate limiting. Examples 35–50
are the pooled, reusable, session-aware, observable, resilient browser-service examples from the settled
source: pool, reuse, authentication fixture, throttle, HAR, instrumentation, scraper, screenshot diff,
SPA, recovery, HTTP service, load, wrapper comparison, headless signals, fleet, and capstone service.

### Advanced (Examples 51–75)

Examples 51–75 add isolated contexts, disposal, admission, correlation, redaction, budgets, idempotent
retry, typed errors, health, reclamation, service planes/schema/rate limits, visual/trace policy,
interception, wrapper and egress policy, resource limits, transcripts, restart, saturation, least
privilege, auditing, and a complete local service flow.

Every heading is directly reachable on its level page: [beginner](./beginner.md),
[intermediate](./intermediate.md), and [advanced](./advanced.md).

## Examples by Level

+### Beginner (Examples 1–25)

- [Example 1: Launch Chrome with a Debug Port](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-1-launch-chrome-with-a-debug-port)
- [Example 2: Connect a WebSocket](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-2-connect-a-websocket)
- [Example 3: Send a First Command](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-3-send-a-first-command)
- [Example 4: Enable a Domain](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-4-enable-a-domain)
- [Example 5: Navigate a URL](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-5-navigate-a-url)
- [Example 6: Wait for Load](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-6-wait-for-load)
- [Example 7: Evaluate a Title](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-7-evaluate-a-title)
- [Example 8: Evaluate an Expression](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-8-evaluate-an-expression)
- [Example 9: Read Text Content](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-9-read-text-content)
- [Example 10: Query Nodes](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-10-query-nodes)
- [Example 11: Capture a Screenshot](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-11-capture-a-screenshot)
- [Example 12: Print a PDF](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-12-print-a-pdf)
- [Example 13: Type into an Input](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-13-type-into-an-input)
- [Example 14: Click a Button](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-14-click-a-button)
- [Example 15: Read Cookies](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-15-read-cookies)
- [Example 16: Compare Headless and Headful](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-16-compare-headless-and-headful)
- [Example 17: Raw CDP vs. a Thin Client](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-17-raw-cdp-vs-a-thin-client)
- [Example 18: Log Lifecycle Events](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-18-log-lifecycle-events)
- [Example 19: Wait for a Selector](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-19-wait-for-a-selector)
- [Example 20: Fill and Submit a Form](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-20-fill-and-submit-a-form)
- [Example 21: Log Network Requests](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-21-log-network-requests)
- [Example 22: Capture a Response Body](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-22-capture-a-response-body)
- [Example 23: Block a Request](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-23-block-a-request)
- [Example 24: Mock a Response](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-24-mock-a-response)
- [Example 25: Set a Cookie](/en/learn/courses/browser-automation-with-cdp/learning/beginner#example-25-set-a-cookie)

### Intermediate (Examples 26–50)

- [Example 26: Drive Multiple Tabs](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-26-drive-multiple-tabs)
- [Example 27: Bound a Navigation Timeout](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-27-bound-a-navigation-timeout)
- [Example 28: Retry a Flaky Step](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-28-retry-a-flaky-step)
- [Example 29: Scroll and Lazy Load](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-29-scroll-and-lazy-load)
- [Example 30: Extract Structured Data](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-30-extract-structured-data)
- [Example 31: Capture a Full-Page Screenshot](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-31-capture-a-full-page-screenshot)
- [Example 32: Emulate a Device](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-32-emulate-a-device)
- [Example 33: Modify Request Headers](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-33-modify-request-headers)
- [Example 34: Respect Robots and Rate Limits](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-34-respect-robots-and-rate-limits)
- [Example 35: Concurrent Page Pool](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-35-concurrent-page-pool)
- [Example 36: Reuse a Browser Across Tasks](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-36-reuse-a-browser-across-tasks)
- [Example 37: Authenticated Session Reuse](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-37-authenticated-session-reuse)
- [Example 38: Network Throttling](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-38-network-throttling)
- [Example 39: Capture a HAR-like Trace](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-39-capture-a-har-like-trace)
- [Example 40: Inject JavaScript Instrumentation](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-40-inject-javascript-instrumentation)
- [Example 41: Build a Robust Scraper](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-41-build-a-robust-scraper)
- [Example 42: Run a Screenshot Diff Test](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-42-run-a-screenshot-diff-test)
- [Example 43: Drive a Single-Page Application](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-43-drive-a-single-page-application)
- [Example 44: Recover from a Crashed Target](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-44-recover-from-a-crashed-target)
- [Example 45: Expose Browser Control as an HTTP Service](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-45-expose-browser-control-as-an-http-service)
- [Example 46: Run a Pooled Service Under Load](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-46-run-a-pooled-service-under-load)
- [Example 47: Compare Raw CDP with Playwright](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-47-compare-raw-cdp-with-playwright)
- [Example 48: Recognize Headless Detection Signals](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-48-recognize-headless-detection-signals)
- [Example 49: Build a Resilient Fleet Slice](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-49-build-a-resilient-fleet-slice)
- [Example 50: Capstone Browser Service](/en/learn/courses/browser-automation-with-cdp/learning/intermediate#example-50-capstone-browser-service)

### Advanced (Examples 51–75)

- [Example 51: Create an Isolated Browser Context](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-51-create-an-isolated-browser-context)
- [Example 52: Dispose a Target on Completion](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-52-dispose-a-target-on-completion)
- [Example 53: Bound Queue Admission](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-53-bound-queue-admission)
- [Example 54: Propagate a Correlation ID](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-54-propagate-a-correlation-id)
- [Example 55: Redact a Network Trace](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-55-redact-a-network-trace)
- [Example 56: Enforce a Screenshot Budget](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-56-enforce-a-screenshot-budget)
- [Example 57: Retry Only Idempotent Navigation](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-57-retry-only-idempotent-navigation)
- [Example 58: Classify a Protocol Error](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-58-classify-a-protocol-error)
- [Example 59: Check Target Health](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-59-check-target-health)
- [Example 60: Reclaim a Stuck Task](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-60-reclaim-a-stuck-task)
- [Example 61: Separate Control and Data Planes](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-61-separate-control-and-data-planes)
- [Example 62: Validate an Operation Schema](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-62-validate-an-operation-schema)
- [Example 63: Apply a Per-Origin Rate Limit](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-63-apply-a-per-origin-rate-limit)
- [Example 64: Produce a Stable Visual Fingerprint](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-64-produce-a-stable-visual-fingerprint)
- [Example 65: Record a HAR Summary](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-65-record-a-har-summary)
- [Example 66: Enforce a Request-Interception Policy](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-66-enforce-a-request-interception-policy)
- [Example 67: Compare a Wrapper Contract](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-67-compare-a-wrapper-contract)
- [Example 68: Enforce an Egress Allowlist](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-68-enforce-an-egress-allowlist)
- [Example 69: Limit Concurrent Screenshots](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-69-limit-concurrent-screenshots)
- [Example 70: Test a Failure Transcript](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-70-test-a-failure-transcript)
- [Example 71: Handle Browser Restart](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-71-handle-browser-restart)
- [Example 72: Measure Pool Saturation](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-72-measure-pool-saturation)
- [Example 73: Design a Least-Privilege Tool](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-73-design-a-least-privilege-tool)
- [Example 74: Audit a Service Request](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-74-audit-a-service-request)
- [Example 75: Verify the Complete Local Service Flow](/en/learn/courses/browser-automation-with-cdp/learning/advanced#example-75-verify-the-complete-local-service-flow)
