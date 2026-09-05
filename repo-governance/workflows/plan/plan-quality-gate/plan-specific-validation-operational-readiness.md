---
title: "Plan-Specific Validation — Operational Readiness and Knowledge Capture"
description: Second half of the plan-checker validation catalog — implementation readiness, codebase alignment, clarity, operational readiness, and knowledge-capture presence.
when_to_use: Use when checking what plan-checker requires for operational readiness (quality gates, CI verification, dev-env setup) or knowledge-capture presence.
---

# Plan-Specific Validation — Operational Readiness and Knowledge Capture

**Continued from** [Plan-Specific Validation — Completeness Through Execution-Grade Clarity](./plan-specific-validation-completeness-through-clarity.md).

- **Implementation Readiness**: Plans are actionable and executable
- **Codebase Alignment**: References to existing files, patterns, and conventions
- **Clarity**: Clear problem statements, well-defined scope, unambiguous requirements
- **Operational Readiness** (CRITICAL): Plans must include all of the following:
  - **Local quality gates**: Steps to run affected tests, linting, typecheck locally before pushing (`apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`, the same registry-declared gate set `.husky/pre-push` invokes; includes `nx affected -t test:quick`)
  - **Post-push CI verification**: Steps to monitor and verify GitHub Actions/workflows pass after
    the push — against the plan's declared delivery target (the PR's check run under `*-to-pr`,
    `origin main` under the direct-push modes) — with instructions to fix failures immediately. This
    requirement is delivery-mode-independent; a `*-to-pr` plan is **not** exempt
  - **Development environment setup**: Steps to set up the dev environment for the features being built (dependencies, env vars, DB, dev server)
  - **Fix-all-issues instruction**: Explicit instruction to fix ALL failures found during quality gates — including preexisting issues not caused by the current changes (root cause orientation principle)
  - **Thematic commit guidance**: Preserves explicit authorization of the named change set, then
    requires the fewest build-valid, independently reviewable/revertible Conventional Commits;
    required completion artifacts stay together and independent concerns split
  - **Manual behavioural assertions**: Steps to use Playwright MCP for web UI verification (navigate, snapshot, click, check console errors) and curl for API verification (hit endpoints, check responses, test error cases) — applicable when the plan touches UI or API code
- **Knowledge Capture presence**: For substantive plans, `delivery.md` contains a Knowledge
  Capture phase (or an explicit "none" record) and the plan folder carries a `learnings.md`
  scaffold. Silent absence is flagged at MEDIUM. See the
  [Knowledge Capture Convention](../../../development/quality/knowledge-capture.md).
