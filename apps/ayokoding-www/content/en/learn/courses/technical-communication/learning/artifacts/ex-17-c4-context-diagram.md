---
title: "Artifact: C4 Context Diagram — Harborlight Shipment Tracker"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 57
---

> C4 Level 1 system-context diagram -- exercises co-11 and co-12.

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC, Brown #CA9161
%% C4 Level 1 -- System Context: Harborlight Shipment Tracker
graph TD
    Customer["Customer<br/>#40;person#41;"]:::purple
    Ops["Warehouse Operator<br/>#40;person#41;"]:::purple
    OrderSvc["Order Service<br/>#40;external system#41;"]:::brown
    ParcelLink["ParcelLink API<br/>#40;external carrier system#41;"]:::brown
    NotifyGate["NotifyGate<br/>#40;external SMS#47;email provider#41;"]:::brown
    Tracker["Harborlight Shipment Tracker<br/>#40;this system#41;"]:::blue

    OrderSvc -->|"sends order-placed events"| Tracker
    Ops -->|"updates shipment status"| Tracker
    Tracker -->|"queries carrier status"| ParcelLink
    Tracker -->|"sends notifications via"| NotifyGate
    NotifyGate -->|"delivers SMS#47;email to"| Customer
    Customer -->|"checks status on"| Tracker

    classDef blue fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef purple fill:#CC78BC,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef brown fill:#CA9161,stroke:#000000,color:#FFFFFF,stroke-width:2px
```

_Diagram: two people (Customer, Warehouse Operator) and three external systems (Order Service,
ParcelLink API, NotifyGate) around the one system this diagram is scoped to, Harborlight Shipment
Tracker. No internal container is shown._
