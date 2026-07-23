---
title: "Artifact: Reconciled C4 Container Diagram — Harborlight Shipment Tracker"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 62
---

> Container diagram reconciled with the prose describing a retry queue -- exercises co-11 and co-12.

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC, Brown #CA9161
%% Corrected container diagram: retry_queue added to match the prose
graph TD
    Worker["Notification Worker"]:::blue
    NotifyGate["NotifyGate<br/>#40;external#41;"]:::brown
    RetryQ["Retry Queue<br/>SQS"]:::orange
    DLQ["Dead-Letter Log<br/>PostgreSQL"]:::teal

    Worker -->|"send fails"| RetryQ
    RetryQ -->|"retry, up to 3x"| Worker
    Worker -->|"send succeeds"| NotifyGate
    RetryQ -->|"exhausted retries"| DLQ

    classDef blue fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef orange fill:#DE8F05,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef teal fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef brown fill:#CA9161,stroke:#000000,color:#FFFFFF,stroke-width:2px
```

_Diagram: the retry path the prose already described -- a failed send routes to the Retry Queue,
retries up to three times back through the Notification Worker, and exhausted retries land in the
Dead-Letter Log -- now matches the prose exactly._
