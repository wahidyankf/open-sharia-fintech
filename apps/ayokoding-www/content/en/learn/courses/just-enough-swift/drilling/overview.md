---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

This is the active-recall companion to the learning track. Answer each prompt before opening its
disclosure: recognizing Swift syntax is not the same as choosing a safe model under pressure.

## Recall Q&A

**Q1 (co-01).** What is the difference between `swift Example.swift` and `swiftc Example.swift -o example`?

<details><summary>Answer</summary>`swift` evaluates the file for a quick script loop; `swiftc` compiles it into the named executable, which you then run as `./example`.</details>

**Q2 (co-02).** When should a binding use `let` rather than `var`?

<details><summary>Answer</summary>Use `let` by default. Choose `var` only when the binding itself must be reassigned as part of the design.</details>

**Q3 (co-03, co-04).** Does type inference make Swift dynamically typed, and how do you combine an `Int` with a `Double`?

<details><summary>Answer</summary>No; inference chooses a static type at compile time. Convert deliberately, for example `Double(count) / 2`.</details>

**Q4 (co-05).** What does `"\(value)"` do?

<details><summary>Answer</summary>It evaluates `value` and embeds its textual representation in a string literal.</details>

**Q5 (co-06).** What extra state does `String?` represent compared with `String`?

<details><summary>Answer</summary>It represents either a present string or `nil`, the explicit absence of a value.</details>

**Q6 (co-07).** Why does `guard let value = input else { return }` improve a function's normal path?

<details><summary>Answer</summary>It exits the absent path and leaves `value` non-optional for the rest of the function, avoiding nesting.</details>

**Q7 (co-08, co-09).** Contrast `user?.address?.city` with `name ?? "Guest"`.

<details><summary>Answer</summary>Chaining safely reads through possibly absent links and returns nil; nil coalescing supplies a chosen fallback when a consumer needs a concrete value.</details>

**Q8 (co-10).** Why is `optional!` not ordinary optional handling?

<details><summary>Answer</summary>It asserts a runtime invariant and traps if nil. Prefer binding, chaining, validation, or a fallback unless the invariant is locally proven.</details>

**Q9 (co-11, co-12).** What do an argument label and default value each improve?

<details><summary>Answer</summary>A label names an argument's role at the call site; a default lets callers omit an ordinary option while retaining an explicit override.</details>

**Q10 (co-13).** What can a closure capture, and when does it become `@escaping`?

<details><summary>Answer</summary>It can capture surrounding constants and variables. It is `@escaping` when stored or used after the receiving function returns.</details>

**Q11 (co-14).** Which collection operation transforms, selects, and combines respectively?

<details><summary>Answer</summary>`map` transforms each item, `filter` retains selected items, and `reduce` combines items into one accumulator result.</details>

**Q12 (co-15–co-17).** What is the observable difference after copying a struct versus copying a class reference?

<details><summary>Answer</summary>Mutating a copied struct leaves the original unchanged. Mutating through either copied class reference changes the same instance.</details>

**Q13 (co-18, co-19).** When do you use a computed property or a `mutating` method?

<details><summary>Answer</summary>Use a computed property to derive from stored truth; mark a struct method `mutating` when it changes the struct's own stored state.</details>

**Q14 (co-20–co-22).** Why model a finite state with an enum and switch it exhaustively?

<details><summary>Answer</summary>The enum closes the alternatives; an exhaustive switch makes every consumer decide what each state means, including new cases added later.</details>

**Q15 (co-21).** What does an associated value buy over a raw value?

<details><summary>Answer</summary>An associated value carries case-specific typed context; a raw value is one uniform literal representation for every case.</details>

**Q16 (co-23, co-24).** Why accept `some Shape` or a protocol-typed dependency?

<details><summary>Answer</summary>The caller depends on required behavior rather than a concrete implementation, allowing different conformers and focused test substitutes.</details>

**Q17 (co-25).** What does `T: Comparable` communicate in a generic function?

<details><summary>Answer</summary>It says the algorithm works for any one concrete `T` that supports comparison; the compiler rejects types lacking that operation.</details>

