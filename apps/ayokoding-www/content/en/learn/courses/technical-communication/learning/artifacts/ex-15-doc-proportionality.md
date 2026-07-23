---
title: "Artifact: Proportionality Map — Three Decisions"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 55
---

> Artifact-weight choice mapped to three decisions of varying reversibility -- exercises co-16.

| Decision                                                           | Reversibility                                          | Artifact chosen   | Why                                                                                                                             |
| ------------------------------------------------------------------ | ------------------------------------------------------ | ----------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Rename an internal config flag, `retry_max` to `carrier_retry_max` | Trivially reversible; a single grep-and-replace        | Inline PR comment | Low stakes, one file, no cross-team impact -- an RFC would spend review attention nobody needed to spend.                       |
| Add exponential backoff to the Carrier Adapter                     | Reversible, but touches production error-handling      | PR description    | One team, one component, moderate stakes -- co-09's structure gives a reviewer everything needed without a formal review cycle. |
| Adopt Kafka as the shipment event bus                              | Expensive to reverse; new infrastructure, new runbooks | Full RFC + ADR    | High stakes, cross-team (SRE now owns on-call for it), genuinely hard to undo once other services depend on Kafka's replay.     |
