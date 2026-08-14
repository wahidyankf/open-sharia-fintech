---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

1. Why does a provider response need schema validation? It is probabilistic external input, not trusted data.
2. What makes RAG grounded? An answer cites the retrieved source used to support it.
3. Why validate tool arguments? A model may produce malformed or unauthorized parameters.

## Scenario judgment

An answer ignores retrieved policy and invents a rule: require a cited local chunk. A tool call includes
shell syntax in a city field: reject it with a typed validator. A loop keeps planning: stop at its iteration
and cost budget.

## Hands-on implementation

Implement a mock provider, top-k retrieval over a local corpus, a cited answer schema, a validated tool,
and an injection guard that treats retrieved instructions as data.

## Automaticity checklist

- [ ] I can test an LLM feature offline through a provider interface.
- [ ] I can distinguish retrieval grounding from deep evaluation design.
- [ ] I can validate tool input and output before downstream use.
- [ ] I can add budgets, retries, redaction, and injection defenses.
