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

Pre-push and PR CI execute their registry-declared projections; they are complementary lifecycle
surfaces, not three hardcoded identical checkpoints. Discover each live projection with `gate
list --surface=<surface>`. A successful PR aggregate is evidence for the exact repository, head,
and applicable base it reports; it does not prove a later head.

For behaviour owners, `test:quick` composes typecheck where applicable, lint, Unit runtime, and all
applicable static `test:coverage:*` validators. Dedicated E2E projects omit Unit runtime. Coverage
validators never execute tests; runtime code coverage belongs to its corresponding runtime target.

```mermaid
flowchart TD
    A[Developer pushes code] --> B[Pre-push hook]
    B --> E["affected test:quick<br/>types + lint + Unit + static"]
    E --> F{All pass?}
    F -- No --> G[Push blocked]
    F -- Yes --> H[Push succeeds]

    P[PR opened / updated] --> Q["GitHub Actions CI<br/>nx affected -t test:quick<br/>(bounded project parallelism)"]
    Q --> R{Pass?}
    R -- No --> S[PR merge blocked]
    R -- Yes --> T[PR merge allowed]

    style A fill:#0173B2,color:#fff
    style B fill:#DE8F05,color:#fff
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

Developers run impacted Integration/E2E scenarios manually. Scheduled workflows run full static
coverage, then complete Integration, then complete unfiltered E2E outside the push/PR path.

```mermaid
flowchart TD
    H2["Scheduled/manual quality CI"] --> C2["all applicable<br/>test:coverage:*"]
    C2 --> I2["complete test:integration"]
    I2 --> E2["complete unfiltered test:e2e"]

    J[On demand / CI matrix] --> K[test:unit]
    J --> L[test:integration]
    L --> M[test:e2e]

    style H2 fill:#0173B2,color:#fff
    style C2 fill:#CA9161,color:#fff
    style I2 fill:#CA9161,color:#fff
    style E2 fill:#CA9161,color:#fff
    style J fill:#0173B2,color:#fff
    style K fill:#CA9161,color:#fff
    style L fill:#CA9161,color:#fff
    style M fill:#CA9161,color:#fff
```
