---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

What is the difference between a subagent's isolated context and the summary returned to its parent?
How do sequential, parallel, and hierarchical orchestration differ?

## Scenario Judgment

Choose whether to delegate, run in parallel, or keep work in the parent when a task has dependencies,
a bounded summary, or irreducible detail. State the failure and cost consequences of the choice.

## Hands-on Implementation

Sketch a local fan-out that returns three typed summaries, records parent and child spans, and merges a
partial result when one worker fails.

## Automaticity Checklist

- [ ] I delegate only bounded work that has a useful summary.
- [ ] I can distinguish orchestration structure from loop and tool boundaries.
- [ ] I record enough trace, log, and metric data to debug a wrong outcome.
- [ ] I forward deep evaluation work to the evaluation course.

## Extension challenge

Design a two-agent task with a bounded handoff. Name the lead's success criterion, the worker's
artifact, the trace attributes you would inspect, and the condition that prevents another retry.
