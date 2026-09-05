---
title: "AI Agent Model Selection Convention"
description: "Standards for selecting the appropriate model tier (planning-grade, execution-grade, fast) for AI agents based on task complexity"
when_to_use: "Read this index to find the right AI Agent Model Selection Convention child document."
---

# AI Agent Model Selection Convention

- [Principles Implemented/Respected](./principles-implemented-respected.md) — Lists the core repository principles this convention implements and respects. Use when checking which principles justify a model-tier choice.
- [Conventions Implemented/Respected](./conventions-implemented-respected.md) — Lists the related repository conventions this convention implements and respects. Use when checking which sibling conventions govern model selection.
- [Purpose](./purpose.md) — States why this convention defines model-tier standards for agents. Use when explaining why an agent must declare a specific model tier.
- [Scope](./scope.md) — Defines what this convention covers and does not cover regarding model selection. Use when checking whether a model-selection question is in scope for this convention.
- [Model Tiers — Planning-Grade (Inherit / No Model Specified)](./model-tiers-planning-grade.md) — Defines the planning-grade tier: when to omit the model field for budget-adaptive inheritance. Use when deciding whether a new agent should omit its model field for planning-grade, budget-adaptive behaviour.
- [Model Tiers — Execution-Grade](./model-tiers-execution-grade.md) — Defines the execution-grade tier: agents that declare sonnet for structured, execution-heavy work. Use when deciding whether a new agent should declare the execution-grade (sonnet) model tier.
- [Model Tiers — Fast](./model-tiers-fast.md) — Defines the fast tier: agents that declare haiku for simple, high-volume, low-reasoning work. Use when deciding whether a new agent should declare the fast (haiku) model tier.
- [Model Selection Decision Tree](./model-selection-decision-tree.md) — Gives the decision tree for walking from a task's characteristics to the correct model tier. Use when unsure which model tier a new agent should declare.
- [Justification Requirement](./justification-requirement.md) — States the requirement that every agent include a Model Selection Justification block explaining its tier choice. Use when writing or reviewing an agent's Model Selection Justification block.
- [Tier Comparison Summary](./tier-comparison-summary.md) — Summarizes the three model tiers in one comparison table. Use when you need a quick side-by-side comparison of the three model tiers.
- [Common Mistakes](./common-mistakes.md) — Lists common mistakes made when selecting a model tier for an agent. Use when reviewing an agent's model-tier choice for a common mistake.
- [Current Model Versions (April 2026)](./current-model-versions.md) — States the current model versions in use as of April 2026. Use when you need the current concrete model version string for a tier.
- [Platform Binding Examples](./platform-binding-examples.md) — Covers the per-harness model-ID mapping tables, tier collapse, and why glm-5.2 is the default on one secondary harness. Use when translating a model tier to a concrete model ID for a specific harness.
- [Special Considerations — Borderline Cases and Tier Assignments](./special-considerations-borderline-and-tier-cases.md) — Covers borderline tier cases and why link checkers, the social media maker, structured makers, the E2E test developer, and the file manager sit at their assigned tiers. Use when an agent's task profile does not cleanly match one model tier, or when checking why a specific existing agent was assigned its tier.
- [Special Considerations — Link Fixer as Fast-Tier](./special-considerations-link-fixer.md) — Explains why the link-fixer agent is assigned the fast tier. Use when checking why link-fixer or a similar mechanical-fix agent should be fast-tier.
- [Tools and Automation](./tools-and-automation.md) — Lists the tools and automation available for checking model-tier compliance. Use when looking for a tool to validate an agent's model-tier declaration.
- [References](./references.md) — Links to related conventions and documents referenced by the model-selection convention. Use when looking for further reading on model selection.
