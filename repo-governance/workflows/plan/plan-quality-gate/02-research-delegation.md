---
title: "Research Delegation — Plan Quality Gate"
description: Explains when plan-checker delegates multi-page web research to web-researcher instead of using its own in-context WebSearch/WebFetch.
when_to_use: Use when checking whether a single technical claim in a plan audit should be delegated to web-researcher.
---

# Research Delegation

The `plan-checker` agent delegates multi-page web research to the
[`web-researcher`](../../../../.claude/agents/web/web-researcher.md) delegated agent when verifying a single
technical claim requires more than one or two searches, or more than two fetches. This keeps the
plan audit context lean — `plan-checker` receives a cited, synthesised summary and translates it
into dual-labelled findings, rather than burning its own context on multi-page research. Checkers
retain in-context `WebSearch` and `WebFetch` for single-shot verification against known
authoritative URLs. No workflow-level configuration is required; the delegation is encoded in the
`plan-checker` prompt.

Multi-page research delegation keeps plan-checker context lean — externalizing 2+ search or 3+ fetch operations into `web-researcher` reduces the checker's per-claim context spend. Tracked under Observability Metrics as 'web-research delegation rate'.
