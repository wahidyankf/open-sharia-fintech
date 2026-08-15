---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

What is the CSP cancellation signal? A closed context channel or cancelled context.

## Calculation practice

Set worker count and queue capacity from a stated arrival rate, service time, and memory limit.

## Scenario judgment

A worker crashes: should the coordinator cancel or should a supervisor restart? State the invariant.

## Design exercise

Map the same fan-out/fan-in topology to channels and to supervised actors.

## Automaticity checklist

- [ ] I can test cancellation and backpressure.
- [ ] I can describe the failure semantics rather than just the syntax.
