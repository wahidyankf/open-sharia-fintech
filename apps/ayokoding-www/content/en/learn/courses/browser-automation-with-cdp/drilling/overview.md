---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

1. What matches a CDP response to its command?
   <details><summary>Answer</summary>The numeric command `id`; events have a `method` but no matching
   request id.</details>
2. Why enable a domain before expecting its events?
   <details><summary>Answer</summary>Enabling declares the subscription and gives the browser permission
   to emit that domain's events to the attached session.</details>
3. What is the difference between a target and a session?
   <details><summary>Answer</summary>A target is a page-like browser entity; a session is a client's
   attachment used to send commands to it.</details>
4. Why is a fixed sleep a poor readiness test?
   <details><summary>Answer</summary>It guesses timing. Wait for the lifecycle, network, or DOM signal
   required by the next step instead.</details>
5. When does a wrapper beat raw CDP?
   <details><summary>Answer</summary>For ordinary product automation, when its higher-level contract
   covers the job. Use raw CDP to understand or implement infrastructure boundaries.</details>
6. What must a pool bound?
   <details><summary>Answer</summary>Concurrent target ownership, not merely the number of incoming
   requests.</details>

## Applied problems

1. A button appears after a client-side fetch. Subscribe to the appropriate event and re-check the
   selector under a deadline; do not add a longer sleep.
2. A screenshot task hangs. Wrap that task in `asyncio.wait_for`, dispose or recycle the target, and
   return a typed timeout result.
3. A caller asks to visit an arbitrary URL. Enforce an allowlist at the service boundary before target
   allocation.
4. A page requests an analytics image. Block only the authorized fixture pattern, log the decision, and
   continue all other requests.
5. Ten callers arrive at a two-target service. Queue or reject deterministically; never create eight
   extra tabs.

## Code katas

1. Replace a `time.sleep` readiness guess with an awaited `load` event.
2. Repair a client that treats the next message as its command response instead of matching `id`.
3. Add a timeout and `finally` cleanup around an attached target.
4. Put an origin allowlist ahead of a navigation command.
5. Limit a fan-out with `asyncio.Semaphore(2)` and assert the observed maximum is two.

## Self-check checklist

- [ ] I can distinguish a command, response, and event on the CDP wire.
- [ ] I can choose a readiness signal instead of a sleep.
- [ ] I can explain why targets need sessions and explicit cleanup.
- [ ] I can preserve authorization, rate-limit, and timeout boundaries in a browser service.
- [ ] I can choose a wrapper when raw CDP is unnecessary.

## Elaborative interrogation and self-explanation

1. Why is an event stream inherently harder to reason about than a linear API call?
2. Which production failure does a bounded pool prevent that a retry loop cannot?
3. Why should request interception be treated as a high-authority action?
