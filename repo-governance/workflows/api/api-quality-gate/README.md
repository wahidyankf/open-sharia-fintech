---
title: "API Quality Gate Workflow"
description: "Exercises a running REST or GraphQL API against its contract and Gherkin specs, fixing every defect via a tester-driven loop until none remain."
when_to_use: "Read this index to find the right API Quality Gate Workflow child document."
---

# API Quality Gate Workflow

- [Shape: Tester-Driven, Not Checker/Fixer](./01-shape-tester-driven-not-checker-fixer.md) — Explains why the API quality gate has no checker/fixer agent pair and instead runs a tester-driven test-fix-retest loop. Use when orchestrating the API quality gate, to confirm which agents to invoke and in what order.
- [Execution Mode](./02-execution-mode.md) — Preferred and fallback execution modes for the API quality gate, and example invocations. Use when starting the API quality gate, to decide between Agent Delegation and Manual Orchestration.
- [Preconditions](./03-preconditions.md) — The three preconditions that must hold before the API quality gate can run — reachable service, identified contract, non-destructive scope. Use when confirming a service is ready to be exercised by the API quality gate.
- [Step 1: Test (Agent Delegation)](./04-step-1-test.md) — How the API quality gate invokes api-exploratory-tester and what it exercises against the live API. Use when running the first step of the API quality gate loop.
- [Step 2: Triage Against Mode](./05-step-2-triage-against-mode.md) — How AET findings' ISTQB severity ratings map onto the gate's CRITICAL/HIGH/MEDIUM/LOW mode threshold. Use when deciding which findings from the tester block termination under the current mode.
- [Step 3: Fix (Agent Delegation)](./06-step-3-fix.md) — How in-threshold findings are routed to the matching swe-\*-dev agent and what every fix must ship with. Use when applying fixes for findings surfaced by the API quality gate tester.
- [Step 4: Re-Test](./07-step-4-re-test.md) — Why the API quality gate re-runs the tester against a rebuilt, redeployed service rather than trusting a source-only fix. Use when verifying a fix after Step 3 has been applied.
- [Step 5: Double-Zero Confirmation](./08-step-5-double-zero-confirmation.md) — Why a single zero-finding pass does not terminate the API quality gate loop and what a second clean pass confirms. Use when a re-test comes back with zero in-threshold findings and you need to decide whether the loop can terminate.
- [Step 6: Iteration Control](./09-step-6-iteration-control.md) — The final pass/partial/fail status rules for the API quality gate loop and the iteration-5 escalation warning. Use when determining the API quality gate's final status after repeated test-fix cycles.
- [Relationship to Other Gates](./10-relationship-to-other-gates.md) — How the API quality gate's surface-conditional applicability and merge-precondition status relate to the UI gates and PR review. Use when determining whether a plan must run the API quality gate, the UI gates, both, or neither.
- [Related Documentation](./11-related-documentation.md) — Cross-references from the API quality gate to the workflows index, the UI gate, and related quality conventions. Use when looking for documentation related to the API quality gate.
