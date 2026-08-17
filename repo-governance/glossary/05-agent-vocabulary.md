---
title: "Agent Vocabulary"
description: Definitions for agent, agent skill, gate, quality gate, and workflow, plus the maker/checker/fixer roles and how they differ.
when_to_use: Use when deciding whether new capability belongs in an agent, an agent skill, a gate, or a workflow.
category: explanation
subcategory: governance
tags:
  - governance
  - glossary
  - agents
  - workflow
created: 2026-08-16
---

# Agent Vocabulary

Five things are routinely confused because all five "run something". They differ by **what holds
the knowledge** and **who decides when it runs**.

| Term             | What it is                                                      | Who triggers it            |
| ---------------- | --------------------------------------------------------------- | -------------------------- |
| **Agent**        | A role with its own context, tools, and charter                 | Delegated to on demand     |
| **Agent skill**  | Reusable methodology an agent declares and loads                | Loaded by its holder       |
| **Gate**         | One declared check with a pass/fail verdict                     | A hook or pipeline trigger |
| **Quality gate** | A multi-agent loop that runs until findings are resolved        | Invoked as a workflow      |
| **Workflow**     | A documented multi-step process composing agents and procedures | Invoked deliberately       |

## Agent Versus Agent Skill

An agent is _who_; an agent skill is _what they know_. Methodology shared by several agents belongs
in a skill, declared by each agent that needs it — duplicating it into each definition is the
failure this split prevents.

Agents run in isolated contexts. They receive their own definition and their declared agent skills,
and nothing else — notably not the canonical instruction file. Guidance every agent must share has
to arrive through a declared skill.

## Gate Versus Quality Gate

A **gate** is a single declared check in the repository configuration: an id, a command, and the
surfaces that trigger it. It returns pass or fail.

A **quality gate** is a workflow — a loop of checker, synthesis, and fixer agents that iterates
until findings are resolved or explicitly deferred. The shared word is unfortunate; the two are not
substitutes.

## Maker, Checker, Fixer

The three-role pattern separates concerns that corrupt each other when merged:

- **Maker** creates content.
- **Checker** validates it and reports findings, changing nothing.
- **Fixer** re-validates each finding and applies only those that survive.

The fixer re-validates rather than trusting the report, because a checker's finding can be a false
positive and applying it blindly makes the content worse.

## Related Documents

- [Glossary](../glossary.md) — the other term clusters.
- [AI Agents Convention](../development/agents/ai-agents.md) — agent structure and standards.
- [Maker/Checker/Fixer Pattern](../development/pattern/maker-checker-fixer.md) — the full pattern.
