---
description: Describes the Agent Delegation (preferred) and Manual Orchestration (fallback) execution modes, the Maker-Checker-Fixer flow diagram, and how the maker/facts-checker agents delegate deep web research.
when_to_use: Use when deciding how to run this quality gate, wanting a visual summary of the flow, or understanding how factual research is delegated.
---

# Execution Mode, Workflow Overview, and Research Delegation

## Execution Mode

**Preferred Mode**: Agent Delegation — invoke `apps-ayokoding-www-by-example-checker` and
`apps-ayokoding-www-by-example-fixer` via the Agent tool with `subagent_type`
(see [Workflow Execution Modes Convention](../../meta/execution-modes.md)).

**Fallback Mode**: Manual Orchestration — execute workflow logic directly using
Read/Write/Edit tools when Agent Delegation is unavailable.

The Agent tool runs delegated agents that persist file changes to the actual filesystem, making it
the preferred approach when these agents exist as defined delegated agent types. Note: this workflow
includes a manual user review step (step 3) — agent delegation applies to the checker and
fixer steps, not the human decision point.

**How to Execute**:

```
User: "Run ayokoding-web by-example quality gate workflow for golang/tutorials/by-example/"
```

The AI will:

1. Invoke `apps-ayokoding-www-by-example-checker` via the Agent tool (validates tutorial, writes audit)
2. User reviews audit report and decides on fixes (manual decision point)
3. Invoke `apps-ayokoding-www-by-example-fixer` via the Agent tool (reads audit, applies fixes, writes fix report)
4. Iterate until EXCELLENT status achieved (zero findings, 75-85 examples, 95% coverage)
5. Show git status with modified files
6. Wait for user commit approval

**Fallback (Manual Mode)**:

```
User: "Run ayokoding-web by-example quality gate workflow for golang/tutorials/by-example/ in manual mode"
```

The AI executes checker and fixer logic directly using Read/Write/Edit tools in the main
context — use this when agent delegation is unavailable.

## Workflow Overview

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'fontSize':'14px'}}}%%
graph TB
    A[Maker: Create/Update Examples] -- maker or manual --> B[Checker: Validate Quality]
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

The `apps-ayokoding-www-by-example-maker` and `apps-ayokoding-www-facts-checker` agents invoked
by this workflow delegate multi-page web research to the
[`web-researcher`](../../../../.claude/agents/web/web-researcher.md) delegated agent when composing or
verifying claims about library versions, API signatures, or best practices requires more than
one or two searches, or more than two fetches. In-context `WebSearch`/`WebFetch` remain available
for single-shot verification against known authoritative URLs. This keeps each agent's context
lean. The delegation is encoded in each agent's prompt — no workflow-level configuration required.
