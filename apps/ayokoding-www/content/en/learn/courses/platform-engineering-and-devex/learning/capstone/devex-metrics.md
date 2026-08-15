---
title: "DevEx measurement policy"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 30
---

## Artifact: Harbor platform-learning policy

**Purpose**: learn whether the service-start path and database capability improve safe delivery and
developer experience for the services that use them. This is not an individual performance system.

| Signal family             | Service-context measure                                                                                               | Improvement question                                                                |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| DORA delivery performance | Change lead time, deployment frequency, failed deployment recovery time, change fail rate, and deployment rework rate | Did the supported path remove a delivery constraint without increasing instability? |
| SPACE experience          | Short confidence response, necessary handoffs, and time to a reviewable safe outcome                                  | Where does a developer lose flow or need hidden knowledge?                          |
| Leading signal            | Starter-path completion duration, support-contact theme, and escape-hatch reason                                      | What small change can we test before a lagging outcome shifts?                      |
| Product use               | Adoption and repeat-use trend, interpreted with interviews                                                            | Does the path win on merit for the users it is meant to serve?                      |

## Use and protection rules

| Rule                   | Policy                                                                                                                 |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Unit of interpretation | Service, team, or value stream with its operating context; never an individual engineer.                               |
| Prohibited uses        | No stack ranking, compensation, promotion, discipline, quota, or competitive leaderboard.                              |
| Review cadence         | Platform team and customer representatives review aggregate trends monthly and choose one improvement experiment.      |
| Data minimization      | Collect only information needed for the questions above; aggregate survey responses and protect free-text attribution. |
| Feedback loop          | Publish the selected action, result, and rationale when an action is deferred.                                         |

## Verification

- [ ] Every signal has a service context, a data period or source, and an improvement question.
- [ ] DORA is paired with SPACE or direct customer feedback rather than treated as a complete DevEx score.
- [ ] At least one leading signal can prompt a near-term experiment.
- [ ] The policy explicitly prohibits individual use and gives customers a visible feedback loop.

## Why this artifact matters

The dashboard is not the outcome. Its value is a safer conversation about constraints and a
repeatable way to test whether the platform helps. The policy preserves that value by removing the
incentive to game a number. It aligns with DORA's advice to use delivery metrics in context and to
improve over time rather than compete. [DORA delivery metrics guide](https://dora.dev/guides/dora-metrics/)
