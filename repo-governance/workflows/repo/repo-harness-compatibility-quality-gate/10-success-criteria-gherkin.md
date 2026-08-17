---
title: "Success Criteria (Gherkin) — Part 1"
description: The first four Gherkin scenarios — Phase 0/Phase 1 ordering, auto-fixed sync drift, cited research, and catalog updates.
when_to_use: Use when verifying or testing this workflow's Phase 0/Phase 1 and fixer-update behavior against its acceptance criteria.
---

# Success Criteria (Gherkin) — Part 1

```gherkin
Scenario: Phase 0 parity invariants pass before external drift check
  Given the five deterministic parity invariants are configured
  When repo-harness-compatibility-checker runs Phase 0
  Then it invokes rhino-cli vendor-audit for governance prose and root instruction surfaces
  And it verifies the binding sync no-op, agent inventory parity, and translation-map coverage
  And only after all five invariants pass does it proceed to Phase 1 web research

Scenario: Phase 0 binding sync drift is auto-fixed
  Given Phase 0 detects Invariant 3 drift (sync produced changes in .opencode/)
  When repo-harness-compatibility-fixer processes the finding
  Then it re-runs npm run generate:bindings
  And stages the updated .opencode/agents/ files
  And verifies the second sync run produces no further changes

Scenario: Checker delegates web research and produces a cited drift audit
  Given the workflow runs with scope "all"
  When repo-harness-compatibility-checker completes Phase 1
  Then it delegates multi-page upstream research to web-researcher for each harness
  And it diffs the fetched data against docs/reference/platform-bindings.md and committed binding files
  And it writes a drift audit to generated-reports/ citing the web sources for each finding
  And each finding identifies the affected harness, the stale field, and the upstream source URL

Scenario: Fixer updates catalog entries for unambiguous in-scope drift
  Given the audit contains a HIGH-confidence finding that a harness now reads AGENTS.md natively
  And the current catalog marks that harness as Tier 2
  When repo-harness-compatibility-fixer is invoked
  Then it updates the harness row in docs/reference/platform-bindings.md to Tier 1
  And it records the web citation and verification date in the catalog entry
  And it writes a fix report using the same UUID chain as the audit
```

**Continued in** [Success Criteria (Gherkin) — Part 2](./11-success-criteria-gherkin-continued.md).
