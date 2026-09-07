---
description: The six-layer diagram and quick-reference table
when_to_use: Use for an at-a-glance view of all six layers.
---

# The Six Layers

```
Layer 0: Vision       WHY WE EXIST       (foundational purpose)
    ↓ inspires
Layer 1: Principles   WHY - Values       (governs L2, L3)
    ↓ governs
Layer 2: Conventions  WHAT - Doc Rules   (governs L3, L4)
    ↓ governs (with L2)
Layer 3: Development  HOW - Practices    (governs L4)
    ↓ governs (implemented by)
Layer 4: AI Agents    WHO - Executors    (atomic tasks)
    ↓ orchestrated by
Layer 5: Workflows    WHEN - Orchestrate (multi-step processes)
```

**Agent skills Infrastructure** (Delivery):

- Inline skills (default): Progressive knowledge injection
- Fork skills (context: fork): Task delegation to isolated agents
- Service relationship: agent skills serve agents, don't govern them

## Quick Reference Table

| Layer | Location                     | Purpose                                                     | Changes?        | Answers?                  |
| ----- | ---------------------------- | ----------------------------------------------------------- | --------------- | ------------------------- |
| **0** | repo-governance/vision/      | WHY we exist                                                | Extremely rare  | Why does project exist?   |
| **1** | repo-governance/principles/  | WHY we value approaches                                     | Rarely          | Why value this approach?  |
| **2** | repo-governance/conventions/ | WHAT documentation rules                                    | Occasionally    | What documentation rules? |
| **3** | repo-governance/development/ | HOW we develop software                                     | More frequently | How develop software?     |
| **4** | `.claude/agents/`            | WHO enforces rules                                          | Often           | Who enforces rules?       |
| **5** | repo-governance/workflows/   | WHEN orchestrate agents, procedures, and/or other workflows | As needed       | When run which steps?     |

**Agent skills**: `.claude/skills/` - Delivery infrastructure serving agents (inline knowledge injection or fork-based delegation)
