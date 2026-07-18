---
title: "Artifact: Opportunity-Solution Tree — Kestrel No-Show Reduction"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 59
---

> An opportunity-solution tree for reducing no-show shift incidents -- exercises co-05. Kestrel is
> a fictional product; every quoted number, question, or finding here is an illustrative,
> constructed example, not real data or a real transcript.

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC
graph TD
    O["Outcome:<br/>Reduce no-show shift<br/>incidents by 30%"]:::blue
    OP1["Opportunity:<br/>Employees forget<br/>upcoming shifts"]:::orange
    OP2["Opportunity:<br/>Shift swaps get<br/>approved too late"]:::orange
    OP3["Opportunity:<br/>New hires don't understand<br/>the scheduling app"]:::orange
    S1["Solution: SMS#47;push reminders<br/>24h and 2h before shift"]:::teal
    S2["Solution: faster swap-approval<br/>workflow + manager push"]:::teal
    S3["Solution: in-app onboarding<br/>checklist for new employees"]:::teal
    T1["Test: reminder pilot,<br/>measure no-show delta"]:::purple
    T2["Test: A#47;B approval-time<br/>vs no-show rate"]:::purple
    T3["Test: checklist completion<br/>vs no-show correlation"]:::purple

    O --> OP1 --> S1 --> T1
    O --> OP2 --> S2 --> T2
    O --> OP3 --> S3 --> T3

    classDef blue fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef orange fill:#DE8F05,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef teal fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef purple fill:#CC78BC,stroke:#000000,color:#FFFFFF,stroke-width:2px
```

_Diagram: one outcome, three opportunities, one solution and one assumption test per opportunity --
every solution traces upward to exactly one opportunity, and every opportunity traces upward to
the stated outcome._
