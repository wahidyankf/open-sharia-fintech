---
description: "Related testing and safety conventions."
when_to_use: "Use when you need a related convention on testing or safety."
---

# Related Documentation

- [Regression Test Mandate](.././regression-test-mandate.md) -- The bug-driven-fix convention this
  document extends: an exit-status assertion alone is a regression-test-style patch that is
  necessary but not sufficient for this defect class; this convention supplies the durable
  defense-in-depth a narrow exit-status check lacks.
- [Behaviour-Driven Development](../../behaviour-driven-development.md) -- CLI-app integration tests
  that use real `/tmp` filesystem fixtures are the primary home for git-fixture tests in this
  monorepo; this convention governs their isolation once their test level is chosen.
- [Reproducible Environments Convention (Git Identity Guardrail)](../../workflow/reproducible-environments.md) --
  The repository-wide policy that no AI agent sets or modifies git identity at any scope, protecting
  the real repository's identity config from **manual** edits and direct agent commands. The
  motivating incident for this convention is a concrete illustration of how that guardrail can be
  violated **by automation** rather than by direct agent action: a fixture bug, not an agent
  editing `.git/config` directly, produced the identity corruption. This convention is the
  test-fixture-specific defense that keeps automated code from becoming the guardrail's blind spot.
- [CI Blocker Resolution Convention](.././ci-blocker-resolution.md) -- Shares this convention's stance
  that a discovered defect must be fixed at the root cause, not bypassed with a partial patch.
- [Criticality Levels Convention](.././criticality-levels.md) -- Defines the CRITICAL severity this
  convention's enforcement findings use.
