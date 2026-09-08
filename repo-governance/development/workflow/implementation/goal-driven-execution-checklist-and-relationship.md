---
description: The before/during-execution checklist for goal-driven execution, and how it relates to core principles and AI agents.
when_to_use: Use before starting a task and during execution to confirm goal-driven execution is actually being followed.
---

# Goal-Driven Execution — Checklist and Relationship

## Goal-Driven Execution Checklist

Before starting any task:

- [ ] Success criteria defined and measurable
- [ ] Verification method identified (test, manual check, measurement)
- [ ] Multi-step tasks broken into verified stages
- [ ] Each stage has clear pass/fail criteria

During execution:

- [ ] Write tests before implementation (when applicable)
- [ ] Verify at each step
- [ ] Loop until verification passes
- [ ] Don't move to next step until current step verified

## Relationship to Principles

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: Clear goals prevent confusion and rework
- **[Reproducibility](../../../principles/software-engineering/reproducibility.md)**: Automated tests ensure reproducible verification
- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: Automated tests > manual verification

## For AI Agents

Agents must practice goal-driven execution by:

1. **Transforming tasks** into verifiable goals with clear success criteria
2. **Writing tests first** when implementing features or fixing bugs
3. **Stating brief plans** for multi-step tasks with verification steps
4. **Verifying continuously** rather than assuming success
5. **Looping until verified** rather than moving on prematurely

This practice enables agents to work more independently by having clear, objective measures of success rather than needing constant clarification on "is this right?"
