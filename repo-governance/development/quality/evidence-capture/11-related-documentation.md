---
title: "Related Documentation"
description: "Cross-references to related verification and plan conventions."
category: explanation
subcategory: development
tags:
  - evidence
  - testing
  - screenshots
  - plans
  - verification
  - locale
  - manual-testing
created: 2026-06-20
when_to_use: "Use when you need a related convention on verification or plan structure."
---

# Related Documentation

- [Plan Execution Workflow](../../../workflows/plan/plan-execution.md) — Step 2d mandates evidence capture
  during manual behavioral assertions.
- [plan-execution-checker](../../../../.claude/agents/plan/plan-execution-checker.md) — validates evidence
  presence as part of Step 7.
- [plan-maker](../../../../.claude/agents/plan/plan-maker.md) — emits evidence-capture steps in delivery
  checklists for web-UI plans.
- [web-exploratory-tester](../../../../.claude/agents/web/web-exploratory-tester.md) — saves screenshots to
  the output destination's `evidence/` folder during exploratory testing: the new backlog plan
  (`plan` mode, default), the existing plan's folder (`delivery` mode), or `local-tmp/` (`local-tmp`
  mode).
- [web-usability-tester](../../../../.claude/agents/web/web-usability-tester.md) — saves screenshots to the
  output destination's `evidence/` folder during usability evaluation (same three-mode selection as
  `web-exploratory-tester`).
- [web-design-tester](../../../../.claude/agents/web/web-design-tester.md) — saves screenshots to the
  output destination's `evidence/` folder during design-fidelity evaluation (same three-mode selection
  as `web-exploratory-tester`).
