---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: true
weight: 1
---

## Mental model

Distributed systems make local certainty unavailable. A node observes messages late, twice, out of
order, or not at all; it cannot know whether another node is slow or dead. A correct design names
the guarantee it needs, the failure it tolerates, and the mechanism that provides only that guarantee.

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC
flowchart TD
    A["Unreliable messages"]:::blue --> B["Replication choice"]:::orange
    B --> C["Consistency behavior"]:::teal
    C --> D["Failure evidence and recovery"]:::purple

    classDef blue fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef orange fill:#DE8F05,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef teal fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef purple fill:#CC78BC,stroke:#000000,color:#FFFFFF,stroke-width:2px
```

## Example progression

- **Beginner** (Examples 1–26): partial failure, causal clocks, consistency, CAP/PACELC, and
  delivery semantics.
- **Intermediate** (Examples 27–54): replication, quorums, failure detection, replicated state,
  coordination, and leases.
- **Advanced** (Examples 55–85): Raft, Paxos, CRDTs, Byzantine tolerance, sagas, fencing, clock
  uncertainty, and when to use a coordination service.

## Safety boundary

The examples use deterministic, intentionally simplified local models. They illuminate a safety or
liveness property but do not account for storage corruption, kernel scheduling, network partitions
in a real topology, upgrade compatibility, or the operational requirements of a production cluster.

Next: [Beginner Examples](./beginner.md) →
