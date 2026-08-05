---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

What synchronizes an unbuffered send? <details><summary>Answer</summary>A matching receive.</details>

## Applied problems

Use a bounded worker pool when producers must be back-pressured.

## Code katas

Repair each before file, then compare it with after.

## Self-check checklist

- [ ] I can close an outbound channel after all senders finish.
- [ ] I can propagate cancellation into every blocking select.

## Elaborative interrogation and self-explanation

Why is a channel hand-off safer than an unguarded shared variable? <details><summary>Answer</summary>It establishes synchronization and transfers ownership.</details>
