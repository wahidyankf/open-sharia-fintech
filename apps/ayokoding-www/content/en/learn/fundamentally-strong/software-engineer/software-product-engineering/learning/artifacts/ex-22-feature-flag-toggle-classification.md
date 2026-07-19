---
title: "Artifact: Feature-Flag Toggle Classification — Kestrel Flags"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 62
---

> Five active Kestrel feature flags classified by toggle category -- exercises co-16. Kestrel is a
> fictional product; every quoted number, question, or finding here is an illustrative,
> constructed example, not real data or a real transcript.

| Flag                            | Category   | Expected lifespan                                                                                    |
| ------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------- |
| `new_scheduling_ui`             | Release    | Short-lived -- removed once the new UI reaches 100% rollout with no rollback need.                   |
| `ai_suggestions_ab_test`        | Experiment | Short-lived -- removed once the experiment concludes and a winner ships.                             |
| `disable_sms_provider_failover` | Ops        | Long-lived -- a permanent operational kill switch for the on-call team, never scheduled for removal. |
| `enterprise_sso_enabled`        | Permission | Long-lived -- per-customer entitlement, active for as long as that customer's plan requires it.      |
| `beta_team_messaging`           | Release    | Medium-lived -- removed once every increment reaches general availability.                           |
