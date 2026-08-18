---
title: "Step 0 — Prompt Parsing and Repo Exploration"
description: Describes the sequential, exploration-only first step that builds a context summary of the repo before any user interaction begins.
when_to_use: Use when starting plan-establishment and needing to understand what already exists in the repo before grilling the user.
---

# Step 0. Prompt Parsing and Repo Exploration (Sequential)

Before any user interaction, understand the current repo state relative to the prompt.

**Orchestrator action**:

1. Parse the prompt: extract the desired behavior, likely affected areas (governance files,
   agents, workflows, apps, libs), and any explicit constraints
2. Explore the repo:
   - Read relevant `repo-governance/` files (conventions, workflows, development practices that
     overlap with the prompt)
   - Search `plans/in-progress/`, `plans/backlog/`, `plans/done/` for related prior plans
   - `Grep` for existing conventions or code that may already address or conflict with the prompt
   - Read `AGENTS.md` for relevant agent and workflow references
3. Build a context summary: what already exists, what gaps remain, what conflicts with the prompt

**Output**: Repo context loaded. Related prior work and conflicts identified.

**Notes**:

- Purely exploratory — no user interaction in this step
- Thorough exploration reduces grill time in Step 1 (pre-read the repo so you can answer "does X
  already exist?" without asking the user)
