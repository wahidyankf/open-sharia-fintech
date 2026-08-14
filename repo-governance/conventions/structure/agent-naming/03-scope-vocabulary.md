---
title: "Scope Vocabulary"
description: The closed set of scope tokens that MUST appear as the first token of every agent filename.
when_to_use: Use when choosing (or adding) the scope token for a new agent filename.
category: explanation
subcategory: conventions
tags:
  - agents
  - naming
  - conventions
created: 2026-04-17
---

# Scope Vocabulary

Exactly one of the following tokens MUST appear as the first token of every agent filename:

- **`agent`** — Meta-agents that operate on other agents (create, validate, refactor agent definitions themselves).
- **`apps`** — Agents scoped to a specific deployable application under `apps/` (web content authoring, app-specific checking, deployers).
- **`ci`** — Agents that diagnose, validate, or repair continuous-integration pipelines and their failures.
- **`docs`** — Agents scoped to the `docs/` tree (Diátaxis content, link integrity, software-engineering separation).
- **`pdf-to-md`** — Agents that convert PDF documents to verbatim Markdown and validate conversion fidelity (text completeness, tables, diagrams, OCR quality).
- **`plan`** — Agents in the plan lifecycle (authoring, checking, executing, validating execution, fixing plans).
- **`pr`** — Agents that operate directly on GitHub pull requests (posting/triaging review findings, resolving review threads), distinct from the `plan` scope's plan-lifecycle agents.
- **`readme`** — Agents that create, validate, or repair README files across the repository.
- **`repo`** — Repository-wide governance agents (conventions, workflows, cross-reference integrity).
- **`social`** — Agents that produce social-media artifacts (LinkedIn posts, monthly updates).
- **`specs`** — Agents scoped to the `specs/` tree (Gherkin features, OpenAPI contracts, C4 diagrams).
- **`swe`** — Software-engineering agents that write or validate production code, grouped by language or test framework.
- **`web`** — Agents that operate against the public web or a live website: read-only research and fact-gathering, and session-based exploratory or spec-blind heuristic-usability testing of a running site (reporting discovered defects/friction).

New scope tokens MUST be added to this vocabulary first before any agent is named against them.
