---
description: Mermaid diagrams for point-to-point JMS messaging and Kafka pub/sub progression with partitioning.
when_to_use: Use when building a messaging-pattern progression diagram.
---

# Guide Structure Part 4: Messaging Flow Diagrams

**Example 6a: Messaging - Point-to-Point (JMS Queue)**

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC
graph TD
    A1[Producer 1] -- send message --> A2[Queue<br/>OrderQueue]
    A3[Producer 2] -- send message --> A2
    A2 -- consume once --> A4[Consumer 1]
    A2 -- waits --> A5[Consumer 2]
    A4 -.-> note1[Message deleted<br/>after processing]

    style A1 fill:#0173B2,stroke:#000,color:#fff
    style A2 fill:#0173B2,stroke:#000,color:#fff
    style A3 fill:#0173B2,stroke:#000,color:#fff
    style A4 fill:#0173B2,stroke:#000,color:#fff
    style A5 fill:#0173B2,stroke:#000,color:#fff
    style note1 fill:#CC78BC,stroke:#000,color:#fff
```

**Use case**: Work queue distribution, only one consumer should process each message.

**Example 6b: Messaging - Pub/Sub (Kafka Topic)**

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC
graph TD
    B1[Producer 1] -->|Publish event| B2[Topic<br/>OrderEvents]
    B3[Producer 2] -->|Publish event| B2
    B2 -->|All subscribers receive| B4[Consumer Group 1<br/>Inventory Service]
    B2 -->|All subscribers receive| B5[Consumer Group 2<br/>Email Service]
    B2 -->|All subscribers receive| B6[Consumer Group 3<br/>Analytics Service]

    note1[Messages retained<br/>for 7 days<br/>Multiple consumers get copy]
    B2 -.-> note1

    style B1 fill:#DE8F05,stroke:#000,color:#fff
    style B2 fill:#DE8F05,stroke:#000,color:#fff
    style B3 fill:#DE8F05,stroke:#000,color:#fff
    style B4 fill:#DE8F05,stroke:#000,color:#fff
    style B5 fill:#DE8F05,stroke:#000,color:#fff
    style B6 fill:#DE8F05,stroke:#000,color:#fff
    style note1 fill:#CC78BC,stroke:#000,color:#fff
```

**Use case**: Event broadcasting, multiple services need same events for different purposes.

**Example 6c: Messaging - Production (Kafka Partitions)**

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC
graph TD
    C1[Producer] -- key routing --> C2[Partition 0]
    C1 -- key routing --> C3[Partition 1]
    C2 -- assigned --> C5[Consumer 1]
    C3 -- assigned --> C6[Consumer 2]
    C5 -- part of --> C8[Consumer Group]
    C6 -- part of --> C8
    C2 -.-> note1[Parallel processing<br/>Order within partition]

    style C1 fill:#029E73,stroke:#000,color:#fff
    style C2 fill:#029E73,stroke:#000,color:#fff
    style C3 fill:#029E73,stroke:#000,color:#fff
    style C5 fill:#029E73,stroke:#000,color:#fff
    style C6 fill:#029E73,stroke:#000,color:#fff
    style C8 fill:#029E73,stroke:#000,color:#fff
    style note1 fill:#CC78BC,stroke:#000,color:#fff
```

**Production benefit**: Parallel processing with ordering guarantees within partition, horizontal scalability.
