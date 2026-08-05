---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

This is the active-recall companion to the learning track. Answer before opening each answer;
then repair the small mistakes without looking at the learning examples.

## Recall Q&A

**Q1.** What does `var value T` contain before assignment?

<details><summary>Answer</summary>The type's zero value: for example 0, empty string, false, or nil.</details>

**Q2.** How does Go report ordinary failure?

<details><summary>Answer</summary>As a final error return value checked explicitly with `if err != nil`.</details>

**Q3.** What makes a type satisfy an interface?

<details><summary>Answer</summary>It has the required methods; there is no implements declaration.</details>

## Applied problems

**AP1.** A caller needs a timeout. Where does cancellation travel?

<details><summary>Answer</summary>Pass context.Context across the call boundary and select on ctx.Done().</details>

**AP2.** A worker must return one value to main. What is the smallest honest mechanism?

<details><summary>Answer</summary>One goroutine and one typed channel hand-off; defer pipeline policy to CSP-Style Concurrency.</details>

## Code katas

1. Repair a nil-map write by allocating it with `make`.
2. Repair an ignored error by returning or handling it at the call site.
3. Repair a shared counter by guarding it with a mutex or redesigning around a channel.
4. Repair a blocked channel send by arranging a receiver or using a bounded buffer deliberately.
5. Repair a context leak by calling its cancel function.

## Self-check checklist

- [ ] I can create a module, run, build, format, and test a Go package.
- [ ] I can choose value versus pointer receivers and explain implicit interfaces.
- [ ] I can wrap and inspect errors without string matching.
- [ ] I can use slices, maps, JSON tags, and generic constraints deliberately.
- [ ] I can explain the preview boundary between this course and CSP-style concurrency.

## Elaborative interrogation and self-explanation

**Why does Go insist on explicit error values?**

<details><summary>Answer</summary>The failure path is visible in the function signature and in control flow, making recovery policy a local, reviewable decision.</details>

**Why is a goroutine preview not enough to design a concurrent system?**

<details><summary>Answer</summary>Starting work is easy; ownership, cancellation, backpressure, memory safety, and pipeline topology require the next course's deeper CSP treatment.</details>
