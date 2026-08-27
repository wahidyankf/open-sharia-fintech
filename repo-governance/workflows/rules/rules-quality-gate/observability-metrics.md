---
title: "Observability Metrics"
description: The nine metrics to track across executions — preflight latency, AI-vs-deterministic token ratios, convergence, success rate, and the target DETERMINISTIC ratio.
when_to_use: Use when instrumenting or reviewing this workflow's execution history for efficiency or drift.
---

# Observability Metrics

Track across executions:

- **Preflight cold-run latency**: Target < 120 seconds for initial run
- **Preflight cached-run latency**: Target < 5 seconds with `RHINO_AUDIT_NOW` pin (SHA-256 hash match avoids re-evaluation)
- **AI tokens spent on Step 1+ vs deterministic findings count**: Ratio of AI token cost to mechanical findings already caught by preflight
- **AI-only-to-domain-deterministic ratio**: Persistent AI-only majority may identify another
  domain predicate worth encoding; delegated lifecycle results are excluded
- **Iterations-to-convergence per mode**: How many check-fix cycles needed per mode level
- **Average iterations to completion**: How many cycles typically needed
- **Success rate**: Percentage reaching zero findings
- **Common finding categories**: What issues appear most often
- **Fix success rate**: Percentage of fixes applied without errors

Calculate this ratio only from retained domain findings. Lifecycle evidence is not a finding and
must not inflate the deterministic side of the metric.
