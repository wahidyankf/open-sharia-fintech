---
title: "Related Workflows and Documentation — Plan Establishment"
description: Links to the workflows and governance documents that plan-establishment calls, precedes, or depends on.
when_to_use: Use when navigating from plan-establishment to plan-quality-gate, plan-execution, or the underlying conventions it relies on.
---

# Related Workflows and Documentation

## Related Workflows

- [Plan Quality Gate](../plan-quality-gate.md) — called in Step 6
- [Plan Execution](../plan-execution.md) — next workflow after plan-establishment

## Related Documentation

- [Plans Organization Convention](../../../conventions/structure/plans.md)
- [Grilling-With-Options Convention](../../../development/workflow/grilling-with-options.md) — format
  and mechanism for Steps 1 and 3 grill sessions
- [Governance Vendor-Independence Convention](../../../conventions/structure/governance-vendor-independence.md)
- [grill-me Skill](../../../../.claude/skills/grill-me/SKILL.md) — Steps 1 and 3
- [plan-maker Agent](../../../../.claude/agents/plan/plan-maker.md) — Step 4
- [web-researcher Agent](../../../../.claude/agents/web/web-researcher.md) — Step 2
- [repo-setup-manager Agent](../../../../.claude/agents/repo/repo-setup-manager.md) — Phase 0 of plans
  created by this workflow
- [Plans Organization Convention §Delivery Mode](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode) —
  the four-mode vocabulary and three-tier precedence confirmed in Step 1 item 8
- [PR-Review Maker→Fixer Cycle](../../pr/pr-review-quality-gate.md) — the review loop that runs
  during execution when the plan's confirmed delivery mode is `worktree-to-pr` or `main-to-pr`
