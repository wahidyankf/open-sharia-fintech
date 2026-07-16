---
title: "Artifact: C4 Container Diagram — Harborlight Shipment Tracker"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 58
---

> C4 Level 2 container diagram -- exercises co-12.

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC, Brown #CA9161
%% C4 Level 2 -- Containers inside Harborlight Shipment Tracker
graph TD
    OrderSvc["Order Service<br/>#40;external#41;"]:::brown
    ParcelLink["ParcelLink API<br/>#40;external#41;"]:::brown
    NotifyGate["NotifyGate<br/>#40;external#41;"]:::brown

    API["Shipment API<br/>Python#47;Flask, REST"]:::blue
    Bus["Event Bus<br/>Kafka"]:::orange
    Worker["Notification Worker<br/>Python consumer"]:::blue
    DB["Shipment DB<br/>PostgreSQL"]:::teal
    Adapter["Carrier Adapter<br/>Python, HTTPS#47;REST"]:::blue

    OrderSvc -->|"HTTPS#47;REST, order-placed event"| API
    API -->|"writes shipment record"| DB
    API -->|"publishes shipment-event"| Bus
    Bus -->|"consumes shipment-event"| Worker
    Worker -->|"sends SMS#47;email"| NotifyGate
    Adapter -->|"HTTPS#47;REST, polls#47;webhook"| ParcelLink
    Adapter -->|"writes carrier-status event"| Bus

    classDef blue fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef orange fill:#DE8F05,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef teal fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef brown fill:#CA9161,stroke:#000000,color:#FFFFFF,stroke-width:2px
```

_Diagram: five containers (Shipment API, Event Bus, Notification Worker, Shipment DB, Carrier
Adapter) inside the Shipment Tracker boundary, each labeled with its technology, connected by edges
labeled with protocol and purpose._
