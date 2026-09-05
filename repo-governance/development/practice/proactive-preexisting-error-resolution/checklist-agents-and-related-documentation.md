---
title: "Proactive Preexisting Error Resolution — Checklist, For AI Agents, and Related Documentation"
description: The completion checklist for preexisting-error work, the five-point AI agent behaviour rules, the relationship to Autonomous Bug Fixing, and links to related documentation
category: explanation
subcategory: development
tags:
  - root-cause
  - quality
  - preexisting-errors
  - proactive
  - bug-fixing
  - ai-agents
created: 2026-03-28
when_to_use: Use as a completion checklist before considering preexisting-error work done, or as a quick-reference for AI agent behaviour.
---

# Checklist, For AI Agents, and Related Documentation

## Checklist

Before considering any work complete:

- [ ] All preexisting errors encountered during this work have been diagnosed
- [ ] Each error has a root cause fix, not a workaround or suppression
- [ ] Each fix has been verified to work
- [ ] Small fixes are committed inline or as part of the current changeset
- [ ] Medium fixes have their own commit with a descriptive message
- [ ] Large fixes have a plan in `plans/in-progress/` with execution underway
- [ ] All findings and fixes have been communicated clearly

## For AI Agents

All agents encountering preexisting errors must follow this practice:

1. **Diagnose the root cause** before proceeding with the primary task
2. **Fix the root cause**, not the symptom, not around the symptom
3. **Verify the fix works** with the relevant tests or checks
4. **Scope the fix appropriately**: inline for small issues, separate commit for medium issues, plan for large issues
5. **Communicate what was found and what was fixed** — never proceed in silence

### What Agents Must Not Do

- Continue working on a primary task while leaving a discovered preexisting error unfixed
- Add a workaround that makes a broken system appear to work
- Write "I noticed X is broken" in a response without taking action on X
- Re-run a failing test hoping it passes without investigating the failure

### Relationship to Autonomous Bug Fixing

[Autonomous Bug Fixing](../../agents/agent-workflow-orchestration/autonomous-bug-fixing.md#autonomous-bug-fixing) covers what to do when a bug report is the primary task. This practice covers what to do when a preexisting error is discovered incidentally during other work. Both require the same behaviour: diagnose, fix, verify, communicate.

The distinction is task origin. The behaviour is identical.

## Related Documentation

- [Root Cause Orientation](../../../principles/general/root-cause-orientation.md) - The foundational principle this practice extends into proactive action
- [Implementation Workflow](../../workflow/implementation.md) - Development workflow that includes surgical changes and goal-driven execution
- [Agent Workflow Orchestration](../../agents/agent-workflow-orchestration.md) - How agents plan, execute, verify, and fix bugs autonomously
- [Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md) - Think before acting; surface assumptions; do not proceed on broken foundations
- [Git Push Default Convention](../../workflow/git-push-default.md) — Domain-specific application of Standard 4 (fix preexisting unsolicited PR steps when encountered in delivery checklists)