**Q18 (co-26).** Compare `do`/`catch` and `try?`.

<details><summary>Answer</summary>`do`/`catch` preserves and handles failure; `try?` deliberately converts an error into nil when failure truly means absence.</details>

**Q19 (co-27).** When is a `Set` a better fit than an `Array`?

<details><summary>Answer</summary>Use a set when unique membership matters more than order or duplicates; use an array when sequence order is part of the data.</details>

**Q20 (co-28).** What does `await` say at a call site?

<details><summary>Answer</summary>It says this asynchronous operation may suspend before producing its result, so the caller must be in an asynchronous context.</details>

## Applied Problems

**AP1.** A profile's city is optional and the UI needs a label. Use safe traversal and show `Unknown` only at rendering time.

<details><summary>Answer</summary>`let label = profile?.address?.city ?? "Unknown"` keeps absence through the model and applies a fallback at the display boundary.</details>

**AP2.** A checkout may be `idle`, `processing(orderID)`, or `failed(message)`. Should it use three booleans, nullable fields, or an enum with associated values?

<details><summary>Answer</summary>An enum with associated values. It prevents impossible flag combinations and makes a switch cover every meaningful state.</details>

**AP3.** A calculation needs to work for `Int` and `Double`, but it must order values. What generic contract is appropriate?

<details><summary>Answer</summary>Use a generic parameter constrained to `Comparable`, such as `func maximum<T: Comparable>(_:_:)->T`.</details>

**AP4.** A parser can explain why input failed. Should it return `0`, use `try?`, or throw a typed error?

<details><summary>Answer</summary>Throw a typed error when the explanation matters. A sentinel `0` is a valid value; `try?` discards useful failure context.</details>

**AP5.** Two independent async lookups are both needed before rendering. Which construct starts both before the join?

<details><summary>Answer</summary>Use `async let` for each child, then await their values together. Use it only when the work is genuinely independent and owned by the same parent scope.</details>

## Deliberate Practice

1. Write `displayName(_:)` that accepts `String?`, uses `guard let`, and prints only a present value.
2. Model `Download` as `queued`, `running(percent: Int)`, and `failed(reason: String)`; write an exhaustive label switch.
3. Given `["1", "oops", "3"]`, use `compactMap(Int.init)`, `map`, and `reduce` to produce `8` without a mutable accumulator.
4. Define a `Clock` protocol and two conforming structs, then write a function accepting `some Clock` that returns a formatted time.
5. Write two small `async` functions, start them with `async let`, and print their summed result only after both complete.

## Automaticity Checklist

- [ ] I use `let` first and can distinguish immutable binding from immutable object state.
- [ ] I choose optional binding, chaining, or nil coalescing deliberately instead of force unwrapping.
- [ ] I can explain why a struct copy and class-reference copy behave differently.
- [ ] I can model mutually exclusive states with an enum and make a switch exhaustive.
- [ ] I can select a protocol, an extension default, or a generic constraint based on the required behavior.
- [ ] I can point to suspension with `await` and explain why `Task {}` needs an owner in real app code.

## Explain Why

**Why is a `struct` usually the safer default for domain data?**

<details><summary>Answer</summary>Assignment and parameter passing create independent values, so accidental shared mutation is opt-in instead of ambient. A class is still appropriate when stable identity or intentionally shared mutable state is the model.</details>

**Why is `nil` not a replacement for every loading or failure state?**

<details><summary>Answer</summary>Nil only says absence. It cannot distinguish not-yet-loaded, unavailable-by-design, and failed-with-context; an enum can preserve those meanings.</details>

**Why avoid `try!` and `!` in ordinary application paths?**

<details><summary>Answer</summary>Both turn a recoverable or explainable condition into a process trap. They are reasonable only where a narrow, enforced invariant makes failure impossible.</details>

**Why is this concurrency treatment only a preview?**

<details><summary>Answer</summary>Knowing the spelling of `async`, `await`, `Task`, and `async let` is not enough for safe iOS work. Ownership, cancellation, actor isolation, and UI integration require the platform context taught next.</details>
