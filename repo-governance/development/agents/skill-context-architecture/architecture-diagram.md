---
title: "Architecture Diagram"
description: "Provides a diagram of the Skill context architecture."
category: explanation
subcategory: development
tags:
  - ai-agents
  - agent-skills
  - architecture
  - development
created: 2025-11-23
when_to_use: Use when you need a visual reference for how Skill context modes relate to each other.
---

# Architecture Diagram

```mermaid
graph TD
    MC[Main Conversation] -->|spawns| SA[Subagent Forked Context]
    MC -->|uses| IS[Inline agent skills<br/>.claude/skills/]
    MC -->|uses| FS[Fork agent skills<br/>project-specific dir]
    SA -->|uses| IS
    SA -->|CANNOT use| FS
    IS -->|references| CONV[Convention Documents<br/>repo-governance/]

    style MC fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
    style SA fill:#CC78BC,stroke:#000000,color:#FFFFFF,stroke-width:2px
    style IS fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:3px
    style FS fill:#DE8F05,stroke:#000000,color:#FFFFFF,stroke-width:2px
    style CONV fill:#CA9161,stroke:#000000,color:#FFFFFF,stroke-width:2px

    linkStyle 4 stroke:#FF0000,stroke-width:3px,stroke-dasharray:5
```

**Key**:

- Blue: Main conversation context
- Purple: Delegated agent (forked) context
- Green: Universal inline skills (works everywhere)
- Orange: Fork skills (main conversation only)
- Brown: Convention documents (governance layer)
- Red dashed: Architectural constraint (cannot do)
