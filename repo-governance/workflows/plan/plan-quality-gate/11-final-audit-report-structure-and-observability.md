---
title: "Final Audit Report Structure and Observability Metrics"
description: Describes the five-part structure of plan-checker's audit report and the metrics tracked across executions.
when_to_use: Use when parsing or generating a plan-checker audit report, or when reviewing what observability data plan-quality-gate tracks.
---

# Final Audit Report Structure and Observability Metrics

## Final Audit Report Structure

The audit report emitted by `plan-checker` follows this structure:

1. **Report metadata** — report ID (UUID chain), date, plan path, mode, iteration number
2. **Scope** — which plan documents were checked (README, brd, prd, tech-docs, delivery)
3. **Findings by criticality** — CRITICAL → HIGH → MEDIUM → LOW, each with:
   - Finding ID
   - Category (structure, requirements, anti-hallucination, acceptance-criteria, etc.)
   - Confidence level (HIGH / MEDIUM / FALSE_POSITIVE)
   - Description and suggested fix
4. **Executive summary** — findings count by criticality, consecutive-zero count, pass/fail verdict
5. **Links to related reports** — previous iteration report (if any), plan quality gate report

## Observability Metrics

Track across executions:

- **Iterations-to-convergence per mode** — how many check-fix cycles needed per mode level
- **Anti-hallucination violations by category** — AP-1 through AP-10 breakdown (from plan-checker Step 5f output)
- **Web-research delegation rate** — count of `web-researcher` invocations per audit; higher rate indicates more external fact-checking
- **AI tokens spent on validation** — measure cost per plan audit
