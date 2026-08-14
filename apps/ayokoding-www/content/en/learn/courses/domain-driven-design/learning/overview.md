---
title: "Learning Overview"
date: 2026-08-14T00:00:00+07:00
draft: true
weight: 1
---

## How to use these examples

Each example has five parts: a concrete context, a complete annotated Python artifact, observable
output or assertion, a design consequence, and a concise takeaway. Run any artifact with
`python3 example.py` from its directory. The first tier establishes a shared domain vocabulary;
the second protects transactional boundaries; the final tier prevents one context's model from
infecting another.

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC
flowchart LR
    A["Language and value<br/>objects"]:::blue --> B["Aggregates and<br/>events"]:::orange
    B --> C["Contexts and<br/>integration"]:::teal
    C --> D["Capstone:<br/>protected seams"]:::purple
    classDef blue fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef orange fill:#DE8F05,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef teal fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef purple fill:#CC78BC,stroke:#000000,color:#FFFFFF,stroke-width:2px
```

## Concepts

- **Language and model**: ubiquitous language, domain model, entities, value objects, and
  side-effect-free behaviour.
- **Tactical design**: aggregates, roots, consistency boundaries, invariants, small aggregates,
  references by identity, repositories, factories, services, specifications, and application
  services.
- **Strategic design**: bounded contexts, context maps, shared kernels, customer/supplier and
  conformist relationships, subdomains, and ACLs.
- **Event and query patterns**: domain events, event decoupling, CQRS, and event sourcing are
  introduced as bounded tools rather than universal defaults.

Start with [Beginner Examples](./beginner.md).
