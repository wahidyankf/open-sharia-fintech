---
title: "Drilling Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

**Why does quote matter to a macro author?**

<details><summary>Answer</summary>It preserves a form as data so a macro can inspect and transform it
before evaluation.</details>

**What does hygiene prevent?**

<details><summary>Answer</summary>Accidental capture of a caller's binding by a binding introduced by
a macro.</details>

## Calculation practice

Trace the recursive sum of the list 2, 4, 6. Each call consumes one pair; the base case returns
zero, producing 12 on the way back.

## Scenario judgment

Use a hygienic Scheme macro for a repeated syntactic pattern. Use a function when values, rather
than unevaluated syntax, are being combined.

## Design exercise

Write a Scheme list processor and a syntax-rules macro that adds an unless-style control form.
Then write the Clojure defmacro counterpart and state how its generated name avoids capture.

## Automaticity checklist

- [ ] I can distinguish a value from a quoted form.
- [ ] I can explain why a tail call matters.
- [ ] I can inspect a macro expansion before trusting it.
- [ ] I can name the cost of macro power.
- [ ] I can compare a Scheme vector with implementation-specific hash tables.

## Why / why not prompts

- Why not use eval on untrusted text?
- Why not replace every function with a macro?
- Why does a uniform syntax aid metaprogramming?
- Why is a Clojure macro not automatically hygienic?
- Why does proper tail recursion affect algorithm shape?
