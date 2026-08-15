---
title: "Operations, learning, and capacity"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 30
---

The reliability loop does not end when the alert clears. Harbor uses a dashboard to orient the
response, assigns clear incident roles, records system conditions without blame, and turns repeated
manual work into maintained automation. Capacity planning brings the loop forward: learn where
saturation begins before a user-visible incident discovers it for you.

## Make response and learning inspectable

| Scenario                           | Decision artifact                                                      | Verification                                            | Concepts     |
| ---------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------- | ------------ |
| ex-37 · golden-signals-dashboard   | Four panels for latency, traffic, errors, and saturation.              | Each panel has unit, window, and owner.                 | co-19        |
| ex-38 · dashboard-slo-panel        | A panel shows objective, observed SLI, and budget remaining.           | A reviewer can tell whether release risk changed.       | co-19, co-05 |
| ex-39 · seeded-incident            | Introduce only fixed synthetic failing events.                         | No external service, user, or credential is touched.    | co-24        |
| ex-40 · incident-detection         | Evaluate the alert against the seeded fixture.                         | The page route is returned for the bad window.          | co-20, co-24 |
| ex-41 · incident-severity-classify | Classify by affected users and duration, not by who is on call.        | The rubric yields the same class for the same evidence. | co-24        |
| ex-42 · incident-command-roles     | Assign incident commander, operations lead, and communications lead.   | Each role has one current responsibility.               | co-25        |
| ex-43 · incident-timeline          | Order observations, decisions, mitigations, and recovery by time.      | Timestamps are chronological and factual.               | co-26        |
| ex-44 · blameless-postmortem       | Explain conditions, defenses, and decisions instead of personal fault. | The document avoids naming a person as the cause.       | co-26        |
| ex-45 · postmortem-action-items    | Give each improvement an owner and due-review date.                    | No action is merely “be more careful.”                  | co-27        |
| ex-46 · postmortem-no-blame        | Replace blame language with system evidence and guard-rail changes.    | The causal explanation remains actionable.              | co-26        |

## Keep operations sustainable

| Scenario                        | Decision artifact                                                                | Verification                                                     | Concepts |
| ------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------- | -------- |
| ex-47 · identify-toil           | Classify a manual report as repetitive, automatable, tactical, and non-enduring. | It satisfies every stated toil criterion.                        | co-28    |
| ex-48 · toil-budget             | Track time spent on qualifying toil each review period.                          | The trend and owner are visible; “50%” is not a universal quota. | co-28    |
| ex-49 · automate-toil           | Replace a reversible daily summary with a checked local generator.               | The manual copy step disappears and output is reviewed.          | co-29    |
| ex-50 · automation-failure-mode | Add input validation and a manual fallback to the generator.                     | Bad input fails closed with an explanation.                      | co-29    |
| ex-51 · capacity-load-test      | Increase fixed synthetic traffic until a defined saturation limit.               | The recorded ceiling identifies the next capacity action.        | co-30    |

## Decision scenario: a busy worker pool with healthy users

Harbor's worker utilization reaches 92% for six minutes. Checkout success remains 99.99%, latency is
under the objective, and error-budget burn is normal. The correct response is a diagnostic ticket:
review queue depth, growth assumptions, and capacity headroom. Paging would train responders to
ignore capacity signals when users are not yet affected; doing nothing would lose a leading signal.
The decision records both truths: saturation matters, and it is not automatically a symptom page.

**Why it matters:** incident command protects cognition under pressure, blamelessness protects the
quality of evidence, and toil reduction protects capacity to improve the system. Automation is a
new production dependency; give it tests, ownership, and a fallback rather than treating it as a
one-time cleanup.

← Previous: [Objectives, budgets, and alerting](./objectives-budgets-and-alerting) · Next:
[Capstone](./capstone/overview) →
