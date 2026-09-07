---
title: "Gherkin Success Criteria and Related Documents"
description: The three Gherkin scenarios this workflow must satisfy, and links to the conventions and workflows it composes.
when_to_use: Use when verifying this workflow's behaviour against its acceptance criteria, or navigating to a related document.
---

# Gherkin Success Criteria and Related Documents

## Gherkin Success Criteria

```gherkin
Feature: plan idea promotion planning

Scenario: A ripe two-pager becomes a backlog plan and is retired atomically
  Given plans/ideas/<slug>.md holds a real answer in every section
  When the workflow runs to completion with the user's approval
  Then a prior-art report appears under local-tmp/plan-idea-promotion-planning/plan-idea-promotion-planning__*__report.md
  And a plan exists at plans/backlog/<identifier>/
  And the backlog plan receives a PASS verdict from plan-quality-gate
  And plans/ideas/<slug>.md no longer exists on the push target
  And the brief's line is removed from plans/ideas/README.md
  And no application or library code is modified

Scenario: A thin two-pager is not promoted
  Given plans/ideas/<slug>.md has a stub Risks & open questions section
  When the workflow runs the ripeness gate
  Then a readiness report names the stub section
  And final-status is not-ripe
  And no plan is created
  And the two-pager is left untouched in plans/ideas/

Scenario: The user declines at the promotion checkpoint
  Given the ripeness gate passed and the prior-art report is presented
  When the user does not approve promotion
  Then no plan is authored
  And the two-pager remains in plans/ideas/
```

## Related Documents

- [Plans Organization Convention → Promoting a Two-Pager to a Full Plan](../../../conventions/structure/plans/promoting-ideas-and-worked-examples.md#promoting-a-two-pager-to-a-full-plan) — the four-step procedure this workflow operationalizes.
- [Plans Organization Convention → Ideas Folder (Two-Pagers)](../../../conventions/structure/plans/ideas-folder-overview-rationale-and-file-layout.md#ideas-folder-two-pagers) — the two-pager format and the deferred deep prior-art rule.
- [plan-planning workflow](../plan-planning.md) — invoked in Phase 4 with `target-stage=backlog`.
- [plan-execution workflow](../plan-execution.md) — runs the plan later, after promotion to `in-progress/`.
- [web-researcher Agent](../../../../.claude/agents/web/web-researcher.md) — Phase 2 deep prior-art survey.
- [Knowledge Capture Convention](../../../development/quality/knowledge-capture.md) — routes future-work learnings into `plans/ideas/` as two-pagers this workflow later promotes.
