---
title: "Agent File Size Standards — Categorization Reference and When to Condense"
description: "Gives the agent categorization reference table and the criteria for when to condense or split an oversized agent."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when an agent definition file is approaching or over its size limit and you need to decide whether to condense or split it.
---

# Agent File Size Standards — Categorization Reference and When to Condense

## Agent Categorization Reference

Quick categorization for existing agents:

| Tier                 | Agents                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Tier 1: Simple**   | apps-ayokoding-www-deployer, apps-ose-www-deployer, apps-organiclever-app-web-deployer, social-linkedin-post-maker, apps-ayokoding-www-facts-fixer, apps-ayokoding-www-link-fixer, apps-ose-www-content-fixer, repo-workflow-maker, repo-workflow-checker, repo-workflow-fixer, ci-fixer, swe-ui-fixer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Tier 2: Standard** | docs-maker, docs-tutorial-maker, docs-checker, docs-tutorial-checker, docs-file-manager, docs-fixer, docs-tutorial-fixer, docs-software-engineering-separation-fixer, readme-maker, readme-checker, readme-fixer, agent-maker, plan-fixer, apps-ayokoding-www-general-maker, apps-ayokoding-www-general-checker, apps-ayokoding-www-general-fixer, apps-ayokoding-www-by-example-maker, apps-ayokoding-www-by-example-checker, apps-ayokoding-www-by-example-fixer, apps-ayokoding-www-in-the-field-maker, apps-ayokoding-www-in-the-field-checker, apps-ayokoding-www-in-the-field-fixer, apps-ayokoding-www-link-checker, apps-ayokoding-www-facts-checker, apps-ose-www-content-maker, apps-ose-www-content-checker, swe-typescript-dev, swe-golang-dev, swe-e2e-dev, swe-csharp-dev, swe-fsharp-dev, swe-rust-dev, swe-code-checker, specs-maker, specs-checker, specs-fixer, ci-checker, web-researcher, swe-ui-maker, swe-ui-checker |
| **Tier 3: Complex**  | plan-maker, plan-checker, plan-execution-checker, repo-rules-maker, repo-rules-checker, repo-rules-fixer, docs-link-checker, docs-software-engineering-separation-checker                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

## When to Condense or Split Agents

**Warning Signs (approaching limits)**:

- Agent approaching warning threshold for its tier
- Agent has multiple unrelated responsibilities
- Documentation becoming hard to navigate
- Users confused about when to use the agent

**Condensation Strategies**:

1. **Move details to conventions OR development docs (PRIMARY STRATEGY)** - **CRITICAL:** MOVE content to appropriate docs, NOT DELETE.

   **Destinations**:
   - `repo-governance/conventions/` (content/format standards)
   - `repo-governance/development/` (process/workflow standards)

   Create or expand documents with comprehensive details, then replace with brief summary + link. Zero content loss required.

2. **Remove redundant examples** - Keep 1-2 clear examples per pattern
3. **Consolidate similar sections** - Merge related guidelines
4. **Use tables instead of lists** - More compact for comparisons
5. **Remove "nice to have" guidance** - Focus on essential requirements

**When to split an agent**:

- Agent exceeds hard limit for its tier
- Agent has two clearly separable responsibilities
- Agent requires different tool sets for different tasks
- Users would benefit from specialized agents

**Example split scenarios**:

- Agent that both creates and validates → Split into maker + checker
- Agent handling multiple unrelated domains → Split by domain
- Agent with basic + advanced modes → Split by complexity level
