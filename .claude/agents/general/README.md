---
title: "General"
description: "Cross-cutting agents scoped to no single app or domain: agent scaffolding, API exploratory testing, CI standards, and social posts."
---

# General

- [Agent Maker](./agent-maker.md) — Creates new AI agent files in .claude/agents/ following AI Agents Convention. Changes are then synced to .opencode/agents/ via npm run generate:bindings. Ensures proper structure, skills integration, and documentation.
- [Api Exploratory Tester](./api-exploratory-tester.md) — Performs spec-aware, contract-aware session-based exploratory testing of a live API — REST or GraphQL — given an endpoint/base-URL and a testing goal, then files findings as a new backlog plan a developer can pick up and fix. Hunts edge cases and boundary conditions (payloads, status codes, error envelopes, auth, pagination, idempotency, GraphQL nullability/partial-errors/depth), not just the happy path. Compares live responses against the API contract and existing specs/\*\* Gherkin, proposing scenarios for correct behaviours lacking coverage. Never drives a browser — for rendered UI use the web tester triad. Output destination selectable via output-mode — plan (default), delivery, or local-tmp.
- [Ci Checker](./ci-checker.md) — Validates all projects against CI/CD standards including mandatory Nx targets, coverage thresholds, Docker setup, Gherkin consumption, workflow files, E2E pairing, and env variable compliance
- [Ci Fixer](./ci-fixer.md) — Applies validated fixes from ci-checker audit reports. Re-validates findings before applying to prevent false positives.
- [Social Linkedin Post Maker](./social-linkedin-post-maker.md) — Creates LinkedIn posts in social-media-posts/linkedin/ from completed origin/main updates across the ose-public and ose-private repos. Enforces the 3,000-character LinkedIn body limit (measured from the "OPEN SHARIA ENTERPRISE" line down). Optimizes for engagement and professional tone. Use every time a LinkedIn post is created in social-media-posts/linkedin/.
