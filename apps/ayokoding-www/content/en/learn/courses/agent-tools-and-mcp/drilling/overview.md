---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

1. What makes a tool callable by a model?
2. Which MCP capabilities are executable, readable, and reusable instruction templates?

## Applied problems

1. A model selects the wrong tool from a large catalog. Decide whether to improve the description,
   filter the advertised surface, or split a capability.
2. A file tool receives `../../secret`. Specify the server-side validation before any file operation.

## Code katas

1. Define a compact result schema for a search tool that returns only titles, URLs, and a bounded
   snippet.
2. Write the success and error shapes for a typed addition tool.

## Self-check checklist

- [ ] I can distinguish a tool from a resource and a prompt.
- [ ] I can explain why a client discovers schemas instead of hard-coding calls.
- [ ] I can keep validation and authorization at the executable boundary.
- [ ] I can justify a compact tool result as a context-budget decision.

## Elaborative interrogation and self-explanation

1. Why is a tool description part of the model-facing interface rather than ordinary documentation?
2. Why can a smaller advertised tool surface be more capable in practice than a larger one?
3. Why must an MCP connection not imply permission to execute every exposed capability?
