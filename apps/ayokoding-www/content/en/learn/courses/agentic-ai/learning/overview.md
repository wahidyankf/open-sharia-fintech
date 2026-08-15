---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Scope boundary

Agentic AI is a survey of how a model, tools, state, and a bounded control loop work together. This
course does **not** teach build-your-own agent runtimes, schedulers, memory stores, sandboxing, or
observability systems; it points to the owning harness courses instead.

Deep evaluation design, judge calibration, statistical confidence, error analysis, and CI evaluation gates
belong to [Evaluating AI Systems in Depth](/en/learn/courses/evaluating-ai-systems-in-depth/learning/overview)
(`evaluating-ai-systems-in-depth`) and are forward-linked rather than re-taught here.

## Harness course map

- [`the-agent-loop`](/en/learn/courses/the-agent-loop/learning/overview) owns durable loop construction.
- [`agent-tools-and-mcp`](/en/learn/courses/agent-tools-and-mcp/learning/overview) owns tool and MCP integration.
- [`agent-context-and-memory`](/en/learn/courses/agent-context-and-memory/learning/overview) owns context and memory systems.
- [`agent-permissions-and-sandboxing`](/en/learn/courses/agent-permissions-and-sandboxing/learning/overview) owns execution authority and isolation.
- [`agent-orchestration-subagents-and-observability`](/en/learn/courses/agent-orchestration-subagents-and-observability/learning/overview) owns delegation, traces, and observability.

## How to use this survey

The examples use deterministic local mocks to introduce vocabulary and operational boundaries. They are not
a substitute for the owning harness courses: follow the links above when a feature needs production depth.
