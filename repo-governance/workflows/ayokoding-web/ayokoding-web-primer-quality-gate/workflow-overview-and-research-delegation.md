---
title: "Workflow Overview and Research Delegation"
description: Shows the Maker-Checker-Fixer flow as a Mermaid diagram and documents how the maker/facts-checker agents delegate multi-page web research to the web-researcher agent.
when_to_use: Use when you need a visual summary of the quality-gate flow or want to understand how deep web research is delegated during content creation/verification.
---

# Workflow Overview and Research Delegation

## Workflow Overview

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'fontSize':'14px'}}}%%
graph TB
    A[Maker: Create/Update Examples] -- maker or manual --> B[Checker: Validate Density<br/>+ Scope Discipline]
    B -- checker --> C{User Review}
    C -- Issues found --> D[Fixer: Apply Fixes]
    D -- re-check --> E[Re-validate Quality]
    C -- Quality approved --> F[Publication Ready]
    C -- Major rework needed --> G[Iterate via Maker]

    style A fill:#0173B2,color:#fff
    style B fill:#DE8F05,color:#fff
    style D fill:#029E73,color:#fff
    style F fill:#CC78BC,color:#fff
    style G fill:#CA9161,color:#fff
```

## Research Delegation

The `apps-ayokoding-www-primer-maker` and `apps-ayokoding-www-facts-checker` agents invoked by
this workflow delegate multi-page web research to the
[`web-researcher`](../../../../.claude/agents/web/web-researcher.md) delegated agent when composing or
verifying claims about language versions, tool versions, or CLI syntax requires more than one or
two searches, or more than two fetches. In-context `WebSearch`/`WebFetch` remain available for
single-shot verification against known authoritative URLs. This keeps each agent's context lean.
The delegation is encoded in each agent's prompt — no workflow-level configuration required.
