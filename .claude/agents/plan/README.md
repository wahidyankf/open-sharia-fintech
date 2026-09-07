---
title: "Plan"
description: "Agents that create, check, and validate execution of project plans."
---

# Plan

- [Plan Checker](./plan-checker.md) — Validates project plan quality including requirements completeness, technical documentation clarity, and delivery checklist executability. Use when reviewing plans before execution.
- [Plan Execution Checker](./plan-execution-checker.md) — Validates completed plan implementation by verifying all requirements met, code quality standards followed, and acceptance criteria satisfied. Final quality gate before marking plan complete.
- [Plan Maker](./plan-maker.md) — Creates project plans with requirements, technical documentation, and delivery checklists. Returns unresolved pre-write and post-write decisions to the calling root orchestrator for grilling, then resumes with resolved answers. Structures plans for systematic execution via the plan-execution workflow (orchestrated by the calling context).
