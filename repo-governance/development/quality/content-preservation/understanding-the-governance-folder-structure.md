---
description: "How the repo-governance/ folder structure maps to offload targets."
when_to_use: "Use when orienting to where a governance document type lives."
---

# Understanding the Governance Folder Structure

**repo-governance/** contains two main subfolders for offloading content:

## 1. conventions/

- **Focus:** Content creation and formatting standards
- **Examples:**
  - `structure/file-naming.md` (how to name files)
  - `formatting/diagrams.md` (how to create diagrams)
  - `writing/quality.md` (how to ensure content quality)
- **When to use:** "How should we write/format this?"

## 2. development/

- **Focus:** Development processes and team workflows
- **Examples:**
  - `agents/ai-agents.md` (how to create agents)
  - `workflow/commit-messages.md` (how to write commits)
  - `workflow/trunk-based-development.md` (how to manage git workflow)
  - `quality/testing-strategy.md` (how to test code)
- **When to use:** "How should we do/manage this?"

**Both are valid offload destinations. Choose based on content nature:**

- Content/format standards → conventions/
- Process/workflow standards → development/
