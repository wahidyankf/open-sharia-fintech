---
title: "Observability and Eval Integration"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 40
---

Theme D covers source Examples 35–46 using local simulations. For deep eval design, grading, and
statistics, continue to [Evaluating AI Systems in Depth](/en/learn/courses/evaluating-ai-systems-in-depth/learning/overview).

### Example 35: Trace a Run

**Brief explanation**: A trace records a parent span and child operations.

**Code**: Run `python3 code/ex-35-trace-a-run/example.py`.

**Expected observation**: The span tree includes turn and tool children.

**Key takeaway**: A trace preserves causal structure.

**Why it matters**: A wrong result needs a navigable execution history.

### Example 36: Write a Structured Run Log

**Brief explanation**: Per-turn logs use named fields rather than prose-only output.

**Code**: Run `python3 code/ex-36-structured-run-log/example.py`.

**Expected observation**: The entry includes decision, tokens, and outcome.

**Key takeaway**: Structured logs are queryable data.

**Why it matters**: Debugging requires more than an unstructured transcript.

### Example 37: Capture Cost and Latency Metrics

**Brief explanation**: A run reports compact operational cost, latency, and success fields.

**Code**: Run `python3 code/ex-37-cost-latency-metrics/example.py`.

**Expected observation**: The metric record contains the three values.

**Key takeaway**: Performance is part of agent behavior.

**Why it matters**: Orchestration cost should be measured, not assumed.

### Example 38: Visualize a Trace

**Brief explanation**: A text diagram connects a root span to nested work.

**Code**: Run `python3 code/ex-38-trace-visualization/example.py`.

**Expected observation**: The flow names root, child, and tool spans.

**Key takeaway**: Visualization makes hierarchy reviewable.

**Why it matters**: A flat log hides parent-child relationships.

### Example 39: Build an Eval Set

**Brief explanation**: An eval case pairs a task with an expected graded outcome.

**Code**: Run `python3 code/ex-39-build-an-eval-set/example.py`.

**Expected observation**: Each fixture has a grader expectation.

**Key takeaway**: Evals are test cases for stochastic behavior.

**Why it matters**: Improvement needs a stable measurement target.

### Example 40: Run the Evals

**Brief explanation**: A local evaluator produces a pass rate from fixture outcomes.

**Code**: Run `python3 code/ex-40-run-the-evals/example.py`.

**Expected observation**: The fixture suite reports its pass rate.

**Key takeaway**: An eval result is evidence, not an intuition.

**Why it matters**: Changes need a repeatable quality signal.

### Example 41: Apply an Eval-Driven Prompt Fix

**Brief explanation**: A failing fixture motivates a narrow prompt or tool-contract repair.

**Code**: Run `python3 code/ex-41-eval-driven-prompt-fix/example.py`.

**Expected observation**: The score improves after the local fix.

**Key takeaway**: Evals should drive deliberate iteration.

**Why it matters**: A fix without a measured target can regress another task.

### Example 42: Detect a Regression Eval

**Brief explanation**: A previously passing case fails after a deliberately changed behavior.

**Code**: Run `python3 code/ex-42-regression-eval/example.py`.

**Expected observation**: The regression is identified as a failure.

**Key takeaway**: Regression evals preserve past quality.

**Why it matters**: Agent changes can silently break a working path.

### Example 43: Handle a Flaky Eval

**Brief explanation**: Repeated local samples and a threshold create a robust pass criterion.

**Code**: Run `python3 code/ex-43-flaky-eval-handling/example.py`.

**Expected observation**: Four of five samples satisfy the threshold.

**Key takeaway**: Stochastic systems need variance-aware evaluation.

**Why it matters**: One lucky pass is not dependable evidence.

### Example 44: Summarize an Observability Dashboard

**Brief explanation**: A compact view joins trace, metric, and eval signals for one run.

**Code**: Run `python3 code/ex-44-observability-dashboard/example.py`.

**Expected observation**: The local dashboard contains all three signal types.

**Key takeaway**: Observability is a connected system.

**Why it matters**: Operators need one coherent diagnosis surface.

### Example 45: Debug through a Trace

**Brief explanation**: A trace identifies the failed decision without replaying the entire run.

**Code**: Run `python3 code/ex-45-debug-via-trace/example.py`.

**Expected observation**: The root cause is `wrong-tool`.

**Key takeaway**: Trace evidence can isolate a fault.

**Why it matters**: Nondeterministic behavior is difficult to repair from final output alone.

### Example 46: Assemble an Observable Orchestrated Agent

**Brief explanation**: A local capstone composes worker summaries, trace data, metrics, and an eval result.

**Code**: Run `python3 code/ex-46-capstone-observable-orchestrated-agent/example.py`.

**Expected observation**: The local run is traced and passes its fixture eval.

**Key takeaway**: An orchestrated system must be observable end to end.

**Why it matters**: A multi-agent result is not trustworthy unless it can be inspected and improved.
