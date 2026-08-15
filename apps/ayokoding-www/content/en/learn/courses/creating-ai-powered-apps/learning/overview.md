---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Scope boundary

This course builds offline-testable application integrations: prompts, structured output, retrieval,
tools, budgets, provider boundaries, and safety guards. It deliberately forward-links deep evaluation
design, judge validation, error analysis, and CI evaluation gates to
[Evaluating AI Systems in Depth](/en/learn/courses/evaluating-ai-systems-in-depth/learning/overview)
(`evaluating-ai-systems-in-depth`) rather than re-teaching deep evals here.

## Prerequisites

- [Backend Essentials](../../backend-essentials/learning/overview.md)
- [API Design](../../api-design/learning/overview.md)

## How to use this course

Each example is an offline, typed Python program with a mock provider seam. Run it with
`python3 example.py`; no paid key, network request, or committed secret is required. The three
levels move from a request boundary, through retrieval and tools, to production guardrails.

## Examples by Level

### Beginner (Examples 1–27)

- [Examples 1–27: Prompting, output, embeddings, and chunking](/en/learn/courses/creating-ai-powered-apps/learning/beginner)

### Intermediate (Examples 28–55)

- [Examples 28–55: Retrieval, tools, bounded loops, and budgets](/en/learn/courses/creating-ai-powered-apps/learning/intermediate)

### Advanced (Examples 56–80)

- [Examples 56–80: Operations, safety, providers, and observability](/en/learn/courses/creating-ai-powered-apps/learning/advanced)
