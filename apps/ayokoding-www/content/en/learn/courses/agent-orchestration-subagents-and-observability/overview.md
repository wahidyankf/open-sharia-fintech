---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

This course scales a bounded agent loop into a system: delegate summarizable work to isolated
subagents, coordinate it deliberately, and instrument the system so its behavior can be debugged and
improved.

## Scope and prerequisites

Complete [Agent Tools & MCP](/en/learn/courses/agent-tools-and-mcp/learning/overview) and
[Agent Context and Memory](/en/learn/courses/agent-context-and-memory/learning/overview) first.
This course owns delegation, orchestration, hooks, skills, terminal interaction, tracing, metrics,
and eval integration.

`remotebrowser` is an illustrative browser-fleet and MCP service shape only. It is not a required
dependency; runnable mechanisms use local deterministic simulations.

## Evals boundary

Deep evaluation design, grading, and statistical interpretation belong to
[Evaluating AI Systems in Depth](/en/learn/courses/evaluating-ai-systems-in-depth/learning/overview).
This course shows where traces, metrics, and regression-eval signals enter an orchestrated system.

## Learning route

The annotated-concept route has 46 contiguous examples: subagents and delegation (1–12),
orchestration and background work (13–24), extension surfaces (25–34), and observability plus
eval integration (35–46). Use a single agent when work cannot be bounded and summarized cleanly.
