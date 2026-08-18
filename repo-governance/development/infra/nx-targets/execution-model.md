---
title: "Execution Model"
description: Explains the mermaid-diagrammed pre-push/PR quality-gate flow and the scheduled/on-demand testing tiers that Nx targets execute.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when tracing how typecheck, lint, and test:quick run at pre-push/PR versus how test:integration and test:e2e run on scheduled CRON.
---

# Execution Model

## Quality Gates (pre-push enforcement)

`typecheck`, `lint`, and `test:quick` run at three identical checkpoints: locally before push, in
the PR gate, and at main merge. `test:quick` is a sequential 5-step composition
(typecheck → lint → test:unit → test:coverage → test:specs) so the specs gate is already
folded in — there is no separate `specs:behavior:coverage` step at pre-push or PR.

**One documented exception — `rhino-cli`**: its `test:quick` is a 4-step composition
(typecheck → lint → test:unit → test:specs). `test:coverage` was lifted out of the local chain
because instrumented rebuilds dominated pre-push wall time, and it now runs in the CI Rust
quality-gate job instead. The `test:coverage` target itself is unchanged and still carries
`--fail-under-lines 90`, so a coverage drop still blocks merge — it blocks at the PR gate rather
than at pre-push. No other project takes this exception.

```mermaid
flowchart TD
    A[Developer pushes code] --> B[Pre-push hook]
    B --> C["typecheck<br/>nx affected -t typecheck"]
    B --> D["lint<br/>nx affected -t lint"]
    C --> E["test:quick<br/>nx affected -t test:quick<br/>(unit+cov+specs)"]
    D --> E
    E --> F{All pass?}
    F -- No --> G[Push blocked]
    F -- Yes --> H[Push succeeds]

    P[PR opened / updated] --> Q["GitHub Actions CI<br/>nx affected -t<br/>typecheck lint test:quick"]
    Q --> R{Pass?}
    R -- No --> S[PR merge blocked]
    R -- Yes --> T[PR merge allowed]

    style A fill:#0173B2,color:#fff
    style B fill:#DE8F05,color:#fff
    style C fill:#029E73,color:#fff
    style D fill:#029E73,color:#fff
    style E fill:#029E73,color:#fff
    style F fill:#DE8F05,color:#fff
    style G fill:#CC78BC,color:#fff
    style H fill:#029E73,color:#fff
    style P fill:#0173B2,color:#fff
    style Q fill:#DE8F05,color:#fff
    style S fill:#CC78BC,color:#fff
    style T fill:#029E73,color:#fff
```

## Scheduled and On-Demand Testing

Deeper tests run outside the pre-push/PR cycle — on a schedule or triggered explicitly.

Scheduled CRON workflows run 5 parallel tracks: lint, typecheck, test:quick (with coverage), specs:behavior:coverage, and integration→e2e (sequential chain).

```mermaid
flowchart TD
    H2["GitHub Actions<br/>e2e-*.yml<br/>cron 2× per day<br/>(WIB 06, 18)"] --> I2["test:integration + test:e2e<br/>per service"]

    J[On demand / CI matrix] --> K[test:unit]
    J --> L[test:integration]
    L --> M[test:e2e]

    style H2 fill:#0173B2,color:#fff
    style I2 fill:#CA9161,color:#fff
    style J fill:#0173B2,color:#fff
    style K fill:#CA9161,color:#fff
    style L fill:#CA9161,color:#fff
    style M fill:#CA9161,color:#fff
```
