---
title: "PR-Review Quality Gate — Pipeline Diagrams"
description: "The two Mermaid diagrams for this workflow: the Participants flowchart (scout to fan-out to coordinator to fixer to CI) and the Loop Algorithm sequence diagram for one cycle."
when_to_use: "Use when you need the visual pipeline shape rather than the prose description — e.g. onboarding someone to the review pipeline's actor flow."
---

# Pipeline Diagrams

## Participants Flowchart

```mermaid
%% Color palette: Gold #ECE133 (scout), Blue #0173B2 (specialists), Purple #CC78BC (coordinator), Orange #DE8F05 (fixer), Teal #029E73 (CI gate)
flowchart LR
  SC["pr-review-scout-maker"]:::gold
  subgraph FANOUT["up to 9 concurrent specialists<br/>(DD-10 content-type filter may skip up to 2)"]
    A["pr-review-architecture-maker"]:::blue
    L["pr-review-logic-maker"]:::blue
    G["pr-review-governance-maker"]:::blue
    S["pr-review-security-maker"]:::blue
    I["pr-review-integrity-maker"]:::blue
    P["pr-review-performance-maker"]:::blue
    D["pr-review-docs-maker"]:::blue
    N["pr-review-instruction-maker"]:::blue
    T["pr-review-types-maker"]:::blue
  end
  SC -->|"route-selected specialist set"| FANOUT
  SC -.->|"context_brief + probe<br/>(class, prior-use)"| SY
  A --> SY
  L --> SY
  G --> SY
  S --> SY
  I --> SY
  P --> SY
  N --> SY
  T --> SY
  D --> SY["pr-review-synthesis-maker<br/>(coordinator)"]:::purple
  SY -->|"ONE consolidated<br/>review, Reviews API"| FX["pr-review-fixer"]:::orange
  FX --> CI["CI-green gate<br/>(hard, per cycle)"]:::teal

  classDef gold fill:#ECE133,stroke:#000000,color:#000000
  classDef blue fill:#0173B2,stroke:#000000,color:#FFFFFF
  classDef purple fill:#CC78BC,stroke:#000000,color:#000000
  classDef orange fill:#DE8F05,stroke:#000000,color:#000000
  classDef teal fill:#029E73,stroke:#000000,color:#FFFFFF
```

## Loop Sequence Diagram (One Cycle)

```mermaid
sequenceDiagram
  participant O as Orchestrator (this workflow)
  participant SC as pr-review-scout-maker
  participant SP as up to 9 specialist-makers<br/>(DD-10 may skip up to 2)
  participant SY as pr-review-synthesis-maker
  participant GH as GitHub PR Reviews API
  participant F as pr-review-fixer
  participant CI as CI on PR

  O->>GH: rehydrate cycle history and ceiling state
  GH-->>O: reviews, dispositions, probes, checkpoints, threads
  O->>SC: cycle number N of {total}
  SC->>SC: pin head, select route/set, build context, choose probe class and prior-use state
  SC->>SP: fan out specialists (context brief + probe fields)
  SC->>SY: hand context brief + probe class/prior-use directly
  SP-->>SY: raw findings per discipline
  SY->>SY: dedup + re-categorize + reasonableness-filter + tool-verify
  SY->>GH: require live head equals scout pin
  SY->>GH: post ONE consolidated review (line-anchored)
  GH->>F: unresolved review threads
  F->>GH: require live head equals scout pin
  F->>F: 4-way triage per comment
  F->>GH: push fixes, reply, resolve
  F->>CI: trigger checks
  CI-->>O: GREEN for exact expected head
  O->>GH: require live expected head; clean only if still scout pin
```
