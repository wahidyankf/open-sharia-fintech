---
title: "Artifact: Flow Diagram — Shipment Event Processing"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 61
---

> Shipment-event processing flow, diagram replacing a dense paragraph -- exercises co-11.

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73
%% Shipment-event processing flow
graph LR
    Order["Order Service"]:::blue --> API["Shipment API"]:::blue
    API --> DB["Shipment DB"]:::teal
    API --> Bus["Event Bus"]:::orange
    Bus --> Worker["Notification Worker"]:::blue
    Worker --> Notify["NotifyGate"]:::blue
    Notify --> Cust["Customer"]:::blue
    ParcelLink["ParcelLink"]:::blue --> Adapter["Carrier Adapter"]:::blue
    Adapter --> Bus

    classDef blue fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef orange fill:#DE8F05,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef teal fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:2px
```

_Diagram: two flows converge on the Event Bus -- the order-to-notification path (Order Service through
to the Customer) and the carrier-status path (ParcelLink through the Carrier Adapter) -- and both feed
the Notification Worker._
