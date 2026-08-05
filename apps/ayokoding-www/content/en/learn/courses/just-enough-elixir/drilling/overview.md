---
title: "Drilling Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Each kata has a runnable before and after script focused on a distinct Elixir concept. State the
invariant before changing the code, then compare the smallest repair with the completed example.

## Recall Q&A

1. Why does rebinding a variable not mutate the value it previously named?
   <details><summary>Answer</summary>Values are immutable. Rebinding gives a name a new value while
   the original value remains available to any code that still references it.</details>
2. What makes a pattern match useful at a function boundary?
   <details><summary>Answer</summary>It documents the accepted shape and separates each valid case
   without a chain of manual field checks.</details>
3. When is recursion preferable to accumulating mutable loop state?
   <details><summary>Answer</summary>When the next result can be expressed from the current input and
   an explicit accumulator, keeping every state transition visible in the function clauses.</details>

## Applied problems

1. A report pipeline must preserve its source list for a later comparison. Bind each transformed list
   to a new name instead of overwriting the original.
2. A parser receives either `{:ok, value}` or `{:error, reason}`. Pattern-match each tuple at the
   call boundary so success and failure paths cannot be silently mixed.
3. A process must send one answer to its caller. Keep the caller PID in the message and reply from
   the receive loop after it computes the next state.

## Code katas

- [Kata 1: Immutability](./kata-01-immutability/overview.md)
- [Kata 2: Pattern matching](./kata-02-pattern-match/overview.md)
- [Kata 3: Pipe composition](./kata-03-pipe/overview.md)
- [Kata 4: Recursion](./kata-04-recursion/overview.md)
- [Kata 5: Process reply](./kata-05-process-reply/overview.md)

Run each `before/main.exs`, describe the violated Elixir property, then compare it with
`after/main.exs`.

## Self-check checklist

- [ ] I can distinguish rebinding from mutation.
- [ ] I can choose a pattern match that makes a function's accepted input explicit.
- [ ] I can use the pipe operator without hiding the data flow.
- [ ] I can express a terminating recursive function with an explicit base case.
- [ ] I can explain how a process mailbox carries a request and reply boundary.

## Elaborative interrogation and self-explanation

1. Why does immutable data make a failed transformation easier to inspect than an in-place update?
2. Why is a pattern match both a control-flow choice and a statement about valid data?
3. Why should a process reply include a caller-specific message shape rather than a shared variable?
